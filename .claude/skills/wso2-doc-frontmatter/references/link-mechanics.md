# How the link scripts work

Read this when a link fix looks wrong, when a report says something surprising, or
before changing any of the link scripts. `SKILL.md` is the procedure; this is the
reasoning behind it.

## The relative-path rule — get this wrong and you break working links

Every applicable tier answers one question: *what relative path, written in this
page, reaches this file in the built site?* Markdown and raw HTML get different
answers, and they differ in **two** ways, not one. `links_lib.link_to()` is the
single place this is decided; never compute a path around it.

| | Markdown `[x](…)` / `![x](…)` | Raw HTML `<img src>` / `<a href>` |
|---|---|---|
| mkdocs rewrites it? | Yes, when the path names a real file | **Never** |
| the path counts from | the **source** directory | the **rendered url** — one level deeper for a non-`index.md` page |
| the path should name | the source file: `../a/b.md` | the published path: `../a/b/` |

The second row is why `<img src="../assets/…">` and `![x](../assets/…)` on the
same page need a different number of `../`. The third row matters just as much:
`hooks.py` publishes a raw `.md` beside every page, so `<a href="../a/b.md">` in
raw HTML *resolves* — and serves Markdown source to the reader. A link checker
calls that fine.

On an `index.md` the two bases coincide, so a wrong rule looks correct on every
landing page. Whenever you touch this, check all four combinations — Markdown and raw
HTML, on an `index.md` page and on a page that is not one.

Three more rules the reporter enforces, and you must not work around:

- **`{{base_path}}` is version-root-relative.** Where the resource exists at that
  path, convert the link to a relative path and drop the variable — that is an exact
  fix. Where it does not exist, leave it: it may be served by a redirect.
- **Never propose a target in a different version.** If a page under one version
  links to something missing, the replacement must live under that same version. A
  cross-version link silently sends a reader to a different release.
- **A `case` fix always changes the LINK, never the file.** Other pages may
  already point at the current filename. These matter more than the count
  suggests: macOS treats `Photo.png` and `photo.png` as one file, so a wrong-case
  link works in a local preview and 404s on the Linux build server — invisible to
  the person most likely to catch it.
- **`{! path !}` does nothing in this repo.** `markdown_include` is not enabled, so
  the directive stays on the page and the reader sees it as text. `pymdownx.snippets`
  IS enabled (`base_path: docs`) and 4.5.0 is already converted to it, so `--8<--`
  is the target form. The address must name the version — the old repo built one
  site per version, so `includes/foo.md` used to mean "this version's includes
  folder" and now names nothing.
- **An anchor is only matched when exactly ONE heading agrees.** `anchor_legacy`
  strips the run-together page-title prefix off an old Confluence anchor and
  compares what is left to each heading with everything but letters and digits
  removed. A unique match is what makes the group safe, so where a match is
  ambiguous `match_anchor` must return nothing rather than take the first. A lower-case anchor that simply does not exist is a reworded
  heading and stays in `anchor`; do not widen the rule to cover it.
- **An anchor on a page that renders itself in the browser is UNVERIFIABLE, not
  missing.** The OpenAPI reference pages (`template: templates/redoc.html` plus
  `<redoc spec-url=…>`) hold no Markdown headings at all; ReDoc builds the operation
  anchors — `#tag/Applications/paths/~1applications~1{applicationId}/put` — at
  runtime from the spec. Harvesting anchors from the `.md` returns an empty set, so
  before `renders_anchors_clientside()` existed **every** such fragment was reported
  as a reworded heading: 53 `ANCHOR_MISSING` and 18 `dir_style` refusals repo-wide,
  all of them working links. All three scripts now skip the check for these pages —
  **skip, not pass**: the fragment is carried through untouched and the *path* half
  of a `dir_style` or `renamed` fix is allowed to land. Verifying one would mean
  reading the OpenAPI spec, which none of these scripts do.
- **`BASE_PATH_ALIASES` is configuration, not logic.** `{{base}}`, `{{basepath}}`
  and `{{base_patgh}}` are `{{base_path}}` mistyped. Add a spelling when one turns
  up; do not replace the list with a similarity measure — `base` is four characters
  from `base_path`, so any threshold loose enough to catch it would swallow real
  variables. Correcting the spelling does not by itself mean the link works: where
  the resource is still missing, the entry stays in `templated` with a note saying
  both things are wrong.
- **Do not switch a block on until its own links work.** Converting `{! !}` makes a
  block render, so every broken link inside it becomes a broken link on every page
  using it. `include` therefore refuses any block that still has links failing from
  an includer, and points at the `partial_fixable` / `partial` entries that say
  what is wrong with it. Fix the block, then convert.
- **A link in a shared block is judged from the pages that INCLUDE it, never from
  the block's own folder.** The include splices the text in before Markdown runs,
  so that is what mkdocs does. Getting this wrong is wrong in both directions, and
  the dangerous direction is the quiet one: making a link correct relative to the
  block breaks it on every page that uses the block, and nothing flags it because
  from the block it looks right.
  `build_include_map()` is shared by the checker and the reporter so the two cannot
  disagree about this. Where every includer needs the same path, that path is the
  fix (`partial_fixable`). Where they need different paths, no relative link can
  serve them all and it goes to `partial`, refused.

