# Broken links and images — `api-manager/4.3.0`

**141 findings** across 751 pages. **0** have an exact or high-confidence mechanical fix; **66** need a decision.

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
| 7 | `include` | `{! !}` shared block, which this repo does not process | 0 of 6 | Convert to `--8<--` with the version spelled out |
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
| `stale` | Pre-migration domain | 1 | Needs the equivalent page on the new site |
| `anchor` | Missing anchor | 60 | The heading was reworded — which one now? |
| `gone` | No target anywhere | 66 | Was it dropped, missed, or merged? |
| `partial` | Broken link inside an included partial | 8 | Resolves against the includer's url, not the partial's |

## Excluded — 8 findings inside 5 included partial(s)

Every one of these would otherwise have been a mechanical fix. They are held back because the file is pulled into other pages with an include directive, so a relative link in it is resolved against **the includer's** url, not the partial's own. Where a partial has includers at different depths, no single relative path is correct for all of them — a fix that works on one page breaks on another, which is the hardest breakage to notice.

The computed path is kept as `unsafe_suggestion` in the JSON rather than `suggested`, and `fix_links.py` refuses this tier. Resolving them needs a decision about how partials should link at all: a root-relative path, or moving the link out of the partial and into each page.

| Partial | Link | Intended group | Included by |
|---|---|---|---|
| `api-manager/4.3.0/includes/deploy/steps-to-deploy-apim-in-a-distributed-setup-with-km-separation.md` | `../../../../install-and-setup/deploying-wso2-api-manager/production-deployment-guidelines/#common-guidelines-and-checklist` | `` | `['api-manager/4.3.0/install-and-setup/setup/distributed-deployment/deploying-wso2-api-m-in-a-distributed-setup-with-km-separated.md']` |
| `api-manager/4.3.0/includes/deploy/steps-to-deploy-apim-in-a-distributed-setup-with-tm-separation.md` | `../../../../install-and-setup/deploying-wso2-api-manager/production-deployment-guidelines/#common-guidelines-and-checklist` | `` | `['api-manager/4.3.0/install-and-setup/setup/distributed-deployment/deploying-wso2-api-m-in-a-distributed-setup-with-tm-separated.md', 'api-manager/4.3.0/install-and-setup/setup/multi-dc-deployment/configuring-multi-dc-deployment-pattern-1.md', 'api-manager/4.3.0/install-and-setup/setup/multi-dc-deployment/configuring-multi-dc-deployment-pattern-2.md']` |
| `api-manager/4.3.0/includes/design/create-graphql-api.md` | `../../../administer/managing-users-and-roles/managing-user-roles/` | `` | `['api-manager/4.3.0/design/create-api/create-a-graphql-api.md', 'api-manager/4.3.0/tutorials/create-and-publish-a-graphql-api.md']` |
| `api-manager/4.3.0/includes/design/create-graphql-api.md` | `../../../administer/managing-users-and-roles/managing-users/` | `` | `['api-manager/4.3.0/design/create-api/create-a-graphql-api.md', 'api-manager/4.3.0/tutorials/create-and-publish-a-graphql-api.md']` |
| `api-manager/4.3.0/includes/design/deploy-revision.md` | `https://apim.docs.wso2.com/en/4.1.0/assets/img/design/revision/delete-and-deploy-revision.png` | `stale_mapped` | `['api-manager/4.3.0/deploy-and-publish/deploy-on-gateway/deploy-api/deploy-an-api.md', 'api-manager/4.3.0/design/create-api/create-api-revisions.md']` |
| `api-manager/4.3.0/includes/design/deploy-revision.md` | `https://apim.docs.wso2.com/en/4.1.0/assets/img/design/revision/deploy-first-revision.png` | `stale_mapped` | `['api-manager/4.3.0/deploy-and-publish/deploy-on-gateway/deploy-api/deploy-an-api.md', 'api-manager/4.3.0/design/create-api/create-api-revisions.md']` |
| `api-manager/4.3.0/includes/design/deploy-revision.md` | `https://apim.docs.wso2.com/en/4.1.0/assets/img/design/revision/deploy-new-revision.png` | `stale_mapped` | `['api-manager/4.3.0/deploy-and-publish/deploy-on-gateway/deploy-api/deploy-an-api.md', 'api-manager/4.3.0/design/create-api/create-api-revisions.md']` |
| `api-manager/4.3.0/includes/design/redis-counter-note.md` | `https://apim.docs.wso2.com/en/4.1.0/design/rate-limiting/advanced-topics/configuring-rate-limiting-api-gateway-cluster` | `stale_mapped` | `['api-manager/4.3.0/design/rate-limiting/setting-maximum-backend-throughput-limits.md', 'api-manager/4.3.0/design/rate-limiting/setting-throttling-limits.md', 'api-manager/4.3.0/install-and-setup/setup/single-node/configuring-an-active-active-deployment.md']` |


