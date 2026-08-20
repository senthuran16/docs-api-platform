# Unrecoverable images and attachments — API Manager 3.2.0

_Generated 2026-08-19 from `BROKEN-LINKS-api-manager-3.2.0.json`._

**41 references** to **40 distinct files** across **19 pages** point at files that do not exist:
39 references to 39 missing images, and 2 references to a single missing attachment.

## Why these are listed rather than fixed

The link address in each case is correct — the *file* is absent. So the fix is to supply
the file, never to edit the link. The broken reference is deliberately left in place: it is
the only record that something is meant to be shown at that spot.

## Where they were looked for

Each file was searched for in all of the following before being called unrecoverable:

| Source | Result |
|---|---|
| `en/docs/api-manager/3.2.0/` (this version) | not found |
| Every other version in this repo (3.0.0 … 4.7.0) | not found |
| `wso2/docs-apim` branch `3.2.0` | not found |
| `wso2/docs-apim` branches `3.1.0`, `4.0.0`, `master` (spot-checked) | not found |

The numeric filenames (`126562631/126562632.png`) are Confluence attachment IDs from the
pre-migration wiki. These references were already broken on the old site — the migration
into this repository did not cause them, and re-running the migration will not recover them.

A separate set of 11 attachments **was** recoverable from `wso2/docs-apim` branch `3.2.0`
and has already been restored; those are not listed here.

## What resolving these needs

- **Images** — a fresh screenshot taken against a running WSO2 API Manager 3.2.0, matching
  the step described in the surrounding text (quoted below for each one).
- **Attachments** — the original artifact from whoever published it.

Re-run `report_links.py --scope api-manager/3.2.0` after adding any file; the finding should
disappear on its own. If it does not, the path is wrong rather than the file being missing.

## Downloadable attachments

- **`assets/attachments/administer/wso2is-km-connector-1.0.16_ga.zip`**
  - referenced by `administer/key-managers/configure-wso2is-connector.md` line 83, under "Step 1 - Configure WSO2 IS"
  - link text: - [WSO2 IS Connector for the WSO2 API-M GA release](../../assets/attachments/administer/wso2is-km-connector-1.0.16_ga.zip).
- **`assets/attachments/administer/wso2is-km-connector-1.0.16_ga.zip`**
  - referenced by `install-and-setup/setup/distributed-deployment/configuring-wso2-identity-server-as-a-key-manager.md` line 151, under "Step 4 - Configure WSO2 IS with WSO2 API-M"
  - link text: - [WSO2 IS Connector for the WSO2 API-M GA release](../../../assets/attachments/administer/wso2is-km-connector-1.0.16_ga.zip).

## Missing images, by page

### `administer/logging-and-monitoring/monitoring/monitoring-tcp-based-messages.md`

| Line | Missing file | Section | What the surrounding text says |
|---|---|---|---|
| 82 | `attachments/45946410/46206514.png` | Sending Requests for Web Services | TCPMon can also be used as a request sender for Web services. The request SOAP message can be pasted on the send screen and sent directly to the serve… |
| 89 | `attachments/45946410/46206513.png` | As a Proxy | TCPMon can act as a proxy. To start it in proxy mode, select the Proxy option. When acting as a proxy, TCPMon only needs the listener port to be confi… |
| 96 | `attachments/45946410/46206512.png` | Advanced Settings | TCPMon can simulate a slow connection, in which case the delay and the bytes to be dropped can be configured. This is useful when testing Web services… |

### `administer/managing-users-and-roles/managing-user-stores/understanding-the-user-realm.md`

| Line | Missing file | Section | What the surrounding text says |
|---|---|---|---|
| 10 | `attachments/126562314/126562315.png` | Understanding the User Realm | The following diagram illustrates the required configurations and repositories: |

### `administer/multitenancy/adding-new-tenants.md`

