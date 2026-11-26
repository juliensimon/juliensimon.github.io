#!/usr/bin/env python3 -I
"""Swap the Umami tag for the Cloudflare Web Analytics beacon in static pages.

Usage: python3 -I infra/migrate_analytics.py [--write] ROOT [ROOT ...]

Without --write it only counts. `archive/` is frozen and not deployed, so do not pass it.
The token belongs to the Web Analytics site `www.julien.org` (Cloudflare dashboard, created
2026-11-26). It is public: it sits in every page's source.
"""
import re
import sys
from pathlib import Path

TOKEN = "abccd4dd49b24480ba0151938f7b0fee"
CF = (
    '<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
    f"""data-cf-beacon='{{"token": "{TOKEN}"}}'></script>"""
)

SCRIPT = re.compile(
    r'<script defer(?:="")? src="https://cloud\.umami\.is/script\.js" data-website-id="[0-9a-f-]+"></script>'
)
LOADER = re.compile(
    r"<script>\s*window\.addEventListener\('load', function\(\) \{\s*"
    r"var script = document\.createElement\('script'\);\s*"
    r"script\.src = 'https://cloud\.umami\.is/script\.js';\s*"
    r"script\.setAttribute\('data-website-id', '[0-9a-f-]+'\);\s*"
    r"document\.head\.appendChild\(script\);\s*\}\);\s*</script>"
)
HINT = re.compile(
    r'[ \t]*<link rel="(?:dns-prefetch|preconnect)" href="(?://|https://)cloud\.umami\.is"[^>]*>[ \t]*\n'
)


def transform(text: str) -> str:
    text = SCRIPT.sub(CF, text)
    text = LOADER.sub(CF, text)
    text = HINT.sub("", text)
    return text.replace("<!-- Umami Analytics -->", "<!-- Cloudflare Web Analytics -->")


def main(argv: list[str]) -> int:
    write = "--write" in argv
    roots = [Path(a) for a in argv if not a.startswith("--")]
    if not roots:
        print(__doc__)
        return 2
    changed = left = total = 0
    for root in roots:
        for p in root.rglob("*.html"):
            total += 1
            try:
                old = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if "umami" not in old.lower():
                continue
            new = transform(old)
            if new != old:
                changed += 1
                if write:
                    p.write_text(new, encoding="utf-8")
            if "umami" in new.lower():
                left += 1
                print("STILL HAS UMAMI:", p)
    print(f"{total} html files, {changed} {'rewritten' if write else 'to rewrite'}, {left} still mention umami")
    return 1 if left else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
