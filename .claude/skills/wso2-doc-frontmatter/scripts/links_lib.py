#!/usr/bin/env python3
"""Shared link logic for check_links.py, report_links.py and fix_links.py.

`url_base`, `slug`, the anchor harvester and the link patterns must have exactly
one definition. If a copy is taken into one of the three scripts and the two drift
— one computing a raw-HTML path against the rendered url, the other against the
source directory — the reporter proposes fixes the fixer refuses, and neither is
obviously wrong on its own. Prefer adding to this file over copying out of it.

The two ideas that matter:

  WHICH BASE A RELATIVE LINK COUNTS FROM — `url_base()`, `link_to()`.
  mkdocs rewrites a Markdown target that names a real file, resolving it against
  the SOURCE directory. It passes raw HTML through untouched, so the browser
  resolves it against the RENDERED url, one level deeper for a non-index page.

  WHERE A TARGET SITS IN THE TEXT — `md_targets()`, `rewrite_target()`.
  Linked images nest (`[![](a.png)](a.png)`), and any pattern for `[text](target)`
  is blind to the outer target because the link text itself contains `](`.
"""
import os
import re

# ----------------------------------------------------------------- link finding
#
# `MD_TARGET_AT` matches only the `](target)` tail, NOT a whole `[text](target)`.
# That is the whole point: a whole-link pattern cannot see the outer target of a
# nested linked image, because the link text contains `](` and the match ends at
# the inner `)`. Anchoring on the tail finds every target regardless of nesting.
MD_TARGET_AT = re.compile(r"""\]\(\s*<?([^)\s>]+)>?(?:\s+"[^"]*")?\s*\)""")

# Kept for callers that need the whole construct (alt text, image syntax checks).
MD_LINK = re.compile(r'(!?)\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+"[^"]*")?\s*\)')

# The tag name is captured so an `<a href>` is reported as a broken LINK, an
# `<img src>` as a missing IMAGE, and a `<video src>` as missing MEDIA — three
# different things to go looking for. The quote character is captured and
# back-referenced: HTML allows either and these pages use both, so a
# double-quote-only pattern skips the single-quoted ones silently.
#
# Every tag that can carry an address belongs here, and every address attribute —
# `poster` and `data` as well as `src` and `href`. A checker that reads only some
# tags reports "clean" for the rest.
HTML_SRC = re.compile(
    r"""<(img|a|source|iframe|video|audio|embed|object|track)\b"""
    r"""[^>]*?\b(?:src|href|data|poster)=(["'])(.*?)\2""", re.I)

LINK_TAGS = {"a"}
IMAGE_TAGS = {"img", "source", "picture"}


def target_kind(tag):
    """`link`, `image` or `media` — so the report says what to go looking for."""
    tag = tag.lower()
    if tag in LINK_TAGS:
        return "link"
    return "image" if tag in IMAGE_TAGS else "media"


# Shared blocks pulled into a page. Two syntaxes are in play here, and only one
# of them is switched on in this repo:
#
#   {! path !}                 markdown_include — NOT enabled, so this stays on
#                              the page as literal text for the reader to see
#   --8<-- "path"              pymdownx.snippets — enabled, base_path: docs
#
# So `{! !}` is not merely misaddressed, it does nothing at all.
MD_INCLUDE = re.compile(r"\{!\s*([^!}\n]+?)\s*!\}")
SNIPPET = re.compile(r'--8<--\s*"([^"\n]+)"')

# What sits IMMEDIATELY around a target — used for rewriting, see rewrite_target.
MD_OPEN = re.compile(r"\]\(\s*<?\Z")
MD_CLOSE = re.compile(r""">?(?:\s+"[^"]*")?\s*\)""")
HTML_OPEN = re.compile(r"""(?:src|href)\s*=\s*(["'])\Z""")


FENCE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")

# An `attr_list` explicit heading id. The spaces matter: these pages write both
# `{#step-8}` and `{ #step-8 }`, and a pattern without `\s*` misses the spaced form,
# which reports real, working anchors as missing.
#
# Note `{ #id }` with a space is also the SAFE form to write: `{#` with no space
# opens a Jinja comment, and `markdownextradata` runs Jinja over every page before
# Markdown sees it, so an unspaced `{#...}` can fail the whole build. Harvest both,
# and keep suggesting `<a name="...">` as the fix — see harvest_anchors.
EXPLICIT_ID = re.compile(r"\{\s*#([\w-]+)\s*\}")


