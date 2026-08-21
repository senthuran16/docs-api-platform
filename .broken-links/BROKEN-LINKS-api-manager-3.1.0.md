# Broken links and images — `api-manager/3.1.0`

**115 findings** across 399 pages. **0** have an exact or high-confidence mechanical fix; **83** need a decision.

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
| `anchor` | Missing anchor | 32 | The heading was reworded — which one now? |
| `gone` | No target anywhere | 83 | Was it dropped, missed, or merged? |
| `partial` | Broken link inside an included partial | 0 | Resolves against the includer's url, not the partial's |

## `anchor` — Missing anchor

The page resolves but the `#fragment` matches no heading, so the reader lands at the top instead of the section. Usually the heading was reworded. Open the target, find the heading that was meant, and use its current slug.

**All 32 rows below have been individually investigated and confirmed unfixable — do not re-investigate.** None of them name a real heading anywhere on the target page:

- **`token-api.md` `#option1-*`/`#option2-*` (5)**, the `xml`/`json`/`regex`-threat-protection pages' hex-hash anchors (11), `production-deployment-guidelines.md`'s two hex-hash anchors (2), and `development-of-developer-optimized-apis-sample.md`'s `#curl-mobile*` (4) — all the same pattern: a bullet label ("Request"/"Response"/"Format"/"Example"/"cURL"/"Output"/"Oracle JDK"/"IBM JDK") sitting directly above a code block, never demarcated as a real heading. Lost content, not a renamed heading.
- **`configuring-wso2-identity-server-as-a-key-manager.md` `#Linux-Mac`/`#windows` (2)** — same pattern: OS-tab bullet labels immediately followed by a code block, no heading.
- **`maintaining-logins-and-passwords.md` `#recovering-a-password`/`#login-in-via-multiple-user-attributes-in-developer-portal` (2)** — TOC lists 5 topics, only 3 have matching headings; these two describe content that was never written on this page (a third occurrence of the second anchor, on the "Setting up an e-mail login" row, was a copy-paste mislink and has been fixed to point at the real heading).
- **`monetizing-an-api.md` `#connectID` (2)** — "Connect ID" exists only as **bold text** inside a numbered step, not a heading. Per policy, bold text gets no invented id.
- **`faq.md` `#FAQ-Keystorepassword`/`#FAQ-Step1-...` (2)** — same bold-text-not-heading situation; the referenced text is `**Step 1 - ...**`/mid-paragraph bold, not a `#` heading.
- **`wip/deleted-pages/changing-to-embedded-h2.md` (2)** — this whole page is a raw, unconverted Confluence export (see the `wip`/`deleted-pages` note under `gone` below); every finding on it is a symptom of that, not an individual anchor problem.

