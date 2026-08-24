#!/usr/bin/env python3
"""Collapse en/mkdocs.yml's "API Manager" nav section down to a single
external-link placeholder, in place.

Used for a lean, fast build of this branch's non-APIM content only (see
Dockerfile.no-apim): api-manager/ is excluded from the build context by
Dockerfile.no-apim.dockerignore, so the real nav subtree (hundreds of local
pages per version) has nothing to point at and must be replaced before
`mkdocs build` runs. extra.versioned_sections is left untouched, so the
version dropdown still lists every API Manager version - picking any of them
falls through to the version switcher's cross-deployment redirect (see
en/docs/assets/js/theme.js) straight to the real site.

Uses scoped regex surgery rather than a full YAML parse/dump, for the same
reason as trim-mkdocs-version.py: mkdocs.yml carries custom Python tags a
generic YAML loader can't construct.

Usage: python3 strip-apim-nav.py en/mkdocs.yml
"""
import re
import sys


def read_default_version(text):
    m = re.search(
        r"    API Manager:\n      slug: api-manager\n      default: \"([^\"]+)\"",
        text,
    )
    if not m:
        sys.exit("could not locate extra.versioned_sections.'API Manager'.default in mkdocs.yml")
    return m.group(1)


def read_site_url(text):
    m = re.search(r"^site_url: (\S+)", text, re.M)
    if not m:
        sys.exit("could not locate site_url in mkdocs.yml")
    return m.group(1).rstrip("/")


def strip_nav(text, default_version, site_url):
    m = re.search(r"(\n  - API Manager:\n)(.*?)(?=\n  - API Gateway:\n)", text, re.S)
    if not m:
        sys.exit("could not locate the 'API Manager' nav block in mkdocs.yml")
    stub = (
        f'    - "{default_version}": '
        f'{site_url}/api-manager/{default_version}/get-started/overview/\n'
    )
    return text[: m.start(2)] + stub + text[m.end(2) :]


def main():
    if len(sys.argv) != 2:
        sys.exit(f"usage: {sys.argv[0]} <mkdocs.yml path>")
    path = sys.argv[1]
    text = open(path, encoding="utf-8").read()
    default_version = read_default_version(text)
    site_url = read_site_url(text)
    text = strip_nav(text, default_version, site_url)
    open(path, "w", encoding="utf-8").write(text)
    print(f"mkdocs.yml's API Manager nav collapsed to a {default_version} stub")


if __name__ == "__main__":
    main()
