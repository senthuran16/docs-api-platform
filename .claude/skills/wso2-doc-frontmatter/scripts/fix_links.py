#!/usr/bin/env python3
"""Apply the link fixes proposed in a `report_links.py` plan, one tier at a time.

    # look, change nothing (the default)
    python3 scripts/fix_links.py en/docs --plan BROKEN-LINKS-4.6.0.json --tier malformed
    # apply that tier
    python3 scripts/fix_links.py en/docs --plan BROKEN-LINKS-4.6.0.json --tier malformed --apply

The split from `report_links.py` is deliberate. The reporter reads and proposes;
this script is the only thing that writes. So a plan can be reviewed, committed,
and handed to someone else, and applying it later is a separate, auditable act.

Tiers are applied ONE AT A TIME on purpose. Each tier has a different failure
mode, so each deserves its own look and its own commit — a bad `renamed`
proposal is a link to a real page about the wrong thing, which no build catches.

Only tiers whose entries carry a `suggested` value can be applied at all:

    malformed   link syntax. Exact.
    dir_style   written in URL shape; add `.md` so mkdocs resolves it. Exact.
    depth       wrong number of `../`. Exact.
    renamed     target moved. Proposed, with a confidence — high only by default.
    templated_fixable   `{{base_path}}` where the resource exists. Exact.

`templated`, `stale`, `anchor` and `gone` are refused. They need information that
is not in the repo, and a guess there produces a confident link to the wrong page.

Every rewrite is verified against the disk BEFORE it is written, and the exact
link text must still be present in the file — so a plan that has gone stale
skips rather than corrupts.
"""
import os
import re
import sys
import json
import argparse
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from links_lib import (  # noqa: E402
    url_base, page_id, slug, harvest_anchors, resolve_candidates,
    rewrite_target, is_raw_html, renders_anchors_clientside,
)

APPLICABLE = {
    "malformed": "link syntax, exact",
    "dir_style": "written as a URL; adding `.md` lets mkdocs resolve it",
    "depth": "wrong relative depth, exact",
    "templated_fixable": "build-time variable where the resource exists, exact",
    "renamed": "target moved, proposed with a confidence",
    "case": "right path, wrong capital letters — exact",
    "include": "`{! !}` shared block converted to `--8<--`, exact",
    "anchor_case": "anchor names a real heading with different capitals — exact",
    "anchor_legacy": "original Confluence anchor, matched to the one heading that agrees",
    "anchor_punct": "anchor names a real heading, different hyphens or underscores — exact",
    "templated_typo": "`{{base_path}}` misspelled and the resource exists — exact",
    "partial_fixable": ("link in a shared block; one path works from every page that "
                        "includes it"),
    "stale_mapped": "old-site url whose path exists under this version — exact",
    "anchor_deep": ("heading is deeper than toc_depth so it has no id; insert "
                    "`<a name>` above it"),
    # An agent's own decisions, in a plan it wrote itself. Same shape, same
    # verification, same journal — so a judgement call is applied by the one thing
    # in this skill that checks its work, and shows up in `git diff` and the
    # journal exactly like a mechanical fix. The alternative is an agent editing
    # pages by hand, where nothing checks the result and nothing records why.
    "agent": ("decided by an agent after reading the pages; verified like any other, "
              "and refused unless the reasoning is quoted in `evidence`"),
}
REFUSED = {
    "templated": "the resource does not exist at that path — may be served by a redirect",
    "stale": "points at a pre-migration domain — needs the new equivalent page",
    "anchor": "the heading was reworded — needs someone to pick the new one",
    "gone": "no target anywhere — was it dropped, missed, or merged?",
    "partial": ("the page is included into other pages, so a relative link resolves "
                "against the includer's url — no single relative path can be right"),
}




def anchors_of(path):
    """Anchor ids the page at `path` publishes, or None when they cannot be known.

    `toc_depth` is not applied here: refusing a fix because an anchor is too deep
    for the TOC would block a correct path rewrite over a separate, separately-
    reported defect.

    Returns **None** — meaning "unverifiable", not "none found" — for a page whose
    anchors are built in the browser (an OpenAPI/ReDoc container). Those hold no
    Markdown headings, so the harvest is empty and every fragment would be refused,
    blocking path rewrites that are correct. Callers must distinguish None from an
    empty set; see `renders_anchors_clientside`."""
    txt = open(path, encoding="utf-8", errors="replace").read()
    if renders_anchors_clientside(txt):
        return None
    anchors, _deep = harvest_anchors(txt)
    return anchors