## `stale` — Links to the pre-migration site

These point at a location the documentation has migrated away from. For each one: find the equivalent page on the new site and link to it relatively, or if the content wasn't migrated, remove the link and say so in the prose. Never leave a reader on the old site.

| Page | Link |
|---|---|
| `api-manager/4.3.0/includes/analytics/configure-synapse-gateway.md` | `https://apim.docs.wso2.com/en/4.2.0/api-analytics/gateways/configure-synapse-gateway/#advanced-configurations` |

## `anchor` — Missing anchor

The page resolves but the `#fragment` matches no heading, so the reader lands at the top instead of the section. Usually the heading was reworded. Open the target, find the heading that was meant, and use its current slug.

**15 already fixed this pass** — 5 in `get-started/overview.md` → `apim-architecture.md` (content moved, confirmed via a sibling link elsewhere in the repo), plus okta-connector, jmx-based-monitoring (typo), vendor-extensions-catalog (malformed `#https://` anchor), `metadata.md` ×2, `setting-throttling-limits.md` ×2, `product-compatibility.md` (×2 source files), and one Confluence-legacy anchor on the single-node deployment page that a heading-markup repair (a genuinely mangled `### ` + text on separate lines) exposed. Several of these targeted **h4 headings deeper than this site's `toc_depth`, which have no id at all in the real build** — verified via the live `mkdocs serve` output, not just the checker — and needed an `<a name="...">` inserted above the heading, the same fix as an `anchor_deep` finding.

**Known checker bug, verified against the real build:** `use-cases/streaming-usecase/extracting-data-from-static-sources-in-real-time.md#extracting-data-from-files` is flagged here as missing, but `curl` against the live built page confirms `id="extracting-data-from-files"` **does** exist — the link already works. `links_lib.py`'s `harvest_anchors()` has a list-indent-tracking heuristic that appears to mis-skip some real headings on pages with heavy list nesting (this page's headings are found inconsistently: some detected, some not, no obvious pattern by depth or position). Don't "fix" this one — it isn't broken. Worth a look at `harvest_anchors()` before trusting the rest of this tier at face value; a `mkdocs build` + heading-id check is the authoritative source when in doubt, not this table.

**Three clusters investigated and left — no heading to match, don't re-investigate:**
- `develop/streaming-apps/working-with-the-design-view.md#WorkingwiththeDesignView-Settings` (10 rows) — legacy Confluence anchor for a generic "the settings icon" reference. No page-wide "Settings" heading exists; each Siddhi component (Stream, Source, Sink, Table, Trigger, etc.) describes its own settings inline instead.
- `design/api-security/threat-protection/gateway-threat-protectors/{xml,json,regular-expression}-threat-protection-for-api-gateway.md` (12 rows) — Confluence hex-ID anchors pointing at "Disabling the XML payload validation", "Request", "Response", ".xsd URL" content that isn't demarcated anywhere on the page, as a heading or otherwise.
- `develop/streaming-apps/streaming-integrator-studio-overview.md#StreamProcessorStudioOverview-SourceView` / `-DesignView` (5 rows) — "Source View" and "Design View" exist only as bold list items, not headings.

Smaller open items also left (each is its own row below): `#connectID` and `#sample-jwt` (inline bold text or content inside a shared include, not a heading), `#common-guidelines-and-checklist` on `production-deployment-guidelines.md` (no such heading or text anywhere — the whole page is a table with no subsections), a handful of Confluence-legacy self-references on `faq.md`/`encrypting-passwords-with-cipher-tool.md`/`configuring-wso2-identity-server-as-a-key-manager.md` pointing at bold text or OS-tab labels rather than real headings, and cross-file anchor mismatches on `using-dynamic-data-in-api-controller-projects.md`, `managing-dashboards.md`, `performance-analysis-results.md`, and `installing-si.md` where no equivalent heading could be found with confidence.

