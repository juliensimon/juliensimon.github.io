#!/usr/bin/env python3
"""Inject meta description, OG, and Twitter Card tags into AWS Medium blog posts."""

import os
import re
import json
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "next-site" / "public" / "blog" / "aws-medium-posts-and-images"
SITE_URL = "https://www.julien.org"
OG_IMAGE = f"{SITE_URL}/assets/og-image-1200x630.webp"

# Parse descriptions from the TypeScript data file
DATA_FILE = Path(__file__).parent.parent / "next-site" / "src" / "data" / "blog-listings" / "aws-medium.ts"


def parse_descriptions():
    """Extract href -> description mapping from aws-medium.ts."""
    content = DATA_FILE.read_text()
    # Match lines with href and description
    entries = re.findall(
        r"href:\s*'([^']+)'.*?description:\s*'((?:[^'\\]|\\.)*)'",
        content,
        re.DOTALL,
    )
    mapping = {}
    for href, desc in entries:
        # Normalize the href to extract the directory path
        # e.g., '/blog/aws-medium-posts-and-images/2021/..../index.html' -> directory path
        desc = desc.replace("\\'", "'").replace('\\"', '"')
        mapping[href] = desc
    return mapping


def extract_date_from_path(path_str):
    """Extract date from directory name like 2021-09-23_..."""
    match = re.search(r"/(\d{4})/(\d{4}-\d{2}-\d{2})_", path_str)
    if match:
        return match.group(2)
    return None


def inject_meta_tags(html_path, description, canonical_path):
    """Inject meta tags into an HTML file just before </head>."""
    content = html_path.read_text(encoding="utf-8")

    # Skip if already has og:title (already processed)
    if 'og:title' in content:
        return False

    # Extract title from <title> tag
    title_match = re.search(r"<title>(.*?)</title>", content)
    if not title_match:
        return False
    title = title_match.group(1).strip()

    # Clean title for meta tags
    meta_title = f"{title} - Julien Simon"

    # Extract date from path
    date = extract_date_from_path(str(html_path))
    date_iso = f"{date}T00:00:00Z" if date else ""

    # Build canonical URL
    canonical_url = f"{SITE_URL}{canonical_path}"

    # Build meta tags block
    meta_tags = f"""
    <link rel="canonical" href="{canonical_url}">
    <meta name="description" content="{escape_attr(description)}">
    <meta name="author" content="Julien Simon">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{escape_attr(meta_title)}">
    <meta property="og:description" content="{escape_attr(description)}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:image" content="{OG_IMAGE}">
    <meta property="og:site_name" content="Julien Simon">
    <meta property="article:author" content="Julien Simon">"""

    if date_iso:
        meta_tags += f"""
    <meta property="article:published_time" content="{date_iso}">"""

    meta_tags += f"""
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{escape_attr(meta_title)}">
    <meta name="twitter:description" content="{escape_attr(description)}">
    <meta name="twitter:creator" content="@julsimon">
    <link rel="icon" type="image/x-icon" href="/assets/favicon.ico">"""

    # Inject before </head>
    content = content.replace("</head>", meta_tags + "\n</head>")
    html_path.write_text(content, encoding="utf-8")
    return True


def escape_attr(text):
    """Escape HTML attribute value."""
    return (
        text.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def main():
    descriptions = parse_descriptions()
    print(f"Loaded {len(descriptions)} descriptions from aws-medium.ts")

    # Build a mapping from directory path to description
    dir_to_desc = {}
    for href, desc in descriptions.items():
        # href is like '/blog/aws-medium-posts-and-images/2021/.../index.html'
        dir_to_desc[href] = desc

    # Find all index.html files
    html_files = sorted(BLOG_DIR.rglob("index.html"))
    # Exclude the root index.html
    html_files = [f for f in html_files if f.parent != BLOG_DIR]

    updated = 0
    skipped = 0
    no_desc = 0

    for html_file in html_files:
        # Build the canonical path relative to site root
        rel_path = html_file.relative_to(BLOG_DIR.parent.parent)
        canonical_path = f"/{rel_path}"

        # Find matching description
        desc = dir_to_desc.get(canonical_path)
        if not desc:
            # Try matching by directory name
            dir_name = html_file.parent.name
            for href, d in dir_to_desc.items():
                if dir_name in href:
                    desc = d
                    break

        if not desc:
            # Generate a fallback description from the title
            title_match = re.search(r"<title>(.*?)</title>", html_file.read_text(encoding="utf-8"))
            if title_match:
                title = title_match.group(1).strip()
                desc = f"{title} - Technical article by Julien Simon on AWS and machine learning."
            else:
                no_desc += 1
                continue

        if inject_meta_tags(html_file, desc, canonical_path):
            updated += 1
        else:
            skipped += 1

    print(f"Updated: {updated}, Skipped (already has tags): {skipped}, No description: {no_desc}")


if __name__ == "__main__":
    main()