def entry_is_html(root, entry):
    """Whether this entry's link was written as raw HTML. The reporter records it;
    reading it back off the page is the fallback for older plans."""
    v = entry.get("is_html")
    if v is not None:
        return bool(v)
    try:
        txt = open(os.path.join(root, entry["file"]), encoding="utf-8",
                   errors="replace").read()
    except OSError:
        return False
    return is_raw_html(txt, entry.get("link", ""))






def resolve(root, src_rel, target, is_html=False):
    """Where does `target`, written in the page `src_rel`, land on disk?

    Returns a repo-relative path that exists, or None. Directory URLs mean a
    bare path may be a file, the same file with `.md`, or a directory's index.

    The base depends on the syntax, and this is the load-bearing part. mkdocs
    resolves a Markdown target against the SOURCE directory, but passes raw HTML
    through untouched, so the browser resolves it against the RENDERED url — one
    level deeper for a non-index page. Checking a raw-HTML fix source-relative
    refuses every correct proposal, and accepts the wrong one.
    """
    target = target.split("#")[0].split("?")[0]
    if not target:
        return src_rel
    base = url_base(src_rel) if is_html else os.path.dirname(src_rel)
    cand = os.path.normpath(os.path.join(base, target)).replace("\\", "/")
    for c in resolve_candidates(cand):
        if os.path.isfile(os.path.join(root, c)):
            return c
    return None


# The two things an agent-decided fix must quote, so a reviewer can check it
# without redoing the reading. See `check_evidence`.
EVIDENCE_KEYS = ("sentence", "matched")


def check_evidence(entry):
    """For an `agent` entry: is the reasoning recorded? Returns (ok, reason).

    A judgement call and a wrong guess produce the same diff — correct syntax, real
    heading, and a reader who silently lands in the wrong section with nothing to
    flag it ever again. The only thing that separates them is the evidence, so the
    evidence is required rather than encouraged:

    - `sentence` — the sentence on the page that contains the link, quoted. That is
      what says where the reader was being sent.
    - `matched` — the heading, page title or filename that was chosen, quoted from
      the target.

    Both must be non-empty, and `sentence` has to actually appear on the page, which
    is what stops the field from being filled in with a summary written from memory.
    Refusing here rather than warning is deliberate: a warning at the bottom of a
    long run is not read.
    """
    for k in EVIDENCE_KEYS:
        v = (entry.get("evidence") or {}).get(k)
        if not v or not str(v).strip():
            return False, (f"agent fix with no `evidence.{k}` — quote the linking "
                           f"sentence and the heading you matched")
    return True, ""


