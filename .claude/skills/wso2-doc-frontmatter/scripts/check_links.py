#!/usr/bin/env python3
"""Link + asset checker for wso2/docs-api-platform (migration-aware)."""
import os, re, sys, json, collections, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fm_lib import is_legacy_url, split_version  # noqa: E402
from links_lib import (  # noqa: E402
    find_targets, harvest_anchors, strip_noise, url_base, page_id,
    read_toc_depth, read_redirect_maps, redirect_targets,
    non_web_scheme, is_http_typo, resolve_candidates, read_extra_vars,
    renders_anchors_clientside,
    version_root, build_include_map, MD_LINK, HTML_SRC,
)

import argparse
_ap = argparse.ArgumentParser()
_ap.add_argument("docs_root", nargs="?", default="en/docs")
_ap.add_argument("--json", dest="json_out", default=None,
                 help="Write full findings to this path. Omitted = summary only.")
_ap.add_argument("--gate", action="store_true", help="Exit 1 if any blocking finding.")
_ap.add_argument("--mkdocs-yml", dest="mkdocs_yml", default=None,
                 help="Where to read `toc_depth` and `redirect_maps` from. "
                      "Defaults to <docs_root>/../mkdocs.yml.")
_args = _ap.parse_args()
DOCS = _args.docs_root.rstrip("/")
SITE = "https://wso2.com/api-platform/docs"
VER = re.compile(r"^(\d+\.\d+(\.\d+)?|next|latest)$")

md_files, all_files = set(), set()
for root, _, fs in os.walk(DOCS):
    for f in fs:
        rel = os.path.relpath(os.path.join(root, f), DOCS)
        all_files.add(rel)
        if f.endswith(".md"):
            md_files.add(rel)


MKDOCS_YML = _args.mkdocs_yml or os.path.join(os.path.dirname(DOCS) or ".", "mkdocs.yml")
TOC_DEPTH = read_toc_depth(MKDOCS_YML)

# Links a redirect makes reachable even though nothing is there on disk.
#
# `mkdocs-redirects` builds a real page at each `redirect_maps` source, so a link
# pointing at one WORKS in the published site. Resolving against the filesystem
# alone reports those as broken. Only the block in mkdocs.yml is consulted — the
# old `docs-apim/en/redirects.yml` is deliberately NOT read, because how the API
# Manager redirects should be carried over has not been decided, and guessing
# here would quietly mark links as fine on the strength of a redirect that does
# not exist yet.
EXTRA_VARS = read_extra_vars(MKDOCS_YML)
REDIRECTS = read_redirect_maps(MKDOCS_YML)
REDIRECT_OK = redirect_targets(REDIRECTS)

# `anchors` is what the build actually produces; `deep_anchors` holds ids a
# heading would have if `toc_depth` allowed it. See links_lib.harvest_anchors.
PAGE_TEXT = {p: open(os.path.join(DOCS, p), encoding="utf-8",
                     errors="replace").read() for p in md_files}
anchors, deep_anchors = {}, {}


# Which pages are SHARED BLOCKS, and which pages pull each one in.
#
# A link inside a block is resolved from the including page, never from the
# block's own folder — so judging a block as if it were a page is wrong in both
# directions. It reports links that are fine, and it passes links that break
# everywhere the block is used. Correctly fixing such a link would then make this
# checker start complaining, which is how a good fix gets reverted.
INCLUDED = build_include_map(DOCS, md_files, lambda x: version_root(x, split_version))

# A page's anchors include the headings of the blocks it pulls in — the text is
# spliced in before Markdown runs. Harvested here, after INCLUDED exists, so the
# checker and the reporter agree about what ids a page publishes.
INCLUDES_OF = {}
for _blk, _pages in INCLUDED.items():
    for _pg in _pages:
        INCLUDES_OF.setdefault(_pg, []).append(_blk)
for p in md_files:
    _extra = [PAGE_TEXT[b] for b in INCLUDES_OF.get(p, []) if b in PAGE_TEXT]
    anchors[p], deep_anchors[p] = harvest_anchors(PAGE_TEXT[p], TOC_DEPTH, _extra)

# Pages that are containers for a client-side renderer. Their anchors are built by
# ReDoc in the browser from the OpenAPI spec, so `anchors[p]` is empty and every
# fragment aimed at one looks missing. Skipping is the only correct answer: the
# fragment cannot be verified from the `.md`, and reporting it says a working deep
# link is broken. `report_links.py` and `fix_links.py` apply the same rule.
CLIENTSIDE_ANCHORS = {p for p in anchors if renders_anchors_clientside(PAGE_TEXT[p])}

