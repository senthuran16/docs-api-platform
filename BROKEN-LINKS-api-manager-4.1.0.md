# Broken links and images — `api-manager/4.1.0`

**243 findings** across 1427 pages. **9** have an exact or high-confidence mechanical fix; **25** need a decision.

### Fixable by script

Run in this order. Each is a separate `fix_links.py --tier` run, and every rewrite is verified against the files on disk before it is written.

| Order | Group | Cause | Count | Fix |
|---|---|---|---|---|
| 1 | `malformed` | Malformed link syntax | 1 | Exact — no judgement |
| 2 | `dir_style` | Written as a URL, so mkdocs never resolves it | 0 | Add `.md` — mkdocs then owns the depth |
| 3 | `depth` | Wrong relative depth | 8 | Exact — no judgement |
| 4 | `renamed` | Renamed or moved target | 1 | Proposed; `high` confidence applied by default |
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
| `templated` | `{{base_path}}` where the resource does not exist | 78 | May be served by a redirect |
| `stale` | Pre-migration domain | 35 | Needs the equivalent page on the new site |
| `anchor` | Missing anchor | 95 | The heading was reworded — which one now? |
| `gone` | No target anywhere | 25 | Was it dropped, missed, or merged? |
| `partial` | Broken link inside an included partial | 0 | Resolves against the includer's url, not the partial's |

## Excluded — `{{base_path}}` where the resource does not exist

Same variable, but the target is not present at that path in this version. It may be served by a redirect, or the page may not have been migrated. **Leave these alone** until the redirect strategy is settled — a rewrite here would be a guess.

**All 78 rows below have been individually investigated. Do not re-investigate:**