def verify(root, entry, tier=None):
    """Can this entry's `suggested` value be trusted? Returns (ok, reason)."""
    src = entry["file"]
    suggested = entry.get("suggested")
    if not suggested:
        return False, "no suggested value in the plan"
    if not os.path.isfile(os.path.join(root, src)):
        return False, "source page no longer exists"

    if tier == "agent":
        ok, why = check_evidence(entry)
        if not ok:
            return False, why
        quoted = " ".join(str(entry["evidence"]["sentence"]).split())
        page = " ".join(open(os.path.join(root, src), encoding="utf-8",
                             errors="replace").read().split())
        if quoted not in page:
            return False, ("`evidence.sentence` is not on the page — quote it "
                           "verbatim, do not paraphrase")

    # An absolute URL or mail link has no on-disk target to check. That is not a
    # reason to skip: these appear in `malformed`, where the fix is purely
    # syntactic (unwrapping backticks, removing a stray quote) and the address
    # itself is untouched.
    if re.match(r"^(?:[a-z][a-z0-9+.-]*:)?//|^mailto:", suggested, re.I):
        return True, "external address, syntax-only fix"

    # Raw HTML and Markdown resolve against different bases, so the check has to
    # know which one this was. The reporter records it; fall back to reading the
    # page only for plans written before it did.
    is_html = entry_is_html(root, entry)

    if entry.get("insert_above"):
        txt = open(os.path.join(root, src), encoding="utf-8", errors="replace").read()
        if entry["insert_above"] not in txt:
            return False, "the heading is no longer in the page"
        return True, ""

    if entry.get("literal"):
        # `--8<-- "path"` is resolved by pymdownx.snippets against `base_path:
        # docs`, so the address is docs-root-relative — not relative to the page.
        # Checking it page-relative would refuse every correct conversion.
        m_snip = re.match(r'--8<--\s*"([^"]+)"', suggested)
        if not m_snip:
            return False, "not a recognised shared-block directive"
        tgt = m_snip.group(1)
        if not os.path.isfile(os.path.join(root, tgt)):
            return False, f"shared block does not exist at {tgt}"
        return True, ""

    # A link in a SHARED BLOCK is resolved from whichever page includes the block,
    # never from the block's own folder — so check it from every includer. Checking
    # it block-relative is what let 62 links be "fixed" into breakage.
    incs = entry.get("includers")
    if incs:
        bad = [i for i in incs if resolve(root, i, suggested, is_html) is None]
        if bad:
            return False, (f"does not resolve from {len(bad)} of {len(incs)} "
                           f"including page(s), e.g. {bad[0]}")
        return True, ""

    frag = suggested.partition("#")[2]
    if suggested.startswith("#") or suggested in ("./", "."):
        landed = src                      # same page
    else:
        landed = resolve(root, src, suggested, is_html)
        if landed is None:
            return False, (f"suggested target does not resolve: {suggested} "
                           f"({'raw HTML' if is_html else 'Markdown'} base)")

    # Where the plan already recorded the on-disk target, the two must agree — on
    # the *page*, not the spelling. The reporter records some targets in their
    # directory-URL form (`foo/bar`) and others as the file (`foo/bar.md`), and
    # those name the same page.
    recorded = entry.get("resolves_to") or entry.get("found_at")
    if recorded and page_id(landed) != page_id(recorded):
        return False, f"resolves to {landed}, but the plan recorded {recorded}"

    if frag and landed.endswith(".md"):
        known = anchors_of(os.path.join(root, landed))
        # None means the page renders its anchors in the browser, so the fragment
        # is unverifiable rather than wrong. Skip the check — do not pass it — so
        # the path half of the rewrite lands and the fragment is carried through
        # untouched. Verifying it would need the OpenAPI spec, not the .md.
        if known is not None and frag not in known:
            return False, f"anchor #{frag} not found in {landed}"
    return True, ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docs_root", nargs="?", default="en/docs")
    ap.add_argument("--plan", required=True, help="The JSON written by report_links.py.")
    ap.add_argument("--tier", required=True,
                    help="One tier name. Run --list to see what a plan holds.")
    ap.add_argument("--apply", action="store_true", help="Write changes. Default is a dry run.")
    ap.add_argument("--sample", type=int, default=5,
                    help="How many before/after examples to print (dry run only).")
    ap.add_argument("--min-confidence", default="high", choices=["high", "medium", "low"],
                    help="For `renamed`: the lowest confidence to act on. Default high.")
    ap.add_argument("--files", nargs="*", default=None,
                    help="Limit to these pages (paths as they appear in the plan, or "
                         "prefixed with the docs root). Use this to try a tier on one "
                         "page before running it across the scope.")
    ap.add_argument("--journal", default=None,
                    help="Write what changed to this JSON, for review or reverting.")
    args = ap.parse_args()

    root = args.docs_root.rstrip("/")
    plan = json.load(open(args.plan, encoding="utf-8"))
    tiers = plan.get("tiers", {})

    if args.tier not in tiers:
        print(f"No tier {args.tier!r} in {args.plan}. This plan holds:")
        for t, items in tiers.items():
            print(f"    {t:<20} {len(items):>5}")
        return 2

    if args.tier in REFUSED:
        print(f"Refusing to apply `{args.tier}`: {REFUSED[args.tier]}.")
        print("Read the pages and decide these, then apply with `--tier agent`.")
        return 2
    if args.tier not in APPLICABLE:
        print(f"`{args.tier}` has no proposed replacements, so there is nothing to apply.")
        return 2

    entries = tiers[args.tier]

    if args.files:
        # Accept either form: `en/docs/a/b.md` or the plan's `a/b.md`.
        wanted = {f[len(root):].lstrip("/") if f.startswith(root) else f for f in args.files}
        before = len(entries)
        entries = [e for e in entries if e.get("file") in wanted]
        unmatched = wanted - {e.get("file") for e in entries}
        print(f"--files: {len(entries)} of {before} entries in this tier match "
              f"{len(wanted)} path(s).")
        if unmatched:
            print("  no entries in this tier for: " + ", ".join(sorted(unmatched)))
        if not entries:
            return 0

    rank = {"high": 3, "medium": 2, "low": 1}
    if args.tier == "renamed":
        floor = rank[args.min_confidence]
        held = [e for e in entries if rank.get(e.get("confidence", "low"), 1) < floor]
        entries = [e for e in entries if rank.get(e.get("confidence", "low"), 1) >= floor]
    else:
        held = []

    # Verify everything first. Nothing is written until the whole tier is checked.
    ready, skipped = [], []
    for e in entries:
        ok, why = verify(root, e, args.tier)
        (ready if ok else skipped).append(e if ok else (e, why))

    print("=" * 70)
    print(f"LINK FIX   tier: {args.tier}   ({APPLICABLE[args.tier]})")
    print("=" * 70)
    print(f"scope in plan     : {plan.get('scope', '?')}")
    print(f"entries in tier   : {len(entries) if args.files else len(tiers[args.tier])}")
    if held:
        print(f"below confidence  : {len(held)}   (raise with --min-confidence)")
    print(f"verified fixable  : {len(ready)}")
    print(f"skipped           : {len(skipped)}")

    if skipped:
        print("\nSkipped, with reasons:")
        for e, why in skipped[:10]:
            print(f"  {e['file']}\n      {e.get('link')}  ->  {why}")
        if len(skipped) > 10:
            print(f"  ... and {len(skipped) - 10} more")

    if not args.apply:
        n = min(args.sample, len(ready))
        if n:
            print(f"\nSample of {n} of {len(ready)} fixes (nothing written):\n")
            for e in ready[:n]:
                print(f"  {e['file']}")
                print(f"    -  {e['link']}")
                print(f"    +  {e['suggested']}")
                if e.get("confidence"):
                    print(f"       confidence: {e['confidence']}")
                print()
        print(f"To apply these {len(ready)}, re-run with --apply.")
        return 0

    # Group by file so each file is read and written once.
    by_file = collections.defaultdict(list)
    for e in ready:
        by_file[e["file"]].append(e)

    changed_files = 0
    rewrites = 0
    missing, already = [], 0
    journal = []
    for rel, es in sorted(by_file.items()):
        path = os.path.join(root, rel)
        txt = open(path, encoding="utf-8", errors="replace").read()
        orig = txt
        done = set()
        for e in es:
            html = entry_is_html(root, e)
            key = (e["link"], html)
            if key in done:
                # The plan lists one entry per occurrence, and the first rewrite
                # replaced every copy in the same syntax. Not a problem.
                already += 1
                continue
            if e.get("insert_above"):
                # Not a link rewrite: this adds an inert anchor above a heading in
                # the TARGET page, so a link to a heading deeper than `toc_depth`
                # has something to land on. Skipped when the anchor is already
                # there, which is what makes re-running safe.
                heading = e["insert_above"]
                if heading not in txt:
                    missing.append((rel, heading))
                    continue
                lines = txt.splitlines(keepends=True)
                out_lines, n = [], 0
                for idx, ln in enumerate(lines):
                    if ln.rstrip("\n") == heading.rstrip("\n"):
                        prev = out_lines[-1].strip() if out_lines else ""
                        if e["suggested"] not in prev:
                            indent = re.match(r"\s*", ln).group(0)
                            out_lines.append(f"{indent}{e['suggested']}\n")
                            n += 1
                    out_lines.append(ln)
                if not n:
                    already += 1
                    continue
                txt = "".join(out_lines)
                done.add(key)
                rewrites += n
                journal.append({"file": rel, "inserted": e["suggested"],
                                "above": heading, "occurrences": n})
                continue

            if e.get("literal"):
                # A shared-block directive is a whole distinctive token, not a
                # target sitting inside a link, so there is no delimiter to anchor
                # on and no substring hazard: `{!a/b.md!}` cannot occur inside
                # another directive because of its closing `!}`.
                n = txt.count(e["link"])
                txt = txt.replace(e["link"], e["suggested"])
            else:
                txt, n = rewrite_target(txt, e["link"], e["suggested"], html)
            if not n:
                missing.append((rel, e["link"]))
                continue
            done.add(key)
            rewrites += n
            rec = {"file": rel, "from": e["link"], "to": e["suggested"],
                   "syntax": "html" if html else "markdown", "occurrences": n}
            if e.get("evidence"):
                rec["evidence"] = e["evidence"]
            journal.append(rec)
        if txt != orig:
            open(path, "w", encoding="utf-8").write(txt)
            changed_files += 1

    print(f"\nAPPLIED   files changed: {changed_files}   link occurrences rewritten: {rewrites}")
    if already:
        print(f"          {already} further entries were duplicates of a link already "
              f"rewritten in the same file")
    if missing:
        print(f"\nNot found in the file, so left alone ({len(missing)}) — the plan is "
              f"older than the page:")
        for rel, link in missing[:10]:
            print(f"  {rel}: {link}")

    if args.journal:
        json.dump(journal, open(args.journal, "w"), indent=1, ensure_ascii=False)
        print(f"\njournal -> {args.journal}")

    print("\nReview with `git diff --stat`, then regenerate the plan before the next "
          "tier — fixing one tier changes what the others resolve to.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