| Line | Missing file | Section | What the surrounding text says |
|---|---|---|---|
| 14 | `attachments/126562777/126562778.png` | Adding tenants using the management console | 1.  Click **Add New Tenant** in the **Configure** tab of your product's management console. |
| 29 | `attachments/126562777/126562781.png` | Adding tenants using the management console | 3.  After saving, the newly added tenant appears in the **Tenants List** page as shown below. Click **View Tenants** in the **Configure** tab of the m… |
| 86 | `attachments/126562777/126562782.png` | Managing tenants using Admin Services | This assumes that you are running the SOAP UI client from the same machine as the product instance. Note that there are several operations shown in th… |

### `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/admin-searching-the-registry.md`

| Line | Missing file | Section | What the surrounding text says |
|---|---|---|---|
| 6 | `attachments/126562657/126562660.png` | Searching the Registry | 1.  Log in to the product's management console a nd select **Search -&gt; Metadata** under the **Registry** menu. |
| 8 | `attachments/126562657/126562659.png` | Searching the Registry | 2.  The **Search** page opens . |
| 15 | `attachments/126562657/126562658.png` | Searching the Registry | Created/updated dates must be in MM/DD/YYYY format. Alternatively, you can pick it from the calendar interface provided. |

### `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/adding-a-resource.md`

