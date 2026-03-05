#!/usr/bin/env python3
"""
Migrate blog HTML files to use the shared blog/style.css stylesheet.

Handles three types of blog files:
1. Files with inline <style>...</style> blocks → replace with <link> to style.css
2. Files referencing css/minimal-blog-styles.css → redirect to blog/style.css
3. Files with no styling → inject <link> to style.css before </head>

Also adds Google Fonts <link> for Inter + Space Grotesk if missing.

Usage:
    python scripts/update_blog_styles.py [--dry-run]
"""

import os
import re
import sys
from pathlib import Path

# Root of the repository
REPO_ROOT = Path(__file__).resolve().parent.parent

# Blog directories to process (both trees)
BLOG_DIRS = [
    REPO_ROOT / "blog",
    REPO_ROOT / "next-site" / "public" / "blog",
]

# Google Fonts link for Inter + Space Grotesk
GOOGLE_FONTS_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">'
)

# Files to skip (listing pages that use css/styles.css)
LISTING_PAGES = {
    "blog/index.html",
    "blog/industry-perspectives/index.html",
    "blog/legacy-posts-and-images/index.html",
}

DRY_RUN = "--dry-run" in sys.argv

stats = {"inline_replaced": 0, "minimal_replaced": 0, "no_style_added": 0, "fonts_added": 0, "skipped": 0, "errors": 0}


def compute_relative_path_to_style(html_path: Path, blog_root: Path) -> str:
    """Compute the relative path from an HTML file to blog/style.css."""
    rel = html_path.parent.relative_to(blog_root)
    depth = len(rel.parts)
    if depth == 0:
        return "style.css"
    return "../" * depth + "style.css"


def has_google_fonts(content: str) -> bool:
    """Check if the file already has Google Fonts links for Inter or Space Grotesk."""
    return "fonts.googleapis.com" in content and ("Inter" in content or "Space+Grotesk" in content)


def add_google_fonts(content: str) -> str:
    """Add Google Fonts link before </head> if not present."""
    if has_google_fonts(content):
        return content

    # Insert before </head>
    if "</head>" in content:
        content = content.replace("</head>", f"  {GOOGLE_FONTS_LINK}\n</head>", 1)
        stats["fonts_added"] += 1
    elif "</HEAD>" in content:
        content = content.replace("</HEAD>", f"  {GOOGLE_FONTS_LINK}\n</HEAD>", 1)
        stats["fonts_added"] += 1

    return content


def process_inline_style(content: str, style_css_path: str) -> str:
    """Replace inline <style>...</style> with <link> to shared stylesheet."""
    # Match the inline style block (the common pattern across all posts)
    pattern = r'\s*<style>.*?</style>\s*'
    replacement = f'\n  <link rel="stylesheet" href="{style_css_path}">\n'

    new_content, count = re.subn(pattern, replacement, content, count=1, flags=re.DOTALL)
    if count > 0:
        stats["inline_replaced"] += 1
    return new_content


def process_minimal_css_ref(content: str, style_css_path: str) -> str:
    """Replace references to css/minimal-blog-styles.css with blog/style.css."""
    pattern = r'<link\s+rel="stylesheet"\s+href="[^"]*minimal-blog-styles\.css"[^>]*>'
    replacement = f'<link rel="stylesheet" href="{style_css_path}">'

    new_content, count = re.subn(pattern, replacement, content, count=1)
    if count > 0:
        stats["minimal_replaced"] += 1
    return new_content


def add_stylesheet_link(content: str, style_css_path: str) -> str:
    """Add stylesheet <link> before </head> for files with no styling."""
    link_tag = f'<link rel="stylesheet" href="{style_css_path}">'

    if "</head>" in content:
        content = content.replace("</head>", f"  {link_tag}\n</head>", 1)
        stats["no_style_added"] += 1
    elif "</HEAD>" in content:
        content = content.replace("</HEAD>", f"  {link_tag}\n</HEAD>", 1)
        stats["no_style_added"] += 1

    return content


def process_file(html_path: Path, blog_root: Path):
    """Process a single HTML file."""
    # Check if this is a listing page we should skip
    try:
        rel_path = html_path.relative_to(blog_root.parent if blog_root.name == "blog" else blog_root.parent.parent.parent)
    except ValueError:
        rel_path = html_path.relative_to(blog_root)
        rel_path = Path("blog") / rel_path

    # Skip listing pages (they use css/styles.css)
    rel_str = str(rel_path).replace("\\", "/")
    # For next-site/public paths, normalize
    if "next-site/public/" in rel_str:
        rel_str = rel_str.replace("next-site/public/", "")

    if rel_str in LISTING_PAGES:
        stats["skipped"] += 1
        return

    try:
        content = html_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"  ERROR reading {html_path}: {e}")
        stats["errors"] += 1
        return

    original = content
    style_css_path = compute_relative_path_to_style(html_path, blog_root)

    # Already has our stylesheet? Skip.
    if 'href="' in content and "style.css" in content and "minimal-blog-styles" not in content:
        # Check if it's specifically our blog style.css (not css/styles.css)
        if re.search(r'href="[^"]*(?<!/css/)style\.css"', content):
            stats["skipped"] += 1
            return

    # Case 1: Has inline <style> block
    if "<style>" in content and "</style>" in content:
        content = process_inline_style(content, style_css_path)

    # Case 2: References minimal-blog-styles.css
    elif "minimal-blog-styles.css" in content:
        content = process_minimal_css_ref(content, style_css_path)

    # Case 3: No styling at all
    elif "<style>" not in content and "stylesheet" not in content.lower().split("</head>")[0] if "</head>" in content.lower() else True:
        # Only add if there's a </head> tag and no existing stylesheet in <head>
        head_section = content.split("</head>")[0] if "</head>" in content else content.split("</HEAD>")[0] if "</HEAD>" in content else ""
        if head_section and 'rel="stylesheet"' not in head_section:
            content = add_stylesheet_link(content, style_css_path)

    # Add Google Fonts if missing
    content = add_google_fonts(content)

    if content != original:
        if DRY_RUN:
            print(f"  WOULD UPDATE: {html_path}")
        else:
            html_path.write_text(content, encoding="utf-8")
            print(f"  Updated: {html_path.relative_to(REPO_ROOT)}")


def main():
    if DRY_RUN:
        print("=== DRY RUN MODE ===\n")

    for blog_dir in BLOG_DIRS:
        if not blog_dir.exists():
            print(f"Skipping (not found): {blog_dir}")
            continue

        print(f"\nProcessing: {blog_dir.relative_to(REPO_ROOT)}")
        html_files = sorted(blog_dir.rglob("*.html"))
        print(f"  Found {len(html_files)} HTML files")

        for html_file in html_files:
            process_file(html_file, blog_dir)

    print(f"\n{'=== DRY RUN RESULTS ===' if DRY_RUN else '=== RESULTS ==='}")
    print(f"  Inline <style> replaced: {stats['inline_replaced']}")
    print(f"  minimal-blog-styles replaced: {stats['minimal_replaced']}")
    print(f"  No-style files updated: {stats['no_style_added']}")
    print(f"  Google Fonts added: {stats['fonts_added']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")
    print(f"  Total changes: {stats['inline_replaced'] + stats['minimal_replaced'] + stats['no_style_added']}")


if __name__ == "__main__":
    main()