| Page | Link | Target file | Missing anchor |
|---|---|---|---|
| `api-manager/3.1.0/develop/product-apis/token-api.md` | `#option1-format` | `api-manager/3.1.0/develop/product-apis/token-api.md` | `option1-format` |
| `api-manager/3.1.0/develop/product-apis/token-api.md` | `#option1-example` | `api-manager/3.1.0/develop/product-apis/token-api.md` | `option1-example` |
| `api-manager/3.1.0/develop/product-apis/token-api.md` | `#option1-response` | `api-manager/3.1.0/develop/product-apis/token-api.md` | `option1-response` |
| `api-manager/3.1.0/develop/product-apis/token-api.md` | `#option2-format` | `api-manager/3.1.0/develop/product-apis/token-api.md` | `option2-format` |
| `api-manager/3.1.0/develop/product-apis/token-api.md` | `#option2-example` | `api-manager/3.1.0/develop/product-apis/token-api.md` | `option2-example` |
| `api-manager/3.1.0/install-and-setup/setup/deployment-best-practices/production-deployment-guidelines.md` | `#cc08b6aaf09742a7b6389db09f3e3b36` | `api-manager/3.1.0/install-and-setup/setup/deployment-best-practices/production-deployment-guidelines.md` | `cc08b6aaf09742a7b6389db09f3e3b36` |
| `api-manager/3.1.0/install-and-setup/setup/deployment-best-practices/production-deployment-guidelines.md` | `#944559bca1c0464fa8a12ec742f9cd07` | `api-manager/3.1.0/install-and-setup/setup/deployment-best-practices/production-deployment-guidelines.md` | `944559bca1c0464fa8a12ec742f9cd07` |
| `api-manager/3.1.0/install-and-setup/setup/distributed-deployment/configuring-wso2-identity-server-as-a-key-manager.md` | `#Linux-Mac` | `api-manager/3.1.0/install-and-setup/setup/distributed-deployment/configuring-wso2-identity-server-as-a-key-manager.md` | `Linux-Mac` |
| `api-manager/3.1.0/install-and-setup/setup/distributed-deployment/configuring-wso2-identity-server-as-a-key-manager.md` | `#windows` | `api-manager/3.1.0/install-and-setup/setup/distributed-deployment/configuring-wso2-identity-server-as-a-key-manager.md` | `windows` |
| `api-manager/3.1.0/install-and-setup/setup/security/logins-and-passwords/maintaining-logins-and-passwords.md` | `#recovering-a-password` | `api-manager/3.1.0/install-and-setup/setup/security/logins-and-passwords/maintaining-logins-and-passwords.md` | `recovering-a-password` |
| `api-manager/3.1.0/install-and-setup/setup/security/logins-and-passwords/maintaining-logins-and-passwords.md` | `#login-in-via-multiple-user-attributes-in-developer-portal` | `api-manager/3.1.0/install-and-setup/setup/security/logins-and-passwords/maintaining-logins-and-passwords.md` | `login-in-via-multiple-user-attributes-in-developer-portal` |
| `api-manager/3.1.0/learn/api-monetization/monetizing-an-api.md` | `#connectID` | `api-manager/3.1.0/learn/api-monetization/monetizing-an-api.md` | `connectID` |
| `api-manager/3.1.0/learn/api-monetization/monetizing-an-api.md` | `#connectID` | `api-manager/3.1.0/learn/api-monetization/monetizing-an-api.md` | `connectID` |
| `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/json-threat-protection-for-api-gateway.md` | `#2fabe5e92ef64a3a999bb756d894221e` | `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/json-threat-protection-for-api-gateway.md` | `2fabe5e92ef64a3a999bb756d894221e` |
| `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/json-threat-protection-for-api-gateway.md` | `#6da49ce3d2cf4091a885d78334d2513e` | `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/json-threat-protection-for-api-gateway.md` | `6da49ce3d2cf4091a885d78334d2513e` |
| `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/regular-expression-threat-protection-for-api-gateway.md` | `#10673ba9a16d49dcaf1b6a073de9cf4d` | `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/regular-expression-threat-protection-for-api-gateway.md` | `10673ba9a16d49dcaf1b6a073de9cf4d` |
| `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/regular-expression-threat-protection-for-api-gateway.md` | `#90b129a29c8c4b74869eb1676bb3f705` | `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/regular-expression-threat-protection-for-api-gateway.md` | `90b129a29c8c4b74869eb1676bb3f705` |
| `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#b95bd611fb2144d0940b193f34addf5b` | `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `b95bd611fb2144d0940b193f34addf5b` |
| `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#70c795c618f04f2cb9983858b263298d` | `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `70c795c618f04f2cb9983858b263298d` |
| `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#389c50828aa24292b0657e037c09c635` | `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `389c50828aa24292b0657e037c09c635` |
| `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#159d32ca825c41a480037880ce2e6413` | `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `159d32ca825c41a480037880ce2e6413` |
| `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#45b87273c80b44ffb18a3f8fe4f5b8f6` | `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `45b87273c80b44ffb18a3f8fe4f5b8f6` |
| `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#194a5a4652e94e609d80ba175c16b449` | `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `194a5a4652e94e609d80ba175c16b449` |
| `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `#db80409dd4d941dc972837213bc340e5` | `api-manager/3.1.0/learn/api-security/threat-protection/gateway-threat-protectors/xml-threat-protection-for-api-gateway.md` | `db80409dd4d941dc972837213bc340e5` |
| `api-manager/3.1.0/reference/faq.md` | `#FAQ-Keystorepassword` | `api-manager/3.1.0/reference/faq.md` | `FAQ-Keystorepassword` |
| `api-manager/3.1.0/reference/faq.md` | `#FAQ-Step1-CreateaselfsignedJavaKeyStorefileandincludeyourdomainastheCN` | `api-manager/3.1.0/reference/faq.md` | `FAQ-Step1-CreateaselfsignedJavaKeyStorefileandincludeyourdomainastheCN` |
| `api-manager/3.1.0/reference/samples/api-development-sample/development-of-developer-optimized-apis-sample.md` | `#curl-mobile` | `api-manager/3.1.0/reference/samples/api-development-sample/development-of-developer-optimized-apis-sample.md` | `curl-mobile` |
| `api-manager/3.1.0/reference/samples/api-development-sample/development-of-developer-optimized-apis-sample.md` | `#curl-mobile-output` | `api-manager/3.1.0/reference/samples/api-development-sample/development-of-developer-optimized-apis-sample.md` | `curl-mobile-output` |
| `api-manager/3.1.0/reference/samples/api-development-sample/development-of-developer-optimized-apis-sample.md` | `#curl-mobile` | `api-manager/3.1.0/reference/samples/api-development-sample/development-of-developer-optimized-apis-sample.md` | `curl-mobile` |
| `api-manager/3.1.0/reference/samples/api-development-sample/development-of-developer-optimized-apis-sample.md` | `#curl-mobile-output` | `api-manager/3.1.0/reference/samples/api-development-sample/development-of-developer-optimized-apis-sample.md` | `curl-mobile-output` |
| `api-manager/3.1.0/wip/deleted-pages/changing-to-embedded-h2.md` | `#ChangingtoEmbeddedH2-Changingthedefaultdatabase` | `api-manager/3.1.0/wip/deleted-pages/changing-to-embedded-h2.md` | `ChangingtoEmbeddedH2-Changingthedefaultdatabase` |
| `api-manager/3.1.0/wip/deleted-pages/changing-to-embedded-h2.md` | `#changing-the-default-wso295carbon95db-datasource` | `api-manager/3.1.0/wip/deleted-pages/changing-to-embedded-h2.md` | `changing-the-default-wso295carbon95db-datasource` |