| Line | Missing file | Section | What the surrounding text says |
|---|---|---|---|
| 9 | `attachments/126562631/126562638.png` | Adding a Resource | 1. To add a new resource, click on the *Add Resource* link. |
| 20 | `attachments/126562631/126562637.png` | Adding a Resource | -   **[Create custom content](#custom-content-creation)** |
| 33 | `attachments/126562631/126562635.png` | Uploading Content from File | 2. Click *Add* once the information is added as shown in the example below. |
| 46 | `attachments/126562631/126562633.png` | Importing Content from URL | 2. Click *Add* once the information is added. |
| 59 | `attachments/126562631/126562632.png` | Text Content Creation | 2. Click *Add* once the information is added. |
| 65 | `attachments/126562631/126562636.png` | Custom Content Creation | 1. If this method was selected, choose the *Media Type* from the drop-down menu and click *Create Content* . |

### `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/editing-collections-using-the-entries-panel.md`

| Line | Missing file | Section | What the surrounding text says |
|---|---|---|---|
| 5 | `attachments/126562643/126562644.png` | Editing collections using the Entries panel | If you select a collection, in its detailed view, you can see the Entries panel with details of child collections and resources it has. It provides a … |

### `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/link-creation.md`

| Line | Missing file | Section | What the surrounding text says |
|---|---|---|---|
| 7 | `attachments/126562639/126562641.png` | Link Creation | 1. Symbolic links and Remote links can be created in a similar way to adding a normal resource. To add a link, click *Create Link* in the *Entries* pa… |
| 15 | `attachments/126562639/126562640.png` | A Symbolic Link | When adding a Symbolic link, enter a name for the link and the path of an existing resource or collection which is being linked. It creates a link to … |
| 21 | `attachments/126562639/126562642.png` | A Remote Link | You can mount a collection in a remotely-deployed registry instance to your registry instance by adding a Remote link. Provide a name for the Remote l… |

### `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/metadata.md`

| Line | Missing file | Section | What the surrounding text says |
|---|---|---|---|
| 17 | `attachments/22185146/22514191.png` | Metadata | For example, |
| 23 | `attachments/126562605/126562606.png` | Creating a checkpoint | T o create a checkpoint, click on the **Create Checkpoint** link: |
| 34 | `attachments/126562605/126562611.png` | Viewing Versions | To view the resource versions, click on the **View versions** link: |
| 38 | `attachments/22185146/22514195.png` | Viewing Versions | It opens the versions. For example, |

### `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/properties.md`

| Line | Missing file | Section | What the surrounding text says |
|---|---|---|---|
| 6 | `attachments/126562613/126562618.png` | Properties | 1.  To add a property, click on th e **Add New Property** link in the **Properties** panel . |
| 8 | `attachments/126562613/126562617.png` | Properties | 2.  E nter a unique name for the property and a value and click **Add . |

### `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/managing-the-registry/role-permissions.md`

| Line | Missing file | Section | What the surrounding text says |
|---|---|---|---|
| 8 | `attachments/126562645/126562646.png` | Adding new role permissions | 1.  In the **New Role Permissions** section, select a role from the drop-down list. This list is populated by all user roles configured in the system. |
| 24 | `attachments/126562645/126562647.png` | Adding new role permissions | 3.  Select whether to allow the action or deny and click **Add Permission** . For example |
| 33 | `attachments/126562645/126562648.png` | Adding new role permissions | 4.  The new permission appears in the list. |

### `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/using-remote-registry/admin-all-partitions-in-a-single-server.md`

| Line | Missing file | Section | What the surrounding text says |
|---|---|---|---|
| 5 | `attachments/21037149/21331970.png` | Strategy 1: Local Registry | — |

### `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/using-remote-registry/admin-config-and-governance-partitions-in-a-remote-registry.md`

| Line | Missing file | Section | What the surrounding text says |
|---|---|---|---|
| 5 | `attachments/21037149/21331972.png` | Config and Governance Partitions in a Remote Registry | In this deployment strategy, the configuration and governance spaces are shared among instances of a group/cluster. For example, two WSO2 Application … |
| 201 | `attachments/21037149/21332021.png` | Configuring server nodes | 3. Start both servers and note the log entries that indicate successful mounting to the remote Governance Registry instance. For example, |
| 204 | `attachments/21037149/21332022.png` | Configuring server nodes | 4. Navigate to the registry browser in the Carbon server's management console and note the config and governance partitions indicating successful moun… |

### `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/using-remote-registry/admin-config-and-governance-partitions-in-separate-nodes.md`

| Line | Missing file | Section | What the surrounding text says |
|---|---|---|---|
| 5 | `attachments/126562675/126562676.png` | Config and Governance Partitions in Separate Nodes | In this deployment strategy, let's assume 2 clusters of Carbon-based product Foo and Carbon-based product Bar that share a governance registry space b… |

### `install-and-setup/setup/setting-up-databases/working-with-the-resgistry/using-remote-registry/admin-governance-partition-in-a-remote-registry.md`

| Line | Missing file | Section | What the surrounding text says |
|---|---|---|---|
| 5 | `attachments/126562673/126562674.png` | Governance Partition in a Remote Registry | In this deployment strategy, only the governance partition is shared among instances of a group/cluster. For example, a WSO2 Application Server instan… |

### `install-and-setup/setup/single-node/deploying-api-manager-using-single-node-instances.md`

| Line | Missing file | Section | What the surrounding text says |
|---|---|---|---|
| 27 | `attachments/103334465/103334466.png` | Single node deployment | In this setup, API traffic is served by one all-in-one instance of WSO2 API Manager. |
| 47 | `attachments/103334465/103334467.png` | — | In this setup, API traffic is served by two single node (all-in-one) instances of WSO2 API Manager. |

### `learn/api-security/oauth2/grant-types/kerberos-oauth2-grant.md`

| Line | Missing file | Section | What the surrounding text says |
|---|---|---|---|
| 128 | `img/learn/learnoauth-sp-clientid-clientsecret.png` | Configuring Kerberos Grant using IS as KM | service provider. |

### `learn/rate-limiting/adding-new-throttling-policies.md`

| Line | Missing file | Section | What the surrounding text says |
|---|---|---|---|
| 78 | `img/learn/anew-jwt-condition-regex.png` | Adding a new advanced throttling policy | [![Add advanced policy page](../../assets/img/learn/new-header-condition-regex.png)](../../assets/img/learn/new-header-condition-regex.png) |

