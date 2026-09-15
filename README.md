# api-manager-router

Experiment: one routing rule for infra instead of one per version.

Today, infra has to configure a separate gateway rule for every single
`apim-<version>` deployment. This is a single, tiny nginx deployment that
sits in front of all of them - infra points ONE rule (`/api-manager`) at
this deployment's URL, and this file decides, per version, which real
deployment to invisibly forward to (`proxy_pass`, server-side - the reader's
address bar never sees the raw Choreo URL underneath).

Adding a new API Manager version later means editing `nginx.conf` here and
redeploying this one component - infra's gateway rule never changes again.

This is purely additive: it doesn't modify, replace, or depend on any
existing deployment. Each location block just points at that version's
already-live, unmodified Choreo URL.

## Known gaps in this first pass

- `4.0.0` / `4.1.0` / `4.2.0` are not yet in `nginx.conf` - those
  deployments are still failing to build independently of this router.
- The default-version manifest block (`/api-manager/product-nav-manifest.json`)
  has to be updated by hand whenever the configured default version changes.
- Backend URLs here are static, resolved once at container start. If a
  version's Choreo URL ever changes, this file needs updating and
  redeploying, same as `SHARED_BASE` in `docs-shared`'s `theme.js`.
