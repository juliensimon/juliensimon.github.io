#!/usr/bin/env python3
"""
Script to process HTML files in public/blog/ and public/youtube/ directories:
1. Remove "About the Author" sections
2. Ensure a backlink to https://www.julien.org exists at the top
"""

import os
import re
import sys

try:
    from bs4 import BeautifulSoup, NavigableString, Comment
except ImportError:
    print("beautifulsoup4 not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
    from bs4 import BeautifulSoup, NavigableString, Comment

BASE_DIR = "/Users/julien/Development/old-repos/juliensimon.github.io/next-site"
BLOG_DIR = os.path.join(BASE_DIR, "public/blog")
YOUTUBE_DIR = os.path.join(BASE_DIR, "public/youtube")

BACKLINK_HTML = '<p style="margin-bottom: 1.5em;"><a href="https://www.julien.org" style="color: #6366f1; text-decoration: none;">\u2190 julien.org</a></p>'

stats = {
    "files_processed": 0,
    "author_sections_removed": 0,
    "backlinks_added": 0,
    "backlinks_fixed": 0,
    "skipped": 0,
    "errors": 0,
}


def collect_html_files(blog_dir, youtube_dir):
    """Collect all HTML files to process."""
    files = []

    # Blog: all HTML files recursively
    for root, dirs, filenames in os.walk(blog_dir):
        for fname in filenames:
            if fname.endswith(".html"):
                files.append(os.path.join(root, fname))

    # YouTube: all HTML files recursively, but skip index.html in year folders
    for root, dirs, filenames in os.walk(youtube_dir):
        for fname in filenames:
            if fname.endswith(".html"):
                fpath = os.path.join(root, fname)
                # Skip index.html in youtube year folders (e.g., youtube/2022/index.html)
                rel = os.path.relpath(fpath, youtube_dir)
                parts = rel.split(os.sep)
                if fname == "index.html" and len(parts) == 2 and parts[0].isdigit():
                    stats["skipped"] += 1
                    continue
                files.append(fpath)

    return files


def remove_about_author(soup):
    """Remove the About the Author section. Returns True if something was removed."""
    removed = False

    # Find all h2 and h3 elements that contain "About the Author"
    for heading in soup.find_all(["h2", "h3"]):
        text = heading.get_text(strip=True)
        if "About the Author" in text:
            # Check if there's an <hr> immediately before this heading
            prev = heading.previous_sibling
            # Skip whitespace/newline NavigableStrings
            while prev and isinstance(prev, NavigableString) and prev.strip() == "":
                prev = prev.previous_sibling

            hr_to_remove = None
            if prev and prev.name == "hr":
                hr_to_remove = prev

            # Collect all following <p> elements until we hit a non-p structural element
            # or end of parent
            elements_to_remove = [heading]
            sibling = heading.next_sibling
            while sibling:
                next_sib = sibling.next_sibling
                if isinstance(sibling, NavigableString):
                    if sibling.strip() == "":
                        elements_to_remove.append(sibling)
                    else:
                        break
                elif sibling.name == "p":
                    elements_to_remove.append(sibling)
                elif sibling.name in ["hr", "br"]:
                    # Also remove trailing hrs
                    elements_to_remove.append(sibling)
                elif isinstance(sibling, Comment):
                    elements_to_remove.append(sibling)
                else:
                    break
                sibling = next_sib

            # Remove the hr before the heading
            if hr_to_remove:
                hr_to_remove.decompose()

            # Remove collected elements
            for elem in elements_to_remove:
                if isinstance(elem, NavigableString):
                    elem.extract()
                else:
                    elem.decompose()

            removed = True

    return removed


def fix_backlink(soup):
    """
    Ensure there's a backlink to https://www.julien.org.
    Returns 'added', 'fixed', or None.
    """
    # Check for existing "Back to" or arrow links that point elsewhere
    back_links = []
    for a_tag in soup.find_all("a"):
        text = a_tag.get_text(strip=True)
        href = a_tag.get("href", "")
        if ("Back to" in text or text.startswith("\u2190")) and href:
            back_links.append(a_tag)

    # Check if there's already a link to julien.org (as visible navigation link, not meta)
    has_julien_link = False
    for a_tag in soup.find_all("a"):
        href = a_tag.get("href", "")
        if href in ("https://www.julien.org", "https://www.julien.org/",
                     "https://julien.org", "https://julien.org/", "/"):
            text = a_tag.get_text(strip=True)
            # Only count visible navigation links, not metadata links
            if text and ("\u2190" in text or "Back" in text or "julien" in text.lower()):
                has_julien_link = True
                break

    if has_julien_link:
        return None

    # Fix existing "Back to" links to point to julien.org
    if back_links:
        for a_tag in back_links:
            href = a_tag.get("href", "")
            # Don't fix if already pointing to julien.org
            if "julien.org" not in href:
                a_tag["href"] = "https://www.julien.org"
                return "fixed"
        return None  # All back links already point to julien.org

    # No back links found - add one
    # Find the best insertion point: after <article> opening, or after <body> opening
    article = soup.find("article")
    body = soup.find("body")

    backlink_soup = BeautifulSoup(BACKLINK_HTML, "html.parser")
    backlink_p = backlink_soup.find("p")

    if article:
        # Insert at the beginning of the article
        if article.contents:
            article.contents[0].insert_before(backlink_p)
        else:
            article.append(backlink_p)
        return "added"
    elif body:
        # Insert at the beginning of the body
        if body.contents:
            body.contents[0].insert_before(backlink_p)
        else:
            body.append(backlink_p)
        return "added"

    return None


def process_file(filepath):
    """Process a single HTML file."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        # Use html.parser to avoid adding html/body tags to fragments
        soup = BeautifulSoup(content, "html.parser")

        author_removed = remove_about_author(soup)
        backlink_result = fix_backlink(soup)

        # Only write if changes were made
        if author_removed or backlink_result:
            output = str(soup)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(output)

        stats["files_processed"] += 1
        if author_removed:
            stats["author_sections_removed"] += 1
        if backlink_result == "added":
            stats["backlinks_added"] += 1
        elif backlink_result == "fixed":
            stats["backlinks_fixed"] += 1

    except Exception as e:
        stats["errors"] += 1
        print(f"  ERROR processing {filepath}: {e}")


def main():
    print(f"Scanning directories:")
    print(f"  Blog:    {BLOG_DIR}")
    print(f"  YouTube: {YOUTUBE_DIR}")
    print()

    files = collect_html_files(BLOG_DIR, YOUTUBE_DIR)
    total = len(files)
    print(f"Found {total} HTML files to process ({stats['skipped']} youtube index files skipped)")
    print()

    for i, filepath in enumerate(sorted(files)):
        rel = os.path.relpath(filepath, BASE_DIR)
        if (i + 1) % 50 == 0 or i == 0:
            print(f"  Processing {i+1}/{total}: {rel}")
        process_file(filepath)

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Files processed:          {stats['files_processed']}")
    print(f"  Author sections removed:  {stats['author_sections_removed']}")
    print(f"  Backlinks added:          {stats['backlinks_added']}")
    print(f"  Backlinks fixed:          {stats['backlinks_fixed']}")
    print(f"  YouTube indexes skipped:  {stats['skipped']}")
    print(f"  Errors:                   {stats['errors']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
