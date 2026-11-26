#!/usr/bin/env python3 -I
"""Fail if the build loads a resource from a host that headers-policy.json does not allow.

Usage: python3 -I infra/check_csp.py next-site/out

Static scan of <script>, <link rel=stylesheet|icon>, <img>, <iframe>, <audio>, <video>, <source>: it cannot
see what a script fetches at run time (check those in a browser: console shows CSP violations).
img-src is an explicit host list, so a new image host in a page fails here.
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

POLICY = Path(__file__).resolve().with_name("headers-policy.json")
TAG = re.compile(r"<(script|link|img|image|iframe|audio|video|source|embed|object)\b([^>]*)>", re.I)
URL = re.compile(r"\b(?:src|href|data)=[\"'](https?://[^\"']+)", re.I)
REL = re.compile(r"rel=[\"']?stylesheet", re.I)
ICON = re.compile(r"rel=[\"']?[a-z -]*icon", re.I)
DIRECTIVE = {
    "script": "script-src",
    "img": "img-src",
    "image": "img-src",  # browsers treat <image> as <img>
    "iframe": "frame-src",
    "link": "style-src",
    "audio": "media-src",
    "video": "media-src",
    "source": "media-src",
    "embed": "object-src",
    "object": "object-src",
}


def parse_csp(text: str) -> dict[str, list[str]]:
    out = {}
    for part in text.split(";"):
        bits = part.split()
        if bits:
            out[bits[0]] = bits[1:]
    return out


def allowed(host: str, sources: list[str]) -> bool:
    for s in sources:
        if s.startswith("https://"):
            pat = s[len("https://"):]
            if pat.startswith("*."):
                if host.endswith(pat[1:]):
                    return True
            elif host == pat:
                return True
    return False


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    out = Path(sys.argv[1]).resolve()
    csp = parse_csp(
        json.loads(POLICY.read_text())["SecurityHeadersConfig"]["ContentSecurityPolicy"]["ContentSecurityPolicy"]
    )
    bad: dict[tuple[str, str], str] = {}
    pages = 0
    for p in out.rglob("*.html"):
        pages += 1
        text = p.read_text(errors="ignore")
        for m in TAG.finditer(text):
            tag, attrs = m.group(1).lower(), m.group(2)
            directive = DIRECTIVE[tag]
            if tag == "link":
                if REL.search(attrs):
                    directive = "style-src"
                elif ICON.search(attrs):
                    directive = "img-src"
                else:
                    continue
            u = URL.search(attrs)
            if not u:
                continue
            host = urlsplit(u.group(1)).hostname or ""
            sources = csp.get(directive, csp.get("default-src", []))
            if host == "www.julien.org":  # 'self'; the apex julien.org is another origin and must be listed
                continue
            if not allowed(host, sources):
                bad.setdefault((directive, host), str(p.relative_to(out)))
    for (directive, host), example in sorted(bad.items()):
        print(f"BLOCKED {directive:11s} {host:32s} e.g. {example}")
    print(f"{pages} pages scanned, {len(bad)} blocked host(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
