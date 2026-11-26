#!/usr/bin/env python3 -I
"""Rewrite the PAGES block of site-fn.js from the build output.

Usage: python3 -I infra/gen_pages.py next-site/out

A route is a Next.js page when `out/<route>.html` exists. Pages under youtube/, blog/ and the Blogger-era
year folders are always linked with their `.html`, so they stay out of the list (CloudFront Functions are
limited to 10 KB). The script fails if the list would not fit.
"""
import json
import re
import sys
from pathlib import Path

SKIP_TOP = {"youtube", "blog", "RoyZ"}
LEGACY = re.compile(r"^\d{4}(_\d{2}_\d{2}_archive\.html)?$")  # Blogger archive: always linked with .html
LIMIT = 6000  # bytes for the PAGES block, well under the 10 KB function limit
FN = Path(__file__).resolve().with_name("site-fn.js")


def routes(out: Path) -> list[str]:
    found = []
    for p in sorted(out.rglob("*.html")):
        rel = p.relative_to(out)
        if p.name == "index.html" or rel.parts[0] in SKIP_TOP:
            continue
        if LEGACY.match(rel.parts[0]):
            continue
        found.append("/" + rel.with_suffix("").as_posix())
    return found


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    out = Path(sys.argv[1]).resolve()
    if not (out / "index.html").is_file():
        print(f"{out} has no index.html: not a build output", file=sys.stderr)
        return 1
    pages = routes(out)
    block = "var PAGES = " + json.dumps({r: 1 for r in pages}, separators=(",", ":")) + ";"
    if len(block) > LIMIT:
        print(f"PAGES block is {len(block)} bytes, limit {LIMIT}", file=sys.stderr)
        return 1
    src = FN.read_text()
    new, n = re.subn(
        r"(// BEGIN PAGES\n).*?(\n// END PAGES)",
        lambda m: m.group(1) + block + m.group(2),
        src,
        flags=re.S,
    )
    if n != 1:
        print("PAGES markers not found exactly once", file=sys.stderr)
        return 1
    FN.write_text(new)
    print(f"{len(pages)} page routes, block {len(block)} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