used = set()          # every target that resolved, for the orphan-asset check
findings = []
def add(f, sev, code, msg):
    findings.append({"file": f, "severity": sev, "code": code, "message": msg})

for p in sorted(md_files):
    full = os.path.join(DOCS, p)
    txt = open(full, encoding="utf-8", errors="replace").read()
    body = re.sub(r"`[^`\n]*`", "", strip_noise(txt))
    d = os.path.dirname(p)

    targets = find_targets(body)

    for kind, t, is_html in targets:
        if t.startswith("#!"):
            continue
        # Anything with a URI scheme is an ADDRESS, not a path on disk. Resolving
        # one against the docs root reports a correct `ldap://10.100.1.100:389`
        # example in a user-store page as a broken link. A mistyped http scheme
        # (`ttps://`) is excluded from this and falls through, because that IS a
        # defect and `malformed` can fix it.
        scheme = non_web_scheme(t)
        if scheme:
            continue
        # Build-time template variables. Whether this is broken depends entirely
        # on whether the variable has a value: `extra.base_path` is not defined in
        # this repo, so `{{base_path}}/x/` renders as `/x/` and points outside the
        # docs. Read the config rather than assuming either way — that keeps the
        # severity correct if someone later defines it.
        tvars = re.findall(r"\{\{\s*([\w.]+)\s*\}\}", t)
        if re.search(r"\{\{.*?\}\}", t):
            undefined = [v for v in tvars if v.split(".")[0] not in EXTRA_VARS]
            if undefined:
                add(p, "blocking", "LINK_TEMPLATED_UNDEFINED",
                    f"`{t}` uses {', '.join('{{' + v + '}}' for v in undefined)}, which "
                    f"has no value under `extra:` in mkdocs.yml — it renders as an empty "
                    f"string, so the link resolves outside the docs.")
            else:
                add(p, "polish", "LINK_TEMPLATED",
                    f"Target contains a build-time variable, so it can't be checked "
                    f"statically: `{t}`")
            continue
        # stale pre-migration domain
        if is_legacy_url(t):
            add(p, "blocking", "STALE_LINK", f"Links to the pre-migration site: `{t}`")
            continue
        if re.match(r"^https?://", t):
            if t.startswith(SITE):
                # absolute self-link — should be relative, and must resolve
                add(p, "should-fix", "ABS_SELF_LINK",
                    f"Absolute link to our own site: `{t}` — use a relative path so it survives moves and works in previews.")
            continue
        if t.startswith("//"):
            continue
        if t.startswith("#"):
            frag = urllib.parse.unquote(t[1:])
            if frag and p not in CLIENTSIDE_ANCHORS and frag not in anchors.get(p, set()):
                if frag in deep_anchors.get(p, set()):
                    add(p, "blocking", "ANCHOR_TOO_DEEP",
                        f"`{t}` names a heading deeper than h{TOC_DEPTH}, and `toc_depth: {TOC_DEPTH}` "
                        f"means the build gives it no id — so the link goes nowhere. Add "
                        f"`<a name=\"{frag}\"></a>` just above the heading, or promote the heading "
                        f"to h{TOC_DEPTH}.")
                else:
                    add(p, "should-fix", "ANCHOR_MISSING", f"In-page anchor `{t}` has no matching heading.")
            continue

        path, _, frag = t.partition("#")
        path = urllib.parse.unquote(path)
        frag = urllib.parse.unquote(frag)
        if not path:
            continue
        # WHICH BASE APPLIES — verified against a real mkdocs build, not inferred.
        #
        # mkdocs rewrites a Markdown target only when the literal path names a file
        # that exists in docs_dir (`../c/target.md`, `../img.png`). Then, and only
        # then, is the target resolved against the SOURCE directory.
        #
        # Everything else is passed through verbatim and resolved by the browser
        # against the RENDERED URL, which sits one level deeper for a non-index page:
        #   * raw HTML (`<img src>`, `<a href>`)
        #   * directory-style Markdown links (`../c/target/`)
        #   * extensionless Markdown links (`../c/target`) — passed through even
        #     when `target.md` exists right there
        #
        # Judging a passed-through link source-relative is how a link that is broken
        # in the browser gets reported as clean.
        if path.startswith("/"):
            cand = path.lstrip("/")
            rewritten = False
        else:
            literal = os.path.normpath(os.path.join(d, path)).replace("\\", "/")
            rewritten = (not is_html) and literal in all_files
            rel_base = d if rewritten else url_base(p)
            cand = os.path.normpath(os.path.join(rel_base, path))
        if cand.startswith(".."):
            add(p, "blocking", "LINK_ESCAPES_ROOT", f"Link `{t}` resolves outside the docs root.")
            continue

        # A shared block: resolve from each including page instead of from here.
        if p in INCLUDED:
            landings = {}
            for inc in sorted(INCLUDED[p]):
                ibase = os.path.dirname(inc)
                ilit = os.path.normpath(os.path.join(ibase, path)).replace("\\", "/")
                irw = (not is_html) and ilit in all_files
                ic = os.path.normpath(
                    os.path.join(ibase if irw else url_base(inc), path)).replace("\\", "/")
                landings[inc] = next((c for c in resolve_candidates(ic) if c in all_files), None)
            for v in landings.values():
                if v:
                    used.add(v)
            bad = [i for i, v in landings.items() if not v]
            if bad:
                add(p, "blocking", "PARTIAL_LINK_BROKEN",
                    f"`{t}` is inside a shared block and does not resolve from "
                    f"{len(bad)} of {len(landings)} page(s) that include it, e.g. "
                    f"`{bad[0]}`. A link in a block is resolved from the including "
                    f"page, not from the block.")
            continue

        resolved = next((c for c in resolve_candidates(cand) if c in all_files), None)
        if resolved:
            used.add(resolved)
        if resolved is None:
            cand_norm = cand.replace("\\", "/")
            if cand_norm in REDIRECT_OK or page_id(cand_norm) in REDIRECT_OK:
                # Nothing on disk, but `redirect_maps` publishes a page here, so the
                # link works in the built site. Reported at `polish` rather than
                # dropped: it is worth knowing a link leans on a redirect.
                add(p, "polish", "LINK_VIA_REDIRECT",
                    f"`{t}` has no file on disk but is served by a `redirect_maps` "
                    f"entry in mkdocs.yml, so it resolves in the built site.")
            elif is_http_typo(t):
                add(p, "blocking", "LINK_SCHEME_TYPO",
                    f"`{t}` looks like an http(s) URL with a mistyped scheme.")
            elif os.path.isdir(os.path.join(DOCS, cand)):
                add(p, "should-fix", "LINK_DIR_NO_INDEX", f"Link `{t}` points at a directory with no index.md/README.md.")
            else:
                code = {"image": "IMG_MISSING", "media": "MEDIA_MISSING"}.get(
                    kind, "LINK_BROKEN")
                add(p, "blocking", code,
                    f"{kind.capitalize()} target does not exist: `{t}`")
            continue
        if frag and resolved.endswith(".md") and resolved not in CLIENTSIDE_ANCHORS:
            if frag not in anchors.get(resolved, set()):
                if frag in deep_anchors.get(resolved, set()):
                    add(p, "blocking", "ANCHOR_TOO_DEEP",
                        f"`{t}` names a heading in `{resolved}` deeper than h{TOC_DEPTH}, which "
                        f"`toc_depth: {TOC_DEPTH}` leaves without an id, so the link goes nowhere.")
                else:
                    add(p, "should-fix", "ANCHOR_MISSING",
                        f"Anchor `#{frag}` not found in `{resolved}` (link was `{t}`).")

    # Alt text. The style guide is specific here and it is easy to get wrong:
    #   - alt="" is CORRECT for purely decorative images or screenshots that
    #     merely mirror the text steps. Do not flag it as missing.
    #   - informative images need meaningful alt text, max 155 characters.
    #   - "Image of" / "Photo of" prefixes are called out to avoid.
    for m in MD_LINK.finditer(body):
        if m.group(1) != "!":
            continue
        alt, src = m.group(2), m.group(3)
        if not alt.strip():
            add(p, "polish", "IMG_ALT_EMPTY_VERIFY",
                f"Image has alt=\"\": `{src}`. Correct if the image is decorative or "
                f"mirrors the text steps; a defect if it carries information.")
        elif len(alt) > 155:
            add(p, "should-fix", "IMG_ALT_TOO_LONG",
                f"Alt text is {len(alt)} chars; the guide caps it at 155: `{src}`")
        if re.match(r"^\s*(image|photo|picture|screenshot)\s+of\b", alt, re.I):
            add(p, "should-fix", "IMG_ALT_PREFIX",
                f"Alt text starts with \"{alt.split()[0]} of\" — the guide calls this out to avoid: `{src}`")
        if re.search(r"\.gif$", src.split("#")[0], re.I):
            add(p, "should-fix", "IMG_ANIMATED_GIF",
                f"Animated GIF: `{src}`. The guide says use a resource-efficient format like MP4 instead.")

