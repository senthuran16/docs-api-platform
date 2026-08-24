#!/usr/bin/env python3
"""Turn raw broken-link findings into a fix plan that can be applied tier by tier.

    python3 scripts/report_links.py en/docs --out BROKEN-LINKS.md
    python3 scripts/report_links.py en/docs --scope <product>/<version> --out BROKEN-LINKS-<version>.md

`check_links.py` answers "what is broken". This answers "what do I change", which
is a different question and the one that actually gets the work done. Every
finding is classified by *cause*, because the causes have completely different
fixes:

  * wrong relative depth  -> exact mechanical rewrite, no judgement at all
  * renamed / moved page  -> a target exists elsewhere; propose it, rank confidence
  * genuinely gone        -> needs the pages read, cannot be automated
  * pre-migration domain  -> map to the new site or drop the link
  * missing anchor        -> heading was reworded

The report ends with a prompt written for an AI coding agent, so the mechanical
tiers can be handed straight off.
"""
import os
import re
import sys
import json
import argparse
import collections
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fm_lib import split_version, is_legacy_url  # noqa: E402
from links_lib import (  # noqa: E402
    find_targets, harvest_anchors, strip_noise, url_base, published, link_to,
    slug, resolve_candidates, version_root as _version_root,
    find_includes, snippet_for, match_anchor, normalise_var,
    build_include_map, legacy_path, read_toc_depth, non_web_scheme,
    has_uri_scheme, renders_anchors_clientside, strip_base_url, base_url_link,
    absolute_candidates,
)