| Page | Link | Target file | Missing anchor |
|---|---|---|---|
| `api-manager/4.3.0/deploy-and-publish/deploy-on-gateway/api-gateway/passing-enduser-attributes-to-the-backend-via-api-gateway.md` | `#sample-jwt` | `api-manager/4.3.0/deploy-and-publish/deploy-on-gateway/api-gateway/passing-enduser-attributes-to-the-backend-via-api-gateway.md` | `sample-jwt` |
| `api-manager/4.3.0/design/api-monetization/monetizing-an-api.md` | `#connectID` | `api-manager/4.3.0/design/api-monetization/monetizing-an-api.md` | `connectID` |
| `api-manager/4.3.0/design/api-monetization/monetizing-an-api.md` | `#connectID` | `api-manager/4.3.0/design/api-monetization/monetizing-an-api.md` | `connectID` |
| `api-manager/4.3.0/design/api-security/authorization/role-based-access-control-using-xacml.md` | `../../../reference/customize-product/extending-api-manager/saml2-sso/configuring-identity-server-as-idp-for-sso.md#sharing-the-user-store` | `api-manager/4.3.0/reference/customize-product/extending-api-manager/saml2-sso/configuring-identity-server-as-idp-for-sso.md` | `sharing-the-user-store` |
| `api-manager/4.3.0/design/api-security/oauth2/token-persistence.md` | `../../../reference/product-apis/devportal-apis/devportal-v3/devportal-v3.md#tag/Applications/paths/~1applications~1%7BapplicationId%7D/put` | `api-manager/4.3.0/reference/product-apis/devportal-apis/devportal-v3/devportal-v3.md` | `tag/Applications/paths/~1applications~1{applicationId}/put` |
| `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/json-threat-protection-for-api-gateway.md` | `#2fabe5e92ef64a3a999bb756d894221e` | `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/json-threat-protection-for-api-gateway.md` | `2fabe5e92ef64a3a999bb756d894221e` |
| `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/json-threat-protection-for-api-gateway.md` | `#6da49ce3d2cf4091a885d78334d2513e` | `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/json-threat-protection-for-api-gateway.md` | `6da49ce3d2cf4091a885d78334d2513e` |
| `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/regular-expression-threat-protection-for-api-gateway.md` | `#10673ba9a16d49dcaf1b6a073de9cf4d` | `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/regular-expression-threat-protection-for-api-gateway.md` | `10673ba9a16d49dcaf1b6a073de9cf4d` |
| `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/regular-expression-threat-protection-for-api-gateway.md` | `#90b129a29c8c4b74869eb1676bb3f705` | `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/regular-expression-threat-protection-for-api-gateway.md` | `90b129a29c8c4b74869eb1676bb3f705` |
| `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#Am300XMLThreatProtectionforAPIGateway-detectvulnerability` | `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `Am300XMLThreatProtectionforAPIGateway-detectvulnerability` |
| `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#b95bd611fb2144d0940b193f34addf5b` | `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `b95bd611fb2144d0940b193f34addf5b` |
| `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#70c795c618f04f2cb9983858b263298d` | `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `70c795c618f04f2cb9983858b263298d` |
| `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#389c50828aa24292b0657e037c09c635` | `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `389c50828aa24292b0657e037c09c635` |
| `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#159d32ca825c41a480037880ce2e6413` | `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `159d32ca825c41a480037880ce2e6413` |
| `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#45b87273c80b44ffb18a3f8fe4f5b8f6` | `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `45b87273c80b44ffb18a3f8fe4f5b8f6` |
| `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#194a5a4652e94e609d80ba175c16b449` | `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `194a5a4652e94e609d80ba175c16b449` |
| `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#db80409dd4d941dc972837213bc340e5` | `api-manager/4.3.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `db80409dd4d941dc972837213bc340e5` |
| `api-manager/4.3.0/develop/streaming-apps/streaming-integrator-studio-overview.md` | `#StreamProcessorStudioOverview-SourceView` | `api-manager/4.3.0/develop/streaming-apps/streaming-integrator-studio-overview.md` | `StreamProcessorStudioOverview-SourceView` |
| `api-manager/4.3.0/develop/streaming-apps/streaming-integrator-studio-overview.md` | `#StreamProcessorStudioOverview-SourceView` | `api-manager/4.3.0/develop/streaming-apps/streaming-integrator-studio-overview.md` | `StreamProcessorStudioOverview-SourceView` |
| `api-manager/4.3.0/develop/streaming-apps/streaming-integrator-studio-overview.md` | `#StreamProcessorStudioOverview-DesignView` | `api-manager/4.3.0/develop/streaming-apps/streaming-integrator-studio-overview.md` | `StreamProcessorStudioOverview-DesignView` |
| `api-manager/4.3.0/develop/streaming-apps/streaming-integrator-studio-overview.md` | `#StreamProcessorStudioOverview-DesignView` | `api-manager/4.3.0/develop/streaming-apps/streaming-integrator-studio-overview.md` | `StreamProcessorStudioOverview-DesignView` |
| `api-manager/4.3.0/develop/streaming-apps/streaming-integrator-studio-overview.md` | `#StreamProcessorStudioOverview-SourceView` | `api-manager/4.3.0/develop/streaming-apps/streaming-integrator-studio-overview.md` | `StreamProcessorStudioOverview-SourceView` |
| `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.3.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.3.0/install-and-setup/setup/api-controller/managing-apis-api-products/importing-apis-via-dev-first-approach.md` | `../../../../install-and-setup/setup/api-controller/advanced-topics/using-dynamic-data-in-api-controller-projects.md#initialize-api-projects-with-dynamic-data` | `api-manager/4.3.0/install-and-setup/setup/api-controller/advanced-topics/using-dynamic-data-in-api-controller-projects.md` | `initialize-api-projects-with-dynamic-data` |
| `api-manager/4.3.0/install-and-setup/setup/deployment-best-practices/tuning-performance.md` | `#configuring-wso2-api-m-to-perform-regular-cleaning` | `api-manager/4.3.0/install-and-setup/setup/deployment-best-practices/tuning-performance.md` | `configuring-wso2-api-m-to-perform-regular-cleaning` |
| `api-manager/4.3.0/install-and-setup/setup/distributed-deployment/configuring-wso2-identity-server-as-a-key-manager.md` | `#Linux-Mac` | `api-manager/4.3.0/install-and-setup/setup/distributed-deployment/configuring-wso2-identity-server-as-a-key-manager.md` | `Linux-Mac` |
| `api-manager/4.3.0/install-and-setup/setup/distributed-deployment/configuring-wso2-identity-server-as-a-key-manager.md` | `#windows` | `api-manager/4.3.0/install-and-setup/setup/distributed-deployment/configuring-wso2-identity-server-as-a-key-manager.md` | `windows` |
| `api-manager/4.3.0/install-and-setup/setup/distributed-deployment/configuring-wso2-identity-server-as-a-key-manager.md` | `#step3-2` | `api-manager/4.3.0/install-and-setup/setup/distributed-deployment/configuring-wso2-identity-server-as-a-key-manager.md` | `step3-2` |
| `api-manager/4.3.0/install-and-setup/setup/distributed-deployment/deploying-wso2-api-m-in-a-distributed-setup.md` | `../../../install-and-setup/setup/deployment-best-practices/production-deployment-guidelines.md#common-guidelines-and-checklist` | `api-manager/4.3.0/install-and-setup/setup/deployment-best-practices/production-deployment-guidelines.md` | `common-guidelines-and-checklist` |

