# Unrecoverable images — `api-manager/3.1.0`

40 broken image references, confirmed by manual review, that cannot be fixed by relinking. The
source files were never migrated anywhere this repo's history reaches — a fresh screenshot
against the current product (or, for two of them, a targeted decision described below) is the
only real fix.

## Confluence attachment images (39)

Same investigation as `UNRECOVERABLE-IMAGES-api-manager-4.1.0.md` and
`UNRECOVERABLE-IMAGES-api-manager-4.3.0.md`. 33 of these 39 rows are the exact same
`assets/attachments/<pageId>/<attachmentId>.png` references, byte-for-byte identical, already
documented as unrecoverable there — this is legacy Confluence boilerplate (Registry management,
Multitenancy, single-node deployment, proxy setup) carried forward unchanged across every version
this repo has. The remaining 6 rows are specific to the 3.x line
(`monitoring-tcp-based-messages.md`, `getting-started/overview.md`) or unique to `3.1.0`
(`adding-a-custom-proxy-path.md`) — confirmed independently against the pre-migration repo
(`wso2/docs-apim`, `3.1.0` branch): the same broken attachment reference is already present there,
so the loss predates this repo and is not something this migration broke.

**No recovery path exists from this repo or its known predecessor.**

| # | Page | Broken image(s) |
|---|---|---|
| 1 | `administer/logging-and-monitoring/monitoring/monitoring-tcp-based-messages.md` | `assets/attachments/45946410/46206512.png`<br>`assets/attachments/45946410/46206513.png`<br>`assets/attachments/45946410/46206514.png` |
| 2 | `administer/managing-users-and-roles/managing-user-stores/understanding-the-user-realm.md` | `assets/attachments/126562314/126562315.png` |
| 3 | `administer/multitenancy/adding-new-tenants.md` | `assets/attachments/126562777/126562778.png`<br>`assets/attachments/126562777/126562781.png`<br>`assets/attachments/126562777/126562782.png` |
| 4 | `getting-started/overview.md` | `assets/attachments/103327648/126556775.png` |
| 5 | `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/admin-searching-the-registry.md` | `assets/attachments/126562657/126562658.png`<br>`assets/attachments/126562657/126562659.png`<br>`assets/attachments/126562657/126562660.png` |
| 6 | `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `assets/attachments/126562631/126562632.png`<br>`assets/attachments/126562631/126562633.png`<br>`assets/attachments/126562631/126562635.png`<br>`assets/attachments/126562631/126562636.png`<br>`assets/attachments/126562631/126562637.png`<br>`assets/attachments/126562631/126562638.png` |
| 7 | `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/editing-collections-using-the-entries-panel.md` | `assets/attachments/126562643/126562644.png` |
| 8 | `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/link-creation.md` | `assets/attachments/126562639/126562640.png`<br>`assets/attachments/126562639/126562641.png`<br>`assets/attachments/126562639/126562642.png` |
| 9 | `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/metadata.md` | `assets/attachments/22185146/22514191.png`<br>`assets/attachments/22185146/22514195.png`<br>`assets/attachments/126562605/126562606.png`<br>`assets/attachments/126562605/126562611.png` |
| 10 | `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/properties.md` | `assets/attachments/126562613/126562617.png`<br>`assets/attachments/126562613/126562618.png` |
| 11 | `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/role-permissions.md` | `assets/attachments/126562645/126562646.png`<br>`assets/attachments/126562645/126562647.png`<br>`assets/attachments/126562645/126562648.png` |
| 12 | `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/using-remote-registry/admin-all-partitions-in-a-single-server.md` | `assets/attachments/21037149/21331970.png` |
| 13 | `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/using-remote-registry/admin-config-and-governance-partitions-in-a-remote-registry.md` | `assets/attachments/21037149/21331972.png`<br>`assets/attachments/21037149/21332021.png`<br>`assets/attachments/21037149/21332022.png` |
| 14 | `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/using-remote-registry/admin-config-and-governance-partitions-in-separate-nodes.md` | `assets/attachments/126562675/126562676.png` |
| 15 | `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/using-remote-registry/admin-governance-partition-in-a-remote-registry.md` | `assets/attachments/126562673/126562674.png` |
| 16 | `install-and-setup/setup/setting-up-proxy-server-and-the-load-balancer/adding-a-custom-proxy-path.md` | `assets/attachments/126562770/126562773.png` |
| 17 | `install-and-setup/setup/single-node/deploying-api-manager-using-single-node-instances.md` | `assets/attachments/103334465/103334466.png`<br>`assets/attachments/103334465/103334467.png` |

## Other missing images (3) — needs a decision, not just a fact

These are not Confluence-shaped paths. The pages themselves (and the same broken reference) exist
unchanged in the pre-migration `wso2/docs-apim` `3.1.0` branch, so the loss predates this repo —
but unlike the Confluence attachments, real replacement files exist under later versions:

| Page | Broken image | Exists elsewhere? |
|---|---|---|
| `develop/wso2-admin-services.md` | `assets/img/develop/discover-admin-services.png` | Present in `3.0.0` and every `3.2.0+` version — `3.1.0` is the only gap in the sequence. Likely a genuine like-for-like copy candidate (generic admin-console screenshot, unlikely to have changed between 3.1 and 3.2). |
| `develop/extending-api-manager/extending-workflows/configuring-workflows-for-tenants.md` | `assets/img/learn/application-creation-pending-request.png` | Missing in `3.0.0` **and** `3.1.0`, present from `3.2.0` onward — the screenshot may never have existed for this version, or the feature's screenshot was added later. |
| `learn/api-security/oauth2/grant-types/kerberos-oauth2-grant.md` | `assets/img/learn/learnoauth-sp-clientid-clientsecret.png` | Does not exist anywhere in this repo, any version. Fully unrecoverable — no copy candidate. |

Copying an image from a different version's docs is a content decision (it shows a later-version
UI on an older-version page), not a mechanical fix — left for the user to decide rather than
applied automatically.
