#!/usr/bin/env python3
"""Trim en/mkdocs.yml down to a single API Manager version, in place.

Keeps only the requested version's nav subtree under "API Manager" and points
the version switcher (extra.versioned_sections) at just that version, so a
single-version image doesn't advertise or link to versions whose docs were
excluded from the build.

Uses scoped regex surgery rather than a full YAML parse/dump: mkdocs.yml here
carries custom Python tags (e.g. pymdownx.emoji.to_svg) that a generic YAML
loader can't construct, and the block being edited has fixed, well-known
indentation, so a full parse buys nothing over slicing the two blocks by hand.

Usage: python3 trim-mkdocs-version.py en/mkdocs.yml 4.6.0
"""
import re
import sys


def trim_nav(text, version):
    m = re.search(r"(\n  - API Manager:\n)(.*?)(?=\n  - API Gateway:\n)", text, re.S)
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


def trim_versioned_sections(text, version):
    pattern = (
        r"(    API Manager:\n"
        r"      slug: api-manager\n"
        r"      default: )\"[^\"]+\"(\n"
        r"      versions:\n)"
        r"(.*?)"
        r"(?=\n    API Gateway:\n)"
    )
    m = re.search(pattern, text, re.S)
    if not m:
        sys.exit("could not locate extra.versioned_sections.'API Manager' in mkdocs.yml")
    prefix, mid, versions_body = m.group(1), m.group(2), m.group(3)
    if f'- "{version}"' not in versions_body:
        sys.exit(f"version {version!r} not found in versioned_sections.'API Manager'.versions")
    replacement = f'{prefix}"{version}"{mid}        - "{version}"\n'
    return text[:m.start()] + replacement + text[m.end():]


def main():
    if len(sys.argv) != 3:
        sys.exit(f"usage: {sys.argv[0]} <mkdocs.yml path> <version>")
    path, version = sys.argv[1], sys.argv[2]
    text = open(path, encoding="utf-8").read()
    text = trim_nav(text, version)
    text = trim_versioned_sections(text, version)
    open(path, "w", encoding="utf-8").write(text)
    print(f"mkdocs.yml trimmed to API Manager {version}")


if __name__ == "__main__":
    main()
