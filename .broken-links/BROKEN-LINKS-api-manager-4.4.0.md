# Broken links and images — `api-manager/4.4.0`

**8 findings** across 470 pages. **0** have an exact or high-confidence mechanical fix; **5** need a decision.

### Fixable by script

Run in this order. Each is a separate `fix_links.py --tier` run, and every rewrite is verified against the files on disk before it is written.

| Order | Group | Cause | Count | Fix |
|---|---|---|---|---|
| 1 | `malformed` | Malformed link syntax | 0 | Exact — no judgement |
| 2 | `dir_style` | Written as a URL, so mkdocs never resolves it | 0 | Add `.md` — mkdocs then owns the depth |
| 3 | `depth` | Wrong relative depth | 0 | Exact — no judgement |
| 4 | `renamed` | Renamed or moved target | 0 | Proposed; `high` confidence applied by default |
| 5 | `templated_fixable` | `{{base_path}}` where the resource exists | 0 | Exact rewrite to a relative path |
| 6 | `case` | Right path, wrong capital letters | 0 | Exact — works on macOS, breaks on the build server |
| 7 | `include` | `{! !}` shared block, which this repo does not process | 0 of 0 | Convert to `--8<--` with the version spelled out |
| 8 | `anchor_case` | Anchor names a real heading, wrong capitals | 0 | Exact — heading ids are always lower-case |
| 9 | `anchor_legacy` | Original Confluence anchor | 0 | Matched to the one heading that agrees letter for letter |
| 9b | `anchor_punct` | Anchor names a real heading, different hyphens/underscores | 0 | Exact — same words in the same order, one heading matches |
| 10 | `templated_typo` | `{{base_path}}` misspelled, resource present | 0 | Corrects the spelling and writes a relative path |
| 11 | `partial_fixable` | Link in a shared block, broken for the pages that include it | 0 | One path that works from every includer |
| 12 | `stale_mapped` | Old-site url whose path exists under this version | 0 | Point it inside the new docs instead |
| 13 | `anchor_deep` | Heading exists but is deeper than h3, so it has no id | 0 | Insert `<a name>` above the heading |

### Needs a decision

`fix_links.py` refuses these. The information needed is not in the repository, and a guess produces a confident link to the wrong page — worse than a visibly broken one, because nobody re-checks it.

| Group | Cause | Count | Why it cannot be automated |
|---|---|---|---|
| `templated` | `{{base_path}}` where the resource does not exist | 0 | May be served by a redirect |
| `stale` | Pre-migration domain | 0 | Needs the equivalent page on the new site |
| `anchor` | Missing anchor | 3 | The heading was reworded — which one now? |
| `gone` | No target anywhere | 5 | Was it dropped, missed, or merged? |
| `partial` | Broken link inside an included partial | 0 | Resolves against the includer's url, not the partial's |

## `anchor` — Missing anchor

The page resolves but the `#fragment` matches no heading, so the reader lands at the top instead of the section. Usually the heading was reworded. Open the target, find the heading that was meant, and use its current slug.

| Page | Link | Target file | Missing anchor |
|---|---|---|---|
| `api-manager/4.4.0/design/api-security/authorization/role-based-access-control-using-xacml.md` | `../../../reference/customize-product/extending-api-manager/saml2-sso/configuring-identity-server-as-idp-for-sso.md#sharing-the-user-store` | `api-manager/4.4.0/reference/customize-product/extending-api-manager/saml2-sso/configuring-identity-server-as-idp-for-sso.md` | `sharing-the-user-store` |
| `api-manager/4.4.0/integrate/develop/working-with-service-catalog.md` | `../../tutorials/tutorials-overview.md#integration-tutorials` | `api-manager/4.4.0/tutorials/tutorials-overview.md` | `integration-tutorials` |
| `api-manager/4.4.0/reference/vendor-extensions-catalog.md` | `#x-wso2-pass-request-payload-to-enforcer` | `api-manager/4.4.0/reference/vendor-extensions-catalog.md` | `x-wso2-pass-request-payload-to-enforcer` |

## `gone` — No target anywhere

No file of this name exists anywhere under the docs root, so there is nothing to point at. Each needs a decision: was the page meant to be migrated and missed, was it deliberately dropped (then the link and its sentence should go), or was it merged into another page (then link there)? **Do not guess these.**

| Page | Broken target | Note |
|---|---|---|
| `api-manager/4.4.0/design/create-api/create-a-websocket-api.md` | `../../observe/api-manager-analytics/overview-of-api-analytics.md` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.4.0/install-and-setup/install-and-setup-overview.md` | `../../install-and-setup/setup/kubernetes-operators/k8s-api-operator/manage-apis/api-deployments/` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.4.0/integrate/develop/working-with-service-catalog.md` | `../../tutorials/integration-tutorials/service-catalog-tutorial.md` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.4.0/integrate/develop/working-with-service-catalog.md` | `../../tutorials/integration-tutorials/service-catalog-tutorial-for-proxy-services.md` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.4.0/integrate/develop/working-with-service-catalog.md` | `../../integrate/develop/integration-development-kickstart.md` | `no file of this name exists anywhere under the docs root` |

---

## Prompt for an AI coding agent

Paste the block below to an agent working in the repo root. It is deliberately scoped to the four groups with a defensible mechanical answer. `templated`, `stale`, `anchor` and `gone` need judgement and are left out on purpose.

Alternatively, run `fix_links.py --tier <group>` yourself — same scope, one group at a time, and every rewrite verified against the files on disk before it is written.

````text
You are fixing broken links in the WSO2 API Platform docs, scope: api-manager/4.4.0.

Read the fix plan in `BROKEN-LINKS-api-manager-4.4.0.md` and the machine-readable list in `BROKEN-LINKS-api-manager-4.4.0.json`.

Apply ONLY these groups:
  - `templated_fixable`: apply every row as given.
  - `malformed`: apply every row exactly as given.
  - `dir_style`: apply every row exactly as given (adds `.md`).
  - `depth`: apply every row exactly as given.
  - `renamed`, the high-confidence subsection only: apply every row as given.

Rules:
  1. Replace only the link target inside the parentheses. Never change the link TEXT,
     the surrounding sentence, or anything else on the line.
  2. A target may appear more than once in a file — replace every occurrence of that
     exact target in that file.
  3. Preserve any `#fragment` already on the link unless the plan says otherwise.
  4. Do NOT touch `templated`, `stale`, `anchor` or `gone`. Do not invent a
     target that is not in the plan.
  5. Do not reformat, reflow, or reorder anything. Minimal diffs only.

Verify when done, from the repo root:
  python3 .claude/skills/wso2-doc-frontmatter/scripts/check_links.py en/docs --json /tmp/after.json

The blocking count must go DOWN and no new codes may appear. If any count rises, stop
and report what you changed rather than continuing.

Then report: rows applied per group, files touched, and the before/after blocking counts.
````

### Why `templated`, `stale`, `anchor` and `gone` are excluded

Each needs information that isn't in the repo: which new page replaces an old-site link, which reworded heading was meant, whether a missing page was dropped on purpose. An agent asked to fix those will produce plausible links to the wrong places, which is worse than a visibly broken link because nobody re-checks it.

Template-variable links are excluded for a different reason: they are not broken at all in their original context. They depend on a build-time substitution, and whether that survives migration is a redirect-strategy decision, not a link fix.
