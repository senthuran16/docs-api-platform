# Broken links and images — `api-manager/3.2.0`

**69 findings** across 432 pages. **3** have an exact or high-confidence mechanical fix; **61** need a decision.

### Fixable by script

Run in this order. Each is a separate `fix_links.py --tier` run, and every rewrite is verified against the files on disk before it is written.

| Order | Group | Cause | Count | Fix |
|---|---|---|---|---|
| 1 | `malformed` | Malformed link syntax | 0 | Exact — no judgement |
| 2 | `dir_style` | Written as a URL, so mkdocs never resolves it | 0 | Add `.md` — mkdocs then owns the depth |
| 3 | `depth` | Wrong relative depth | 0 | Exact — no judgement |
| 4 | `renamed` | Renamed or moved target | 3 | Proposed; `high` confidence applied by default |
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
| `stale` | Pre-migration domain | 4 | Needs the equivalent page on the new site |
| `anchor` | Missing anchor | 1 | The heading was reworded — which one now? |
| `gone` | No target anywhere | 61 | Was it dropped, missed, or merged? |
| `partial` | Broken link inside an included partial | 0 | Resolves against the includer's url, not the partial's |

## `renamed` — Renamed or moved target

The target does not exist at the path written, but a file of the same name exists elsewhere under the same version. This is the restructure: directories were renamed and the inbound links were never updated.

### Exactly one candidate — high confidence (3)

| Page | Currently | Change to |
|---|---|---|
| `api-manager/3.2.0/develop/customizations/adding-a-user-signup-workflow-using-bps.md` | `../../learn/consume-api/customizations/adding-a-user-signup-workflow/#configuring-the-business-process-server` | `adding-a-user-signup-workflow.md#configuring-the-business-process-server` |
| `api-manager/3.2.0/develop/customizations/adding-a-user-signup-workflow-using-bps.md` | `../../learn/consume-api/customizations/adding-a-user-signup-workflow/#configuring-the-enterprise-integrator` | `adding-a-user-signup-workflow.md#configuring-the-enterprise-integrator` |
| `api-manager/3.2.0/learn/api-security/authorization/role-based-access-control-using-xacml.md` | `../../../learn/extensions/saml2-sso/configuring-identity-server-as-idp-for-sso.md#sharing-the-user-store` | `../../../develop/extending-api-manager/saml2-sso/configuring-identity-server-as-idp-for-sso.md#sharing-the-user-store` |

## `stale` — Links to the pre-migration site

These point at a location the documentation has migrated away from. For each one: find the equivalent page on the new site and link to it relatively, or if the content wasn't migrated, remove the link and say so in the prose. Never leave a reader on the old site.

| Page | Link |
|---|---|
| `api-manager/3.2.0/getting-started/about-this-release.md` | `https://apim.docs.wso2.com/en/3.1.0/develop/product-apis/devportal-apis/devportal-v0.16/devportal-v0.16/` |
| `api-manager/3.2.0/getting-started/about-this-release.md` | `https://apim.docs.wso2.com/en/3.1.0/develop/product-apis/publisher-apis/publisher-v0.16/publisher-v0.16/` |
| `api-manager/3.2.0/getting-started/about-this-release.md` | `https://apim.docs.wso2.com/en/3.1.0/develop/product-apis/admin-apis/admin-v0.16/admin-v0.16/` |
| `api-manager/3.2.0/getting-started/about-this-release.md` | `https://apim.docs.wso2.com/en/4.1.0/install-and-setup/setup/distributed-deployment/deploying-wso2-api-m-in-a-distributed-setup-with-km-separated` |

## `anchor` — Missing anchor

The page resolves but the `#fragment` matches no heading, so the reader lands at the top instead of the section. Usually the heading was reworded. Open the target, find the heading that was meant, and use its current slug.

| Page | Link | Target file | Missing anchor |
|---|---|---|---|
| `api-manager/3.2.0/install-and-setup/setup/reference/default-product-ports.md` | `#product-specific-ports` | `api-manager/3.2.0/install-and-setup/setup/reference/default-product-ports.md` | `product-specific-ports` |

## `gone` — No target anywhere

No file of this name exists anywhere under the docs root, so there is nothing to point at. Each needs a decision: was the page meant to be migrated and missed, was it deliberately dropped (then the link and its sentence should go), or was it merged into another page (then link there)? **Do not guess these.**