_…and 20 more. Full list in the JSON sidecar._

## `gone` — No target anywhere

No file of this name exists anywhere under the docs root, so there is nothing to point at. Each needs a decision: was the page meant to be migrated and missed, was it deliberately dropped (then the link and its sentence should go), or was it merged into another page (then link there)? **Do not guess these.**

**36 of the rows below are missing images already investigated in `UNRECOVERABLE-IMAGES-api-manager-4.3.0.md`** — no recovery path exists in this repo or its known predecessor (`wso2/docs-apim`); a fresh screenshot against the current product is the only fix. Don't re-investigate those; they're listed here only because the checker has no "confirmed unrecoverable" state.

**19 of the rows below are all in one page, `wip/need-to-update/create-and-publish-an-api.md`** — that page is a raw, unconverted Confluence export (mangled tables, broken image refs, `_Underscore_Style_` placeholder links) sitting in a folder literally named for needing a rewrite. Patching its links wouldn't fix it; it needs a full content rewrite, which is out of scope for a link-fix pass.

**Remaining ~11 rows are genuine open decisions** — an ambiguous choice between two current MI docs pages for a keystore link, and a handful with no equivalent page found anywhere in this repo's history (kubernetes-operators deploy-APIs guide, Hazelcast clustering, a general analytics-overview page, an anchor on an OpenAPI-viewer-rendered reference page that the checker cannot statically verify).

