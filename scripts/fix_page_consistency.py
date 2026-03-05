#!/usr/bin/env python3
"""
Bulk-fix HTML page consistency across the site.

Fixes:
  4a: YouTube video pages — remove old top back-link, add correct bottom links
  4b: Legacy blog year pages — fix "All Years" nav link
  4c: YouTube pages (all) — add favicon if missing
  4d: Industry-perspectives posts — add analytics if missing
  4e: Industry-perspectives pages — add favicon if missing
  4f: Industry-perspectives posts — fix back link to point to index

Usage:
  python scripts/fix_page_consistency.py --dry-run   # Preview changes
  python scripts/fix_page_consistency.py              # Apply changes
"""

import argparse
import re
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "next-site" / "public"
YOUTUBE_DIR = PUBLIC / "youtube"
INDUSTRY_DIR = PUBLIC / "blog" / "industry-perspectives"
LEGACY_DIR = PUBLIC / "blog" / "legacy-posts-and-images"

FAVICON_TAG = '<link rel="icon" type="image/x-icon" href="/assets/favicon.ico">'
UMAMI_SCRIPT = '<script defer src="https://cloud.umami.is/script.js" data-website-id="27550dad-d418-4f5d-ad1b-dab573da1020"></script>'

stats = {"checked": 0, "modified": 0, "skipped": 0}


def fix_youtube_video_pages(dry_run: bool):
    """4a: Fix back links on YouTube video pages (not index.html)."""
    count = 0
    for year_dir in sorted(YOUTUBE_DIR.iterdir()):
        if not year_dir.is_dir():
            continue
        year = year_dir.name
        for html_file in sorted(year_dir.glob("*.html")):
            if html_file.name == "index.html":
                continue
            stats["checked"] += 1
            content = html_file.read_text(encoding="utf-8")
            original = content

            # Remove old-style top back-link div pointing to homepage
            content = re.sub(
                r'<div class="back-link"><a href="https://www\.julien\.org">[^<]*</a></div>\s*',
                "",
                content,
            )

            # Fix any remaining back links pointing to homepage (various templates)
            content = content.replace(
                'href="https://www.julien.org"',
                'href="index.html"',
            )

            # Replace entire links div with correct back links
            new_links_block = (
                '<div class="links">\n'
                f'            <a href="index.html">&larr; Back to {year} Videos</a>\n'
                '            <a href="/youtube-videos">&larr; Back to YouTube Overview</a>\n'
                "        </div>"
            )
            # Match both empty and non-empty links divs
            content = re.sub(
                r'<div class="links">.*?</div>',
                new_links_block,
                content,
                flags=re.DOTALL,
            )

            if content != original:
                count += 1
                stats["modified"] += 1
                if dry_run:
                    print(f"  [DRY RUN] Would fix back links: {html_file.relative_to(PUBLIC)}")
                else:
                    html_file.write_text(content, encoding="utf-8")
                    print(f"  Fixed back links: {html_file.relative_to(PUBLIC)}")
            else:
                stats["skipped"] += 1

    return count


def fix_legacy_blog_year_pages(dry_run: bool):
    """4b: Fix 'All Years' nav link in legacy blog year index pages."""
    count = 0
    for year_dir in sorted(LEGACY_DIR.iterdir()):
        if not year_dir.is_dir():
            continue
        index_file = year_dir / "index.html"
        if not index_file.exists():
            continue
        stats["checked"] += 1
        content = index_file.read_text(encoding="utf-8")
        original = content

        # Fix the "All Years" nav link
        content = content.replace(
            'href="https://www.julien.org" class="nav-link"',
            'href="../index.html" class="nav-link"',
        )

        if content != original:
            count += 1
            stats["modified"] += 1
            if dry_run:
                print(f"  [DRY RUN] Would fix nav link: {index_file.relative_to(PUBLIC)}")
            else:
                index_file.write_text(content, encoding="utf-8")
                print(f"  Fixed nav link: {index_file.relative_to(PUBLIC)}")
        else:
            stats["skipped"] += 1

    return count


def add_favicon_to_youtube(dry_run: bool):
    """4c: Add favicon to all YouTube pages if missing."""
    count = 0
    for html_file in sorted(YOUTUBE_DIR.rglob("*.html")):
        stats["checked"] += 1
        content = html_file.read_text(encoding="utf-8")
        if "favicon" in content:
            stats["skipped"] += 1
            continue

        # Insert favicon before </head>
        if "</head>" in content:
            content = content.replace("</head>", f"    {FAVICON_TAG}\n</head>")
            count += 1
            stats["modified"] += 1
            if dry_run:
                print(f"  [DRY RUN] Would add favicon: {html_file.relative_to(PUBLIC)}")
            else:
                html_file.write_text(content, encoding="utf-8")
                print(f"  Added favicon: {html_file.relative_to(PUBLIC)}")

    return count


