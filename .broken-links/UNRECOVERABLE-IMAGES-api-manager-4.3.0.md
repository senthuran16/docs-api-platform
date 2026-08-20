# Unrecoverable images — `api-manager/4.3.0`

18 broken image references, confirmed by manual review, that cannot be fixed by relinking. The
source files were never migrated anywhere this repo's history reaches — a fresh screenshot
against the current product is the only real fix.

## Why these can't be relinked

The path shape (`assets/attachments/<pageId>/<attachmentId>.png`) is Confluence's own attachment
download URL scheme, not a filename anyone chose. That means the image was never given a
readable name — it was carried over as a raw Confluence reference at export time, and the actual
binary was never copied alongside it.

Checked against every version this repo has (4.0.0, 4.1.0, 4.2.0, 4.3.0): **all four carry the
identical broken reference, byte-for-byte.** This content (Registry management, Multitenancy,
single-node deployment) is legacy boilerplate copied forward unchanged at each release, so the
break happened once, upstream of all four versions, and has been mechanically propagated forward
ever since — nobody re-validates unchanged boilerplate pages when cutting a new version.

Also checked the pre-migration `wso2/docs-apim` repo (4.3.0 branch): none of the 14 numeric
attachment folders these images reference exist there. The images were already gone before either
migration this repo's git history can see — the loss predates 4.0.0, which is as far back as this
repo goes.

**No recovery path exists from this repo or its known predecessor.** The only way to fix these is
either a fresh screenshot taken against the current product UI, or someone with access to the
original Confluence space (if it still exists) pulling the attachment from there directly.

## The list

