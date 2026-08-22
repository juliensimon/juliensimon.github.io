#!/usr/bin/env python3
"""Backfill three SEO essentials on legacy article pages.

The Medium-exported AWS posts shipped without a viewport meta, without an <h1>
(the title lives in an <h3> inside the content), and without structured data.
The personal-blog posts have everything except structured data.

Adds, only when absent:
  1. <meta name="viewport">      - mobile-first indexing needs it
  2. a single <h1>               - promoted from the first heading, or injected
  3. BlogPosting JSON-LD         - author/date/publisher for AI answer engines

Idempotent: re-running changes nothing. Reads the values it needs from the
meta tags already on the page, so it invents no content.
"""
import html
import json
import pathlib
import re
import sys

PUBLIC = pathlib.Path(__file__).resolve().parent.parent / "next-site" / "public"
TREES = ["blog/aws-medium-posts-and-images", "blog/legacy-posts-and-images"]

AUTHOR = {"@type": "Person", "name": "Julien Simon", "url": "https://www.julien.org"}
VIEWPORT = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
DEFAULT_IMAGE = "https://www.julien.org/assets/og-image.webp"
# Google drops the rich result if headline runs long.
HEADLINE_MAX = 110


def meta(doc, attr, key):
    """Read a meta tag's content. Attribute order varies (BeautifulSoup sorts
    them alphabetically), so match the tag first, then pull content out of it."""
    for tag in re.findall(r"<meta\b[^>]*>", doc, re.I):
        if re.search(rf'{attr}="{re.escape(key)}"', tag, re.I):
            m = re.search(r'content="([^"]*)"', tag, re.I)
            if m:
                return html.unescape(m.group(1))
    return None


def text_of(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", fragment)).replace("\xa0", " ")).strip()


def add_viewport(doc):
    if re.search(r'name="viewport"', doc, re.I):
        return doc, False
    m = re.search(r"<head[^>]*>", doc, re.I)
    if not m:
        return doc, False
    return doc[: m.end()] + "\n" + VIEWPORT + doc[m.end():], True


def add_h1(doc, title):
    if re.search(r"<h1\b", doc, re.I):
        return doc, False
    body = doc.find("<body")
    if body == -1:
        return doc, False
    # Prefer promoting the heading the article already shows, so the page does
    # not end up displaying its title twice.
    m = re.search(r"<(h[2-6])\b([^>]*)>(.*?)</\1>", doc[body:], re.S | re.I)
    if m:
        s, e = body + m.start(), body + m.end()
        promoted = f"<h1{m.group(2)}>{m.group(3)}</h1>"
        return doc[:s] + promoted + doc[e:], True
    m = re.search(r"<article\b[^>]*>", doc[body:], re.I)
    if not m:
        return doc, False
    at = body + m.end()
    return doc[:at] + f"<h1>{html.escape(title)}</h1>" + doc[at:], True


def add_jsonld(doc, path):
    if "application/ld+json" in doc:
        return doc, False
    tm = re.search(r"<title>(.*?)</title>", doc, re.S | re.I)
    canonical = re.search(r'rel="canonical"\s+href="([^"]+)"', doc, re.I) or re.search(
        r'href="([^"]+)"\s+rel="canonical"', doc, re.I
    )
    published = meta(doc, "property", "article:published_time")
    if not (tm and canonical and published):
        print(f"  SKIP (missing title/canonical/date): {path}")
        return doc, False

    title = text_of(tm.group(1))
    url = canonical.group(1)
    data = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title[:HEADLINE_MAX],
        "url": url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "datePublished": published,
        "dateModified": meta(doc, "property", "article:modified_time") or published,
        "author": AUTHOR,
        "publisher": AUTHOR,
        "image": meta(doc, "property", "og:image") or DEFAULT_IMAGE,
        "inLanguage": "en",
    }
    desc = meta(doc, "name", "description")
    if desc:
        data["description"] = desc
    block = (
        '<script type="application/ld+json">'
        + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        + "</script>"
    )
    i = doc.lower().rfind("</head>")
    if i == -1:
        return doc, False
    return doc[:i] + block + "\n" + doc[i:], True


def main():
    dry = "--dry-run" in sys.argv
    totals = {"viewport": 0, "h1": 0, "jsonld": 0, "files": 0}
    for tree in TREES:
        root = PUBLIC / tree
        if not root.exists():
            print(f"  Warning: missing tree {root}")
            continue
        for path in sorted(root.rglob("*.html")):
            doc = original = path.read_text(encoding="utf-8", errors="ignore")
            if re.search(r'name="robots"[^>]*noindex|noindex[^>]*name="robots"', doc, re.I):
                continue  # redirect stubs stay untouched
            title = text_of(re.search(r"<title>(.*?)</title>", doc, re.S | re.I).group(1)) if "<title>" in doc else ""
            doc, a = add_viewport(doc)
            doc, b = add_h1(doc, title)
            doc, c = add_jsonld(doc, path.relative_to(PUBLIC))
            totals["viewport"] += a
            totals["h1"] += b
            totals["jsonld"] += c
            if doc != original:
                totals["files"] += 1
                if not dry:
                    path.write_text(doc, encoding="utf-8")
    verb = "would update" if dry else "updated"
    print(f"{verb} {totals['files']} files: "
          f"+{totals['viewport']} viewport, +{totals['h1']} h1, +{totals['jsonld']} JSON-LD")


if __name__ == "__main__":
    main()
