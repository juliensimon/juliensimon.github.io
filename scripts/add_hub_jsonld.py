#!/usr/bin/env python3
"""Add CollectionPage + ItemList structured data to the blog section hubs.

The four section index pages list dozens of articles each but carried no
structured data, so an answer engine had no machine-readable signal that the
page is a listing, who wrote the items, or how many there are.

Built from the links already on each page, so it stays truthful if the
listings change. Regenerates the block wholesale rather than merging.
"""
import html
import json
import pathlib
import re

PUBLIC = pathlib.Path(__file__).resolve().parent.parent / "next-site" / "public"
BASE = "https://www.julien.org"
AUTHOR = {"@type": "Person", "name": "Julien Simon", "url": BASE}
HUBS = [
    "blog/industry-perspectives",
    "blog/arcee-posts",
    "blog/aws-posts-and-images",
    "blog/huggingface-posts-and-images",
]
MARKER = "<!-- hub-jsonld -->"


def text_of(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", fragment))).strip()


def main():
    for hub in HUBS:
        path = PUBLIC / hub / "index.html"
        doc = path.read_text(encoding="utf-8")
        base_url = f"{BASE}/{hub}/"

        # Links to sibling post folders: relative, no scheme, trailing slash.
        seen, items = set(), []
        for href, label in re.findall(r'<a\s+href="([^":/][^":]*/)"[^>]*>(.*?)</a>', doc, re.S):
            name = text_of(label)
            if not name or href in seen or href.startswith(("#", "..")):
                continue
            seen.add(href)
            items.append({
                "@type": "ListItem",
                "position": len(items) + 1,
                "url": base_url + href,
                "name": name,
            })

        title = text_of(re.search(r"<title>(.*?)</title>", doc, re.S).group(1))
        desc = re.search(r'<meta name="description" content="([^"]*)"', doc)
        data = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": title,
            "url": base_url,
            "mainEntityOfPage": {"@type": "WebPage", "@id": base_url},
            "author": AUTHOR,
            "isPartOf": {"@type": "WebSite", "name": "Julien Simon", "url": BASE},
            "mainEntity": {
                "@type": "ItemList",
                "numberOfItems": len(items),
                "itemListElement": items,
            },
        }
        if desc:
            data["description"] = html.unescape(desc.group(1))

        block = (MARKER + '<script type="application/ld+json">'
                 + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
                 + "</script>")
        doc = re.sub(re.escape(MARKER) + r'<script type="application/ld\+json">.*?</script>', "", doc, flags=re.S)
        i = doc.lower().rfind("</head>")
        path.write_text(doc[:i] + block + "\n" + doc[i:], encoding="utf-8")
        print(f"{hub}: {len(items)} items")


if __name__ == "__main__":
    main()
