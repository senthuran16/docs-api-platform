#!/usr/bin/env python3
"""Check the external `http(s)` links the other scripts deliberately skip.

    python3 scripts/check_external.py en/docs --scope api-manager/4.6.0 \
        --json BROKEN-EXTERNAL-<scope>.json

Every other script in this skill resolves targets against the file tree, so an
external URL is invisible to them. This one asks the network — which introduces a
failure mode a file check does not have: a host can refuse an automated request
whether or not the page exists. `wso2.com` answers `403` to a bare client for
*every* path, including its own home page.

So each host is calibrated before its links are judged. The host root is fetched
first as a control:

  * control answers        -> a 404/410 on that host is real, and reported `dead`
  * control refuses too    -> nothing on that host can be judged, reported
                              `unverifiable`; a human has to open them
  * host does not resolve  -> `dead`, regardless of control

`unverifiable` is not a softer `dead`. It means the check failed, not the link, and
it must never be counted as a broken link.
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from links_lib import strip_noise, find_targets           # noqa: E402

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Hosts that are examples in prose, not addresses anyone can fetch.
PLACEHOLDER = re.compile(
    r"localhost|127\.0\.0\.1|\{|\}|\$|<|>|example\.(com|org)|"
    r"^(https?://)?[\d.]+:\d+|your-|<?hostname", re.I)

TRAILING = ".,;:!?'\"`)]}"


def collect(root, scope):
    """Unique external URLs in scope -> the pages that use them."""
    urls = defaultdict(set)
    for dp, _, fns in os.walk(root):
        for fn in fns:
            if not fn.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(dp, fn), root).replace("\\", "/")
            if scope and not rel.startswith(scope):
                continue
            body = strip_noise(open(os.path.join(root, rel), encoding="utf-8",
                                    errors="replace").read())
            for _kind, t, _is_html in find_targets(body):
                if not re.match(r"^https?://", t):
                    continue
                t = t.rstrip(TRAILING)
                if PLACEHOLDER.search(t):
                    continue
                urls[t].add(rel)
    return urls


def fetch(url, timeout, method="HEAD"):
    """(status, note). status is None when nothing answered."""
    req = urllib.request.Request(url, headers=HEADERS, method=method)
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return r.status, ""
    except urllib.error.HTTPError as e:
        if method == "HEAD" and e.code in (403, 405, 501):
            return fetch(url, timeout, "GET")       # some hosts refuse HEAD only
        return e.code, ""
    except urllib.error.URLError as e:
        reason = str(getattr(e, "reason", e))
        if method == "HEAD":
            return fetch(url, timeout, "GET")
        return None, reason[:80]
    except Exception as e:                          # noqa: BLE001
        return None, str(e)[:80]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--scope", default="")
    ap.add_argument("--json")
    ap.add_argument("--timeout", type=float, default=20)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--gate", action="store_true",
                    help="exit 1 when any link is dead (unverifiable never fails)")
    args = ap.parse_args()
    root = args.root.rstrip("/")

    urls = collect(root, args.scope)
    if not urls:
        print("no external links in scope")
        return
    by_host = defaultdict(list)
    for u in urls:
        by_host[urllib.parse.urlsplit(u).netloc].append(u)

    print(f"{len(urls)} unique external links across {len(by_host)} hosts "
          f"— calibrating each host first")

    # ---- control probe, one per host ----
    controls = {}
    with cf.ThreadPoolExecutor(args.workers) as ex:
        futs = {ex.submit(fetch, f"https://{h}/", args.timeout): h for h in by_host}
        for f in cf.as_completed(futs):
            st, note = f.result()
            controls[futs[f]] = (st, note)

    blocked = {h for h, (st, _) in controls.items()
               if st is None or st >= 400}
    if blocked:
        print(f"  {len(blocked)} host(s) refuse automated requests or did not "
              f"resolve — their links cannot be judged here")

    # ---- the links ----
    def judge(url):
        time.sleep(0.15)
        st, note = fetch(url, args.timeout)
        host = urllib.parse.urlsplit(url).netloc
        cst, _ = controls.get(host, (None, ""))
        host_gone = cst is None and "resolve" in (controls.get(host, (None, ""))[1] or "")
        if st is not None and 200 <= st < 400:
            return "ok", st, note
        if host_gone or (st is None and "resolve" in (note or "")):
            return "dead", st, note or "host does not resolve"
        if host in blocked:
            return "unverifiable", st, note or "host refuses automated requests"
        if st in (404, 410):
            return "dead", st, note
        return "unverifiable", st, note

    results = {}
    with cf.ThreadPoolExecutor(args.workers) as ex:
        futs = {ex.submit(judge, u): u for u in urls}
        for f in cf.as_completed(futs):
            results[futs[f]] = f.result()

    buckets = defaultdict(list)
    for u, (verdict, st, note) in results.items():
        buckets[verdict].append((u, st, note))

    print(f"\n  {len(buckets['ok']):5}  ok")
    print(f"  {len(buckets['dead']):5}  dead            <- fix these")
    print(f"  {len(buckets['unverifiable']):5}  unverifiable    <- open in a browser; NOT broken links")

    for u, st, note in sorted(buckets["dead"]):
        print(f"\nDEAD  {st or ''} {u}")
        for pg in sorted(urls[u]):
            print(f"      {pg}")

    if args.json:
        out = {"scope": args.scope,
               "hosts_blocked": sorted(blocked),
               "findings": {
                   v: [{"url": u, "status": st, "note": n,
                        "files": sorted(urls[u])}
                       for u, st, n in sorted(items)]
                   for v, items in buckets.items()}}
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=2)
        print(f"\njson -> {args.json}")

    if args.gate and buckets["dead"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