# ORPHAN ASSETS — an image no page points at.
#
# `used` is filled by the main loop above, from targets that actually RESOLVED.
# It must not be recomputed in a separate pass: re-resolving every target against
# the source directory regardless of syntax sends every raw-HTML reference — most
# of the images in these docs — to the wrong path, and counts its image as
# unreferenced.
#
# Images referenced only through a `{{base_path}}` link are added below rather
# than counted as orphans. They ARE currently unreachable, but that is the
# templated-link problem, already reported per link; listing the same files again
# as orphans would double-count one cause and invite deleting a screenshot whose
# only fault is the link pointing at it.
# WHAT COUNTS AS AN ORPHAN — two different things, kept apart on purpose.
#
# `used` holds targets that RESOLVED. An image whose only referrer is a broken
# link is not in it — and calling that image "never referenced" is worse than
# useless: it is already reported as `IMG_MISSING` from the link's side, and
# listing it here as unused invites deleting a screenshot whose only fault is the
# link pointing at it. Fixing the link would make it referenced again.
#
# So `mentioned` records every basename that appears in ANY target on a page in
# the same version, resolving or not. An asset is only an orphan when nothing in
# its own version so much as names it. Per-version matters because each version
# keeps its own copy of the same file: 4.1.0's `conditional-groups.png` being used
# by a 4.4.0 page says nothing about whether 4.1.0 needs it.
mentioned = collections.defaultdict(set)
for p in sorted(md_files):
    vroot = version_root(p, split_version)
    body = strip_noise(open(os.path.join(DOCS, p), encoding="utf-8",
                            errors="replace").read())
    for _kind, t, _is_html in find_targets(body):
        bare = urllib.parse.unquote(t.partition("#")[0].rstrip("/"))
        if bare:
            mentioned[vroot].add(os.path.basename(bare))
        # A `{{base_path}}` target is version-root-relative; where the file is
        # actually there, count it as used rather than as a second finding.
        m_bp = re.match(r"^\{\{\s*base_path\s*\}\}/?(.*)$", t)
        if m_bp:
            rest = urllib.parse.unquote(m_bp.group(1).partition("#")[0]).strip("/")
            cand = os.path.normpath(f"{vroot}/{rest}" if vroot else rest).replace("\\", "/")
            hit = next((c for c in resolve_candidates(cand) if c in all_files), None)
            if hit:
                used.add(hit)