## `gone` — No target anywhere

No file of this name exists anywhere under the docs root, so there is nothing to point at. Each needs a decision: was the page meant to be migrated and missed, was it deliberately dropped (then the link and its sentence should go), or was it merged into another page (then link there)? **Do not guess these.**

**All 83 rows below have been individually investigated. Do not re-investigate — every row falls into one of these settled buckets:**

- **39 rows are Confluence attachment images** (`assets/attachments/<pageId>/<attachmentId>.png`) — see `UNRECOVERABLE-IMAGES-api-manager-3.1.0.md`. No recovery path exists in this repo or the pre-migration `wso2/docs-apim` repo.
- **21 rows are on `wip/need-to-update/create-and-publish-an-api.md`** (`_Key_Concepts_`-style underscore placeholders) — this page is a raw, unconverted Confluence export and needs a content rewrite, not link patching.
- **3 underscore-placeholder rows are genuinely dropped content**: `monitoring-tcp-based-messages.md`'s "Message Monitoring with TCPMon", `extending-key-validation.md`'s "Skipping Role Validation for Scopes", `configuring-database-and-the-file-system-state-persistence.md`'s "Configuring Datasources" — confirmed by reading the target page and finding no matching heading anywhere.
- **6 rows are binary/zip attachments that don't exist for this version**: `sample-theme.zip`, `org.wso2.carbon.sample.admin.service.invoker.zip`, `kerberos-grant-1.0.0.jar`, `saml2-assertion-creator.zip` (all exist under `4.1.0`/`4.6.0` but not `3.1.0` or `3.2.0` — copying a compiled sample artifact across major versions isn't safe to do without being able to verify it still matches this version's instructions, unlike a UI screenshot), `TestSSLServer.jar` (only a differently-packaged `.zip` exists in later versions, and the page's instructions explicitly run `java -jar TestSSLServer.jar` — a `.zip` may not be a drop-in replacement), `org.wso2.apim.monetization.impl-1.1.1.jar` (absent from every version).
- **`writing-custom-handlers.md`'s `adding-mediation-extensions` (x2) and `analyzing-the-log-overview`** — neither page exists in this repo (any version) or the pre-migration repo's `3.1.0` branch. Confirmed dropped content.
- **`configuring-the-gateway-in-a-distributed-environment-with-rsync.md`'s 3 rows** (`distributed-deployment-of-the-gateway`, `configuring-rsync-for-deployment-synchronization`, `working-with-hazelcast-clustering`) **and `configuring-an-active-active-deployment.md`'s 2 rows** (same `configuring-rsync-for-deployment-synchronization` target) — none of these pages exist in this version, any other version, or the pre-migration repo, **except** `distributed-deployment-of-the-gateway.md` which exists only in `3.0.0`. Genuinely ambiguous whether this is a 3.1.0-specific dropped-content gap or an intentional removal — left rather than guessed at a cross-version link.
- **`managing-permissions.md`'s `monitoring-performance-statistics`** — exists only in `3.0.0`, no explicit textual evidence (unlike the `about-this-release.md` case elsewhere on this page) that a cross-version link was intended. Left rather than guessed.
- **`adding-an-api-state-change-workflow.md`'s `admin-managing-users-roles-and-permissions`** — the old single page has since been split into three (`managing-users.md`, `managing-user-roles.md`, `introduction-to-user-management.md`); the link text ("managing users and roles") doesn't clearly pick one. Left rather than guessed.
- **`wip/deleted-pages/changing-to-embedded-h2.md`'s 2 rows** — same raw-Confluence-export situation as the other `wip/` page; needs a content rewrite.