| # | Page | Broken image(s) |
|---|---|---|
| 1 | `en/docs/api-manager/4.3.0/administer/managing-users-and-roles/managing-user-stores/understanding-the-user-realm.md` | `en/docs/api-manager/4.3.0/assets/attachments/126562314/126562315.png` |
| 2 | `en/docs/api-manager/4.3.0/administer/multitenancy/adding-new-tenants.md` | `en/docs/api-manager/4.3.0/assets/attachments/126562777/126562778.png`<br>`en/docs/api-manager/4.3.0/assets/attachments/126562777/126562781.png`<br>`en/docs/api-manager/4.3.0/assets/attachments/126562777/126562782.png` |
| 3 | `en/docs/api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/admin-searching-the-registry.md` | `en/docs/api-manager/4.3.0/assets/attachments/126562657/126562660.png`<br>`en/docs/api-manager/4.3.0/assets/attachments/126562657/126562659.png`<br>`en/docs/api-manager/4.3.0/assets/attachments/126562657/126562658.png` |
| 4 | `en/docs/api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `en/docs/api-manager/4.3.0/assets/attachments/126562631/126562638.png`<br>`en/docs/api-manager/4.3.0/assets/attachments/126562631/126562637.png`<br>`en/docs/api-manager/4.3.0/assets/attachments/126562631/126562635.png`<br>`en/docs/api-manager/4.3.0/assets/attachments/126562631/126562633.png`<br>`en/docs/api-manager/4.3.0/assets/attachments/126562631/126562632.png`<br>`en/docs/api-manager/4.3.0/assets/attachments/126562631/126562636.png` |
| 5 | `en/docs/api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/editing-collections-using-the-entries-panel.md` | `en/docs/api-manager/4.3.0/assets/attachments/126562643/126562644.png` |
| 6 | `en/docs/api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/link-creation.md` | `en/docs/api-manager/4.3.0/assets/attachments/126562639/126562641.png`<br>`en/docs/api-manager/4.3.0/assets/attachments/126562639/126562640.png`<br>`en/docs/api-manager/4.3.0/assets/attachments/126562639/126562642.png` |
| 7 | `en/docs/api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/metadata.md` | `en/docs/api-manager/4.3.0/assets/attachments/22185146/22514191.png`<br>`en/docs/api-manager/4.3.0/assets/attachments/126562605/126562606.png`<br>`en/docs/api-manager/4.3.0/assets/attachments/126562605/126562611.png`<br>`en/docs/api-manager/4.3.0/assets/attachments/22185146/22514195.png` |
| 8 | `en/docs/api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/properties.md` | `en/docs/api-manager/4.3.0/assets/attachments/126562613/126562618.png`<br>`en/docs/api-manager/4.3.0/assets/attachments/126562613/126562617.png` |
| 9 | `en/docs/api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/role-permissions.md` | `en/docs/api-manager/4.3.0/assets/attachments/126562645/126562646.png`<br>`en/docs/api-manager/4.3.0/assets/attachments/126562645/126562647.png`<br>`en/docs/api-manager/4.3.0/assets/attachments/126562645/126562648.png` |
| 10 | `en/docs/api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/using-remote-registry/admin-all-partitions-in-a-single-server.md` | `en/docs/api-manager/4.3.0/assets/attachments/21037149/21331970.png` |
| 11 | `en/docs/api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/using-remote-registry/admin-config-and-governance-partitions-in-a-remote-registry.md` | `en/docs/api-manager/4.3.0/assets/attachments/21037149/21331972.png`<br>`en/docs/api-manager/4.3.0/assets/attachments/21037149/21332021.png`<br>`en/docs/api-manager/4.3.0/assets/attachments/21037149/21332022.png` |
| 12 | `en/docs/api-manager/4.3.0/install-and-setup/setup/single-node/deploying-api-manager-using-single-node-instances.md` | `en/docs/api-manager/4.3.0/assets/attachments/103334465/103334466.png`<br>`en/docs/api-manager/4.3.0/assets/attachments/103334465/103334467.png` |
| 13 | `en/docs/api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/using-remote-registry/admin-config-and-governance-partitions-in-separate-nodes.md` | `en/docs/api-manager/4.3.0/assets/attachments/126562675/126562676.png` |
| 14 | `en/docs/api-manager/4.3.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/using-remote-registry/admin-governance-partition-in-a-remote-registry.md` | `en/docs/api-manager/4.3.0/assets/attachments/126562673/126562674.png` |

Rows 13–14 were listed as "not yet confirmed" in the previous pass. Confirmed now: both references
are byte-for-byte identical across 4.0.0–4.3.0, the same signature as rows 1–12.

## Confirmed separately — same conclusion, different cause

These two pages are missing images too, but the images aren't Confluence attachment references —
they're normal, readable filenames. They still can't be relinked, for a reason specific to each:

| # | Page | Broken image(s) | Why unrecoverable |
|---|---|---|---|
| 15 | `en/docs/api-manager/4.3.0/use-cases/examples/streaming-examples/execution-geo-sample.md` | `en/docs/api-manager/4.3.0/assets/img/streaming/execution-geo-sample/siddhi-app-and-stream.png`<br>`en/docs/api-manager/4.3.0/assets/img/streaming/execution-geo-sample/attribute-values.png` | Same broken reference exists in the 4.0.0 branch of this same page — inherited legacy breakage, like rows 1–14. Checked `wso2/docs-apim` (4.3.0 branch): 404, the folder was never there. |
| 16 | `en/docs/api-manager/4.3.0/streaming/getting-started/monitor-statistics.md` | `en/docs/api-manager/4.3.0/assets/img/streaming/quick-start-guide-101/app-staistics.png`<br>`en/docs/api-manager/4.3.0/assets/img/streaming/quick-start-guide-101/destination.png` | Different cause from the rest of this list: this page's "App statistics" and "Destination statistics" steps don't exist at all in 4.0.0–4.2.0 — the steps and their screenshots were meant to be added new for 4.3.0, and the screenshots were never taken. Checked `wso2/docs-apim` (4.3.0 branch): 404, confirming it's not a copy-over miss either. |

## Not yet confirmed

None remaining from this pass.
