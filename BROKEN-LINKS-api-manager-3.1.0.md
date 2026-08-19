# Broken links and images — `api-manager/3.1.0`

**146 findings** across 399 pages. **0** have an exact or high-confidence mechanical fix; **114** need a decision.

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
| `gone` | No target anywhere | 114 | Was it dropped, missed, or merged? |
| `partial` | Broken link inside an included partial | 0 | Resolves against the includer's url, not the partial's |

## `anchor` — Missing anchor

The page resolves but the `#fragment` matches no heading, so the reader lands at the top instead of the section. Usually the heading was reworded. Open the target, find the heading that was meant, and use its current slug.

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

| Page | Broken target | Note |
|---|---|---|
| `api-manager/3.1.0/administer/logging-and-monitoring/monitoring/monitoring-tcp-based-messages.md` | `_Message_Monitoring_with_TCPMon_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/administer/logging-and-monitoring/monitoring/monitoring-tcp-based-messages.md` | `../../../assets/attachments/45946410/46206514.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/administer/logging-and-monitoring/monitoring/monitoring-tcp-based-messages.md` | `../../../assets/attachments/45946410/46206513.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/administer/logging-and-monitoring/monitoring/monitoring-tcp-based-messages.md` | `../../../assets/attachments/45946410/46206512.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/administer/managing-users-and-roles/managing-permissions.md` | `../../../../administer/product-administration/monitoring/monitoring-performance-statistics` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/administer/managing-users-and-roles/managing-user-roles.md` | `../../administer/product-administration/managing-users-and-roles/managing-user-roles/#update-before-the-first-startup-recommended` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/administer/managing-users-and-roles/managing-user-stores/configure-primary-user-store/configuring-a-read-only-ldap-user-store.md` | `properties-used-in-a-read-only-ldap-user-store-managers` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/administer/managing-users-and-roles/managing-user-stores/understanding-the-user-realm.md` | `../../../assets/attachments/126562314/126562315.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/administer/multitenancy/adding-new-tenants.md` | `../../assets/attachments/126562777/126562778.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/administer/multitenancy/adding-new-tenants.md` | `../../assets/attachments/126562777/126562781.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/administer/multitenancy/adding-new-tenants.md` | `../../assets/attachments/126562777/126562782.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/develop/customizations/adding-a-user-signup-workflow.md` | `/learn/consume-api/customizations/adding-a-user-signup-workflow/#configuring-the-business-process-server` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/develop/customizations/adding-a-user-signup-workflow.md` | `/learn/consume-api/customizations/adding-a-user-signup-workflow/#configuring-the-enterprise-integrator` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/develop/customizations/customizing-the-developer-portal/customize-api-listing/categorizing-and-grouping-apis/api-category-based-grouping.md` | `../../../../../learn/consume-api/customizations/customizing-the-developer-portal/customize-api-listing/categorizing-and-grouping-apis/api-category-based-grouping/#add-an-api-category-using-the-admin-portal-ui` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/develop/customizations/customizing-the-developer-portal/customize-api-listing/categorizing-and-grouping-apis/api-category-based-grouping.md` | `../../../../../learn/consume-api/customizations/customizing-the-developer-portal/customize-api-listing/categorizing-and-grouping-apis/api-category-based-grouping/#add-an-api-category-using-the-admin-rest-api` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/develop/customizations/customizing-the-developer-portal/overriding-developer-portal-theme.md` | `../../../assets/attachments/learn/sample-theme.zip` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/develop/extending-api-manager/extending-gateway/writing-custom-handlers.md` | `../../../extensions/adding-mediation-extensions` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/develop/extending-api-manager/extending-gateway/writing-custom-handlers.md` | `../../../analytics/analyzing-the-log-overview` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/develop/extending-api-manager/extending-gateway/writing-custom-handlers.md` | `../../../extensions/adding-mediation-extensions` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/develop/extending-api-manager/extending-key-management/extending-key-validation.md` | `_Extending_Scope_Validation_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/develop/extending-api-manager/extending-workflows/configuring-workflows-for-tenants.md` | `../../../assets/img/learn/application-creation-pending-request.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/develop/product-apis/getting-started/guide-devportal-v0.16.md` | `../../../develop/product-apis/devportal-apis/devportal-v1/guide/` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/develop/product-apis/getting-started/guide-publisher-v0.16.md` | `../../../develop/product-apis/publisher-apis/publisher-v1/guide/` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/develop/wso2-admin-services.md` | `../assets/attachments/develop/org.wso2.carbon.sample.admin.service.invoker.zip` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/getting-started/overview.md` | `../assets/attachments/103327648/126556775.png` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/install/installing-the-product/installing-the-binary/installing-as-a-linux-service.md` | `../../../../install-and-setup/ProductCompatibility` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/install/installing-the-product/installing-the-binary/installing-as-a-windows-service.md` | `../../../../install-and-setup/ProductCompatibility` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/install/installing-the-product/installing-the-binary/installing-as-a-windows-service.md` | `../../../../administer/product-security/General/logins-and-passwords/admin-carbon-secure-vault-implementation` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/install/installing-the-product/installing-the-binary/installing-on-linux-or-os-x.md` | `../../../../install-and-setup/ProductCompatibility` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/install/installing-the-product/installing-the-binary/installing-on-solaris.md` | `../../../../install-and-setup/ProductCompatibility` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/install/installing-the-product/installing-the-binary/installing-on-solaris.md` | `../../../../administer/product-security/General/logins-and-passwords/admin-carbon-secure-vault-implementation` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/deployment-best-practices/production-deployment-guidelines.md` | `../../../install-and-setup/deploying-wso2-api-manager/distributed-deployment/product-profiles
/#product-profiles` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/distributed-deployment/configure-apim-analytics/configuring-database-and-the-file-system-state-persistence.md` | `_Configuring_Datasources_` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/distributed-deployment/configuring-the-gateway-in-a-distributed-environment-with-rsync.md` | `../distributed-deployment-of-the-gateway/` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/distributed-deployment/configuring-the-gateway-in-a-distributed-environment-with-rsync.md` | `../../configuring-rsync-for-deployment-synchronization/` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/distributed-deployment/configuring-the-gateway-in-a-distributed-environment-with-rsync.md` | `../working-with-hazelcast-clustering/` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/distributed-deployment/configuring-wso2-identity-server-as-a-key-manager.md` | `../../../install-and-setup/ProductCompatibility/#compatible-wso2-identity-server-as-the-key-managers` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/distributed-deployment/configuring-wso2-identity-server-as-a-key-manager.md` | `../../../administer/product-security/General/UsingAsymmetricEncryption/admin-creating-new-keystores/#step-3-importing-certificates-to-the-truststore` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/security/configuring-transport-level-security.md` | `../../../assets/attachments/TestSSLServer.jar` | `no file of this name exists anywhere under the docs root` |
| `api-manager/3.1.0/install-and-setup/setup/security/logins-and-passwords/maintaining-logins-and-passwords.md` | `../../../../learn/consume-api/customizations/log-in-to-the-api-store-using-social-media/` | `no file of this name exists anywhere under the docs root` |

_…and 74 more. Full list in the JSON sidecar._

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
