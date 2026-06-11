#!/usr/bin/env python3
"""
Verify the built Next.js site for broken links and missing resources.
Crawls the locally-served static export and reports issues.
"""

import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
from http.client import HTTPConnection


BASE = "http://localhost:8080"
TIMEOUT = 10

# All Next.js routes that must exist
REQUIRED_PAGES = [
    "/",
    "/experience",
    "/speaking",
    "/publications",
    "/youtube-videos",
    "/books",
    "/code",
    "/computers",
    "/blog-posts/aws",
    "/blog-posts/aws-medium",
    "/blog-posts/huggingface",
    "/blog-posts/arcee",
    "/blog-posts/medium",
]

# Speaking year pages
REQUIRED_PAGES += [f"/speaking/{y}" for y in range(2016, 2027)]

# Sample legacy content pages
SAMPLE_BLOG_PAGES = [
    "/blog/legacy-posts-and-images/2016/",
    "/blog/aws-posts-and-images/",
    "/blog/huggingface-posts-and-images/",
]

SAMPLE_YOUTUBE_PAGES = [
    "/youtube/2024/",
    "/youtube/2023/",
]

# Redirects: source -> expected destination pattern
REDIRECTS = {
    "/youtube.html": "/youtube-videos",
    "/speaking.html": "/speaking",
}


class LinkExtractor(HTMLParser):
    """Extract resource URLs from HTML."""

    def __init__(self):
        super().__init__()
        self.links = []  # <a href>
        self.resources = []  # <link>, <script>, <img>

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "a" and "href" in attrs_dict:
            self.links.append(attrs_dict["href"])
        elif tag == "link" and "href" in attrs_dict:
            self.resources.append(attrs_dict["href"])
        elif tag == "script" and "src" in attrs_dict:
            self.resources.append(attrs_dict["src"])
        elif tag == "img" and "src" in attrs_dict:
            self.resources.append(attrs_dict["src"])


def fetch(path):
    """Fetch a path from the local server. Returns (status, body, headers)."""
    parsed = urlparse(BASE)
    conn = HTTPConnection(parsed.hostname, parsed.port, timeout=TIMEOUT)
    try:
        conn.request("GET", path)
        resp = conn.getresponse()
        body = resp.read().decode("utf-8", errors="replace")
        headers = dict(resp.getheaders())
        return resp.status, body, headers
    except Exception as e:
        return None, str(e), {}
    finally:
        conn.close()


def is_internal(url):
    """Check if a URL is internal to our site."""
    if url.startswith("#") or url.startswith("mailto:") or url.startswith("javascript:"):
        return False
    parsed = urlparse(url)
    if parsed.scheme and parsed.scheme not in ("http", "https"):
        return False
    if parsed.netloc and parsed.netloc not in ("localhost:8080", "localhost"):
        return False
    return True


def normalize_path(base_path, url):
    """Convert a relative or absolute URL to a path."""
    if url.startswith("http"):
        return urlparse(url).path
    full = urljoin(f"http://localhost:8080{base_path}", url)
    return urlparse(full).path


def crawl_page(path, visited, broken_links, broken_resources, pages_to_visit):
    """Crawl a single page, check its resources, and discover new links."""
    if path in visited:
        return
    visited.add(path)

    status, body, headers = fetch(path)
    if status is None:
        broken_links.append((path, "CONNECTION_ERROR", body))
        return
    if status == 404:
        broken_links.append((path, 404, "Not Found"))
        return
    if status not in (200, 301, 302, 304):
        broken_links.append((path, status, f"Unexpected status"))
        return

    # Only parse HTML responses
    content_type = headers.get("content-type", headers.get("Content-Type", ""))
    if "text/html" not in content_type:
        return

    parser = LinkExtractor()
    try:
        parser.feed(body)
    except Exception:
        return

    # Check resources (CSS, JS, images)
    for res_url in parser.resources:
        if not is_internal(res_url):
            continue
        res_path = normalize_path(path, res_url)
        if res_path in visited:
            continue
        res_status, _, _ = fetch(res_path)
        if res_status != 200:
            broken_resources.append((path, res_url, res_status))

    # Discover internal links
    for link_url in parser.links:
        if not is_internal(link_url):
            continue
        link_path = normalize_path(path, link_url)
        # Strip fragment
        link_path = link_path.split("#")[0]
        if link_path and link_path not in visited:
            pages_to_visit.add(link_path)