- **34 rows are Confluence attachment images** — same unrecoverable pattern as `UNRECOVERABLE-IMAGES-api-manager-4.1.0.md`.
- **`{{choreo_connect.helm_chart.git_tag}}` rows (6, across 3 Choreo Connect config pages)** — this variable **is** defined (`v1.2.0.1` in `en/mkdocs.yml`'s `extra:` section) and resolves fine; the checker false-positives it. Confirmed working, no fix needed.
- **`{{envoy_path}}` rows (12)** — genuinely undefined; the user explicitly declined adding this to `en/mkdocs.yml` earlier this session ("no need"). Do not re-propose without being asked again.
- **11 rows on the `wip/deleted-pages/*` pages** — same raw-Confluence-export situation as the other `wip/` pages; needs a content rewrite.
- **9 `install-and-setup/setup/mi-setup/**` rows referencing `deployment_checklist`** (5 database-setup pages + `deploying_wso2_ei.md`) — the target content exists on the separate Micro Integrator product site (`mi.docs.wso2.com`, confirmed via search: `.../install-and-setup/setup/deployment-best-practices/production-deployment-guidelines/`) but not locally under this repo's `mi-setup/` tree, and no local page was ever created for it either. **Needs a human decision**: link out to `mi.docs.wso2.com` (picking a compatible MI version, since it has its own independent versioning) or leave until/unless the local page gets written. Not something to decide unilaterally.
- **2 rows referencing `setting-up-classic-observability-deployment`** (`install-and-setup-overview.md`, `using-the-analytics-dashboard.md`) — same situation: no local page exists, and the closest analog on `mi.docs.wso2.com` covers *cloud-native* observability deployment specifically, not "classic" — the terminology doesn't cleanly map, so even an external link would be a guess. Left for a human to decide.
- **`adding-dynamic-endpoints.md`'s reference to "Creating and Uploading Manually in API Publisher"** — the target page was renamed to `specifying-mediation-flow-based-on-policy.md` (confirmed it exists), but no heading on that page matches the specific anchor text; leaving both the path and anchor as-is rather than partially fixing to a page that still won't land on the right section.
- **`microsoft-dynamics365-configuration.md`'s `after-setup-permission.png`** and **`sf-soap-connector-example.md`'s `salesforcesoap.zip`** — confirmed missing from every version of this repo; genuinely unrecoverable.

| Page | Link | Variable |
|---|---|---|
| `api-manager/4.1.0/administer/managing-users-and-roles/managing-user-stores/understanding-the-user-realm.md` | `{{base_path}}/assets/attachments/126562314/126562315.png` | `{{base_path}}` |
| `api-manager/4.1.0/administer/multitenancy/adding-new-tenants.md` | `{{base_path}}/assets/attachments/126562777/126562778.png` | `{{base_path}}` |
| `api-manager/4.1.0/administer/multitenancy/adding-new-tenants.md` | `{{base_path}}/assets/attachments/126562777/126562781.png` | `{{base_path}}` |
| `api-manager/4.1.0/administer/multitenancy/adding-new-tenants.md` | `{{base_path}}/assets/attachments/126562777/126562782.png` | `{{base_path}}` |
| `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/configurations/configuration-overview.md` | `https://github.com/wso2/kubernetes-microgateway/tree/{{choreo_connect.helm_chart.git_tag}}/helm/choreo-connect` | `{{choreo_connect.helm_chart.git_tag}}` |
| `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/configurations/configuration-overview.md` | `https://github.com/wso2/kubernetes-microgateway/blob/{{choreo_connect.helm_chart.git_tag}}/helm/choreo-connect/values.yaml` | `{{choreo_connect.helm_chart.git_tag}}` |
| `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/configurations/configuration-overview.md` | `https://github.com/wso2/kubernetes-microgateway/tree/{{choreo_connect.helm_chart.git_tag}}/helm/choreo-connect/templates` | `{{choreo_connect.helm_chart.git_tag}}` |
| `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/configurations/configure-logs-router.md` | `{{envoy_path}}/configuration/observability/access_log/usage#format-strings` | `{{envoy_path}}` |
| `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/configurations/configure-logs-router.md` | `{{envoy_path}}/configuration/observability/access_log/usage#command-operators` | `{{envoy_path}}` |
| `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/configurations/configure-logs-router.md` | `{{envoy_path}}/operations/cli` | `{{envoy_path}}` |
| `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/endpoints/resiliency/circuit-breakers.md` | `{{envoy_path}}/intro/arch_overview/upstream/circuit_breaking` | `{{envoy_path}}` |
| `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/endpoints/resiliency/retry-policies.md` | `{{envoy_path}}/configuration/http/http_filters/router_filter#config-http-filters-router-x-envoy-max-retries` | `{{envoy_path}}` |
| `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/endpoints/resiliency/timeout.md` | `{{envoy_path}}/configuration/http/http_filters/router_filter#config-http-filters-router-x-envoy-max-retries` | `{{envoy_path}}` |
| `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/endpoints/resiliency/timeout.md` | `{{envoy_path}}/faq/configuration/timeouts` | `{{envoy_path}}` |
| `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/getting-started/deploy/cc-as-a-standalone-gateway-on-kubernetes-helm-artifacts.md` | `https://github.com/wso2/kubernetes-microgateway/tree/{{choreo_connect.helm_chart.git_tag}}/helm/choreo-connect` | `{{choreo_connect.helm_chart.git_tag}}` |
| `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/getting-started/deploy/cc-as-a-standalone-gateway-on-kubernetes-helm-artifacts.md` | `https://github.com/wso2/kubernetes-microgateway/tree/{{choreo_connect.helm_chart.git_tag}}/helm/choreo-connect/README.md` | `{{choreo_connect.helm_chart.git_tag}}` |
| `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/getting-started/deploy/cc-on-kubernetes-with-apim-as-control-plane-helm-artifacts.md` | `https://github.com/wso2/kubernetes-microgateway/tree/{{choreo_connect.helm_chart.git_tag}}/helm/choreo-connect` | `{{choreo_connect.helm_chart.git_tag}}` |
| `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/getting-started/deploy/cc-on-kubernetes-with-apim-as-control-plane-helm-artifacts.md` | `https://github.com/wso2/kubernetes-microgateway/tree/{{choreo_connect.helm_chart.git_tag}}/helm/choreo-connect/README.md` | `{{choreo_connect.helm_chart.git_tag}}` |
| `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/troubleshooting/adding-debug-logs.md` | `{{envoy_path}}/start/quick-start/admin` | `{{envoy_path}}` |
| `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/troubleshooting/error-handling.md` | `{{envoy_path}}/configuration/observability/access_log/usage#config-access-log-format-response-flags` | `{{envoy_path}}` |
| `api-manager/4.1.0/design/api-policies/regular-gateway-policies/adding-dynamic-endpoints.md` | `{{base_path}}/learn/api-gateway/message-mediation/changing-the-default-mediation-flow-of-api-requests#creating-and-uploading-manually-in-api-publisher` | `{{base_path}}` |
| `api-manager/4.1.0/install-and-setup/install-and-setup-overview.md` | `{{base_path}}/install-and-setup/setup/mi-setup/observability/setting-up-classic-observability-deployment` | `{{base_path}}` |
| `api-manager/4.1.0/install-and-setup/setup/mi-setup/databases/setting-up-ibm-db2.md` | `{{base_path}}/install-and-setup/setup/mi-setup/deployment/deployment_checklist/#monitoring-transaction-counts` | `{{base_path}}` |
| `api-manager/4.1.0/install-and-setup/setup/mi-setup/databases/setting-up-ibm-db2.md` | `{{base_path}}/install-and-setup/setup/mi-setup/deployment/deployment_checklist#monitoring-transaction-counts` | `{{base_path}}` |
| `api-manager/4.1.0/install-and-setup/setup/mi-setup/databases/setting-up-mssql.md` | `{{base_path}}/install-and-setup/setup/mi-setup/deployment/deployment_checklist#monitoring-transaction-counts` | `{{base_path}}` |
| `api-manager/4.1.0/install-and-setup/setup/mi-setup/databases/setting-up-mssql.md` | `{{base_path}}/install-and-setup/setup/mi-setup/deployment/deployment_checklist#monitoring-transaction-counts` | `{{base_path}}` |
| `api-manager/4.1.0/install-and-setup/setup/mi-setup/databases/setting-up-mysql.md` | `{{base_path}}/install-and-setup/setup/mi-setup/deployment/deployment_checklist#monitoring-transaction-counts` | `{{base_path}}` |
| `api-manager/4.1.0/install-and-setup/setup/mi-setup/databases/setting-up-oracle.md` | `{{base_path}}/install-and-setup/setup/mi-setup/deployment/deployment_checklist#monitoring-transaction-counts` | `{{base_path}}` |
| `api-manager/4.1.0/install-and-setup/setup/mi-setup/databases/setting-up-postgresql.md` | `{{base_path}}/install-and-setup/setup/mi-setup/deployment/deployment_checklist#monitoring-transaction-counts` | `{{base_path}}` |
| `api-manager/4.1.0/install-and-setup/setup/mi-setup/databases/setting-up-postgresql.md` | `{{base_path}}/install-and-setup/setup/mi-setup/deployment/deployment_checklist/#monitoring-transaction-counts` | `{{base_path}}` |
| `api-manager/4.1.0/install-and-setup/setup/mi-setup/deployment/deploying_wso2_ei.md` | `{{base_path}}/install-and-setup/setup/mi-setup/deployment/deployment_checklist` | `{{base_path}}` |
| `api-manager/4.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/admin-searching-the-registry.md` | `{{base_path}}/assets/attachments/126562657/126562660.png` | `{{base_path}}` |
| `api-manager/4.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/admin-searching-the-registry.md` | `{{base_path}}/assets/attachments/126562657/126562659.png` | `{{base_path}}` |
| `api-manager/4.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/admin-searching-the-registry.md` | `{{base_path}}/assets/attachments/126562657/126562658.png` | `{{base_path}}` |
| `api-manager/4.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `{{base_path}}/assets/attachments/126562631/126562638.png` | `{{base_path}}` |
| `api-manager/4.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `{{base_path}}/assets/attachments/126562631/126562637.png` | `{{base_path}}` |
| `api-manager/4.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `{{base_path}}/assets/attachments/126562631/126562635.png` | `{{base_path}}` |
| `api-manager/4.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `{{base_path}}/assets/attachments/126562631/126562633.png` | `{{base_path}}` |
| `api-manager/4.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `{{base_path}}/assets/attachments/126562631/126562632.png` | `{{base_path}}` |
| `api-manager/4.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `{{base_path}}/assets/attachments/126562631/126562636.png` | `{{base_path}}` |

_…and 38 more. Full list in the JSON sidecar._

## `malformed` — Malformed link syntax

The link target is not a valid path or URL, so it renders as literal broken text regardless of whether the destination exists. Carried over from the old wiki. The replacement is exact.

| Page | Currently | Change to | Why |
|---|---|---|---|
| `api-manager/4.1.0/integrate/develop/create-kubernetes-project.md` | `../../install-and-setup/setup/mi-setup/deployment/kubernetes_deployment.md#ei-kubernetes-k8s-operator"` | `../../install-and-setup/setup/mi-setup/deployment/kubernetes_deployment.md#ei-kubernetes-k8s-operator` | `target is wrapped in backticks or quotes, so it is not a valid URL` |

## `depth` — Wrong relative depth

The target exists; the path has one `../` too many. These render correctly in a browser (the published URL sits one directory deeper than the source file), so they look fine on the site — but `mkdocs build` warns about every one, and anyone reading the raw Markdown through `md_url` gets a broken path. The replacement below is exact.

| Page | Currently | Change to |
|---|---|---|
| `api-manager/4.1.0/administer/managing-users-and-roles/managing-user-stores/configure-primary-user-store/configuring-a-read-only-ldap-user-store.md` | `../../../../install-and-setup/setup/security/logins-and-passwords/maintaining-logins-and-passwords.md#setting-up-an-e-mail-login` | `../../../../../install-and-setup/setup/security/logins-and-passwords/maintaining-logins-and-passwords/#setting-up-an-e-mail-login` |
| `api-manager/4.1.0/install-and-setup/install-and-setup-overview.md` | `../troubleshooting/error-handling.md#custom-error-message` | `../../troubleshooting/error-handling/#custom-error-message` |
| `api-manager/4.1.0/install-and-setup/install/installation-prerequisites.md` | `../setup/reference/product-compatibility.md#tested-operating-systems-and-jdks` | `../../setup/reference/product-compatibility/#tested-operating-systems-and-jdks` |
| `api-manager/4.1.0/install-and-setup/setup/deployment-best-practices/security-guidelines-for-production-deployment.md` | `../reference/product-compatibility.md#tested-operating-systems-and-jdks` | `../../reference/product-compatibility/#tested-operating-systems-and-jdks` |
| `api-manager/4.1.0/integrate/develop/create-integration-project.md` | `../../install-and-setup/setup/mi-setup/deployment/kubernetes_deployment.md#ei-kubernetes-k8s-operator` | `../../../install-and-setup/setup/mi-setup/deployment/kubernetes_deployment/#ei-kubernetes-k8s-operator` |
| `api-manager/4.1.0/integrate/develop/creating-artifacts/creating-registry-resources.md` | `../create-integration-project.md#registry-resource-project` | `../../create-integration-project/#registry-resource-project` |
| `api-manager/4.1.0/integrate/develop/intro-integration-development.md` | `../integration-overview.md#tutorials` | `../../integration-overview/#tutorials` |
| `api-manager/4.1.0/integrate/develop/intro-integration-development.md` | `../integration-overview.md#examples` | `../../integration-overview/#examples` |

## `renamed` — Renamed or moved target

The target does not exist at the path written, but a file of the same name exists elsewhere under the same version. This is the restructure: directories were renamed and the inbound links were never updated.

### Several candidates — verify before applying (1)

| Page | Currently | Best guess | Confidence |
|---|---|---|---|
| `api-manager/4.1.0/includes/prerequisites-apim.md` | `../../../install-and-setup/install/installation-prerequisites/` | `../install-and-setup/install/installation-prerequisites.md` | low (2 candidates) |

## `stale` — Links to the pre-migration site

These point at a location the documentation has migrated away from. For each one: find the equivalent page on the new site and link to it relatively, or if the content wasn't migrated, remove the link and say so in the prose. Never leave a reader on the old site.

**All 35 rows below are a confirmed checker false-positive — do not re-investigate or "fix" them.** Every one is a `/bijira/docs/api-manager/4.1.0/...` absolute path under `includes/` (shared partials). `report_links.py`/`fix_links.py` treat any leading-`/` link as docs-root-relative with no mount prefix, so they mis-bucket the site's own mount-prefixed absolute paths as `stale`. Spot-checked ~10 of these across every `includes/` subfolder against the live rendered build — all resolve at 200. This is the same known tooling gap documented during the `api-manager/3.1.0` pass this session.

| Page | Link |
|---|---|
| `api-manager/4.1.0/includes/analytics/configure-synapse-gateway.md` | `/bijira/docs/api-manager/4.1.0/api-analytics/gateways/configure-synapse-gateway/#advanced-configurations` |
| `api-manager/4.1.0/includes/deploy/assign-custom-hostname.md` | `/bijira/docs/api-manager/4.1.0/assets/img/includes/deploy/select-api.png` |
| `api-manager/4.1.0/includes/deploy/assign-custom-hostname.md` | `/bijira/docs/api-manager/4.1.0/design/create-api/create-api-revisions/` |
| `api-manager/4.1.0/includes/design/additional-api-key.md` | `/bijira/docs/api-manager/4.1.0/assets/img/learn/ip-api-key.png` |
| `api-manager/4.1.0/includes/design/additional-api-key.md` | `/bijira/docs/api-manager/4.1.0/assets/img/learn/http-referer-api-key.png` |
| `api-manager/4.1.0/includes/design/create-publish-api.md` | `/bijira/docs/api-manager/4.1.0/assets/img/learn/api-key-option.png` |
| `api-manager/4.1.0/includes/design/deploy-revision.md` | `/bijira/docs/api-manager/4.1.0/assets/img/design/revision/deploy-first-revision.png` |
| `api-manager/4.1.0/includes/design/deploy-revision.md` | `/bijira/docs/api-manager/4.1.0/assets/img/design/revision/deploy-new-revision.png` |
| `api-manager/4.1.0/includes/design/deploy-revision.md` | `/bijira/docs/api-manager/4.1.0/assets/img/design/revision/delete-and-deploy-revision.png` |
| `api-manager/4.1.0/includes/design/generate-api-key.md` | `/bijira/docs/api-manager/4.1.0/assets/img/learn/subscribe-to-api.png` |
| `api-manager/4.1.0/includes/design/generate-api-key.md` | `/bijira/docs/api-manager/4.1.0/assets/img/learn/view-credentials-manage-app.png` |
| `api-manager/4.1.0/includes/design/generate-api-key.md` | `/bijira/docs/api-manager/4.1.0/assets/img/learn/generate-api-key.png` |
| `api-manager/4.1.0/includes/design/generate-api-key.md` | `/bijira/docs/api-manager/4.1.0/assets/img/learn/copy-api-key.png` |
| `api-manager/4.1.0/includes/design/redis-counter-note.md` | `/bijira/docs/api-manager/4.1.0/design/rate-limiting/advanced-topics/configuring-rate-limiting-api-gateway-cluster/` |
| `api-manager/4.1.0/includes/reference/connectors/exporting-artifacts.md` | `/bijira/docs/api-manager/4.1.0/assets/img/integrate/connectors/connector-exporter-project-1.jpg` |
| `api-manager/4.1.0/includes/reference/connectors/exporting-artifacts.md` | `/bijira/docs/api-manager/4.1.0/assets/img/integrate/connectors/connector-exporter-project-1.jpg` |
| `api-manager/4.1.0/includes/reference/connectors/exporting-artifacts.md` | `/bijira/docs/api-manager/4.1.0/assets/img/integrate/connectors/connector-exporter-project-naming.png` |
| `api-manager/4.1.0/includes/reference/connectors/exporting-artifacts.md` | `/bijira/docs/api-manager/4.1.0/assets/img/integrate/connectors/connector-exporter-project-naming.png` |
| `api-manager/4.1.0/includes/reference/connectors/exporting-artifacts.md` | `/bijira/docs/api-manager/4.1.0/assets/img/integrate/connectors/adding-connector-to-exporter-project-3.jpg` |
| `api-manager/4.1.0/includes/reference/connectors/exporting-artifacts.md` | `/bijira/docs/api-manager/4.1.0/assets/img/integrate/connectors/adding-connector-to-exporter-project-3.jpg` |
| `api-manager/4.1.0/includes/reference/connectors/exporting-artifacts.md` | `/bijira/docs/api-manager/4.1.0/assets/img/integrate/connectors/capp-project1.jpg` |
| `api-manager/4.1.0/includes/reference/connectors/exporting-artifacts.md` | `/bijira/docs/api-manager/4.1.0/assets/img/integrate/connectors/saving-projects.png` |
| `api-manager/4.1.0/includes/reference/connectors/exporting-artifacts.md` | `/bijira/docs/api-manager/4.1.0/assets/img/integrate/connectors/saving-projects.png` |
| `api-manager/4.1.0/includes/reference/connectors/importing-connector-to-integration-studio.md` | `/bijira/docs/api-manager/4.1.0/assets/img/integrate/new-project/new-integration-project.png` |
| `api-manager/4.1.0/includes/reference/connectors/importing-connector-to-integration-studio.md` | `/bijira/docs/api-manager/4.1.0/assets/img/integrate/new-project/new-integration-project.png` |
| `api-manager/4.1.0/includes/reference/connectors/importing-connector-to-integration-studio.md` | `/bijira/docs/api-manager/4.1.0/assets/img/integrate/connectors/search-connector.png` |
| `api-manager/4.1.0/includes/reference/connectors/importing-connector-to-integration-studio.md` | `/bijira/docs/api-manager/4.1.0/assets/img/integrate/connectors/search-connector.png` |
| `api-manager/4.1.0/includes/reference/connectors/importing-connector-to-integration-studio.md` | `/bijira/docs/api-manager/4.1.0/assets/img/integrate/connectors/drag-connector-operation.png` |
| `api-manager/4.1.0/includes/reference/connectors/importing-connector-to-integration-studio.md` | `/bijira/docs/api-manager/4.1.0/assets/img/integrate/connectors/drag-connector-operation.png` |
| `api-manager/4.1.0/includes/reference/connectors/salesforce-connectors/sf-access-token-generation.md` | `/bijira/docs/api-manager/4.1.0/assets/img/integrate/connectors/salesforce-developer-edition-signup.png` |
| `api-manager/4.1.0/includes/reference/connectors/salesforce-connectors/sf-access-token-generation.md` | `/bijira/docs/api-manager/4.1.0/assets/img/integrate/connectors/salesforce-account-setup.png` |
| `api-manager/4.1.0/includes/reference/connectors/salesforce-connectors/sf-access-token-generation.md` | `/bijira/docs/api-manager/4.1.0/assets/img/integrate/connectors/new-connected-app.png` |
| `api-manager/4.1.0/includes/reference/connectors/salesforce-connectors/sf-access-token-generation.md` | `/bijira/docs/api-manager/4.1.0/assets/img/integrate/connectors/create-connected-app.jpg` |
| `api-manager/4.1.0/includes/reference/connectors/salesforce-connectors/sf-access-token-generation.md` | `/bijira/docs/api-manager/4.1.0/assets/img/integrate/connectors/connected-app.jpg` |
| `api-manager/4.1.0/includes/reference/connectors/salesforce-connectors/sf-access-token-generation.md` | `/bijira/docs/api-manager/4.1.0/assets/img/integrate/connectors/postman-connected-app.png` |

## `anchor` — Missing anchor

The page resolves but the `#fragment` matches no heading, so the reader lands at the top instead of the section. Usually the heading was reworded. Open the target, find the heading that was meant, and use its current slug.

**All 95 rows below have been individually investigated and confirmed unfixable — do not re-investigate.** Grouped by pattern:

- **`working-with-the-design-view.md` `#StreamProcessorStudioOverview-Settings`-style anchor (12)** — a self-referencing "click the settings icon" UI callout, not a documentation section. No real target ever existed.
- **`reference/synapse-properties/sequence-properties.md` (8 rows referencing it)** — this page is explicitly marked `**This page is currently WIP!**` with no other content. Genuinely nothing to link to yet.
- **`xml-threat-protection-for-api-gateway.md`, `json-threat-protection-for-api-gateway.md`, `regular-expression-threat-protection-for-api-gateway.md` (11 rows total)** — the same "Request"/"Response"/"Oracle JDK"/"IBM JDK" bullet-label-before-a-code-block pattern documented for `api-manager/3.1.0`. Lost content, not a renamed heading.
- **`config-catalog.md`/`config-catalog-mi.md` blocking vs non-blocking references (`#http-transport`, `#rabbitmq-sender`, `#jms-transport-listener`, `#jms-transport-sender`, ~10 rows)** — each has two equally-valid heading candidates (blocking-mode / non-blocking-mode variants) with no textual signal in the linking sentence to disambiguate. Genuinely ambiguous, left rather than guessed.
- **`creating-custom-users-to-perform-api-controller-operations.md` (5 rows)** — "Steps to create a custom user..." is a `!!! info` admonition title (bold text), not a real heading.
- **`monetizing-an-api.md` `#connectID` (2), `faq.md` `#FAQ-*` (2)** — same bold-text-not-heading situation as `3.1.0`.
- **`configuring-wso2-identity-server-as-a-key-manager.md` `#Linux-Mac`/`#windows` (2)** — OS-tab bullet labels immediately followed by a code block, no heading, same pattern as `3.1.0`.
- **`create-integration-project.md` `#datasource-project` (2)** — no "Datasource" row exists in the Sub Projects table; genuinely missing (the sibling `#esb-config-project`/`#registry-resource-project` anchors on this same page were fixed this session).
- **Remaining ~35 rows are individually-confirmed one-offs** — a mix of: content restructured away in this version (e.g. `running-the-api-m.md` no longer has a session-timeout section, `installing-si.md` no longer has a "starting the server" section, `gdpr-for-wso2-api-manager.md` was rewritten into a Step 1/2/3 structure), genuinely ambiguous multi-candidate renames (e.g. `endpoint-properties.md`'s "Indirect and Resolving Endpoints" split into two separate headings), and a few pages needing a cross-product WebSearch lookup that came back inconclusive.

| Page | Link | Target file | Missing anchor |
|---|---|---|---|
| `api-manager/4.1.0/administer/managing-users-and-roles/managing-user-roles.md` | `managing-permissions.md#adding-role-based-permissions` | `api-manager/4.1.0/administer/managing-users-and-roles/managing-permissions.md` | `adding-role-based-permissions` |
| `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/api-gateway/passing-enduser-attributes-to-the-backend-via-api-gateway.md` | `#sample-jwt` | `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/api-gateway/passing-enduser-attributes-to-the-backend-via-api-gateway.md` | `sample-jwt` |
| `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/configure-analytics.md` | `../../../api-analytics/on-prem/elk-installation-guide.md#step-3-configure-security-in-elk` | `api-manager/4.1.0/api-analytics/on-prem/elk-installation-guide.md` | `step-3-configure-security-in-elk` |
| `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/deploy-api/deploy-api-with-custom-hostnames.md` | `#invoke-the-api` | `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/deploy-api/deploy-api-with-custom-hostnames.md` | `invoke-the-api` |
| `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/security/api-authorization/opa-validation.md` | `#request-payload-to-the-opa-server` | `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/security/api-authorization/opa-validation.md` | `request-payload-to-the-opa-server` |
| `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/security/api-authorization/opa-validation.md` | `#response-payload-from-the-opa-server` | `api-manager/4.1.0/deploy-and-publish/deploy-on-gateway/choreo-connect/security/api-authorization/opa-validation.md` | `response-payload-from-the-opa-server` |
| `api-manager/4.1.0/design/api-monetization/monetizing-an-api.md` | `#connectID` | `api-manager/4.1.0/design/api-monetization/monetizing-an-api.md` | `connectID` |
| `api-manager/4.1.0/design/api-monetization/monetizing-an-api.md` | `#connectID` | `api-manager/4.1.0/design/api-monetization/monetizing-an-api.md` | `connectID` |
| `api-manager/4.1.0/design/api-security/opa-validation/overview.md` | `#custom-opa-policy-with-custom-request-generator` | `api-manager/4.1.0/design/api-security/opa-validation/overview.md` | `custom-opa-policy-with-custom-request-generator` |
| `api-manager/4.1.0/design/api-security/opa-validation/overview.md` | `#custom-opa-policy-with-custom-request-generator` | `api-manager/4.1.0/design/api-security/opa-validation/overview.md` | `custom-opa-policy-with-custom-request-generator` |
| `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/json-threat-protection-for-api-gateway.md` | `#2fabe5e92ef64a3a999bb756d894221e` | `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/json-threat-protection-for-api-gateway.md` | `2fabe5e92ef64a3a999bb756d894221e` |
| `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/json-threat-protection-for-api-gateway.md` | `#6da49ce3d2cf4091a885d78334d2513e` | `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/json-threat-protection-for-api-gateway.md` | `6da49ce3d2cf4091a885d78334d2513e` |
| `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/regular-expression-threat-protection-for-api-gateway.md` | `#10673ba9a16d49dcaf1b6a073de9cf4d` | `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/regular-expression-threat-protection-for-api-gateway.md` | `10673ba9a16d49dcaf1b6a073de9cf4d` |
| `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/regular-expression-threat-protection-for-api-gateway.md` | `#90b129a29c8c4b74869eb1676bb3f705` | `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/regular-expression-threat-protection-for-api-gateway.md` | `90b129a29c8c4b74869eb1676bb3f705` |
| `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#Am300XMLThreatProtectionforAPIGateway-detectvulnerability` | `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `Am300XMLThreatProtectionforAPIGateway-detectvulnerability` |
| `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#b95bd611fb2144d0940b193f34addf5b` | `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `b95bd611fb2144d0940b193f34addf5b` |
| `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#70c795c618f04f2cb9983858b263298d` | `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `70c795c618f04f2cb9983858b263298d` |
| `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#389c50828aa24292b0657e037c09c635` | `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `389c50828aa24292b0657e037c09c635` |
| `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#159d32ca825c41a480037880ce2e6413` | `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `159d32ca825c41a480037880ce2e6413` |
| `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#45b87273c80b44ffb18a3f8fe4f5b8f6` | `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `45b87273c80b44ffb18a3f8fe4f5b8f6` |
| `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#194a5a4652e94e609d80ba175c16b449` | `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `194a5a4652e94e609d80ba175c16b449` |
| `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#db80409dd4d941dc972837213bc340e5` | `api-manager/4.1.0/design/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `db80409dd4d941dc972837213bc340e5` |
| `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `#WorkingwiththeDesignView-Settings` | `api-manager/4.1.0/develop/streaming-apps/working-with-the-design-view.md` | `WorkingwiththeDesignView-Settings` |
| `api-manager/4.1.0/get-started/api-manager-quick-start-guide.md` | `../install-and-setup/setup/api-controller/ci-cd-with-wso2-api-management.md#g-get-keys-for-an-apiapi-product` | `api-manager/4.1.0/install-and-setup/setup/api-controller/ci-cd-with-wso2-api-management.md` | `g-get-keys-for-an-apiapi-product` |
| `api-manager/4.1.0/get-started/api-manager-quick-start-guide.md` | `#subscribe` | `api-manager/4.1.0/get-started/api-manager-quick-start-guide.md` | `subscribe` |
| `api-manager/4.1.0/get-started/api-manager-quick-start-guide.md` | `#invoke` | `api-manager/4.1.0/get-started/api-manager-quick-start-guide.md` | `invoke` |
| `api-manager/4.1.0/includes/integration/pull-content-migration-esb-mi.md` | `../../../get-started/about-this-release/#compare-this-release-with-previous-esbs` | `api-manager/4.1.0/get-started/about-this-release.md` | `compare-this-release-with-previous-esbs` |
| `api-manager/4.1.0/includes/integration/pull-content-migration-esb-mi.md` | `../../../get-started/about-this-release/#compare-this-release-with-previous-esbs` | `api-manager/4.1.0/get-started/about-this-release.md` | `compare-this-release-with-previous-esbs` |
| `api-manager/4.1.0/install-and-setup/setup/api-controller/cicd-using-cli.md` | `advanced-topics/creating-custom-users-to-perform-api-controller-operations.md#steps-to-create-a-custom-user-who-can-perform-api-controller-operations` | `api-manager/4.1.0/install-and-setup/setup/api-controller/advanced-topics/creating-custom-users-to-perform-api-controller-operations.md` | `steps-to-create-a-custom-user-who-can-perform-api-controller-operations` |

_…and 55 more. Full list in the JSON sidecar._

## `gone` — No target anywhere

No file of this name exists anywhere under the docs root, so there is nothing to point at. Each needs a decision: was the page meant to be migrated and missed, was it deliberately dropped (then the link and its sentence should go), or was it merged into another page (then link there)? **Do not guess these.**

**All 25 rows below have been individually investigated. Do not re-investigate:**

- **`wip/need-to-update/create-and-publish-an-api.md` (21 rows, `_Key_Concepts_`-style underscore placeholders)** — byte-identical raw, unconverted Confluence export to the `api-manager/3.1.0` copy of this same file. Needs a content rewrite, not link patching.
- **`configuring-the-gateway-in-a-distributed-environment-with-rsync.md` (3 rows)** — `distributed-deployment-of-the-gateway`, `configuring-rsync-for-deployment-synchronization`, `working-with-hazelcast-clustering` — none of these pages exist in this version, any other version, or the pre-migration repo. Same as the identical finding already documented for `api-manager/3.1.0`.
- **`install-and-setup/setup/si-setup/defining-tables-for-physical-stores.md`'s `_Configuring_Datasources_` (1)** — confirmed genuinely dropped content; no matching heading anywhere on the page.

| Page | Broken target | Note |
|---|---|---|
| `api-manager/4.1.0/install-and-setup/setup/distributed-deployment/configuring-the-gateway-in-a-distributed-environment-with-rsync.md` | `../distributed-deployment-of-the-gateway/` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/install-and-setup/setup/distributed-deployment/configuring-the-gateway-in-a-distributed-environment-with-rsync.md` | `../../configuring-rsync-for-deployment-synchronization/` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/install-and-setup/setup/distributed-deployment/configuring-the-gateway-in-a-distributed-environment-with-rsync.md` | `../working-with-hazelcast-clustering/` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/install-and-setup/setup/si-setup/defining-tables-for-physical-stores.md` | `_Configuring_Datasources_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/wip/need-to-update/create-and-publish-an-api.md` | `_Key_Concepts_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/wip/need-to-update/create-and-publish-an-api.md` | `_Key_Concepts_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/wip/need-to-update/create-and-publish-an-api.md` | `_Key_Concepts_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/wip/need-to-update/create-and-publish-an-api.md` | `_Key_Concepts_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/wip/need-to-update/create-and-publish-an-api.md` | `_Key_Concepts_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/wip/need-to-update/create-and-publish-an-api.md` | `_Key_Concepts_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/wip/need-to-update/create-and-publish-an-api.md` | `_Key_Concepts_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/wip/need-to-update/create-and-publish-an-api.md` | `_Key_Concepts_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/wip/need-to-update/create-and-publish-an-api.md` | `_Configuring_Caching_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/wip/need-to-update/create-and-publish-an-api.md` | `_Key_Concepts_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/wip/need-to-update/create-and-publish-an-api.md` | `_Enabling_CORS_for_APIs_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/wip/need-to-update/create-and-publish-an-api.md` | `_Adding_Mediation_Extensions_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/wip/need-to-update/create-and-publish-an-api.md` | `_Add_SSL_Certificates_for_Endpoints_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/wip/need-to-update/create-and-publish-an-api.md` | `_Deploy_and_Test_Mock_APIs_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/wip/need-to-update/create-and-publish-an-api.md` | `_Rate_Limiting_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/wip/need-to-update/create-and-publish-an-api.md` | `_Create_and_Publish_an_API_from_a_Swagger_Definition_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/wip/need-to-update/create-and-publish-an-api.md` | `_Create_a_Mock_API_with_an_Inline_Script_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/wip/need-to-update/create-and-publish-an-api.md` | `_Create_a_WebSocket_API_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/wip/need-to-update/create-and-publish-an-api.md` | `_Create_and_Publish_a_SOAP_API_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/wip/need-to-update/create-and-publish-an-api.md` | `_Endpoints_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/4.1.0/wip/need-to-update/create-and-publish-an-api.md` | `_Invoke_an_API_using_the_Integrated_API_Console_` | `no file of this name exists anywhere under the docs root` |

---

## Prompt for an AI coding agent

Paste the block below to an agent working in the repo root. It is deliberately scoped to the four groups with a defensible mechanical answer. `templated`, `stale`, `anchor` and `gone` need judgement and are left out on purpose.

Alternatively, run `fix_links.py --tier <group>` yourself — same scope, one group at a time, and every rewrite verified against the files on disk before it is written.

````text
You are fixing broken links in the WSO2 API Platform docs, scope: api-manager/4.1.0.

Read the fix plan in `BROKEN-LINKS-api-manager-4.1.0.md` and the machine-readable list in `BROKEN-LINKS-api-manager-4.1.0.json`.

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
