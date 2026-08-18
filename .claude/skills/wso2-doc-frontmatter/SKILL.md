---
name: wso2-doc-frontmatter
description: Adds and validates YAML frontmatter on WSO2 API Platform documentation pages, and finds and fixes broken links and images on the same pages. Use this when migrating docs into wso2/docs-api-platform, when a page is missing frontmatter or has a wrong canonical_url/md_url/content_type/description, when checking a docs PR before merge, or when asked things like "add frontmatter to 4.6.0 and fix the broken links", "add frontmatter to these pages", "why is this page's canonical URL wrong", "check this PR for broken links", or "audit the migrated docs". Handles the repo's multi-version layout (product/1.0.0/, product/1.1.0/, product/next/), where every version is published at a URL that includes its version segment. Also runs non-interactively as a CI gate, so keep output structured.
---

# WSO2 API Platform doc frontmatter and links

Most of this work is mechanical, and mechanical work belongs in a script. The
scripts here do everything with one correct answer. Your job is the part that needs
reading the page: `description`, `content_type`, `title`, and the link fixes that
have no computable answer.

Never hand-edit frontmatter or link text field by field across many files. Run the
scripts, then fill in what they hand back.

**Requirements:** Python 3.8+, nothing to install. Run every command from this
skill's directory, with paths relative to the repo root (`en/docs`, `en/mkdocs.yml`).

## The usual request

> *Add frontmatter to `<version>` and fix the broken links and images*

`<version>` is a scope path like `api-manager/4.6.0`. Pass it as `--scope` to every
command — never run repo-wide because someone asked about one version.

**Always keep the docs root at `en/docs` and narrow with `--scope`.** Pointing a
script at `en/docs/api-manager/4.6.0` instead looks equivalent and is not:
`canonical_url` and `md_url` are derived from each page's path *relative to the
root*, so a narrowed root writes every URL with the version segment missing, on
every page, and nothing downstream catches it. `fm_audit.py` and `fm_fix.py` now
refuse a root that looks narrowed, but do not rely on that — use `--scope`.

Run these seven steps in order. Every step that writes shows a sample first and
waits for a yes.

| | Step | Changes files? |
|---|---|---|
| 1 | Audit frontmatter | no |
| 2 | Fix mechanical frontmatter | yes |
| 3 | Fill in `description` / `content_type` / `title` | yes |
| 4 | Report broken links and images | no |
| 5 | Apply the link tiers, one at a time | yes |
| 6 | Fix what needs reading — see `references/judgement-calls.md` | yes |
| 7 | Re-audit and verify | no |

Tell the person up front roughly how many approvals to expect — step 5 asks once per
non-empty tier, which is usually eight to twelve — so the run does not feel like it
has stalled.

Deliverables at the end: every page in scope with complete frontmatter,
`BROKEN-LINKS-<scope>.md` listing what is left to decide, and
`BROKEN-EXTERNAL-<scope>.json` from the external-link check in step 7.

**Make the smallest change that fixes the finding.** This governs every step below.

- **Stay in scope.** Pass `--scope` to every command. A file outside it must not be
  touched, however obviously wrong it looks — report it instead.
- **Fix where a link points, not what it says.** Changing link text, headings or
  prose alters what the page means; that is a content decision, so ask first.
- **Do not delete content to clear a finding.** A link to a missing page is evidence
  the page is missing. Removing it destroys the evidence and the finding both. Repoint
  it, or leave it and report it.
- **Do not fix a version you were not asked about.** Say which other versions carry
  the same problem; do not go and fix them.
- **Leave and report beats guess.** A wrong link that resolves is worse than a broken
  one, because nothing will ever flag it again.

**Which spec you are working from.** At the start of every run, check for
`.claude/rules/doc-frontmatter-and-metadata.md` in the target repo:

```bash
ls .claude/rules/doc-frontmatter-and-metadata.md 2>/dev/null
```

- **Present** — it is the authoritative spec and it changes, so read it. Where it and
  `references/conventions.md` disagree, the repo rule wins.