def strip_noise(text, drop_pre=True):
    """Blank out comments and fenced code, so their contents are not read as links.

    Line by line, tracking the open fence — NOT `re.sub("```.*?```")`. That
    shortcut pairs the first fence with the next one anywhere in the document, and
    these pages are full of fences that do not pair that way: indented inside list
    items, `~~~` as well as backticks, and fence characters shown *inside* another
    fence. Whatever such a shortcut eats goes invisible — anchors reported as
    missing when the heading is right there, and links never checked at all.

    A closing fence must be the same character, at least as long, and carry no info
    string; that is the CommonMark rule and it is what makes indented and nested
    fences come out right.

    An opener with no closer is NOT treated as a fence, and this is checked against
    the renderer rather than reasoned about: given ```` ``` ```` followed by a link
    and no closing fence, Python-Markdown with `pymdownx.superfences` publishes that
    link as a real `<a href>`. superfences wants a closing fence and falls back to
    plain markdown without one. So an unclosed opener must not blank anything —
    otherwise the pages that have one go invisible from that line to the end while
    the published site really does carry those links. Pages do have stray fences
    like that, most often an unmatched *closing* fence left behind after someone
    pasted console output.

    Lines are blanked rather than deleted so line numbers still line up with the
    file, which matters when a finding has to be pointed at.
    """
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    # Raw `<pre>` is literal text, not Markdown. Generated pages hold configuration
    # samples inside `<pre><code>`, where a line like `#offset=0` would otherwise
    # read as a heading — inventing an anchor id that lets a genuinely broken link
    # pass as fine. Newlines are preserved so line numbers still match the file.
    if drop_pre:
        text = re.sub(r"(?is)<pre\b.*?</pre\s*>",
                      lambda m: "\n" * m.group(0).count("\n"), text)
    lines = text.split("\n")

    # First pass: find the fenced regions that actually close. An opener still open
    # at end of file is discarded, matching what the renderer does with it.
    blank = [False] * len(lines)
    fence = None
    for i, line in enumerate(lines):
        m = FENCE.match(line)
        if fence is None:
            # CommonMark: a backtick fence's info string may not contain a backtick.
            # That rule is what keeps a prose line like
            #     ```--query deployed:true``` filters the revisions
            # from being read as the start of a code block — it is inline code, and
            # the renderer treats it that way. Without the rule one such line hides
            # every link below it on the page.
            if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
                fence = (m.group(1)[0], len(m.group(1)), i)
        else:
            ch, n, start = fence
            if m and m.group(1)[0] == ch and len(m.group(1)) >= n and not m.group(2).strip():
                for j in range(start, i + 1):
                    blank[j] = True
                fence = None

    return "\n".join("" if blank[i] else line for i, line in enumerate(lines))


def _matching_open(text, close_idx):
    """Index of the `[` that opens the `]` at `close_idx`, or -1.

    Counts nesting, so the outer `[` of `[![](x)](y)` is found rather than the
    inner one.
    """
    depth = 1
    for i in range(close_idx - 1, -1, -1):
        c = text[i]
        if c == "]":
            depth += 1
        elif c == "[":
            depth -= 1
            if depth == 0:
                return i
    return -1


def md_destination(body, at):
    """Read the destination of the `](...)` that starts at index `at`.

    Returns `(target, end_index)` where `end_index` is just past the closing `)`,
    or None if there is no closing `)`.

    This is a scanner rather than a regular expression because two shapes in this
    repo need it, and both were checked against the renderer (Python-Markdown)
    rather than guessed at:

    - **Parentheses inside the address.** `](../admin-v4/#tag/Workflows-(Individual)/paths/~1x/post)`
      — the renderer counts parentheses and takes the address up to the one that
      balances. A `[^)]+` pattern stops at the `)` after `Individual`, which both
      truncates the address and loses the rest. These are the ReDoc anchors in the
      product-API pages, and some of them point at the pre-migration `develop/`
      tree, so they are exactly the links worth finding.
    - **A literal space in a filename.** `](../assets/img/deploy/revision deployment-updated-status.png)`
      — strictly invalid CommonMark, but the renderer publishes the whole path and
      the file on disk really is named with a space. A pattern that stops at
      whitespace matched nothing at all here, so the link was invisible.

    An optional `"title"` after the address is dropped, and the `<...>` form is
    unwrapped, both the way the renderer does it.
    """
    i = at + 2
    n = len(body)
    if i < n and body[i] == "<":
        j = body.find(">", i)
        k = body.find(")", j) if j >= 0 else -1
        if j >= 0 and k >= 0:
            return body[i + 1:j].strip(), k + 1
        return None
    depth, j = 1, i
    while j < n:
        c = body[j]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                break
        elif c == "\n" and body[j - 1:j] == "\n":
            return None            # a blank line ends the construct
        j += 1
    if depth != 0:
        return None
    raw = body[i:j].strip()
    # Drop a trailing title, which is quoted and separated by whitespace. A space
    # with no quotes around the tail is part of the filename, not a title.
    tm = re.search(r"""\s+(?:"[^"]*"|'[^']*')\Z""", raw)
    if tm:
        raw = raw[:tm.start()].strip()
    return raw, j + 1


