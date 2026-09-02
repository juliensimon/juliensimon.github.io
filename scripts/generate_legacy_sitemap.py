#!/usr/bin/env python3
"""
Generate sitemaps for static HTML content not covered by Next.js sitemap.xml.

Produces:
  - sitemap-blog.xml    — blog posts (Arcee, HF, AWS, Medium, Legacy).
                          Industry Perspectives URLs are owned by next-site/src/app/sitemap.ts.
  - sitemap-videos.xml  — all YouTube transcript pages
  - sitemap-index.xml   — index referencing all individual sitemaps.

Run as part of the postbuild step.

Speaking-year URLs are owned by next-site/src/app/sitemap.ts and are NOT
duplicated here. A legacy combined sitemap-legacy.xml used to exist but was
removed because it was a pure union of sitemap-blog + sitemap-videos.
"""

import re
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

PUBLIC = Path(__file__).resolve().parent.parent / "next-site" / "public"
OUT = Path(__file__).resolve().parent.parent / "next-site" / "out"
SITE_URL = "https://www.julien.org"

# Blog directories to scan
BLOG_DIRS = [
    # Note: industry-perspectives is excluded here because sitemap.ts
    # already generates those URLs dynamically from the data file
    "blog/arcee-posts",
    "blog/huggingface-posts-and-images",
    "blog/aws-posts-and-images",
    "blog/aws-medium-posts-and-images",
    "blog/legacy-posts-and-images",
]

# Video directories
VIDEO_DIRS = [
    "youtube",
]

SKIP_FILES = {
    "blog/index.html",
    "youtube/index.html",
}


def extract_date_from_path(path_str: str) -> str:
    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', path_str)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    m = re.search(r'/(\d{4})(\d{2})(\d{2})_', path_str)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    m = re.search(r'/(\d{4})/', path_str)
    if m:
        return f"{m.group(1)}-12-31"
    return datetime.now().strftime("%Y-%m-%d")


def _is_redirect_stub(path: Path) -> bool:
    """True for a page that only bounces to another URL.

    Renames leave these behind so old links keep working, but they are not
    pages to index — Search Console reports a sitemap-listed redirect as an
    error, and they would inflate the counts the site publishes.
    """
    try:
        head = path.read_text(encoding='utf-8', errors='replace')[:2000]
    except OSError:
        return False
    return 'http-equiv="refresh"' in head.lower()


def scan_dirs(dirs, priority_fn=None):
    urls = []
    for scan_dir in dirs:
        dir_path = PUBLIC / scan_dir
        if not dir_path.exists():
            continue
        for html_file in sorted(dir_path.rglob("*.html")):
            rel_path = str(html_file.relative_to(PUBLIC))
            if rel_path in SKIP_FILES:
                continue
            if _is_redirect_stub(html_file):
                continue
            # Use directory URL for index.html files (e.g. blog/slug/ instead of blog/slug/index.html)
            if rel_path.endswith("/index.html"):
                url_path = rel_path[:-len("index.html")]
            else:
                url_path = rel_path
            encoded_path = "/".join(quote(part, safe="") for part in url_path.split("/"))
            url = f"{SITE_URL}/{encoded_path}"
            lastmod = extract_date_from_path(rel_path)
            priority = priority_fn(rel_path) if priority_fn else "0.5"
            changefreq = "monthly" if "/index.html" in rel_path else "yearly"
            urls.append((url, lastmod, changefreq, priority))
    return urls


def blog_priority(rel_path):
    if "arcee-posts" in rel_path:
        return "0.6"
    if "huggingface-posts" in rel_path:
        return "0.6"
    if "aws-posts-and-images" in rel_path:
        return "0.5"
    return "0.4"


def video_priority(rel_path):
    if "/index.html" in rel_path:
        return "0.5"
    return "0.4"


def write_sitemap(filename, urls):
    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url, lastmod, changefreq, priority in urls:
        xml_parts.append(f"  <url>")
        xml_parts.append(f"    <loc>{url}</loc>")
        xml_parts.append(f"    <lastmod>{lastmod}</lastmod>")
        xml_parts.append(f"    <changefreq>{changefreq}</changefreq>")
        xml_parts.append(f"    <priority>{priority}</priority>")
        xml_parts.append(f"  </url>")
    xml_parts.append("</urlset>")
    xml_content = "\n".join(xml_parts) + "\n"

    target = OUT / filename
    target.write_text(xml_content, encoding="utf-8")
    print(f"  Written {len(urls)} URLs to {target}")

    return len(urls)


def write_sitemap_index(filename, sitemaps):
    """Generate a sitemap index file referencing all individual sitemaps."""
    now = datetime.now().strftime("%Y-%m-%d")
    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for sitemap_url in sitemaps:
        xml_parts.append("  <sitemap>")
        xml_parts.append(f"    <loc>{sitemap_url}</loc>")
        xml_parts.append(f"    <lastmod>{now}</lastmod>")
        xml_parts.append("  </sitemap>")
    xml_parts.append("</sitemapindex>")
    xml_content = "\n".join(xml_parts) + "\n"

    target = OUT / filename
    target.write_text(xml_content, encoding="utf-8")
    print(f"  Written sitemap index to {target}")


def remove_obsolete_sitemaps():
    """Remove obsolete sitemap files that were previously generated.

    sitemap-speaking.xml: speaking URLs are owned by next-site/src/app/sitemap.ts.
    sitemap-legacy.xml:   was a pure union of sitemap-blog + sitemap-videos.
    """
    for filename in ("sitemap-speaking.xml", "sitemap-legacy.xml"):
        for target_dir in (PUBLIC, OUT):
            target = target_dir / filename
            if target.exists():
                target.unlink()
                print(f"  Removed obsolete {target}")


def main():
    blog_urls = scan_dirs(BLOG_DIRS, blog_priority)
    video_urls = scan_dirs(VIDEO_DIRS, video_priority)

    n_blog = write_sitemap("sitemap-blog.xml", blog_urls)
    n_video = write_sitemap("sitemap-videos.xml", video_urls)

    remove_obsolete_sitemaps()

    # Generate sitemap index referencing all individual sitemaps
    write_sitemap_index("sitemap-index.xml", [
        f"{SITE_URL}/sitemap.xml",
        f"{SITE_URL}/sitemap-blog.xml",
        f"{SITE_URL}/sitemap-videos.xml",
    ])

    print(f"\nGenerated sitemap-blog.xml with {n_blog} URLs")
    print(f"Generated sitemap-videos.xml with {n_video} URLs")
    print(f"Generated sitemap-index.xml (sitemap index)")


if __name__ == "__main__":
    main()
