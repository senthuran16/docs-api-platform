# This Is a Template Branch, Not a Deployment

This branch is never deployed anywhere — it's a checkpoint, kept around
purely as a reference for how a version branch gets created for this
product.

## What it is

A branch scoped down to just **one product** (nav trimmed to Overview, Get
Started, and this one product; `docs-shared` wired up; `versioned_sections`
and `redirects.yml` correct) — but still holding *every* version's docs
together, unsplit.

## Why it exists

Creating a real version branch (e.g. `apim-4.6.0`) means two things happen:
1. Scope the branch down to just this one product — the harder, more
   original part: trimming `nav:`, wiring up `docs-shared`, getting
   `versioned_sections`/`redirects.yml` right.
2. Prune down to one version's docs folder, add its Dockerfile pair — the
   easy, mechanical part, repeated once per version.

Doing step 1 once here, then fanning out into every version branch from
this single correctly-configured base, is simpler than repeating step 1
separately for every version.

## Using it to add a new version later

1. Branch from here.
2. Remove every other version's docs folder, keep only the new one.
3. Copy an existing version's `Dockerfile.<version>` +
   `Dockerfile.<version>.dockerignore` pair, renaming the version number
   inside both.
4. Commit as its own version branch (e.g. `apim-4.8.0`).
