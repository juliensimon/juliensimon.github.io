#!/usr/bin/env python3
"""
Generate sitemaps for static HTML content not covered by Next.js sitemap.xml.

Produces:
  - sitemap-blog.xml    — all blog posts (Arcee, HF, AWS, Medium, Industry Perspectives, Legacy)
  - sitemap-videos.xml  — all YouTube transcript pages

Run as part of the postbuild step.
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
    "blog/industry-perspectives",
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
            encoded_path = "/".join(quote(part, safe="") for part in rel_path.split("/"))
            url = f"{SITE_URL}/{encoded_path}"
            lastmod = extract_date_from_path(rel_path)
            priority = priority_fn(rel_path) if priority_fn else "0.5"
            changefreq = "monthly" if "/index.html" in rel_path else "yearly"
            urls.append((url, lastmod, changefreq, priority))
    return urls


def blog_priority(rel_path):
    if "industry-perspectives" in rel_path:
        return "0.7"
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

    for target_dir in [PUBLIC, OUT]:
        target = target_dir / filename
        target.write_text(xml_content, encoding="utf-8")
        print(f"  Written {len(urls)} URLs to {target}")

    return len(urls)


def main():
    blog_urls = scan_dirs(BLOG_DIRS, blog_priority)
    video_urls = scan_dirs(VIDEO_DIRS, video_priority)

    n_blog = write_sitemap("sitemap-blog.xml", blog_urls)
    n_video = write_sitemap("sitemap-videos.xml", video_urls)

    # Also generate combined sitemap-legacy.xml for backwards compat
    all_urls = blog_urls + video_urls
    n_all = write_sitemap("sitemap-legacy.xml", all_urls)

    print(f"\nGenerated sitemap-blog.xml with {n_blog} URLs")
    print(f"Generated sitemap-videos.xml with {n_video} URLs")
    print(f"Generated sitemap-legacy.xml with {n_all} URLs (combined)")


if __name__ == "__main__":
    main()