# `assets/` AT ANY DEPTH, not just the docs root.
#
# `startswith("assets/")` matches only `en/docs/assets/`, while each version keeps
# its own `api-manager/<version>/assets/` holding the bulk of the images. Anchoring
# the match at the docs root measures a fraction of the repo while reading like a
# whole-repo figure.
ASSET_EXT = re.compile(r"\.(png|jpg|jpeg|gif|svg|webp|mp4)$", re.I)
assets = {f for f in all_files
          if ("assets/" in f.replace("\\", "/") + "/") and ASSET_EXT.search(f)}

orphans, wanted_but_broken = [], []
for f in sorted(assets - used):
    if os.path.basename(f) in mentioned.get(version_root(f, split_version), ()):
        wanted_but_broken.append(f)     # a page asks for it; the link is broken
    else:
        orphans.append(f)               # nothing in its version names it at all
orphans_by_area = collections.Counter(
    "/".join(o.split("/")[:2]) if "/" in o else o for o in orphans)

by = collections.Counter((f["code"], f["severity"]) for f in findings)
print("=" * 68); print("LINK & ASSET CHECK"); print("=" * 68)
print(f"md files scanned  : {len(md_files)}")
print(f"total findings    : {len(findings)}")
print(f"images            : {len(assets)}  "
      f"({len(used & assets)} referenced, {len(wanted_but_broken)} asked for by a "
      f"broken link, {len(orphans)} never named in their version)")
if orphans_by_area:
    top = ", ".join(f"{k} ({v})" for k, v in orphans_by_area.most_common(4))
    print(f"  orphans by area : {top}")
print()
print(f"{'COUNT':>6}  {'SEV':<11} CODE"); print("-" * 68)
for (code, sev), n in by.most_common():
    print(f"{n:>6}  {sev:<11} {code}")
if _args.json_out:
    json.dump({"findings": findings, "orphans": orphans,
               "wanted_but_broken": wanted_but_broken}, open(_args.json_out, "w"), indent=1)
    print(f"\n(full findings -> {_args.json_out})")
else:
    print("\n(re-run with --json <path> for the full findings list)")

if _args.gate and any(f["severity"] == "blocking" for f in findings):
    sys.exit(1)