def md_targets(body):
    """Every Markdown link and image target in `body`, nesting included.

    Returns a list of dicts: `target`, `is_img`, `start`, `end`, `open`.

    `[![](a.png)](a.png)` — a linked image, and the normal way images are written
    in these docs — holds two targets. A `[text](target)` pattern finds only the
    inner one.

    Where the outer target is IDENTICAL to the image it wraps, it is one authored
    construct pointing at one file, and is reported once: counting it twice would
    double every linked image while finding nothing new. Where the two DIFFER, the
    outer target is a separate link worth checking, and it is kept.
    """
    found = []
    for m in re.finditer(r"\]\(", body):
        dest = md_destination(body, m.start())
        if dest is None:
            continue
        target, end = dest
        if not target:
            continue
        open_idx = _matching_open(body, m.start())
        found.append({"target": target,
                      "is_img": open_idx > 0 and body[open_idx - 1] == "!",
                      "start": m.start(), "end": end, "open": open_idx})
    images = [f for f in found if f["is_img"]]
    out = []
    for f in found:
        if not f["is_img"] and any(
                f["open"] < g["start"] and g["end"] <= f["start"]
                and g["target"] == f["target"] for g in images):
            continue
        out.append(f)
    return out


def find_targets(body):
    """Every link target on the page as `(kind, target, is_html)`.

    `kind` is `link`, `image` or `media`. `is_html` decides which base the target
    resolves against, so it must travel with the target everywhere — see
    `url_base()`.
    """
    out = [("image" if f["is_img"] else "link", f["target"], False)
           for f in md_targets(body)]
    out += [(target_kind(m.group(1)), m.group(3), True)
            for m in HTML_SRC.finditer(body)]
    return out


def find_includes(body):
    """Shared-block directives on the page, as `(syntax, path, whole_match)`.

    `syntax` is `md_include` for `{! path !}` or `snippet` for `--8<-- "path"`.
    """
    out = [("md_include", m.group(1).strip(), m.group(0))
           for m in MD_INCLUDE.finditer(body)]
    out += [("snippet", m.group(1).strip(), m.group(0))
            for m in SNIPPET.finditer(body)]
    return out