def add_analytics_to_industry_perspectives(dry_run: bool):
    """4d: Add Umami analytics to industry-perspectives post pages if missing."""
    count = 0
    for post_dir in sorted(INDUSTRY_DIR.iterdir()):
        if not post_dir.is_dir():
            continue
        index_file = post_dir / "index.html"
        if not index_file.exists():
            continue
        stats["checked"] += 1
        content = index_file.read_text(encoding="utf-8")

        if "umami" in content:
            stats["skipped"] += 1
            continue

        # Insert analytics before </head>
        if "</head>" in content:
            content = content.replace("</head>", f"    {UMAMI_SCRIPT}\n</head>")
            count += 1
            stats["modified"] += 1
            if dry_run:
                print(f"  [DRY RUN] Would add analytics: {index_file.relative_to(PUBLIC)}")
            else:
                index_file.write_text(content, encoding="utf-8")
                print(f"  Added analytics: {index_file.relative_to(PUBLIC)}")

    return count


def add_favicon_to_industry_perspectives(dry_run: bool):
    """4e: Add favicon to all industry-perspectives pages if missing."""
    count = 0
    for html_file in sorted(INDUSTRY_DIR.rglob("*.html")):
        stats["checked"] += 1
        content = html_file.read_text(encoding="utf-8")
        if "favicon" in content:
            stats["skipped"] += 1
            continue

        # Insert favicon before </head>
        if "</head>" in content:
            content = content.replace("</head>", f"    {FAVICON_TAG}\n</head>")
            count += 1
            stats["modified"] += 1
            if dry_run:
                print(f"  [DRY RUN] Would add favicon: {html_file.relative_to(PUBLIC)}")
            else:
                html_file.write_text(content, encoding="utf-8")
                print(f"  Added favicon: {html_file.relative_to(PUBLIC)}")

    return count


def fix_industry_perspectives_backlinks(dry_run: bool):
    """4f: Fix back links in industry-perspectives post pages to point to ../index.html."""
    count = 0
    for post_dir in sorted(INDUSTRY_DIR.iterdir()):
        if not post_dir.is_dir():
            continue
        index_file = post_dir / "index.html"
        if not index_file.exists():
            continue
        stats["checked"] += 1
        content = index_file.read_text(encoding="utf-8")
        original = content

        # Fix back link from homepage to industry-perspectives index (various text patterns)
        content = re.sub(
            r'<a href="https://www\.julien\.org"([^>]*)>(?:&larr;|←)\s*(?:julien\.org|Back to Industry Perspectives)</a>',
            r'<a href="../index.html"\1>&larr; Back to Industry Perspectives</a>',
            content,
        )

        if content != original:
            count += 1
            stats["modified"] += 1
            if dry_run:
                print(f"  [DRY RUN] Would fix back link: {index_file.relative_to(PUBLIC)}")
            else:
                index_file.write_text(content, encoding="utf-8")
                print(f"  Fixed back link: {index_file.relative_to(PUBLIC)}")
        else:
            stats["skipped"] += 1

    return count


def main():
    parser = argparse.ArgumentParser(description="Fix HTML page consistency across the site")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying files")
    args = parser.parse_args()

    mode = "DRY RUN" if args.dry_run else "APPLYING"
    print(f"\n=== Page Consistency Fix ({mode}) ===\n")

    print("4a: Fixing YouTube video page back links...")
    n = fix_youtube_video_pages(args.dry_run)
    print(f"    -> {n} pages\n")

    print("4b: Fixing legacy blog year page nav links...")
    n = fix_legacy_blog_year_pages(args.dry_run)
    print(f"    -> {n} pages\n")

    print("4c: Adding favicon to YouTube pages...")
    n = add_favicon_to_youtube(args.dry_run)
    print(f"    -> {n} pages\n")

    print("4d: Adding analytics to industry-perspectives posts...")
    n = add_analytics_to_industry_perspectives(args.dry_run)
    print(f"    -> {n} pages\n")

    print("4e: Adding favicon to industry-perspectives pages...")
    n = add_favicon_to_industry_perspectives(args.dry_run)
    print(f"    -> {n} pages\n")

    print("4f: Fixing industry-perspectives back links...")
    n = fix_industry_perspectives_backlinks(args.dry_run)
    print(f"    -> {n} pages\n")

    print(f"=== Summary ===")
    print(f"  Checked:  {stats['checked']}")
    print(f"  Modified: {stats['modified']}")
    print(f"  Skipped:  {stats['skipped']}")
    if args.dry_run:
        print(f"\n  (No files were modified — run without --dry-run to apply)\n")


if __name__ == "__main__":
    main()