| Page | Broken target | Note |
|---|---|---|
| `api-manager/4.3.0/administer/managing-users-and-roles/managing-user-stores/configure-primary-user-store/configuring-a-read-write-ldap-user-store.md` | `../../../../../deploy/performance/performance-tuning-recommendations/#performance-tuning-ldaps-pooling` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/administer/managing-users-and-roles/managing-user-stores/understanding-the-user-realm.md` | `../../../assets/attachments/126562314/126562315.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/administer/multitenancy/adding-new-tenants.md` | `../../assets/attachments/126562777/126562778.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/administer/multitenancy/adding-new-tenants.md` | `../../assets/attachments/126562777/126562781.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/administer/multitenancy/adding-new-tenants.md` | `../../assets/attachments/126562777/126562782.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/design/create-api/create-a-websocket-api.md` | `../../observe/api-manager-analytics/overview-of-api-analytics.md` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/install-and-setup-overview.md` | `../../install-and-setup/setup/kubernetes-operators/k8s-api-operator/manage-apis/api-deployments/` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/distributed-deployment/configuring-the-gateway-in-a-distributed-environment-with-rsync.md` | `../distributed-deployment-of-the-gateway/` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/distributed-deployment/configuring-the-gateway-in-a-distributed-environment-with-rsync.md` | `../working-with-hazelcast-clustering/` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/admin-searching-the-registry.md` | `../../../../assets/attachments/126562657/126562660.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/admin-searching-the-registry.md` | `../../../../assets/attachments/126562657/126562659.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/admin-searching-the-registry.md` | `../../../../assets/attachments/126562657/126562658.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `../../../../../assets/attachments/126562631/126562638.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `../../../../../assets/attachments/126562631/126562637.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `../../../../../assets/attachments/126562631/126562635.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `../../../../../assets/attachments/126562631/126562633.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `../../../../../assets/attachments/126562631/126562632.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `../../../../../assets/attachments/126562631/126562636.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/editing-collections-using-the-entries-panel.md` | `../../../../../assets/attachments/126562643/126562644.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/link-creation.md` | `../../../../../assets/attachments/126562639/126562641.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/link-creation.md` | `../../../../../assets/attachments/126562639/126562640.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/link-creation.md` | `../../../../../assets/attachments/126562639/126562642.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/metadata.md` | `../../../../../assets/attachments/22185146/22514191.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/metadata.md` | `../../../../../assets/attachments/126562605/126562606.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/metadata.md` | `../../../../../assets/attachments/126562605/126562611.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/metadata.md` | `../../../../../assets/attachments/22185146/22514195.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/properties.md` | `../../../../../assets/attachments/126562613/126562618.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/properties.md` | `../../../../../assets/attachments/126562613/126562617.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/role-permissions.md` | `../../../../../assets/attachments/126562645/126562646.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/role-permissions.md` | `../../../../../assets/attachments/126562645/126562647.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/role-permissions.md` | `../../../../../assets/attachments/126562645/126562648.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/using-remote-registry/admin-all-partitions-in-a-single-server.md` | `../../../../../assets/attachments/21037149/21331970.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/using-remote-registry/admin-config-and-governance-partitions-in-a-remote-registry.md` | `../../../../../assets/attachments/21037149/21331972.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/using-remote-registry/admin-config-and-governance-partitions-in-a-remote-registry.md` | `../../../../../assets/attachments/21037149/21332021.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/using-remote-registry/admin-config-and-governance-partitions-in-a-remote-registry.md` | `../../../../../assets/attachments/21037149/21332022.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/using-remote-registry/admin-config-and-governance-partitions-in-separate-nodes.md` | `../../../../../assets/attachments/126562675/126562676.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/using-remote-registry/admin-governance-partition-in-a-remote-registry.md` | `../../../../../assets/attachments/126562673/126562674.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/setup-overview.md` | `../../install-and-setup/setup/mi-setup/security/creating_keystore.md` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/single-node/deploying-api-manager-using-single-node-instances.md` | `../../../assets/attachments/103334465/103334466.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.3.0/install-and-setup/setup/single-node/deploying-api-manager-using-single-node-instances.md` | `../../../assets/attachments/103334465/103334467.png` | `no file of this name exists anywhere under the docs root` |

_…and 26 more. Full list in the JSON sidecar._

---

## Prompt for an AI coding agent

Paste the block below to an agent working in the repo root. It is deliberately scoped to the four groups with a defensible mechanical answer. `templated`, `stale`, `anchor` and `gone` need judgement and are left out on purpose.

Alternatively, run `fix_links.py --tier <group>` yourself — same scope, one group at a time, and every rewrite verified against the files on disk before it is written.

````text
You are fixing broken links in the WSO2 API Platform docs, scope: api-manager/4.3.0.

Read the fix plan in `BROKEN-LINKS-api-manager-4.3.0.md` and the machine-readable list in `BROKEN-LINKS-api-manager-4.3.0.json`.

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