`stale`, `anchor`, `gone` and `partial` need information that is not in the repo,
and an agent asked to fix them produces confident links to the wrong pages — worse
than a visibly broken link, because a plausible wrong link never gets re-checked.

When you report back, give the tier counts and say how many still need a decision.
A raw total is alarming and useless on its own; "N have an exact fix, M need a
decision" is what can be acted on.


## What each script is for

`scripts/fix_links.py` applies one tier of a `report_links.py` plan. Dry run by
default; `--apply` writes; `--journal` records every rewrite so a tier can be
reviewed or undone. It is the only script here that edits link text.

`scripts/check_redirects.py` validates `redirect_maps` in `mkdocs.yml` — targets exist, no source shadowed by a real file, no chains (the plugin doesn't follow them), no map left pointing at a superseded version after a version bump.

`CANONICAL_UNREACHABLE` only fires under `--policy latest-only`. Under the default `keep-all` a canonical is a versioned path, so it cannot depend on a redirect existing.

`scripts/links_lib.py` holds the link logic all three link scripts share — `url_base`, `published`, `link_to`, `slug`, the anchor harvester, the target finder, the rewriter, and the `mkdocs.yml` readers. **Add to it rather than copying out of it.** If a copy is taken and the two drift, one script counts from the rendered url while the other counts from the source directory — the reporter then proposes fixes the fixer refuses, and neither looks wrong on its own.

**The two scheme helpers are not interchangeable, and swapping them fails silently.**

| | returns | use it when |
|---|---|---|
| `has_uri_scheme(t)` | true for **any** scheme, http and typos included | the only question is "can this be resolved as a path on disk?" — false for every scheme |
| `non_web_scheme(t)` | the scheme, but **None** for `http`, `https` and `HTTP_TYPOS` | an http(s) target still has to be classified afterwards (legacy domain, mistyped scheme) |

`non_web_scheme` deliberately lets http through so the caller keeps handling it. So narrowing a has-any-scheme guard to `non_web_scheme` lets **external URLs fall through to path resolution**, where they are reported as broken links — and widening the other way swallows `ttps://` typos that `malformed` could have fixed. Neither mistake changes a count you would think to look at: the first inflated `partial` by 63 on one version while `gone` fell as intended, which reads like success unless every moved tier is accounted for. That is what `SKILL.md` step 7 means by accounting for every count that moved.

`scripts/check_links.py` resolves every relative link, image, and anchor against what's on disk, and flags links still pointing at a pre-migration location (the list is `LEGACY_DOMAINS` in `fm_lib.py`). It catches everything `mkdocs build` warns about plus two classes mkdocs stays silent on: bare directory links to a directory with no `index.md`/`README.md`, and directory links to a path that doesn't exist at all. Four of its codes need a word of explanation:

- **`LINK_TEMPLATED_UNDEFINED`** (blocking) vs **`LINK_TEMPLATED`** (polish). The severity is read from the config, not assumed: a `{{var}}` whose name has no value under `extra:` in `mkdocs.yml` renders as an empty string, so the link points at the server root. Define the variable under `extra:` and these become informational automatically.
- **`LINK_VIA_REDIRECT`** (polish). No file on disk, but `mkdocs-redirects` publishes a page at that path, so the link works in the built site. Reported rather than dropped, because it is worth knowing a link leans on a redirect.
- **`LINK_SCHEME_TYPO`** (blocking). `ttps://` and friends. Any *other* non-http scheme (`ldap:`, `ldaps:`) is skipped entirely — those are example addresses, not paths, and resolving them against the docs root reported correct configuration samples as broken links. `report_links.py` now shares this rule; until it did, the two scripts disagreed and four correct `<a href="ldap://10.100.1.100:389">` samples in the LDAP user-store pages sat in `gone` on every version.

Its image accounting keeps two things apart. An image asked for by a link that doesn't resolve is **not** an orphan — it is the other side of an `IMG_MISSING`, and listing it as unused invites deleting a screenshot whose only fault is the link pointing at it. Only an image that nothing in its own version so much as names is counted as never referenced. Per-version matters: every version keeps its own copy of the same file.

Note what `check_links.py` does **not** do: it only resolves links whose target is inside the repo. It cannot tell you whether a page is reachable at its own published URL — that is `check_redirects.py`'s job. "No broken links" and "every canonical URL resolves" are two different claims, and passing the first says nothing about the second.

## Redirects: what is settled and what is not

The scripts read the `redirect_maps` block in `mkdocs.yml` and nothing else. `docs-apim/en/redirects.yml` — which records where API Manager pages moved during the old repo's own restructuring — is **deliberately not read**, because how those should be carried over has not been decided.

Do not wire it in without that decision. Consulting it in the checker would mark links as fine on the strength of a redirect that does not exist yet; using it as a rename map would produce fixes nobody has agreed the shape of. Until then, work the tiers whose fix does not depend on it: `malformed`, `dir_style`, `depth`, `renamed`, `templated_fixable` all resolve against files that are present on disk. `templated` and `stale` are exactly the redirect-dependent cases, and stay refused.