| Page | Broken target | Note |
|---|---|---|
| `api-manager/3.2.0/administer/key-managers/configure-wso2is-connector.md` | `../../assets/attachments/administer/wso2is-km-connector-1.0.16_ga.zip` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/administer/logging-and-monitoring/monitoring/monitoring-tcp-based-messages.md` | `_Message_Monitoring_with_TCPMon_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/administer/logging-and-monitoring/monitoring/monitoring-tcp-based-messages.md` | `../../../assets/attachments/45946410/46206514.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/administer/logging-and-monitoring/monitoring/monitoring-tcp-based-messages.md` | `../../../assets/attachments/45946410/46206513.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/administer/logging-and-monitoring/monitoring/monitoring-tcp-based-messages.md` | `../../../assets/attachments/45946410/46206512.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/administer/managing-users-and-roles/managing-user-stores/understanding-the-user-realm.md` | `../../../assets/attachments/126562314/126562315.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/administer/multitenancy/adding-new-tenants.md` | `../../assets/attachments/126562777/126562778.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/administer/multitenancy/adding-new-tenants.md` | `../../assets/attachments/126562777/126562781.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/administer/multitenancy/adding-new-tenants.md` | `../../assets/attachments/126562777/126562782.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/develop/extending-api-manager/extending-gateway/writing-custom-handlers.md` | `../../../extensions/adding-mediation-extensions` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/develop/extending-api-manager/extending-gateway/writing-custom-handlers.md` | `../../../analytics/analyzing-the-log-overview` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/develop/extending-api-manager/extending-gateway/writing-custom-handlers.md` | `../../../extensions/adding-mediation-extensions` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/distributed-deployment/configure-apim-analytics/configuring-database-and-file-system-state-persistence.md` | `_Configuring_Datasources_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/distributed-deployment/configuring-the-gateway-in-a-distributed-environment-with-rsync.md` | `../distributed-deployment-of-the-gateway/` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/distributed-deployment/configuring-the-gateway-in-a-distributed-environment-with-rsync.md` | `../../configuring-rsync-for-deployment-synchronization/` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/distributed-deployment/configuring-the-gateway-in-a-distributed-environment-with-rsync.md` | `../working-with-hazelcast-clustering/` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/distributed-deployment/configuring-wso2-identity-server-as-a-key-manager.md` | `../../../assets/attachments/administer/wso2is-km-connector-1.0.16_ga.zip` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/admin-searching-the-registry.md` | `../../../../assets/attachments/126562657/126562660.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/admin-searching-the-registry.md` | `../../../../assets/attachments/126562657/126562659.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/admin-searching-the-registry.md` | `../../../../assets/attachments/126562657/126562658.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `../../../../../assets/attachments/126562631/126562638.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `../../../../../assets/attachments/126562631/126562637.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `../../../../../assets/attachments/126562631/126562635.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `../../../../../assets/attachments/126562631/126562633.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `../../../../../assets/attachments/126562631/126562632.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `../../../../../assets/attachments/126562631/126562636.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/editing-collections-using-the-entries-panel.md` | `../../../../../assets/attachments/126562643/126562644.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/link-creation.md` | `../../../../../assets/attachments/126562639/126562641.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/link-creation.md` | `../../../../../assets/attachments/126562639/126562640.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/link-creation.md` | `../../../../../assets/attachments/126562639/126562642.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/metadata.md` | `../../../../../assets/attachments/22185146/22514191.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/metadata.md` | `../../../../../assets/attachments/126562605/126562606.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/metadata.md` | `../../../../../assets/attachments/126562605/126562611.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/metadata.md` | `../../../../../assets/attachments/22185146/22514195.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/properties.md` | `../../../../../assets/attachments/126562613/126562618.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/properties.md` | `../../../../../assets/attachments/126562613/126562617.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/role-permissions.md` | `../../../../../assets/attachments/126562645/126562646.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/role-permissions.md` | `../../../../../assets/attachments/126562645/126562647.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/role-permissions.md` | `../../../../../assets/attachments/126562645/126562648.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.2.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/using-remote-registry/admin-all-partitions-in-a-single-server.md` | `../../../../../assets/attachments/21037149/21331970.png` | `no file of this name exists anywhere under the docs root` |

_…and 21 more. Full list in the JSON sidecar._

---

## Prompt for an AI coding agent

Paste the block below to an agent working in the repo root. It is deliberately scoped to the four groups with a defensible mechanical answer. `templated`, `stale`, `anchor` and `gone` need judgement and are left out on purpose.

Alternatively, run `fix_links.py --tier <group>` yourself — same scope, one group at a time, and every rewrite verified against the files on disk before it is written.

````text
You are fixing broken links in the WSO2 API Platform docs, scope: api-manager/3.2.0.

Read the fix plan in `BROKEN-LINKS-api-manager-3.2.0.md` and the machine-readable list in `BROKEN-LINKS-api-manager-3.2.0.json`.

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