def build_include_map(root, md_files, version_root_of=None):
    """`{shared block -> set of pages that include it}`.

    Needed by both the checker and the reporter, and they must agree: an include
    splices the block's text into the including page BEFORE Markdown runs, so
    every link in a block is resolved from the INCLUDING page. Judging a block
    from its own folder is not a near-enough approximation — it reports links that
    are fine and, worse, passes links that break on every page using the block.

    The three syntaxes are written relative to different roots depending on plugin
    configuration, so each candidate is tried and the first that names a real file
    wins.
    """
    out = {}
    for p in sorted(md_files):
        try:
            txt = open(os.path.join(root, p), encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        vr = version_root_of(p) if version_root_of else ""
        for rx in (MD_INCLUDE, SNIPPET,
                   re.compile(r'\{%\s*include\s+"([^"\n]+)"')):
            for m in rx.finditer(txt):
                tgt = m.group(1).strip()
                for cand in ([f"{vr}/{tgt}"] if vr else []) + [
                        tgt,
                        os.path.normpath(
                            os.path.join(os.path.dirname(p), tgt)).replace("\\", "/")]:
                    if cand in md_files:
                        out.setdefault(cand, set()).add(p)
                        break
    return out


def snippet_for(path, page_version_root):
    """The `--8<--` directive that pulls in `path` as written on a page.

    `pymdownx.snippets` is configured with `base_path: docs`, so the address is
    relative to `en/docs` — NOT to the page, and NOT to the version. The old repo
    built one site per version, so a page could write `includes/foo.md` and mean
    "this version's includes folder". Here all eleven versions share one tree, so
    that same text now names a folder that does not exist and the version has to
    be spelled out.
    """
    rest = path.lstrip("./").lstrip("/")
    full = f"{page_version_root}/{rest}" if page_version_root else rest
    return f'--8<-- "{os.path.normpath(full)}"'.replace("\\", "/")


# ------------------------------------------------------------------ URI schemes
SCHEME = re.compile(r"^([a-zA-Z][a-zA-Z0-9+.\-]*):")

# Mistypings of http/https seen in these pages. These ARE defects, and exactly
# the kind `malformed` can fix, so they must not be swallowed by the
# "unknown scheme, leave it alone" rule below.
HTTP_TYPOS = {"ttp", "ttps", "htp", "htps", "hhttp", "hhttps",
              "htttp", "htttps", "ttpss", "http s", "https s"}


def non_web_scheme(target):
    """The URI scheme of `target` when it is neither http nor https, else None.

    Anything with a scheme is an address, not a path on disk. Resolving
    `ldap://10.100.1.100:389` against the docs root reports a correct example
    connection string in a user-store page as a broken link. Only `mailto:` and
    Every non-web scheme must be listed here, or it falls through to path
    resolution.

    A scheme in `HTTP_TYPOS` is returned as None so the caller keeps treating it
    as something to fix rather than something to ignore.
    """
    m = SCHEME.match(target)
    if not m:
        return None
    s = m.group(1).lower()
    if s in ("http", "https") or s in HTTP_TYPOS:
        return None
    return s


def is_http_typo(target):
    """Does `target` look like an http(s) URL with a mistyped scheme?"""
    m = SCHEME.match(target)
    return bool(m) and m.group(1).lower() in HTTP_TYPOS


# Markers of a page that is a container for a client-side renderer rather than
# Markdown content. Both appear on the OpenAPI reference pages in this repo.
CLIENTSIDE_ANCHOR_MARKERS = ("templates/redoc.html", "<redoc")


def renders_anchors_clientside(text):
    """Are this page's anchors generated in the BROWSER rather than by Markdown?

    An OpenAPI reference page is a ReDoc container — `template: templates/redoc.html`
    plus a `<redoc spec-url=...>` element — and ReDoc builds the operation anchors
    (`#tag/Applications/paths/~1applications~1{applicationId}/put`) at runtime from
    the spec file. The `.md` holds no headings at all, so harvesting anchors from it
    returns an empty set and every fragment "fails".

    Treat a fragment on such a page as **unverifiable, not invalid**: skip the
    anchor check rather than pass or fail it. Failing it reports correct deep links
    as broken; passing it would claim a guarantee that was never checked. Skipping
    is what lets the *path* half of a `dir_style` or `renamed` fix be applied while
    leaving the fragment untouched.
    """
    return any(m in text for m in CLIENTSIDE_ANCHOR_MARKERS)


def has_uri_scheme(target):
    """Does `target` carry ANY uri scheme — including http, https and typos?

    Distinct from `non_web_scheme()`, and the difference matters. Use this where
    the only question is "can this be resolved as a path on disk?", which is
    false for every scheme. Use `non_web_scheme()` where an http(s) target still
    has to be classified afterwards (a legacy domain, a mistyped scheme), because
    that one deliberately returns None for http, https and `HTTP_TYPOS` so the
    caller keeps handling them.

    Swapping one for the other silently changes what is skipped: narrowing a
    has-any-scheme guard to non_web_scheme lets external URLs fall through to
    path resolution and be reported as broken links.
    """
    return bool(SCHEME.match(target))


# --------------------------------------------------------------- page addresses
def url_base(rel):
    """Directory the RENDERED page sits in, under `use_directory_urls: true`.

    `a/b/page.md` is served at `/a/b/page/`, one level DEEPER than the source
    file; `a/b/index.md` is served at `/a/b/`, the same level.

    A relative target written in raw HTML is resolved by the browser against
    this, not against the source directory — so the identical string is correct
    in one syntax and broken in the other. On an `index.md` the two coincide,
    which is why a wrong rule looks right on every landing page.
    """
    d = os.path.dirname(rel)
    stem = os.path.basename(rel)[:-3] if rel.endswith(".md") else os.path.basename(rel)
    return d if stem in ("index", "README") else (f"{d}/{stem}" if d else stem)


def published(rel):
    """Where a source file is SERVED. `a/b.md` -> `a/b`, `a/index.md` -> `a`, and
    a non-Markdown file is served where it sits."""
    return url_base(rel) if rel.endswith(".md") else rel


def link_to(target, page, is_html):
    """A relative link from `page` to `target` that resolves in the BUILT site.

    Markdown and raw HTML differ in two ways, not one:

      * WHAT IT COUNTS FROM — the source directory, or the rendered url.
      * WHAT IT POINTS AT — for Markdown, the source path (`../a/b.md`), so
        mkdocs computes the url and the link survives the page moving. For raw
        HTML, the published path with a trailing slash (`../a/b/`). `../a/b.md`
        in raw HTML resolves — `hooks.py` publishes a raw `.md` beside every page
        — and serves Markdown source to the reader. A link checker calls that
        fine.

    `target` must be a path that exists, not a candidate.
    """
    if not is_html:
        return os.path.relpath(target, os.path.dirname(page)).replace("\\", "/")
    rel = os.path.relpath(published(target), url_base(page)).replace("\\", "/")
    if not target.endswith(".md"):
        return rel                      # an asset is served where it sits
    return "./" if rel == "." else rel.rstrip("/") + "/"


# ------------------------------------------------------- the {BASE_URL} address
#
# `{BASE_URL}` is the repo's depth-independent way of writing a link. `hooks.py`
# replaces the literal string with the path half of `site_url` (`/api-platform/
# docs`) in `on_post_page`, after the page HTML is assembled — so what follows the
# token is a path from the DOCS ROOT, and it means the same thing no matter which
# page the text ends up on.
#
# That last part is the whole point. `pymdownx.snippets` splices a shared block
# into pages at different depths, so no relative path can be right for all of
# them; a `{BASE_URL}` address does not depend on depth at all. This repo uses it
# inside `includes/` and nowhere else — ordinary pages stay source-relative,
# because those are the only links mkdocs validates at build time.
#
# SINGLE braces, and that is deliberate. `{{base_path}}` is Jinja, substituted by
# `markdownextradata` at `on_page_markdown` — which runs BEFORE Markdown parsing,
# and therefore before snippets has spliced any block in. A `{{...}}` written in a
# block is never seen by the plugin and reaches the reader as literal text.
BASE_URL_TOKEN = "{BASE_URL}"


def strip_base_url(target):
    """The docs-root-relative path inside a `{BASE_URL}/...` target, else None.

    None means "not one of these", which is not the same as an empty path, so
    callers must test `is not None` rather than truthiness.
    """
    if not target.startswith(BASE_URL_TOKEN):
        return None
    return target[len(BASE_URL_TOKEN):].lstrip("/")


def base_url_link(target, frag=""):
    """The `{BASE_URL}` address for `target`, a path from the docs root.

    mkdocs does not resolve a link it considers absolute (`path_to_url` returns
    any URL starting with `/` untouched), and after substitution these do start
    with `/`. So unlike a Markdown relative link, this must name the PUBLISHED
    path, not the source file: `.../endpoint-types/`, never `.../endpoint-types.md`,
    which would ship the `.md` verbatim and serve Markdown source to the reader.

    An asset is served where it sits, so it keeps its extension and takes no
    trailing slash.
    """
    if target.endswith(".md"):
        addr = f"{BASE_URL_TOKEN}/{published(target)}/"
    else:
        addr = f"{BASE_URL_TOKEN}/{target}"
    return addr + (("#" + frag) if frag else "")


# Site base paths that have been hardcoded into links in these pages. This is
# CONFIGURATION, not logic — add a value when another turns up. `/bijira/docs` is
# the current `site_url`; `/api-platform/docs` is what the local preview uses and
# what most of the migrated pages were written against.
SITE_BASE_PREFIXES = ("/bijira/docs", "/api-platform/docs")

_VERSION_SEG = re.compile(r"^\d+\.\d+\.\d+$")


def absolute_candidates(path, vroot=""):
    """Docs-root-relative paths an ABSOLUTE link might have meant, best first.

    An absolute link is passed through to the browser untouched, so unlike a
    relative one it does not depend on the page — but it also is not checked by
    anything, and three different meanings are written the same way here:

      /bijira/docs/api-manager/4.1.0/x   the site base path, hardcoded
      /api-manager/4.1.0/x               already relative to the docs root
      /deploy-and-publish/x              relative to the VERSION root, which is
                                         what it meant in the old repo, where
                                         every version was built as its own site

    The caller resolves these in order and takes the first that exists, so a
    shape that names nothing on disk proposes nothing. Where a candidate names a
    version other than the page's own, a copy re-anchored on `vroot` is offered
    after it — a cross-version link sends the reader to a different release, and
    this page's version is the right answer.
    """
    p = path.strip("/")
    if not p:
        return []
    out = []
    for prefix in SITE_BASE_PREFIXES:
        pre = prefix.strip("/")
        if p == pre or p.startswith(pre + "/"):
            out.append(p[len(pre):].strip("/"))
    out.append(p)
    if vroot:
        out.append(f"{vroot}/{p}")
    if vroot:
        for c in list(out):
            parts = c.split("/")
            if len(parts) > 2 and _VERSION_SEG.match(parts[1]) and \
                    "/".join(parts[:2]) != vroot:
                out.append(f"{vroot}/" + "/".join(parts[2:]))
    seen = set()
    return [c for c in out if c and not (c in seen or seen.add(c))]


def version_root(rel, split_version):
    """`<product>/<version>/a/b.md` -> `<product>/<version>`, else ''.

    Takes `split_version` as an argument rather than importing `fm_lib`, to keep
    this module free of a dependency it would only need for one call.
    """
    ver, _ = split_version(rel)
    if not ver:
        return ""
    parts = rel.split("/")
    return "/".join(parts[: parts.index(ver) + 1])


def resolve_candidates(cand):
    """The spellings a bare path may have on disk, in the order to try them."""
    return (cand, cand + ".md", cand + "/index.md", cand + "/README.md")


def page_id(p):
    """Collapse the ways one page can be spelled into a single identity, so
    `foo/bar`, `foo/bar.md` and `foo/bar/index.md` compare equal."""
    p = (p or "").rstrip("/")
    for suffix in ("/index.md", "/README.md"):
        if p.endswith(suffix):
            return p[: -len(suffix)]
    return p[:-3] if p.endswith(".md") else p


# ----------------------------------------------------------------------- anchors
def slug(h):
    """python-markdown's toc slugify: strip non-word characters, then collapse
    runs of whitespace AND hyphens into a single hyphen."""
    # `<api-name>` inside a code span is TEXT, not a tag. The renderer escapes it to
    # `&lt;api-name&gt;` and then slugifies that, giving `...name-ltapi-namegt`.
    # Stripping it as if it were markup produced a different id and a false claim.
    h = re.sub(r"`+([^`]*)`+",
               lambda m: m.group(1).replace("&", "amp").replace("<", "lt")
                                   .replace(">", "gt"), h)
    h = re.sub(r"`|\*", "", h)                        # keep _, it is a \w char
    h = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", h)    # link text only
    h = re.sub(r"<[^>]+>", "", h)
    h = re.sub(r"[^\w\s-]", "", h).strip().lower()
    return re.sub(r"[-\s]+", "-", h)


LIST_ITEM = re.compile(r"^(\s*)(?:[-*+]|\d+[.)])\s")
# `\s*` not `\s+` after the hashes: python-markdown is not in strict mode, so
# `#Gateway Policies` with no space IS a heading and does get an id. Requiring a
# space reports those anchors as missing when they work.
HEADING = re.compile(r"^(\s*)(#{1,6})\s*([^#\s].*?)\s*$")


def headings(text):
    """`(level, text)` for every heading the renderer will publish.

    Headings INDENTED INSIDE A LIST ITEM count. These pages are full of them —

        3.  Add the specific documentation.

            -   [Add in-line documentation](#add-in-line-documentation)

            ### Add in-line documentation

    — and Python-Markdown publishes that as `<h3 id="add-in-line-documentation">`,
    so the link works. A pattern anchored with `^#` misses it and reports a working
    anchor as missing, which is the dangerous direction: an agent asked to fix it
    would repoint a link that was already right.

    An indented heading only counts when a list is actually open above it. At top
    level the same line is not a heading at all — 4 spaces makes it an indented code
    block, and even 2 spaces gets no heading out of Python-Markdown — so treating
    every indented `###` as a heading would invent ids that do not exist and hide
    genuinely broken links.
    """
    out = []
    # The OUTERMOST open list marker, not the most recent one. In
    #     3.  Add the documentation.
    #         -   [x](#add-in-line-documentation)
    #         ### Add in-line documentation
    # the heading sits at the same indent as the `-`, so comparing against the
    # nearest marker would reject it. It is content of item `3.` at indent 0.
    open_min = None
    for line in text.split("\n"):
        li = LIST_ITEM.match(line)
        if li:
            n = len(li.group(1))
            open_min = n if open_min is None else min(open_min, n)
        elif line.strip() and not line[:1].isspace():
            open_min = None               # back at column 0, the list is closed
        m = HEADING.match(line)
        if not m:
            continue
        indent = len(m.group(1))
        if indent and (open_min is None or indent <= open_min):
            continue                      # not a heading the renderer will publish
        out.append((len(m.group(2)), m.group(3)))
    return out


def harvest_anchors(text, toc_depth=6, included_text=()):
    """Anchor ids a page actually publishes, and the ones it should but doesn't.

    Pass the text of any `--8<--` block the page includes as `included_text`: the
    block's headings are spliced into the page before Markdown runs, so they are the
    including page's anchors too. Without it, a link to a heading that lives in a
    shared block reads as broken.

    Returns `(anchors, deep)`. `deep` holds ids a heading WOULD have if
    `toc_depth` allowed it: with `toc_depth: 3`, python-markdown gives h4 and
    deeper NO id, so `#some-h4-heading` resolves to nothing even though the
    heading is right there in the Markdown. Keeping them separate lets that be
    reported as its own cause.

    Do NOT suggest `{#id}` as the fix for a deep heading, even though `attr_list`
    honours it: the `markdownextradata` plugin runs every page through Jinja
    BEFORE Markdown, and `{#` opens a Jinja comment — an unterminated one fails
    the whole build with "Missing end of comment tag". The safe additive fix is
    `<a name="...">` immediately above the heading: inert HTML, already the pattern
    used in these docs, and it leaves the heading level and the TOC untouched.
    """
    # Two views of the page. Headings must not be read out of a raw `<pre>` block
    # (TOML comments in there are not headings), but `id=` attributes inside one
    # ARE real anchors — the Confluence code export writes `<span id="cb1-1">`
    # inside `<pre>`, and those ids resolve. So headings come from the stripped
    # text and ids from the text that still has its `<pre>` blocks.
    with_pre = "\n\n".join([strip_noise(text, drop_pre=False)]
                            + [strip_noise(e, drop_pre=False) for e in included_text])
    text = "\n\n".join([strip_noise(text)]
                        + [strip_noise(e) for e in included_text])
    anchors, deep = set(), set()
    seen = {}                  # slug -> how many times, for the `_1` suffix below
    for level, h in headings(text):
        exp = re.search(EXPLICIT_ID, h)
        if exp:
            # An explicit id REPLACES the generated one — `attr_list` publishes
            # `{ #step-9 }` and nothing else, so adding the slug of the heading text
            # as well would claim an id the page does not have, and a link pointing
            # at that id would be passed as fine.
            anchors.add(exp.group(1))          # explicit id survives any toc_depth
            continue
        base = slug(h)
        # python-markdown makes a repeated heading unique with `_1`, `_2`, ... The
        # second `## Step 2 - Verify the changes` on a page is `#step-2-verify-the-
        # changes_1`, and a link to it looks broken unless that is modelled.
        n = seen.get(base, 0)
        seen[base] = n + 1
        ident = base if not n else f"{base}_{n}"
        (anchors if level <= toc_depth else deep).add(ident)
    # Any element's `id`, and `name` on an `<a>` — not just `<a id>`. A fragment
    # resolves against any id on the page, and these pages are full of ids on other
    # tags: the Confluence code-block export writes
    #     <span id="cb1-1"><a href="#cb1-1"></a>...
    # so the target and the link sit on the same line, and reading only `<a id>`
    # reports those working anchors as missing.
    for m in re.finditer(r"""<[a-zA-Z][^>]*?\bid=(["'])(.*?)\1""", with_pre):
        anchors.add(m.group(2))
    for m in re.finditer(r"""<a[^>]+\bname=(["'])(.*?)\1""", with_pre):
        anchors.add(m.group(2))
    for m in re.finditer(EXPLICIT_ID, text):
        anchors.add(m.group(1))
    return anchors, deep - anchors


LEGACY_URL = re.compile(
    r"^https?://apim\.docs\.wso2\.com/(?:en/)?([^/]+)/(.*?)/?$", re.I)


def legacy_path(url):
    """The documentation path inside an old-site URL, or None.

    `https://apim.docs.wso2.com/en/latest/install-and-setup/setup/security/x/`
    -> `install-and-setup/setup/security/x`

    The version segment in the URL is deliberately DISCARDED. A link like this on
    a 4.6.0 page should point at 4.6.0's copy of the content, not at whatever the
    URL happens to name — and `/en/latest/` names no version at all, it follows
    the newest release. So a 4.6.0 page currently linking to `latest` is showing
    readers 4.7.0 content and will show them 4.8.0 content when that ships. The
    page's own version is the right answer; the caller supplies it.
    """
    m = LEGACY_URL.match(url.split("#")[0])
    if not m:
        return None
    path = m.group(2).strip("/")
    return path or None


def squash(s):
    """Reduce to letters and digits only, lower-cased.

    Used to compare an anchor against a heading when the two disagree about
    spaces, hyphens, colons and capitals but not about the words.
    """
    return re.sub(r"[^a-z0-9]", "", s.lower())


LEGACY_ANCHOR = re.compile(r"^[A-Za-z0-9]+-")


SLUG_SHAPE = re.compile(r"\A[\w-]+\Z")


def sep_key(s):
    """Reduce runs of hyphens and underscores to one hyphen, lower-cased.

    Words and their order are kept exactly — this only forgives how the separators
    between them were written. That is much tighter than `squash()`, which throws
    every separator away: `set-a-limit` and `set-alimit` are the same under
    `squash` but different under this.
    """
    return re.sub(r"[-_]+", "-", s.lower()).strip("-")


def match_anchor(frag, anchors):
    """The heading `frag` was meant to name. Returns `(anchor, how)` or `(None, None)`.

    Three shapes, all left over from the migration, all with a definite answer:

    `case` — `#Upload-new-API-thumbnail` where the heading id is
    `upload-new-api-thumbnail`. Heading ids are always lower-cased when they are
    generated, so this is exact, not a guess.

    `legacy` — `#AddingaCustomProxyPath-Step1:Installandconfigureareverseproxy`
    where the heading id is `step-1-install-and-configure-a-reverse-proxy`. The
    original Confluence export joined the page title and the heading text with a
    hyphen and threw away every space and separator. Dropping the title prefix and
    comparing letters-and-digits only lines the two up again.

    `punct` — `#step-1---enable-the-community-links-option` where the heading is
    `### Step 1 - Enable the community links option`. python-markdown collapses the
    spaces AND the hyphen around the dash into a single hyphen, so the published id
    is `step-1-enable-the-community-links-option`. The link kept all three. Same
    class: `#step-2-verify-the-changes-1` where a repeated heading gets the id
    `step-2-verify-the-changes_1`. The words and their order are identical and only
    the separators differ, so there is one answer. Candidates are restricted to
    ids of normal slug shape, which keeps a hand-written oddity like
    `<a name="#step3-2">` out of it.

    **Only accepted when exactly ONE heading matches.** A unique match is the whole
    reason this is safe to propose; where a match is ambiguous, returning None and
    returning None is the correct outcome, not picking the first.
    """
    if not frag or frag in anchors:
        return None, None

    lower = {a.lower(): a for a in anchors}
    if frag.lower() in lower:
        return lower[frag.lower()], "case"

    # Only the Confluence shape: a run-together prefix, then a hyphen, and at
    # least one capital somewhere. An ordinary lower-case anchor that simply does
    # not exist must fall through as unresolved.
    if LEGACY_ANCHOR.match(frag) and not frag.islower():
        key = squash(frag.split("-", 1)[1])
        if key:
            hits = [a for a in anchors if squash(a) == key]
            if len(hits) == 1:
                return hits[0], "legacy"

    key = sep_key(frag)
    if key:
        hits = [a for a in anchors if SLUG_SHAPE.match(a) and sep_key(a) == key]
        if len(hits) == 1:
            return hits[0], "punct"
    return None, None


# Misspellings of `base_path` seen in these pages. CONFIGURATION, not logic —
# extend it when another spelling turns up. Deliberately an explicit list rather
# than a similarity measure: `base` is four characters away from `base_path`, so
# any distance threshold loose enough to catch it would also catch real variables.
BASE_PATH_ALIASES = {"base", "basepath", "base_patgh", "basepth", "base-path"}


def normalise_var(name):
    """`base_path` when `name` is one of its known misspellings, else `name`."""
    return "base_path" if name.lower() in BASE_PATH_ALIASES else name


# ------------------------------------------------------------------- mkdocs.yml
def read_toc_depth(mkdocs_yml):
    """The `toc_depth` configured for the python-markdown toc extension."""
    if not os.path.isfile(mkdocs_yml):
        return 6
    text = open(mkdocs_yml, encoding="utf-8", errors="replace").read()
    m = re.search(r"^\s*toc_depth:\s*['\"]?(\d)", text, re.M)
    return int(m.group(1)) if m else 6


def read_extra_vars(mkdocs_yml):
    """Top-level keys defined under `extra:` in mkdocs.yml.

    These are the variables `markdownextradata` can substitute into a page. A
    `{{base_path}}` in the content is only checkable if `base_path` is here — and
    in this repo it is NOT, so those links render with an empty string and point
    at the server root. Reading the config beats hardcoding either assumption:
    the answer changes the moment someone defines it.

    Scoped regex for the same reason as `read_redirect_maps`.
    """
    if not os.path.isfile(mkdocs_yml):
        return set()
    text = open(mkdocs_yml, encoding="utf-8", errors="replace").read()
    m = re.search(r"^extra:\s*\n(.*?)(?=^\S|\Z)", text, re.S | re.M)
    if not m:
        return set()
    return set(re.findall(r"^  ([A-Za-z_][\w-]*):", m.group(1), re.M))


def read_redirect_maps(mkdocs_yml):
    """The `redirect_maps` block from mkdocs.yml as `{source: target}`.

    A scoped regex rather than a YAML load: this mkdocs.yml carries custom tags
    and a very large nav, so a strict parse is slow and prone to choking. The
    block is flat `source: target` pairs.

    Why a link checker needs this at all: `mkdocs-redirects` builds a real page
    at each source path, so a link pointing at one WORKS in the published site.
    Checking only the files on disk reports those as broken.
    """
    if not os.path.isfile(mkdocs_yml):
        return {}
    text = open(mkdocs_yml, encoding="utf-8", errors="replace").read()
    m = re.search(r"^\s*redirect_maps:\s*\n(.*?)(?=\n\s{0,4}\S|\Z)", text, re.S | re.M)
    if not m:
        return {}
    return dict(re.findall(r"^\s+(\S+\.md):\s*(\S+\.md)\s*$", m.group(1), re.M))


def redirect_targets(redirect_maps):
    """The set of paths a link may point at and still work, because a redirect is
    published there. Both the `.md` source and its directory url are included."""
    out = set()
    for src in redirect_maps:
        out.add(src)
        out.add(page_id(src))
    return out


# ------------------------------------------------------------------- rewriting
def rewrite_target(txt, link, suggested, is_html):
    """Replace `link` with `suggested` where it sits in a TARGET position of the
    matching syntax. Returns `(new_text, occurrences_changed)`.

    A plain `str.replace` is wrong twice over:

      * SUBSTRINGS. A short target sits inside a longer one — `moved` is inside
        `../target/moved.md` — so replacing the short one corrupts the long one.
        The damage lands in a DIFFERENT link than the one being fixed, which is
        why it survives review.

      * TWO SYNTAXES, TWO ANSWERS. One target can appear as Markdown and as raw
        HTML on the same page with a different correct replacement for each (see
        `link_to`). Whole-file replaces let the first rewrite's output be
        re-matched by the second.

    But it must not work by matching a whole link construct either, because
    linked images nest and `[![](a.png)](a.png)` would get one of its two
    identical targets rewritten and the other silently left behind.

    So it anchors on the delimiters immediately either side of the target: each
    occurrence is judged on its own two characters of context, which is blind to
    nesting by construction. Matching uses `str.find`, so a target containing
    regex metacharacters needs no escaping.
    """
    out, i, count, n = [], 0, 0, len(link)
    while True:
        j = txt.find(link, i)
        if j < 0:
            out.append(txt[i:])
            break
        before, after = txt[:j], txt[j + n:]
        if is_html:
            m = HTML_OPEN.search(before)
            # Must close with the same quote it opened with, or this is a
            # substring of a longer attribute value.
            hit = bool(m) and after.startswith(m.group(1))
        else:
            hit = bool(MD_OPEN.search(before)) and bool(MD_CLOSE.match(after))
        out.append(txt[i:j])
        out.append(suggested if hit else link)
        count += 1 if hit else 0
        i = j + n
    return "".join(out), count


def is_raw_html(text, link):
    """Was `link` written as a raw HTML attribute rather than Markdown syntax?

    A fallback for plans written before `is_html` was recorded. Weaker than the
    reporter's own answer, because the same target can appear in both syntaxes on
    one page — so a recorded value always wins.
    """
    if not link:
        return False
    esc = re.escape(link)
    in_html = re.search(r"""<(?:img|a|source|iframe)[^>]*(?:src|href)=["']""" + esc, text)
    in_md = re.search(r"\]\(\s*<?" + esc, text)
    return bool(in_html) and not in_md