- **Absent** — that is expected on some branches (the rules live on `main` and have
  not reached every branch yet). Do not stop and do not go looking on another branch.
  Work from `references/conventions.md`, which records the same field list plus the
  mechanics the rule leaves implicit — version-to-URL mapping, quoting, field order.

Either way, **say in your report which one you used.** It is the difference between
"checked against the repo's current rule" and "checked against the skill's copy of
it", and a reviewer needs to know which they are getting.

## 1. Audit first, always

```bash
python3 scripts/fm_audit.py en/docs --scope <version> --json /tmp/fm.json
```

Read the output before changing anything. `--files a.md b.md` narrows to a PR's
changed files; `--gate` exits non-zero on blocking issues.

`--policy` decides how the version segment maps to a URL. `keep-all` (the default)
matches the site. The other two do not. Never change it without saying so in your
report — it rewrites URLs across hundreds of files.

## 2. Let the script fix what's mechanical

```bash
python3 scripts/fm_fix.py en/docs --scope <version> --dry-run        # inspect first
python3 scripts/fm_fix.py en/docs --scope <version> --scaffold --apply \
    --worklist /tmp/work.json
```

This derives `canonical_url` and `md_url` from the path, normalises `last_updated`
(from `git log` when missing or malformed), maps out-of-enum `content_type` values,
lowercases `tags`, sets the standard `author`, and with `--scaffold` adds a whole
frontmatter block to pages that have none, taking `title` from the H1.

The script never invents a `description` or `title` — **you do, in step 3.** That
split is the design: a regex guessing a description produces something plausible and
wrong that looks finished, so nobody revisits it. A page left with
`description: "TODO"` is not done.

## 3. Fill in the judgement calls

`--worklist` writes the files still needing you, with each page's H1 and current
values. For each one **read the page** — headings and opening section at minimum —
then decide:

- **`description`** — 90 to 155 characters, hard limit 158. Say what the reader can
  do or learn on this page, naming the actual feature or task. Present tense. No
  "This page describes…", no marketing adjectives, none of the qualitative words the
  style guide bans ("easy", "simple", "quick"). When one is merely too long,
  **rewrite it — never truncate it.**
- **`content_type`** — exactly one of `how-to`, `tutorial`, `reference`, `concept`,
  `explanation`, `troubleshooting`, `faq`, `release-notes`, `changelog`,
  `quickstart`. Pick by what the page *is*: numbered task steps → `how-to`;
  end-to-end walkthrough → `tutorial`; parameter tables → `reference`; explains an
  idea without steps → `concept`; diagnosing failures → `troubleshooting`. Section
  landing pages that are mostly link lists are `concept` — settled for this repo, so
  apply it without asking. `overview` is not valid; `CT_ALIASES` in `fm_lib.py` maps
  it to the closest valid type.
- **`title`** — sentence case, under 60 characters. Only the first word plus genuine
  proper nouns and acronyms are capitalised: "AI Gateway", "API Platform",
  "Developer Portal" stay capitalised; "Analytics", "Configuration", "Policy" do
  not, unless part of a product name.

Hand your decisions back to the script as one batch — not one run per file:

```bash
cat > /tmp/filled.json <<'EOF'
{"cloud/api-platform-gateway/troubleshooting.md": {
   "title": "Troubleshoot the Self-Hosted Gateway",
   "description": "Diagnose and resolve connection, registration, startup, TLS, policy, and routing failures on the API Platform Self-Hosted Gateway.",
   "content_type": "troubleshooting"}}
EOF
python3 scripts/fm_fix.py en/docs --fill /tmp/filled.json --apply
```

## 4. Report the broken links and images

```bash
python3 scripts/report_links.py en/docs --scope <scope> \
    --out BROKEN-LINKS-<scope>.md --json BROKEN-LINKS-<scope>.json
```

**Always pass `--scope`** and name the output after it. A repo-wide report goes
stale immediately and nobody can tell which parts are theirs.

This is a separate deliverable from frontmatter. It is a work queue someone else
will pick up, so it belongs in a committed file, not in the chat reply.

The report groups every finding by **cause**, because the causes have different
fixes and different risk:

| Tier name | Cause | Fix | Applied by `fix_links.py`? |
|---|---|---|---|
| `templated_fixable` | `{{base_path}}` and the resource exists | Exact rewrite to a relative path | Yes |
| `malformed` | Malformed link syntax | Exact rewrite. No judgement. | Yes |
| `dir_style` | Markdown link written in URL shape, so mkdocs never resolves it | Add `.md`; mkdocs then owns the depth | Yes |
| `depth` | Wrong relative depth | Exact rewrite. No judgement. | Yes |
| `renamed` | Renamed or moved target | A file of that name exists elsewhere; proposed, with confidence | Yes, `high` confidence only by default |
| `case` | Right path, wrong capital letters | Corrects the link to match the file | Yes |
| `include` | `{! !}` shared block, which this repo does not process | Converts to `--8<--` with the version spelled out | Yes, but only when the block's own links are clean |
| `anchor_case` | Anchor names a real heading, wrong capitals | Lower-cases it — heading ids always are | Yes |
| `anchor_deep` | Heading exists but sits below `toc_depth`, so it has no id | Inserts `<a name>` above the heading in the TARGET page | Yes |
| `stale_mapped` | Old-site url whose path exists under this version | Points it inside the new docs, at this page's own version | Yes |
| `anchor_legacy` | Original Confluence anchor (`#PageTitle-HeadingRunTogether`) | Matched to the one heading that agrees letter for letter | Yes |
| `anchor_punct` | Anchor names a real heading but writes the separators differently (`#step-1---enable-x` for the id `step-1-enable-x`) | Exact — same words in the same order, and exactly one heading matches | Yes |
| `templated_typo` | `{{base_path}}` misspelled, and the resource exists | Corrects the spelling, then writes a relative path | Yes |
| `templated` | `{{base_path}}` and it does not exist | **Leave alone.** May be served by a redirect | No — refused |
| `stale` | Pre-migration domain | Needs the new equivalent page | No — refused |
| `anchor` | Missing anchor | Heading was reworded | No — refused |
| `gone` | No target anywhere | Was it dropped, missed, or merged? | No — refused |
| `partial` | Would be mechanical, but the page is an included partial | Needs a decision on how partials link at all | No — refused |

**External links are in no tier** — they are checked separately, by
`check_external.py` in step 7.

## 5. Apply the link tiers, one at a time

`scripts/fix_links.py` is the only thing that edits link text, and it takes one
tier per run:

```bash
# nothing is written
python3 scripts/fix_links.py en/docs --plan BROKEN-LINKS-<scope>.json --tier malformed
# apply, and record what changed
python3 scripts/fix_links.py en/docs --plan BROKEN-LINKS-<scope>.json --tier malformed \
    --apply --journal /tmp/fixed-malformed.json
```

Work the tiers in this order, safest first:

1. `malformed`
2. `anchor_deep` — give deep headings an id, so the target exists before anything is
   pointed at it
3. `partial_fixable`
4. `include` — changes what the page contains
5. `case`
6. `templated_typo`, `templated_fixable`
7. `stale_mapped`
8. `anchor_case`, `anchor_legacy`, `anchor_punct`
9. `dir_style`
10. `depth`
11. `renamed` — `high` confidence only; `--min-confidence` widens it

**Run the whole sequence again until it applies nothing.** Fixing a path reveals
anchor problems that could not be seen while the link went nowhere, so a second lap
finds work the first could not. It usually converges on the third.

**The rule for every tier: dry-run it, show a sample, say how many would change and
how many the verifier refused, and wait for an explicit yes before `--apply`.**
Never chain tiers, and never apply one the person has not seen — their answer for
`depth`, which is arithmetic, is not their answer for `renamed`, which is a
proposal. **Skip a tier silently when it has no findings**; do not ask about an
empty tier.

After each applied tier, report what changed and stop:

```
tier `depth`: <n> verified, <n> refused, <n> files changed, <n> links rewritten.
Refused: <n> where the anchor no longer exists.
Next tier is `renamed` (<n> findings, <n> verified). Apply it?
```

**Regenerate the plan between tiers** — fixing one tier changes what the others
resolve to, and a stale plan gets skipped rather than guessed at.

Two things the script does that you must not work around:

- **It verifies every rewrite against the files before writing.** A proposal whose
  target does not resolve, or whose anchor does not exist on the new page, is
  refused. Those refusals are the useful output.
- **It refuses `templated`, `stale`, `anchor`, `gone` and `partial` outright.** Do
  not hand-apply them in bulk. A plausible wrong link is worse than a visibly broken
  one, because nobody re-checks it.

If a fix looks wrong, or before changing any link script, read
`references/link-mechanics.md` — it holds the relative-path rule that decides
whether a path is counted from the source file or from the published URL. Getting
that wrong breaks working links.

## 6. Fix what needs reading

The tiers above have one computable answer each. What is left needs the target pages
read before it can be fixed, which is your work, not something to hand back as a
list. `references/judgement-calls.md` covers it: which groups to work, what evidence
justifies a fix, how to judge images, how to copy files the migration left behind,
and how to work through it in reviewable batches.

Route those decisions through `fix_links.py --tier agent`, never by hand-editing.
Each entry must quote the linking sentence verbatim and the heading it matched; the
script refuses entries that do not.

## 7. Re-audit and verify

```bash
python3 scripts/fm_audit.py en/docs --scope <version> --gate
python3 scripts/check_links.py en/docs
python3 scripts/check_redirects.py en/mkdocs.yml en/docs --gate
python3 scripts/check_external.py en/docs --scope <scope> \
    --json BROKEN-EXTERNAL-<scope>.json
```

Re-auditing is not optional — it is the only thing that proves the fix worked rather
than moved the problem.

`check_external.py` makes network calls, so run it here rather than in a merge gate.
It reports three verdicts: `dead`, `unverifiable` (the check failed, not the link —
never count these as broken) and `ok`. **Ask the user before changing any `dead`
external link**, offering: unlink and keep the text, repoint to a URL they supply, or
leave it and record it. See `references/judgement-calls.md`.

Where the repo can be built, `mkdocs build` is the authoritative check on links. If
you have the dependencies, run it and reconcile any difference rather than assuming
the script is right.

**If you change `report_links.py`, `fix_links.py`, `check_links.py` or
`links_lib.py`, prove it on a version before trusting it.** These three have to
agree about what path is correct. When they drift apart the failure is silent — the
reporter proposes fixes the fixer then refuses, and neither looks wrong on its own.
So:

1. Note the per-tier counts from `report_links.py` on one version *before* your change.
2. Make the change, re-run, and account for every count that moved. A tier that grew
   or shrank without a reason you can state is the change misfiring.
3. Dry-run `fix_links.py` on a tier and read the sample. Proposals the fixer refuses
   are where the reporter is being optimistic.
4. Build the site and resolve the links in the generated HTML, not in your own
   report. That is the only check that is not the scripts grading themselves.

Test both a page whose name is `index.md` and one whose name is not — on an
`index.md` the two path bases coincide, so a wrong rule looks correct on every
landing page and breaks everywhere else.

## Reporting

Lead with the counts and what you changed. Group findings by code, not by file — a
hundred identical `canonical_url` corrections are one line, not a hundred. Show one
representative diff per group.

Separate three things, because they need different responses:

1. **Fixed automatically** — what the scripts changed, by code and count.
2. **Needs the user to decide** — genuine ambiguity, or a repo-wide convention
   question. State the options and your recommendation; do not silently pick one.
3. **Still outstanding** — what neither the scripts nor you could resolve, and why.

Never report a count without saying whether it counts occurrences or affected files.
Those differ by an order of magnitude.

For each group you worked by reading, say how many you fixed and how many you left,
and why. "Fixed all 98 anchors" is less trustworthy than "fixed 58, left 29 because
the sentence did not name a section clearly enough".

Style-guide review is a separate skill — `wso2-doc-style-checker`. Do not duplicate
it here.

When running in CI, end with one machine-readable line:

```
<!-- wso2-doc-frontmatter: STATUS=FAIL files=<N> blocking=<N> should_fix=<N> -->
```

`STATUS=FAIL` only when there is at least one blocking issue. Blocking counts drive
a merge gate, so do not inflate severity.