def main():
    print("=" * 60)
    print("Site Verification - Legacy Decoupling Check")
    print("=" * 60)

    broken_links = []
    broken_resources = []
    visited = set()
    failed_required = []

    # Step 1: Check all required pages
    print(f"\n[1/5] Checking {len(REQUIRED_PAGES)} required Next.js pages...")
    for page in REQUIRED_PAGES:
        status, body, _ = fetch(page)
        if status != 200:
            failed_required.append((page, status))
            print(f"  FAIL {page} -> {status}")
        else:
            print(f"  OK   {page}")

    # Step 2: Crawl all pages starting from required pages
    print(f"\n[2/5] Crawling site for broken links and resources...")
    pages_to_visit = set(REQUIRED_PAGES)
    while pages_to_visit:
        path = pages_to_visit.pop()
        crawl_page(path, visited, broken_links, broken_resources, pages_to_visit)

    print(f"  Crawled {len(visited)} URLs")

    # Step 3: Check sample legacy content
    print(f"\n[3/5] Checking sample legacy content pages...")
    for page in SAMPLE_BLOG_PAGES + SAMPLE_YOUTUBE_PAGES:
        status, _, _ = fetch(page)
        label = "OK" if status == 200 else f"FAIL ({status})"
        print(f"  {label}  {page}")
        if status != 200:
            broken_links.append((page, status, "Legacy content missing"))

    # Step 4: Check redirects
    print(f"\n[4/5] Checking redirects...")
    for src, expected_dest in REDIRECTS.items():
        status, body, _ = fetch(src)
        if status == 200:
            # Check if the page contains a meta refresh or JS redirect
            if expected_dest in body:
                print(f"  OK   {src} -> {expected_dest}")
            else:
                print(f"  WARN {src} returned 200 but redirect target '{expected_dest}' not found in body")
        elif status in (301, 302):
            print(f"  OK   {src} -> redirect ({status})")
        else:
            print(f"  FAIL {src} -> {status}")
            broken_links.append((src, status, f"Expected redirect to {expected_dest}"))

    # Step 5: Check robots.txt and sitemap.xml
    print(f"\n[5/5] Checking robots.txt and sitemap.xml...")

    status, body, _ = fetch("/robots.txt")
    if status == 200:
        if "sitemap.xml" in body and "sitemap-index" not in body:
            print("  OK   robots.txt exists and references sitemap.xml")
        elif "sitemap-index" in body:
            print("  FAIL robots.txt still references legacy sitemap-index.xml")
            broken_links.append(("/robots.txt", "CONTENT", "References legacy sitemap-index.xml"))
        else:
            print("  WARN robots.txt exists but doesn't reference sitemap.xml")
    else:
        print(f"  FAIL robots.txt -> {status}")
        broken_links.append(("/robots.txt", status, "Missing"))

    status, body, _ = fetch("/sitemap.xml")
    if status == 200:
        try:
            ET.fromstring(body)
            print("  OK   sitemap.xml exists and is valid XML")
        except ET.ParseError as e:
            print(f"  FAIL sitemap.xml is not valid XML: {e}")
            broken_links.append(("/sitemap.xml", "PARSE", str(e)))
    else:
        print(f"  FAIL sitemap.xml -> {status}")
        broken_links.append(("/sitemap.xml", status, "Missing"))

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Pages crawled:       {len(visited)}")
    print(f"  Required pages OK:   {len(REQUIRED_PAGES) - len(failed_required)}/{len(REQUIRED_PAGES)}")
    print(f"  Broken links:        {len(broken_links)}")
    print(f"  Broken resources:    {len(broken_resources)}")

    if broken_links:
        print("\nBroken links:")
        for page, status, detail in broken_links:
            print(f"  [{status}] {page} - {detail}")

    if broken_resources:
        print("\nBroken resources:")
        for page, res, status in broken_resources:
            print(f"  [{status}] {res} (on page {page})")

    if broken_links or broken_resources or failed_required:
        print("\nVERDICT: FAIL")
        return 1
    else:
        print("\nVERDICT: PASS")
        return 0


if __name__ == "__main__":
    sys.exit(main())