def version_root(rel):
    return _version_root(rel, split_version)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docs_root", nargs="?", default="en/docs")
    ap.add_argument("--scope", default=None,
                    help="Only report files under this path prefix, e.g. <product>/<version>")
    ap.add_argument("--out", default="BROKEN-LINKS.md")
    ap.add_argument("--json", dest="json_out", default=None)
    ap.add_argument("--max-rows", type=int, default=40,
                    help="Rows per table in the Markdown before truncating (JSON is always complete).")
    args = ap.parse_args()

    root = args.docs_root.rstrip("/")

    all_files, md_list = set(), []
    for r, _, fs in os.walk(root):
        for f in fs:
            rel = os.path.relpath(os.path.join(r, f), root).replace("\\", "/")
            all_files.add(rel)
            if f.endswith(".md"):
                md_list.append(rel)
    md_list.sort()

    # SORTED, not set order. `all_files` is a set, so iterating it puts candidates
    # in hash order — which varies between processes. The `renamed` tier breaks
    # ties on candidate order, so without sorting the same command can propose a
    # different target from one run to the next. A plan nobody can reproduce cannot
    # be reviewed, and two people running the skill would disagree. Sorting makes
    # the choice a property of the repo, not of the run.
    by_basename = collections.defaultdict(list)
    for f in sorted(all_files):
        by_basename[os.path.basename(f)].append(f)

    # Lower-cased index, for spotting a link that differs from a real file only by
    # capital letters. Built once: this is 50k+ paths.
    lower_index = {}
    for f in sorted(all_files):
        lower_index.setdefault(f.lower(), f)

    def resolved_ci(cand):
        """The real file `cand` names if capital letters are ignored, else None.
        Returns None when an exact match exists — that is not a case problem."""
        for c in resolve_candidates(cand):
            if c in all_files:
                return None
            hit = lower_index.get(c.lower())
            if hit:
                return hit
        return None

    def resolved(cand):
        """The file `cand` actually names, or None. A bare path may be the file
        itself, the same path with `.md`, or a directory's index."""
        return next((c for c in resolve_candidates(cand) if c in all_files), None)

    def resolves(cand):
        return resolved(cand) is not None

    # `toc_depth` matters here, not just in the checker: with `toc_depth: 3` a
    # heading at h4 or deeper gets NO id, so a link to it goes nowhere even though
    # the heading is plainly there. Those are a separate, fixable cause.
    TOC = read_toc_depth(os.path.join(os.path.dirname(root) or ".", "mkdocs.yml"))

    # A page's anchors include the headings of every block it pulls in with
    # `--8<--`: the block's text is spliced in before Markdown runs, so those
    # headings get ids on the including page. Read the file text once, here, and
    # hand it to the harvester — otherwise a link to a heading that lives in a
    # shared block reads as broken on every page that uses the block.
    page_text = {}
    for p in md_list:
        page_text[p] = open(os.path.join(root, p), encoding="utf-8",
                            errors="replace").read()
    included = build_include_map(root, set(md_list), version_root)
    includes_of = {}
    for blk, pages in included.items():
        for pg in pages:
            includes_of.setdefault(pg, []).append(blk)

    anchors, deep_anchors = {}, {}
    for p in md_list:
        extra = [page_text[b] for b in includes_of.get(p, []) if b in page_text]
        anchors[p], deep_anchors[p] = harvest_anchors(page_text[p], TOC, extra)

    # Pages whose anchors are built in the browser, not by Markdown — the OpenAPI
    # reference pages are ReDoc containers. They hold no headings, so `anchors[p]`
    # is empty for them and EVERY fragment aimed at one would be filed as a
    # reworded heading. 49 findings repo-wide were sitting in the refused `anchor`
    # tier for exactly this reason, where nobody could act on them.
    clientside_anchor_pages = {
        p for p in md_list if renders_anchors_clientside(page_text[p])}

    # ---- which pages are PARTIALS, included into other pages ----
    #
    # A relative link inside a partial is resolved against the url of whatever page
    # included it, never against the partial's own location. So there is no
    # relative path this script can propose that is right — and when a partial has
    # two includers at different depths, no path exists that is right for both.
    # Proposing one anyway produces a link that works on one page and breaks on
    # another, which is the hardest kind of breakage to notice.
    # `included` is built above, next to the anchor harvest.

    # ---- WHICH SHARED BLOCKS STILL HAVE BROKEN LINKS OF THEIR OWN ----
    #
    # `{! !}` does nothing in this repo, so a block's content never reaches a page
    # and its broken links are inert. Converting to `--8<--` makes the block
    # render — and every broken link in it becomes a broken link on every page
    # that uses it.
    #
    # So switching on a block whose own links are broken trades hidden instructions
    # for visible broken images on every page that includes it. A block is only safe
    # to convert once its links work. This records which blocks are not ready, and
    # the `include` group refuses those.
    def block_link_broken_for(block, includer):
        """Does any link in `block` fail to resolve when spliced into `includer`?"""
        btxt = strip_noise(open(os.path.join(root, block), encoding="utf-8",
                                errors="replace").read())
        for _k, bt, bhtml in find_targets(btxt):
            if bt.startswith(("mailto:", "tel:", "//", "#", "#!")) or "{{" in bt:
                continue
            if has_uri_scheme(bt):
                continue
            bpath = urllib.parse.unquote(bt.partition("#")[0])
            if not bpath or bpath.startswith("/"):
                continue
            ibase = os.path.dirname(includer)
            lit = os.path.normpath(os.path.join(ibase, bpath)).replace("\\", "/")
            rw = (not bhtml) and lit in all_files
            cand = os.path.normpath(
                os.path.join(ibase if rw else url_base(includer), bpath)).replace("\\", "/")
            if not resolved(cand):
                return True
        return False

    block_unready = {}
    for blk in included:
        for inc in included[blk]:
            if block_link_broken_for(blk, inc):
                block_unready.setdefault(blk, set()).add(inc)

    deep_seen = set()      # (target page, anchor) already queued for an <a name>
    tiers = {k: [] for k in ("templated_fixable", "templated", "malformed", "dir_style",
                             "depth", "renamed", "case", "include", "gone", "stale",
                             "anchor", "anchor_case", "anchor_legacy", "anchor_punct",
                             "templated_typo", "partial", "include_abs",
                             "stale_mapped", "anchor_deep")}

    # Tiers whose fix is a relative path, and so cannot be applied inside a partial.
    RELATIVE_TIERS = ("templated_fixable", "templated_typo", "dir_style", "depth",
                      "renamed", "case", "stale_mapped")

    targets = [p for p in md_list if not args.scope or p.startswith(args.scope)]
    for p in targets:
        txt = open(os.path.join(root, p), encoding="utf-8", errors="replace").read()
        body = strip_noise(txt)
        d = os.path.dirname(p)
        stem = os.path.basename(p)[:-3]
        vroot = version_root(p)
        includers = sorted(included.get(p, ()))

        def queue_deep_anchor(target_file, anchor, referenced_by):
            """Queue an `<a name>` for a heading that sits below `toc_depth`.

            python-markdown gives no id to a heading deeper than `toc_depth`, so a
            link to it lands nowhere even though the heading is right there. An
            inert `<a name>` above it restores the target and leaves the heading
            level and the table of contents alone — the house pattern in these docs.

            NEVER `{#id}` instead: `markdownextradata` runs every page through Jinja
            before Markdown, `{#` opens a Jinja comment, and an unterminated one
            fails the whole build.

            One entry per heading, not per link: several links can name the same
            heading and the anchor only needs inserting once.
            """
            if anchor not in deep_anchors.get(target_file, set()):
                return False
            if (target_file, anchor) in deep_seen:
                return True
            ttxt = open(os.path.join(root, target_file), encoding="utf-8",
                        errors="replace").read()
            heading = next((ln for ln in ttxt.splitlines()
                            if re.match(r"^#{1,6}\s+", ln) and slug(
                                re.sub(r"^#{1,6}\s+", "", ln).strip()) == anchor), None)
            if not heading:
                return False
            deep_seen.add((target_file, anchor))
            tiers["anchor_deep"].append({
                "file": target_file, "anchor": anchor,
                "link": heading, "insert_above": heading,
                "suggested": f'<a name="{anchor}"></a>',
                "referenced_by": referenced_by,
                "why": f"the heading is deeper than h{TOC}, so the build gives it no "
                       f"id; an `<a name>` above it restores the target without "
                       f"touching the heading or the table of contents"})
            return True

        def place_anchor(t, target_file, frag):
            """File an anchor finding — but first check the two shapes that have a
            definite answer rather than being left unresolved.

            `case`   the heading exists, spelled with different capitals. Exact.
            `legacy` the anchor is an original Confluence one — page title and
                     heading run together — and exactly one heading matches once
                     both sides are reduced to letters and digits.

            Anything else is a reworded heading, and only reading the page says which
            one was meant.

            Nothing is filed when the target builds its anchors client-side: there
            are no headings to match, the fragment is resolved at runtime from the
            OpenAPI spec, and there is neither a fix to apply nor a decision to
            make. Reporting those trained readers to ignore the tier."""
            if target_file in clientside_anchor_pages:
                return
            # The heading EXISTS but sits deeper than `toc_depth`, so the build
            # gives it no id and the link goes nowhere. Fixable, and the fix edits
            # the TARGET page rather than this one: an inert `<a name>` above the
            # heading. Already the house pattern in these docs. Never
            # `{#id}`: the markdownextradata plugin runs every page through Jinja
            # before Markdown, `{#` opens a Jinja comment, and an unterminated one
            # fails the whole build.
            if queue_deep_anchor(target_file, frag, p):
                return

            # Match against the deep headings too. A heading below `toc_depth` is
            # still a heading someone can have been aiming at — it just has no id
            # yet. When the match lands on one, BOTH fixes are needed: give the
            # heading an anchor, and repoint the link at it. They are separate
            # groups, so run `anchor_deep` first and the target exists by the time
            # the link is repointed.
            known = anchors.get(target_file, set())
            hit, how = match_anchor(frag, known | deep_anchors.get(target_file, set()))
            if hit and hit not in known:
                queue_deep_anchor(target_file, hit, p)
            if hit:
                place("anchor_" + how, {
                    "file": p, "link": t, "target_file": target_file,
                    "anchor": frag, "resolves_to": target_file,
                    "is_html": is_html,
                    "suggested": t.partition("#")[0] + "#" + hit,
                    "confidence": "high",
                    "why": ("the heading exists with different capital letters"
                            if how == "case" else
                            "the heading exists; only the hyphens and underscores "
                            "between the words were written differently"
                            if how == "punct" else
                            "original Confluence anchor; exactly one heading on the "
                            "page matches once both are reduced to letters and digits")})
                return
            tiers["anchor"].append({"file": p, "link": t,
                                    "target_file": target_file, "anchor": frag})

        def place(name, entry):
            """File a proposal under its tier — unless this page is a partial.

            A relative fix inside a partial is unsafe no matter how carefully it is
            computed, because it is resolved from the includer's url and not from
            this file. Where the tier identified a real target, that is exactly the
            case `{BASE_URL}` exists for: re-aim the same fix at the docs root and
            it stops depending on depth. Where it did not, the proposal is kept to
            be read and moved out of reach of `fix_links.py` — `suggested` is
            renamed on the way, because a key named `suggested` is exactly what an
            agent would apply."""
            if includers and name in RELATIVE_TIERS:
                entry = dict(entry)
                target = entry.get("resolves_to") or entry.get("found_at")
                if target and target in all_files:
                    frag = entry.get("link", "").partition("#")[2]
                    entry["suggested"] = base_url_link(target, frag)
                    entry["resolves_to"] = target
                    entry["includers"] = includers
                    entry["intended_tier"] = name
                    entry["why"] = (
                        f"{entry.get('why', name)} — and this page is included into "
                        f"{len(includers)} other page(s), so the fix is written from "
                        f"the docs root rather than as a relative path")
                    tiers["include_abs"].append(entry)
                    return
                entry["unsafe_suggestion"] = entry.pop("suggested", None)
                entry["intended_tier"] = name
                entry["includers"] = includers
                entry["why"] = ("this page is included into "
                                f"{len(includers)} other page(s), so a relative link "
                                "resolves against the includer's url, not this file's")
                tiers["partial"].append(entry)
                return
            tiers[name].append(entry)

        # ---- SHARED BLOCKS: `{! path !}` does nothing in this repo ----
        #
        # Not a link, but the same kind of migration damage and far more visible.
        # `{! path !}` needs the `markdown_include` extension, which the old repo
        # switched on and this one does not — so the directive is left on the page
        # and the READER SEES IT as text where the steps should be.
        #
        # `pymdownx.snippets` IS switched on and does the same job with a different
        # syntax, and 4.5.0 was already converted to it, so that is the target
        # form rather than turning on a second mechanism.
        #
        # The address has to change too. The old repo built one site per version, so
        # a page could write `includes/foo.md` and mean "this version's includes
        # folder". Here all eleven versions share one tree, so the version has to be
        # spelled out. Nothing is proposed unless the resulting file really exists.
        for syntax, inc_path, whole in find_includes(txt):
            if syntax == "snippet":
                if inc_path not in all_files:
                    tiers["include"].append({
                        "file": p, "link": whole, "kind": "shared block",
                        "note": f"snippet target `{inc_path}` does not exist; the "
                                f"block it pulled in may have been dropped for this "
                                f"version"})
                continue
            fixed = snippet_for(inc_path, vroot)
            target = re.match(r'--8<--\s*"([^"]+)"', fixed).group(1)
            if target in all_files and target in block_unready:
                # Switching this block on would put its own broken links onto this
                # page. Fix the block first — the `include_abs` and `partial`
                # groups list exactly what is wrong with it.
                tiers["include"].append({
                    "file": p, "link": whole, "kind": "shared block",
                    "blocked_by": target,
                    "note": f"`{target}` has links that do not resolve from this "
                            f"page, so switching the block on would move its broken "
                            f"links onto {len(included.get(target, ()))} page(s). "
                            f"Fix the block first — see `include_abs` / `partial`."})
            elif target in all_files:
                tiers["include"].append({
                    "file": p, "link": whole, "suggested": fixed,
                    "resolves_to": target, "literal": True, "kind": "shared block",
                    "why": "`{! !}` is not enabled in this repo, so it stays on the "
                           "page as text; `--8<--` is enabled and does the same job"})
            else:
                tiers["include"].append({
                    "file": p, "link": whole, "kind": "shared block",
                    "note": f"no file at `{target}` — the shared block was not "
                            f"carried into this version, so someone has to say "
                            f"whether the page still needs it"})

        # The third element records whether the target was written in raw HTML.
        # mkdocs rewrites Markdown targets and leaves HTML alone, so the two need
        # different bases — see url_base() above.
        raw = find_targets(body)

        for kind, t, is_html in raw:
            if t.startswith(("mailto:", "tel:", "//", "#!")):
                continue

            # Anything carrying a URI scheme is an ADDRESS, not a path on disk.
            # `check_links.py` has always skipped these; the reporter did not, so
            # the two disagreed and correct `ldap://10.100.1.100:389` examples in
            # the user-store pages were filed under `gone`. non_web_scheme()
            # returns None for HTTP_TYPOS, so `ttps://` stays a `malformed` fix.
            if non_web_scheme(t):
                continue

            # Already written from the docs root. `check_links.py` resolves these
            # and reports a genuinely missing target; there is no tier for them
            # here, because there is no rewrite to propose.
            if strip_base_url(t) is not None:
                continue

            # Malformed syntax, caught before resolution so it isn't mis-filed as a
            # missing target. Both forms below occur in migrated pages and both
            # render as literal broken text, so the fix is exact.
            # `{{base_path}}` stands for the root of the version's site, so the
            # remainder is a path relative to that version's directory. Where the
            # resource actually exists there, the link can be rewritten as an
            # ordinary relative path and the variable dropped — that is a real fix,
            # not a guess. Where it does not exist, the target may be served by a
            # redirect, so leave it alone until the redirect strategy is settled.
            if re.search(r"\{\{.*?\}\}", t):
                # A MISSPELLED VARIABLE NAME is a different defect from a missing
                # file, and it hides one: `{{base}}/x/` cannot resolve however
                # present `x` is, so it lands in `templated` and looks like a
                # content problem. Correct the spelling first and the link is
                # judged on its target like any other.
                m_var = re.match(r"^\{\{\s*([\w.-]+)\s*\}\}(/?.*)$", t)
                typo_of = None
                if m_var and m_var.group(1) != "base_path":
                    fixed_name = normalise_var(m_var.group(1))
                    if fixed_name == "base_path":
                        typo_of = m_var.group(1)
                        t_norm = "{{base_path}}" + m_var.group(2)
                    else:
                        t_norm = t
                else:
                    t_norm = t

                m_bp = re.match(r"^\{\{\s*base_path\s*\}\}/?(.*)$", t_norm)
                fixed = None
                if m_bp:
                    rest, _, bfrag = m_bp.group(1).partition("#")
                    rest = urllib.parse.unquote(rest).strip("/")
                    base_dir = vroot if vroot else ""
                    cand = f"{base_dir}/{rest}" if base_dir else rest
                    cand = os.path.normpath(cand).replace("\\", "/")
                    target = resolved(cand)
                    if target == p:
                        # The page links to itself. A relative path back to your own
                        # url works but reads as a mistake; the fragment alone is
                        # what someone would write by hand.
                        fixed = ("#" + bfrag) if bfrag else "./"
                    elif target:
                        fixed = link_to(target, p, is_html)
                        if bfrag:
                            fixed += "#" + bfrag
                if fixed:
                    place("templated_typo" if typo_of else "templated_fixable", {
                        "file": p, "link": t, "suggested": fixed,
                        "is_html": is_html, "resolves_to": target,
                        **({"misspelled": f"{{{{{typo_of}}}}}"} if typo_of else {}),
                        "why": (f"`{{{{{typo_of}}}}}` is `{{{{base_path}}}}` mistyped; "
                                f"with the spelling corrected the resource exists"
                                if typo_of else
                                "resource exists, so the variable can be replaced "
                                "with a relative path")})
                else:
                    tiers["templated"].append({
                        "file": p, "link": t,
                        "variable": ", ".join(sorted(set(re.findall(r"\{\{.*?\}\}", t)))),
                        **({"misspelled": f"{{{{{typo_of}}}}}",
                            "note": f"`{{{{{typo_of}}}}}` is `{{{{base_path}}}}` mistyped, "
                                    f"but the resource is missing too, so correcting "
                                    f"the spelling alone would not fix it"} if typo_of else {})})
                continue

            raw_t = t
            cleaned = t.strip("`'\"")                       # [text](`https://…`)
            m_hash = re.match(r"^(#{2,})([\w-]+)$", cleaned)  # [text](###anchor)
            if m_hash:
                tiers["malformed"].append({
                    "file": p, "link": raw_t, "suggested": "#" + m_hash.group(2),
                    "why": f"{len(m_hash.group(1))} `#` characters; an anchor takes exactly one"})
                continue
            if cleaned != raw_t:
                tiers["malformed"].append({
                    "file": p, "link": raw_t, "suggested": cleaned,
                    "why": "target is wrapped in backticks or quotes, so it is not a valid URL"})
                continue
            if is_legacy_url(t):
                # The old site is still up, so these links WORK today — which is
                # exactly what makes them dangerous: nothing looks broken, and they
                # all die together when that site is retired. Most can be mapped
                # mechanically, because the migration kept the path: look the old
                # path up under THIS page's version.
                lfrag = t.partition("#")[2]
                # Two shapes reach here. An old-site URL keeps its path but not
                # its version — see legacy_path(). A hardcoded site base path
                # (`/bijira/docs/...`) is already a path inside this repo, so it
                # is resolved as one rather than having its version discarded.
                if t.startswith("/"):
                    mapped = next((m for m in (
                        resolved(c) for c in absolute_candidates(
                            t.partition("#")[0], vroot)) if m), None)
                else:
                    lp = legacy_path(t)
                    mapped = resolved(f"{vroot}/{lp}") if (lp and vroot) else None
                if mapped and mapped != p:
                    place("stale_mapped", {
                        "file": p, "link": t, "resolves_to": mapped,
                        "is_html": is_html, "kind": kind,
                        "suggested": link_to(mapped, p, is_html)
                                     + (("#" + lfrag) if lfrag else ""),
                        "why": "the same path exists under this version, so the link "
                               "can point inside the new docs instead of at the old site"})
                else:
                    tiers["stale"].append({"file": p, "link": t})
                continue
            if re.match(r"^https?://", t):
                continue

            # A SHARED BLOCK is not judged from its own folder. Every relative
            # answer below — does it resolve, how deep is it, what should it say —
            # depends on a base that mkdocs never uses for a block, because the
            # block's text is spliced into the including page before Markdown runs.
            # The includer-aware pass further down owns these, and it can also tell
            # a link that is genuinely fine (this loop reported those as broken)
            # from one that breaks on the pages that use it (this loop called those
            # clean, which is how 62 of them were "fixed" into breakage).
            if includers:
                continue

            path, _, frag = t.partition("#")
            path = urllib.parse.unquote(path)
            frag = urllib.parse.unquote(frag)

            if not path:
                if frag and frag not in anchors.get(p, set()):
                    place_anchor(t, p, frag)
                continue

            # WHICH BASE APPLIES — verified against a real mkdocs build.
            #
            # mkdocs rewrites a Markdown target only when the literal path names a
            # file that exists; then it is resolved against the SOURCE directory.
            # Everything else — raw HTML, directory-style links (`../foo/bar/`),
            # extensionless links (`../foo/bar`) — is passed through verbatim and
            # resolved by the browser against the RENDERED URL, one level deeper.
            if is_html:
                own_base, alt_base = url_base(p), d
                rewritten = False
            else:
                literal = os.path.normpath(os.path.join(d, path)).replace("\\", "/")
                rewritten = literal in all_files
                own_base, alt_base = (d, url_base(p)) if rewritten else (url_base(p), d)

            own_rel = os.path.normpath(os.path.join(own_base, path)).replace("\\", "/")
            if resolves(own_rel):
                if frag:
                    tf = next((c for c in (own_rel, own_rel + ".md", own_rel + "/index.md",
                                           own_rel + "/README.md") if c in all_files), None)
                    if tf and tf.endswith(".md") and frag not in anchors.get(tf, set()):
                        place_anchor(t, tf, frag)
                continue

            # A Markdown link written in URL shape, whose `.md` file sits exactly
            # where the link already points. Adding the extension is the real fix,
            # not adding a `../`: mkdocs then owns the depth calculation and the link
            # keeps working when the page moves. Checked BEFORE the depth tier so the
            # brittle fix never wins.
            if not is_html and not rewritten:
                src_guess = os.path.normpath(os.path.join(d, path)).replace("\\", "/")
                md_target = next((c for c in (src_guess + ".md", src_guess + "/index.md",
                                              src_guess + "/README.md") if c in all_files), None)
                if md_target:
                    # Markdown-only by construction (`not is_html` above), so the
                    # source path is the right form — mkdocs rewrites it from here.
                    fixed = link_to(md_target, p, False)
                    place("dir_style", {
                        "file": p, "link": t, "resolves_to": md_target,
                        "suggested": fixed + (("#" + frag) if frag else ""),
                        "why": "written as a URL, so mkdocs passes it through unresolved"})
                    continue

            # Resolves against the OTHER base — so the depth is wrong by exactly the
            # one level between a source file and its rendered directory.
            alt_rel = os.path.normpath(os.path.join(alt_base, path)).replace("\\", "/")
            cand_ci_source = resolved_ci(own_rel)
            cand_ci_url = resolved_ci(alt_rel)
            alt_file = resolved(alt_rel)
            if alt_file:
                if alt_file == p:
                    fixed = ("#" + frag) if frag else "./"
                else:
                    fixed = link_to(alt_file, p, is_html) + (("#" + frag) if frag else "")
                place("depth", {"file": p, "link": t, "resolves_to": alt_file,
                                       "is_html": is_html, "suggested": fixed})
                continue

            # SAME PATH, WRONG CAPITAL LETTERS.
            #
            # Checked before the rename search, because this is not a guess: the
            # file is exactly where the link says, spelled with different capitals.
            # It matters more than the count suggests — macOS treats `Photo.png`
            # and `photo.png` as one file, so these links work perfectly in a local
            # preview and 404 on the Linux machine that builds the real site. They
            # are invisible to the person most likely to catch them.
            #
            # The fix always changes the LINK to match the FILE, never the other
            # way round: other pages may already point at the current filename.
            ci = None
            for cc in (cand_ci_source, cand_ci_url):
                if cc:
                    ci = cc
                    break
            if ci:
                place("case", {"file": p, "link": t, "resolves_to": ci,
                               "is_html": is_html, "kind": kind,
                               "suggested": link_to(ci, p, is_html) + (("#" + frag) if frag else ""),
                               "why": "the file is at that path but spelled with "
                                      "different capital letters; this works on "
                                      "macOS and breaks on the build server"})
                continue

            # Nothing resolves. Look for a file of the same name elsewhere — the
            # restructure renamed directories without updating links, so the page
            # usually still exists somewhere under the same version root.
            base = os.path.basename(path.rstrip("/")) or stem
            cands = by_basename.get(base + ".md", []) + by_basename.get(base, [])
            if vroot:
                # STRICT — never fall back to the unscoped candidate list when
                # nothing matches inside the version. That proposes targets in
                # *other* versions, sending a reader from a current page to an old
                # release. A missing page inside this version is `gone`, not a
                # reason to look in another version.
                cands = [c for c in cands if c.startswith(vroot + "/")]
            cands = [c for c in cands if c != p]

            if len(cands) == 1:
                sug = link_to(cands[0], p, is_html)
                place("renamed", {"file": p, "link": t, "found_at": cands[0],
                                         "is_html": is_html,
                                         "suggested": sug + (("#" + frag) if frag else ""),
                                         "confidence": "high"})
            elif 2 <= len(cands) <= 5:
                ranked = sorted(cands, key=lambda c: (-len(os.path.commonprefix([c, p])), c))
                sug = link_to(ranked[0], p, is_html)
                place("renamed", {"file": p, "link": t, "found_at": ranked[0],
                                         "is_html": is_html,
                                         "suggested": sug + (("#" + frag) if frag else ""),
                                         "confidence": f"low ({len(cands)} candidates)",
                                         "alternatives": ranked[:5]})
            elif cands:
                # A generic basename like `overview.md` matches dozens of pages.
                # Guessing one would be worse than saying nothing: a guess reads as
                # an answer, and nobody re-checks an answer. List the field instead.
                ranked = sorted(cands, key=lambda c: (-len(os.path.commonprefix([c, p])), c))
                tiers["gone"].append({"file": p, "link": t,
                                      "kind": kind,
                                      "note": f"{len(cands)} files share this name — too ambiguous to propose one",
                                      "candidates": ranked[:6]})
            else:
                tiers["gone"].append({"file": p, "link": t,
                                      "kind": kind,
                                      "note": "no file of this name exists anywhere under the docs root"})

    # ---- LINKS INSIDE SHARED BLOCKS, judged from the pages that include them ----
    #
    # An include splices the block's text into the including page BEFORE Markdown
    # runs, so every link in the block is resolved as if it had been written in
    # that page. Judging it from the block's own folder — which is what the loop
    # above does, because it has no other way to treat a file — is wrong twice:
    #
    #   * it reports links that are perfectly fine, and
    #   * it calls links CLEAN that break on every page using the block.
    #
    # The second is the dangerous direction and it is not hypothetical. A previous
    # pass over 4.6.0 "fixed" 62 links to be correct relative to the block itself.
    # They resolve from the block, they point at nothing from the includer, and
    # nothing flagged them — because from the block's own folder they look right.
    #
    # So resolve from each includer instead — and where the target can be
    # identified, the fix is not a relative path at all.
    #
    # THE CONVENTION, settled for this repo: a link inside a shared block is
    # written `{BASE_URL}/<path from the docs root>`. `hooks.py` swaps the token
    # for the site base path, so the address does not depend on the depth of the
    # page the block lands on — which is the one thing no relative path can
    # manage. It applies to every link in a block, not only the broken ones: a
    # relative link that works today does so because every page using the block
    # happens to sit at the same depth, and the next page to use it need not.
    #
    # Ordinary pages are deliberately NOT converted. mkdocs only validates
    # relative Markdown links (`path_to_url` returns anything absolute untouched),
    # so making a page absolute buys nothing and gives up build-time checking.
    for part in sorted(included):
        if args.scope and not part.startswith(args.scope):
            continue
        incs = sorted(included[part])
        body = strip_noise(open(os.path.join(root, part), encoding="utf-8",
                                errors="replace").read())
        for kind, t, is_html in find_targets(body):
            if t.startswith(("mailto:", "tel:", "//", "#", "#!")) or "{{" in t:
                continue
            if has_uri_scheme(t):
                continue
            if strip_base_url(t) is not None:
                continue                       # already converted
            path, _, frag = t.partition("#")
            path = urllib.parse.unquote(path)
            if not path:
                continue

            # An ABSOLUTE link in a block does not depend on the including page,
            # so there is nothing to resolve per includer — but it is still the
            # wrong address. `/bijira/docs/...` hardcodes a site base path that
            # `site_url` can change, and `/deploy-and-publish/...` meant "the
            # version root" in the old one-site-per-version repo and now points
            # at the server root. Both become `{BASE_URL}` like everything else,
            # and only when the target is actually found on disk.
            if path.startswith("/"):
                hit = next((m for m in (resolved(c) for c in
                            absolute_candidates(path, version_root(part))) if m), None)
                if hit:
                    tiers["include_abs"].append({
                        "file": part, "link": t, "suggested": base_url_link(hit, frag),
                        "resolves_to": hit, "is_html": is_html, "includers": incs,
                        "broken_for": [], "kind": kind,
                        "why": "absolute link inside a shared block; `{BASE_URL}` "
                               "replaces a hardcoded site base path with one that "
                               "follows `site_url`"})
                continue

            def land(page, _path=path, _html=is_html):
                """Where this link lands when the block is spliced into `page`."""
                base = os.path.dirname(page)
                literal = os.path.normpath(os.path.join(base, _path)).replace("\\", "/")
                rewritten = (not _html) and literal in all_files
                rel = base if rewritten else url_base(page)
                return resolved(os.path.normpath(os.path.join(rel, _path)).replace("\\", "/"))

            landings = {i: land(i) for i in incs}
            broken_for = [i for i, v in landings.items() if not v]
            # Where the includers that DO resolve disagree about which file they
            # land on, the same text means two different pages depending on where
            # the block is used. Converting would silently pick one of them.
            distinct = {v for v in landings.values() if v}
            if len(distinct) > 1:
                tiers["partial"].append({
                    "file": part, "link": t, "includers": incs,
                    "broken_for": broken_for, "kind": kind,
                    "candidates": sorted(distinct),
                    "note": "resolves to a DIFFERENT file depending on which page "
                            "includes the block, so no single address is right — "
                            "someone has to say which page was meant"})
                continue

            # What did the author mean? The file the includers land on, and failing
            # that whatever the link resolves to from the block's own folder — that
            # is the base whoever wrote it was thinking in.
            intent = next(iter(distinct), None) or land(part)
            if not intent:
                # Resolves from no including page AND not from the block itself, so
                # there is no evidence of what was meant. Still has to be reported:
                # the main loop deliberately skips block pages now, so if this
                # returned early the finding would vanish entirely.
                tiers["partial"].append({
                    "file": part, "link": t, "includers": incs,
                    "broken_for": broken_for, "kind": kind,
                    "note": "does not resolve from any page that includes this "
                            "block, and no target of that name could be identified "
                            "— someone has to say where it was meant to point"})
                continue

            why = (f"broken from {len(broken_for)} of {len(incs)} including page(s)"
                   if broken_for else
                   f"resolves from all {len(incs)} including page(s) today, but only "
                   f"because they sit at the same depth")
            tiers["include_abs"].append({
                "file": part, "link": t,
                "suggested": base_url_link(intent, frag),
                "resolves_to": intent, "is_html": is_html, "includers": incs,
                "broken_for": broken_for, "kind": kind,
                "why": f"link inside a shared block — {why}; `{{BASE_URL}}` "
                       f"addresses it from the docs root, so it does not depend on "
                       f"the depth of the page the block lands on"})

    # ---------------- write the report ----------------
    n = {k: len(v) for k, v in tiers.items()}
    total = sum(n.values())
    scope_label = args.scope or f"all of {root}"
    auto = (n["templated_fixable"] + n["malformed"] + n["dir_style"] + n["depth"]
            + n["case"] + n["anchor_case"] + n["anchor_legacy"] + n["anchor_punct"]
            + n["templated_typo"]
            + n["include_abs"] + n["stale_mapped"] + n["anchor_deep"]
            + len([e for e in tiers["include"] if e.get("suggested")])
            + len([x for x in tiers["renamed"] if x["confidence"] == "high"]))

    L = []
    w = L.append
    w(f"# Broken links and images — `{scope_label}`")
    w("")
    w(f"**{total} findings** across {len(targets)} pages. "
      f"**{auto}** have an exact or high-confidence mechanical fix; "
      f"**{n['gone']}** need a decision.")
    w("")
    # Groups are named, not numbered. The name is the value `fix_links.py --tier`
    # takes, so a row in this table is directly runnable. Numbering them invited
    # the obvious question of why two groups shared a number and one had none.
    w("### Fixable by script")
    w("")
    w("Run in this order. Each is a separate `fix_links.py --tier` run, and every "
      "rewrite is verified against the files on disk before it is written.")
    w("")
    w("| Order | Group | Cause | Count | Fix |")
    w("|---|---|---|---|---|")
    w(f"| 1 | `malformed` | Malformed link syntax | {n['malformed']} | Exact — no judgement |")
    w(f"| 2 | `dir_style` | Written as a URL, so mkdocs never resolves it | {n['dir_style']} | Add `.md` — mkdocs then owns the depth |")
    w(f"| 3 | `depth` | Wrong relative depth | {n['depth']} | Exact — no judgement |")
    w(f"| 4 | `renamed` | Renamed or moved target | {n['renamed']} | Proposed; `high` confidence applied by default |")
    w(f"| 5 | `templated_fixable` | `{{{{base_path}}}}` where the resource exists | {n['templated_fixable']} | Exact rewrite to a relative path |")
    w(f"| 6 | `case` | Right path, wrong capital letters | {n['case']} | Exact — works on macOS, breaks on the build server |")
    w(f"| 7 | `include` | `{{! !}}` shared block, which this repo does not process | "
      f"{len([e for e in tiers['include'] if e.get('suggested')])} of {n['include']} | "
      f"Convert to `--8<--` with the version spelled out |")
    w(f"| 8 | `anchor_case` | Anchor names a real heading, wrong capitals | {n['anchor_case']} | Exact — heading ids are always lower-case |")
    w(f"| 9 | `anchor_legacy` | Original Confluence anchor | {n['anchor_legacy']} | Matched to the one heading that agrees letter for letter |")
    w(f"| 9b | `anchor_punct` | Anchor names a real heading, different hyphens/underscores | {n['anchor_punct']} | Exact — same words in the same order, one heading matches |")
    w(f"| 10 | `templated_typo` | `{{{{base_path}}}}` misspelled, resource present | {n['templated_typo']} | Corrects the spelling and writes a relative path |")
    w(f"| 11 | `include_abs` | Link inside a shared block, written as a relative path | {n['include_abs']} | Rewrite as `{{BASE_URL}}/…` from the docs root, so it does not depend on the depth of the page the block lands on |")
    w(f"| 12 | `stale_mapped` | Old-site url whose path exists under this version | {n['stale_mapped']} | Point it inside the new docs instead |")
    w(f"| 13 | `anchor_deep` | Heading exists but is deeper than h{TOC}, so it has no id | {n['anchor_deep']} | Insert `<a name>` above the heading |")
    w("")
    w("### Needs a decision")
    w("")
    w("`fix_links.py` refuses these. The information needed is not in the repository, "
      "and a guess produces a confident link to the wrong page — worse than a visibly "
      "broken one, because nobody re-checks it.")
    w("")
    w("| Group | Cause | Count | Why it cannot be automated |")
    w("|---|---|---|---|")
    w(f"| `templated` | `{{{{base_path}}}}` where the resource does not exist | {n['templated']} | May be served by a redirect |")
    w(f"| `stale` | Pre-migration domain | {n['stale']} | Needs the equivalent page on the new site |")
    w(f"| `anchor` | Missing anchor | {n['anchor']} | The heading was reworded — which one now? |")
    w(f"| `gone` | No target anywhere | {n['gone']} | Was it dropped, missed, or merged? |")
    w(f"| `partial` | Broken link inside an included partial | {n['partial']} | "
      f"Resolves against the includer's url, not the partial's |")
    w("")

    def table(rows, cols, keys, limit):
        w("| " + " | ".join(cols) + " |")
        w("|" + "|".join(["---"] * len(cols)) + "|")
        for r in rows[:limit]:
            w("| " + " | ".join(f"`{r.get(k,'')}`" if k != "confidence" else str(r.get(k, ""))
                                for k in keys) + " |")
        if len(rows) > limit:
            w("")
            w(f"_…and {len(rows) - limit} more. Full list in the JSON sidecar._")
        w("")

    if n["templated_fixable"]:
        w("## `templated_fixable` — `{{base_path}}` where the resource exists")
        w("")
        w("`{{base_path}}` stands for the root of the version's site, so the rest of the "
          "target is a path within that version's directory. For these, the resource is "
          "there: the variable can be dropped and the link written as an ordinary relative "
          "path. The replacement below is exact.")
        w("")
        table(tiers["templated_fixable"], ["Page", "Currently", "Change to"],
              ["file", "link", "suggested"], args.max_rows)

    if n["partial"]:
        files = sorted({e["file"] for e in tiers["partial"]})
        w(f"## Excluded — {n['partial']} findings inside {len(files)} included partial(s)")
        w("")
        w("Every one of these would otherwise have been a mechanical fix. They are held "
          "back because the file is pulled into other pages with an include directive, "
          "so a relative link in it is resolved against **the includer's** url, not the "
          "partial's own. Where a partial has includers at different depths, no single "
          "relative path is correct for all of them — a fix that works on one page "
          "breaks on another, which is the hardest breakage to notice.")
        w("")
        w("The computed path is kept as `unsafe_suggestion` in the JSON rather than "
          "`suggested`, and `fix_links.py` refuses this tier. Resolving them needs a "
          "decision about how partials should link at all: a root-relative path, or "
          "moving the link out of the partial and into each page.")
        w("")
        table(sorted(tiers["partial"], key=lambda e: (e["file"], e["link"])),
              ["Partial", "Link", "Intended group", "Included by"],
              ["file", "link", "intended_tier", "includers"], args.max_rows)
        w("")

    if n["templated"]:
        w("## Excluded — `{{base_path}}` where the resource does not exist")
        w("")
        w("Same variable, but the target is not present at that path in this version. It may "
          "be served by a redirect, or the page may not have been migrated. **Leave these "
          "alone** until the redirect strategy is settled — a rewrite here would be a guess.")
        w("")
        table(tiers["templated"], ["Page", "Link", "Variable"],
              ["file", "link", "variable"], args.max_rows)

    if n["malformed"]:
        w("## `malformed` — Malformed link syntax")
        w("")
        w("The link target is not a valid path or URL, so it renders as literal broken text "
          "regardless of whether the destination exists. Carried over from the old wiki. "
          "The replacement is exact.")
        w("")
        table(tiers["malformed"], ["Page", "Currently", "Change to", "Why"],
              ["file", "link", "suggested", "why"], args.max_rows)

    if n["dir_style"]:
        w("## `dir_style` — Written as a URL, so mkdocs never resolves it")
        w("")
        w("These point at the right page already. Because the target is written in URL "
          "shape rather than naming the `.md` file, mkdocs passes it through untouched and "
          "the browser resolves it against the rendered page URL — one directory deeper "
          "than the source file, so it lands one level short. Adding the extension hands "
          "the depth calculation back to mkdocs, permanently.")
        w("")
        table(tiers["dir_style"], ["Page", "Currently", "Change to"],
              ["file", "link", "suggested"], args.max_rows)
        w("")

    if n["depth"]:
        w("## `depth` — Wrong relative depth")
        w("")
        w("The target exists; the path has one `../` too many. These render correctly in a "
          "browser (the published URL sits one directory deeper than the source file), so they "
          "look fine on the site — but `mkdocs build` warns about every one, and anyone reading "
          "the raw Markdown through `md_url` gets a broken path. The replacement below is exact.")
        w("")
        table(tiers["depth"], ["Page", "Currently", "Change to"],
              ["file", "link", "suggested"], args.max_rows)

    if n["renamed"]:
        hi = [x for x in tiers["renamed"] if x["confidence"] == "high"]
        lo = [x for x in tiers["renamed"] if x["confidence"] != "high"]
        w("## `renamed` — Renamed or moved target")
        w("")
        w("The target does not exist at the path written, but a file of the same name exists "
          "elsewhere under the same version. This is the restructure: directories were renamed "
          "and the inbound links were never updated.")
        w("")
        if hi:
            w(f"### Exactly one candidate — high confidence ({len(hi)})")
            w("")
            table(hi, ["Page", "Currently", "Change to"], ["file", "link", "suggested"], args.max_rows)
        if lo:
            w(f"### Several candidates — verify before applying ({len(lo)})")
            w("")
            table(lo, ["Page", "Currently", "Best guess", "Confidence"],
                  ["file", "link", "suggested", "confidence"], args.max_rows)

    if n["stale"]:
        w("## `stale` — Links to the pre-migration site")
        w("")
        w("These point at a location the documentation has migrated away from. For each "
          "one: find the equivalent page on the new site and link to it relatively, or if the "
          "content wasn't migrated, remove the link and say so in the prose. Never leave a "
          "reader on the old site.")
        w("")
        table(tiers["stale"], ["Page", "Link"], ["file", "link"], args.max_rows)

    if n["anchor"]:
        w("## `anchor` — Missing anchor")
        w("")
        w("The page resolves but the `#fragment` matches no heading, so the reader lands at the "
          "top instead of the section. Usually the heading was reworded. Open the target, find "
          "the heading that was meant, and use its current slug.")
        w("")
        table(tiers["anchor"], ["Page", "Link", "Target file", "Missing anchor"],
              ["file", "link", "target_file", "anchor"], args.max_rows)

    if n["gone"]:
        w("## `gone` — No target anywhere")
        w("")
        w("No file of this name exists anywhere under the docs root, so there is nothing to "
          "point at. Each needs a decision: was the page meant to be migrated and missed, was it "
          "deliberately dropped (then the link and its sentence should go), or was it merged into "
          "another page (then link there)? **Do not guess these.**")
        w("")
        table(tiers["gone"], ["Page", "Broken target", "Note"],
              ["file", "link", "note"], args.max_rows)

    # ---- the agent prompt ----
    w("---")
    w("")
    w("## Prompt for an AI coding agent")
    w("")
    w("Paste the block below to an agent working in the repo root. It is deliberately scoped to "
      "the four groups with a defensible mechanical answer. `templated`, `stale`, `anchor` and "
      "`gone` need judgement and are left out on purpose.")
    w("")
    w("Alternatively, run `fix_links.py --tier <group>` yourself — same scope, one group at a "
      "time, and every rewrite verified against the files on disk before it is written.")
    w("")
    w("````text")
    w(f"You are fixing broken links in the WSO2 API Platform docs, scope: {scope_label}.")
    w("")
    w(f"Read the fix plan in `{args.out}`" +
      (f" and the machine-readable list in `{args.json_out}`." if args.json_out else "."))
    w("")
    w("Apply ONLY these groups:")
    w("  - `templated_fixable`: apply every row as given.")
    w("  - `malformed`: apply every row exactly as given.")
    w("  - `dir_style`: apply every row exactly as given (adds `.md`).")
    w("  - `depth`: apply every row exactly as given.")
    w("  - `renamed`, the high-confidence subsection only: apply every row as given.")
    w("")
    w("Rules:")
    w("  1. Replace only the link target inside the parentheses. Never change the link TEXT,")
    w("     the surrounding sentence, or anything else on the line.")
    w("  2. A target may appear more than once in a file — replace every occurrence of that")
    w("     exact target in that file.")
    w("  3. Preserve any `#fragment` already on the link unless the plan says otherwise.")
    w("  4. Do NOT touch `templated`, `stale`, `anchor` or `gone`. Do not invent a")
    w("     target that is not in the plan.")
    w("  5. Do not reformat, reflow, or reorder anything. Minimal diffs only.")
    w("")
    w("Verify when done, from the repo root:")
    w(f"  python3 .claude/skills/wso2-doc-frontmatter/scripts/check_links.py {root}" +
      (f" --json /tmp/after.json" if True else ""))
    w("")
    w("The blocking count must go DOWN and no new codes may appear. If any count rises, stop")
    w("and report what you changed rather than continuing.")
    w("")
    w("Then report: rows applied per group, files touched, and the before/after blocking counts.")
    w("````")
    w("")
    w("### Why `templated`, `stale`, `anchor` and `gone` are excluded")
    w("")
    w("Each needs information that isn't in the repo: which new page replaces an old-site link, "
      "which reworded heading was meant, whether a missing page was dropped on purpose. An agent "
      "asked to fix those will produce plausible links to the wrong places, which is worse than "
      "a visibly broken link because nobody re-checks it.")
    w("")
    w("Template-variable links are excluded for a different reason: they are not broken at all "
      "in their original context. They depend on a build-time substitution, and whether that "
      "survives migration is a redirect-strategy decision, not a link fix.")

    open(args.out, "w", encoding="utf-8").write("\n".join(L) + "\n")

    if args.json_out:
        json.dump({"scope": args.scope, "docs_root": root, "counts": n, "tiers": tiers},
                  open(args.json_out, "w"), indent=1)

    print(f"{total} findings across {len(targets)} pages "
          f"({auto} mechanically fixable, {n['gone']} need a decision)")
    for k in ("templated_fixable", "templated_typo", "templated", "malformed",
              "dir_style", "depth", "renamed", "case", "include", "anchor_case",
              "anchor_legacy", "anchor_punct", "include_abs", "stale_mapped",
              "anchor_deep",
              "stale", "anchor", "gone", "partial"):
        print(f"  {n[k]:5d}  {k}")
    print(f"\nreport -> {args.out}")
    if args.json_out:
        print(f"json   -> {args.json_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