| Page | Broken target | Note |
|---|---|---|
| `api-manager/3.1.0/administer/logging-and-monitoring/monitoring/monitoring-tcp-based-messages.md` | `_Message_Monitoring_with_TCPMon_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/administer/logging-and-monitoring/monitoring/monitoring-tcp-based-messages.md` | `../../../assets/attachments/45946410/46206514.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/administer/logging-and-monitoring/monitoring/monitoring-tcp-based-messages.md` | `../../../assets/attachments/45946410/46206513.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/administer/logging-and-monitoring/monitoring/monitoring-tcp-based-messages.md` | `../../../assets/attachments/45946410/46206512.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/administer/managing-users-and-roles/managing-permissions.md` | `../../../../administer/product-administration/monitoring/monitoring-performance-statistics` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/administer/managing-users-and-roles/managing-user-stores/understanding-the-user-realm.md` | `../../../assets/attachments/126562314/126562315.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/administer/multitenancy/adding-new-tenants.md` | `../../assets/attachments/126562777/126562778.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/administer/multitenancy/adding-new-tenants.md` | `../../assets/attachments/126562777/126562781.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/administer/multitenancy/adding-new-tenants.md` | `../../assets/attachments/126562777/126562782.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/develop/customizations/customizing-the-developer-portal/overriding-developer-portal-theme.md` | `../../../assets/attachments/learn/sample-theme.zip` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/develop/extending-api-manager/extending-gateway/writing-custom-handlers.md` | `../../../extensions/adding-mediation-extensions` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/develop/extending-api-manager/extending-gateway/writing-custom-handlers.md` | `../../../analytics/analyzing-the-log-overview` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/develop/extending-api-manager/extending-gateway/writing-custom-handlers.md` | `../../../extensions/adding-mediation-extensions` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/develop/extending-api-manager/extending-key-management/extending-key-validation.md` | `_Extending_Scope_Validation_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/develop/extending-api-manager/extending-workflows/configuring-workflows-for-tenants.md` | `../../../assets/img/learn/application-creation-pending-request.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/develop/wso2-admin-services.md` | `../assets/attachments/develop/org.wso2.carbon.sample.admin.service.invoker.zip` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/getting-started/overview.md` | `../assets/attachments/103327648/126556775.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/distributed-deployment/configure-apim-analytics/configuring-database-and-the-file-system-state-persistence.md` | `_Configuring_Datasources_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/distributed-deployment/configuring-the-gateway-in-a-distributed-environment-with-rsync.md` | `../distributed-deployment-of-the-gateway/` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/distributed-deployment/configuring-the-gateway-in-a-distributed-environment-with-rsync.md` | `../../configuring-rsync-for-deployment-synchronization/` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/distributed-deployment/configuring-the-gateway-in-a-distributed-environment-with-rsync.md` | `../working-with-hazelcast-clustering/` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/security/configuring-transport-level-security.md` | `../../../assets/attachments/TestSSLServer.jar` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/admin-searching-the-registry.md` | `../../../../assets/attachments/126562657/126562660.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/admin-searching-the-registry.md` | `../../../../assets/attachments/126562657/126562659.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/admin-searching-the-registry.md` | `../../../../assets/attachments/126562657/126562658.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `../../../../../assets/attachments/126562631/126562638.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `../../../../../assets/attachments/126562631/126562637.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `../../../../../assets/attachments/126562631/126562635.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `../../../../../assets/attachments/126562631/126562633.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `../../../../../assets/attachments/126562631/126562632.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md` | `../../../../../assets/attachments/126562631/126562636.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/editing-collections-using-the-entries-panel.md` | `../../../../../assets/attachments/126562643/126562644.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/link-creation.md` | `../../../../../assets/attachments/126562639/126562641.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/link-creation.md` | `../../../../../assets/attachments/126562639/126562640.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/link-creation.md` | `../../../../../assets/attachments/126562639/126562642.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/metadata.md` | `../../../../../assets/attachments/22185146/22514191.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/metadata.md` | `../../../../../assets/attachments/126562605/126562606.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/metadata.md` | `../../../../../assets/attachments/126562605/126562611.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/metadata.md` | `../../../../../assets/attachments/22185146/22514195.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/properties.md` | `../../../../../assets/attachments/126562613/126562618.png` | `no file of this name exists anywhere under the docs root` |

_…and 43 more. Full list in the JSON sidecar._

---

## Prompt for an AI coding agent

Paste the block below to an agent working in the repo root. It is deliberately scoped to the four groups with a defensible mechanical answer. `templated`, `stale`, `anchor` and `gone` need judgement and are left out on purpose.

Alternatively, run `fix_links.py --tier <group>` yourself — same scope, one group at a time, and every rewrite verified against the files on disk before it is written.

````text
You are fixing broken links in the WSO2 API Platform docs, scope: api-manager/3.1.0.

Read the fix plan in `BROKEN-LINKS-api-manager-3.1.0.md` and the machine-readable list in `BROKEN-LINKS-api-manager-3.1.0.json`.

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
