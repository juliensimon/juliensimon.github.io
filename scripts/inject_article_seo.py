#!/usr/bin/env python3
"""Inject SEO tags into industry-perspectives article HTML files.

Adds to each article's <head>:
- <meta name="description"> from metadata.json
- <link rel="canonical"> pointing to the original URL
- Article schema.org JSON-LD structured data
"""

import json
import os
import re
from pathlib import Path

SITE_URL = "https://www.julien.org"
ARTICLES_DIR = Path(__file__).parent.parent / "blog" / "industry-perspectives"


def load_metadata(article_dir: Path) -> dict | None:
    meta_path = article_dir / "metadata.json"
    if not meta_path.exists():
        return None
    with open(meta_path) as f:
        return json.load(f)


def extract_meta_from_html(html: str) -> dict:
    """Fallback: extract metadata from HTML tags when no metadata.json exists."""
    title_match = re.search(r"<title>(.+?)</title>", html)
    date_match = re.search(r'<meta\s+name="date"\s+content="([^"]+)"', html)
    source_match = re.search(r'<meta\s+name="source"\s+content="([^"]+)"', html)
    return {
        "title": title_match.group(1).replace(" - Julien Simon", "") if title_match else "",
        "date": date_match.group(1) if date_match else "",
        "original_url": source_match.group(1) if source_match else "",
        "author": "Julien Simon",
        "description": "",
    }


def build_jsonld(meta: dict, page_url: str) -> str:
    canonical = meta.get("original_url", "")
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": meta.get("title", ""),
        "description": meta.get("description", ""),
        "datePublished": meta.get("date", ""),
        "dateModified": meta.get("date", ""),
        "author": {
            "@type": "Person",
            "name": "Julien Simon",
            "url": SITE_URL,
        },
        "publisher": {
            "@type": "Organization",
            "name": "The AI Realist",
            "url": "https://www.airealist.ai/",
        },
        "mainEntityOfPage": canonical if canonical else page_url,
        "url": page_url,
        "inLanguage": "en",
    }
    if meta.get("tags"):
        schema["keywords"] = ", ".join(meta["tags"])
    if meta.get("read_time"):
        schema["timeRequired"] = meta["read_time"]
    schema["potentialAction"] = {
        "@type": "SubscribeAction",
        "target": "https://www.airealist.ai/subscribe",
        "name": "Subscribe to The AI Realist",
    }
    return json.dumps(schema, indent=2, ensure_ascii=False)


def inject_seo_tags(article_dir: Path) -> bool:
    index_path = article_dir / "index.html"
    if not index_path.exists():
        return False

    html = index_path.read_text(encoding="utf-8")

    # If already processed, check if we need to update the JSON-LD
    if 'rel="canonical"' in html and "schema.org" in html:
        if "SubscribeAction" in html:
            print(f"  SKIP (already has SEO tags): {article_dir.name}")
            return False
        # Remove existing JSON-LD to re-inject with updated schema
        html = re.sub(
            r'\s*<script type="application/ld\+json">\s*\{.*?\}\s*</script>',
            '',
            html,
            flags=re.DOTALL,
        )

    # Load metadata
    meta = load_metadata(article_dir)
    if meta is None:
        meta = extract_meta_from_html(html)
        if not meta.get("title"):
            print(f"  SKIP (no metadata): {article_dir.name}")
            return False

    # Normalize original_url: some metadata uses "url" key instead
    if "original_url" not in meta and "url" in meta:
        meta["original_url"] = meta["url"]

    canonical_url = meta.get("original_url", "")
    description = meta.get("description", "")
    slug = article_dir.name
    page_url = f"{SITE_URL}/blog/industry-perspectives/{slug}/index.html"

    # Build injection block
    seo_lines = []
    if description and f'name="description"' not in html:
        escaped_desc = description.replace('"', "&quot;")
        seo_lines.append(f'  <meta name="description" content="{escaped_desc}">')
    if canonical_url and 'rel="canonical"' not in html:
        seo_lines.append(f'  <link rel="canonical" href="{canonical_url}">')
    if "schema.org" not in html:
        jsonld = build_jsonld(meta, page_url)
        seo_lines.append(f'  <script type="application/ld+json">\n{jsonld}\n  </script>')

    if not seo_lines:
        print(f"  SKIP (nothing to inject): {article_dir.name}")
        return False

    injection = "\n".join(seo_lines)

    # Inject before </head>
    if "</head>" in html:
        html = html.replace("</head>", f"{injection}\n</head>")
    else:
        print(f"  WARN (no </head> tag): {article_dir.name}")
        return False

    index_path.write_text(html, encoding="utf-8")
    print(f"  OK: {article_dir.name}")
    return True


def main():
    print("Injecting SEO tags into industry-perspectives articles...\n")
    count = 0
    for entry in sorted(ARTICLES_DIR.iterdir()):
        if entry.is_dir():
            if inject_seo_tags(entry):
                count += 1
    print(f"\nDone. Updated {count} article(s).")


if __name__ == "__main__":
    main()
