#!/usr/bin/env python3
"""Trim en/mkdocs.yml down to a single API Manager version, in place.

Keeps only the requested version's nav subtree under "API Manager" so a
single-version image only builds that version's pages. extra.versioned_sections
is left untouched: the version dropdown still lists every version, and
theme.js sends a version not present in this build's nav out to that
version's page on the live site (see the "not built into this image" branch
in theme.js's dropdown change handler).

Uses scoped regex surgery rather than a full YAML parse/dump: mkdocs.yml here
carries custom Python tags (e.g. pymdownx.emoji.to_svg) that a generic YAML
loader can't construct, and the block being edited has fixed, well-known
indentation, so a full parse buys nothing over slicing the two blocks by hand.

Usage: python3 trim-mkdocs-version.py en/mkdocs.yml 4.6.0
"""
import re
import sys


def trim_nav(text, version):
    # The end boundary is either the next top-level nav item (2-space indent,
    # as "API Gateway:" normally is) or, on a branch scoped to just API
    # Manager (see the product/api-manager PoC branch), the end of the nav
    # list itself.
    m = re.search(
        r"(\n  - API Manager:\n)(.*?)(?=\n  - \S|\nmarkdown_extensions:\n)", text, re.S
    )
    if not m:
        sys.exit("could not locate the 'API Manager' nav block in mkdocs.yml")
    body = m.group(2)
    blocks = re.split(r"(?=^    - \"[^\"]+\":\n)", body, flags=re.M)
    blocks = [b for b in blocks if b.strip()]
    target = f'    - "{version}":\n'
    match = next((b for b in blocks if b.startswith(target)), None)
    if match is None:
        available = [re.match(r'    - "([^"]+)":', b).group(1) for b in blocks]
        sys.exit(f"version {version!r} not found in nav; available: {available}")
    return text[:m.start(2)] + match + text[m.end(2):]


def main():
    if len(sys.argv) != 3:
        sys.exit(f"usage: {sys.argv[0]} <mkdocs.yml path> <version>")
    path, version = sys.argv[1], sys.argv[2]
    text = open(path, encoding="utf-8").read()
    text = trim_nav(text, version)
    open(path, "w", encoding="utf-8").write(text)
    print(f"mkdocs.yml trimmed to API Manager {version}")


if __name__ == "__main__":
    main()
