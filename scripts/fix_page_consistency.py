#!/usr/bin/env python3
"""
Bulk-fix HTML page consistency across the site.

Round 1 fixes (back links, favicons, analytics):
  4a: YouTube video pages — remove old top back-link, add correct bottom links
  4b: Legacy blog year pages — fix "All Years" nav link
  4c: YouTube pages (all) — add favicon if missing
  4d: Industry-perspectives posts — add analytics if missing
  4e: Industry-perspectives pages — add favicon if missing
  4f: Industry-perspectives posts — fix back link to point to index

Round 2 fixes (SEO):
  5a: Add canonical URLs to all pages missing them
  5b: Add OG/Twitter tags to industry-perspectives posts
  5c: Add VideoObject schema to YouTube video pages
  5d: Add meta descriptions to YouTube video pages missing them

Round 3 fixes (remaining SEO gaps):
  6a: Add canonical/OG/favicon/analytics to Arcee pages missing them
  6b: Add OG tags to legacy blog pages
  6c: Add BlogPosting JSON-LD to industry-perspectives posts
  6d: Add meta descriptions to legacy blog pages missing them

Round 4 fixes (full coverage):
  7a: Add OG/Twitter tags to YouTube video pages
  7b: Add favicon to legacy blog pages
  7c: Fix industry-perspectives posts with missing/malformed meta descriptions
  7d: Add Article schema to Arcee pages missing it

Round 5 fixes (cleanup):
  8a: Add OG tags to legacy blog listing/index pages

Usage:
  python scripts/fix_page_consistency.py --dry-run   # Preview changes
  python scripts/fix_page_consistency.py              # Apply changes
"""

import argparse
import html as html_mod
import json
import re
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "next-site" / "public"
YOUTUBE_DIR = PUBLIC / "youtube"
INDUSTRY_DIR = PUBLIC / "blog" / "industry-perspectives"
LEGACY_DIR = PUBLIC / "blog" / "legacy-posts-and-images"
AWS_DIR = PUBLIC / "blog" / "aws-posts-and-images"
HF_DIR = PUBLIC / "blog" / "huggingface-posts-and-images"
ARCEE_DIR = PUBLIC / "blog" / "arcee-posts"

FAVICON_TAG = '<link rel="icon" type="image/x-icon" href="/assets/favicon.ico">'
UMAMI_SCRIPT = '<script defer src="https://cloud.umami.is/script.js" data-website-id="27550dad-d418-4f5d-ad1b-dab573da1020"></script>'
OG_IMAGE = "https://www.julien.org/assets/og-image-1200x630.webp"
SITE_URL = "https://www.julien.org"

stats = {"checked": 0, "modified": 0, "skipped": 0}


def _write_if_changed(filepath, content, original, label, dry_run):
    """Helper to write file only if content changed."""
    if content != original:
        stats["modified"] += 1
        if dry_run:
            print(f"  [DRY RUN] Would fix: {filepath.relative_to(PUBLIC)} ({label})")
        else:
            filepath.write_text(content, encoding="utf-8")
            print(f"  Fixed: {filepath.relative_to(PUBLIC)} ({label})")
        return True
    stats["skipped"] += 1
    return False


def _extract_title(content):
    """Extract title from <title> tag."""
    m = re.search(r"<title>([^<]+)</title>", content)
    return m.group(1).strip() if m else ""


def _extract_description(content):
    """Extract meta description."""
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content)
    if not m:
        m = re.search(r'<meta\s+content="([^"]*)"\s+name="description"', content)
    return m.group(1).strip() if m else ""


def _extract_h1(content):
    """Extract h1 text."""
    m = re.search(r"<h1[^>]*>([^<]+)</h1>", content)
    return m.group(1).strip() if m else ""


# ── Round 1 fixes ──────────────────────────────────────────────


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

            content = re.sub(
                r'<div class="back-link"><a href="https://www\.julien\.org">[^<]*</a></div>\s*',
                "", content,
            )
            content = content.replace('href="https://www.julien.org"', 'href="index.html"')

            new_links_block = (
                '<div class="links">\n'
                f'            <a href="index.html">&larr; Back to {year} Videos</a>\n'
                '            <a href="/youtube-videos">&larr; Back to YouTube Overview</a>\n'
                "        </div>"
            )
            content = re.sub(
                r'<div class="links">.*?</div>', new_links_block, content, flags=re.DOTALL,
            )

            if _write_if_changed(html_file, content, original, "back links", dry_run):
                count += 1

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
        content = content.replace(
            'href="https://www.julien.org" class="nav-link"',
            'href="../index.html" class="nav-link"',
        )
        if _write_if_changed(index_file, content, original, "nav link", dry_run):
            count += 1
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
        if "</head>" in content:
            content = content.replace("</head>", f"    {FAVICON_TAG}\n</head>")
            stats["modified"] += 1
            count += 1
            if dry_run:
                print(f"  [DRY RUN] Would add favicon: {html_file.relative_to(PUBLIC)}")
            else:
                html_file.write_text(content, encoding="utf-8")
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
        if "</head>" in content:
            content = content.replace("</head>", f"    {UMAMI_SCRIPT}\n</head>")
            stats["modified"] += 1
            count += 1
            if dry_run:
                print(f"  [DRY RUN] Would add analytics: {index_file.relative_to(PUBLIC)}")
            else:
                index_file.write_text(content, encoding="utf-8")
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
        if "</head>" in content:
            content = content.replace("</head>", f"    {FAVICON_TAG}\n</head>")
            stats["modified"] += 1
            count += 1
            if dry_run:
                print(f"  [DRY RUN] Would add favicon: {html_file.relative_to(PUBLIC)}")
            else:
                html_file.write_text(content, encoding="utf-8")
    return count


def fix_industry_perspectives_backlinks(dry_run: bool):
    """4f: Fix back links in industry-perspectives post pages."""
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
        content = re.sub(
            r'<a href="https://www\.julien\.org"([^>]*)>(?:&larr;|←)\s*(?:julien\.org|Back to Industry Perspectives)</a>',
            r'<a href="../index.html"\1>&larr; Back to Industry Perspectives</a>',
            content,
        )
        if _write_if_changed(index_file, content, original, "back link", dry_run):
            count += 1
    return count


# ── Round 2 fixes (SEO) ───────────────────────────────────────


def add_canonical_urls(dry_run: bool):
    """5a: Add canonical URLs to all pages missing them."""
    count = 0

    # YouTube pages
    for html_file in sorted(YOUTUBE_DIR.rglob("*.html")):
        stats["checked"] += 1
        content = html_file.read_text(encoding="utf-8")
        if 'rel="canonical"' in content:
            stats["skipped"] += 1
            continue
        rel_path = html_file.relative_to(PUBLIC)
        canonical = f'{SITE_URL}/{rel_path}'
        tag = f'<link rel="canonical" href="{canonical}">'
        if "</head>" in content:
            content = content.replace("</head>", f"    {tag}\n</head>")
            stats["modified"] += 1
            count += 1
            if dry_run:
                print(f"  [DRY RUN] Would add canonical: {rel_path}")
            else:
                html_file.write_text(content, encoding="utf-8")

    # Industry-perspectives pages
    for html_file in sorted(INDUSTRY_DIR.rglob("*.html")):
        stats["checked"] += 1
        content = html_file.read_text(encoding="utf-8")
        if 'rel="canonical"' in content:
            stats["skipped"] += 1
            continue
        rel_path = html_file.relative_to(PUBLIC)
        canonical = f'{SITE_URL}/{rel_path}'
        tag = f'<link rel="canonical" href="{canonical}">'
        if "</head>" in content:
            content = content.replace("</head>", f"    {tag}\n</head>")
            stats["modified"] += 1
            count += 1
            if dry_run:
                print(f"  [DRY RUN] Would add canonical: {rel_path}")
            else:
                html_file.write_text(content, encoding="utf-8")

    # Legacy blog pages
    for html_file in sorted(LEGACY_DIR.rglob("*.html")):
        stats["checked"] += 1
        content = html_file.read_text(encoding="utf-8")
        if 'rel="canonical"' in content:
            stats["skipped"] += 1
            continue
        rel_path = html_file.relative_to(PUBLIC)
        canonical = f'{SITE_URL}/{rel_path}'
        tag = f'<link rel="canonical" href="{canonical}">'
        if "</head>" in content:
            content = content.replace("</head>", f"    {tag}\n</head>")
            stats["modified"] += 1
            count += 1
            if dry_run:
                print(f"  [DRY RUN] Would add canonical: {rel_path}")
            else:
                html_file.write_text(content, encoding="utf-8")

    return count


def add_og_tags_to_industry_perspectives(dry_run: bool):
    """5b: Add OG/Twitter tags to industry-perspectives posts missing them."""
    count = 0
    for post_dir in sorted(INDUSTRY_DIR.iterdir()):
        if not post_dir.is_dir():
            continue
        index_file = post_dir / "index.html"
        if not index_file.exists():
            continue
        stats["checked"] += 1
        content = index_file.read_text(encoding="utf-8")
        if 'og:title' in content:
            stats["skipped"] += 1
            continue

        title = _extract_title(content) or _extract_h1(content)
        description = _extract_description(content) or title
        rel_path = index_file.relative_to(PUBLIC)
        url = f"{SITE_URL}/{rel_path}"

        # Extract date from directory name if possible
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', post_dir.name)
        date_str = date_match.group(1) if date_match else ""

        og_tags = f'''    <meta property="og:type" content="article">
    <meta property="og:title" content="{html_mod.escape(title)}">
    <meta property="og:description" content="{html_mod.escape(description[:200])}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{OG_IMAGE}">'''
        if date_str:
            og_tags += f'\n    <meta property="article:published_time" content="{date_str}T00:00:00Z">'
        og_tags += f'''
    <meta property="article:author" content="Julien Simon">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{html_mod.escape(title)}">
    <meta name="twitter:description" content="{html_mod.escape(description[:200])}">
    <meta name="twitter:creator" content="@julsimon">'''

        if "</head>" in content:
            content = content.replace("</head>", f"{og_tags}\n</head>")
            stats["modified"] += 1
            count += 1
            if dry_run:
                print(f"  [DRY RUN] Would add OG tags: {rel_path}")
            else:
                index_file.write_text(content, encoding="utf-8")
                print(f"  Added OG tags: {rel_path}")

    return count


def add_video_schema_to_youtube(dry_run: bool):
    """5c: Add VideoObject JSON-LD schema to YouTube video pages missing it."""
    count = 0
    for year_dir in sorted(YOUTUBE_DIR.iterdir()):
        if not year_dir.is_dir():
            continue
        for html_file in sorted(year_dir.glob("*.html")):
            if html_file.name == "index.html":
                continue
            stats["checked"] += 1
            content = html_file.read_text(encoding="utf-8")
            if "VideoObject" in content:
                stats["skipped"] += 1
                continue

            title = _extract_title(content) or _extract_h1(content)
            if not title:
                stats["skipped"] += 1
                continue

            # Extract video ID from iframe
            vid_match = re.search(r'youtube\.com/embed/([a-zA-Z0-9_-]+)', content)
            if not vid_match:
                stats["skipped"] += 1
                continue
            video_id = vid_match.group(1)

            # Extract date from filename (YYYYMMDD prefix)
            date_match = re.match(r'(\d{4})(\d{2})(\d{2})', html_file.stem)
            upload_date = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}T00:00:00+00:00" if date_match else ""

            schema = {
                "@context": "https://schema.org",
                "@type": "VideoObject",
                "name": title,
                "description": f"{title} - YouTube video by Julien Simon",
                "embedUrl": f"https://www.youtube.com/embed/{video_id}",
                "thumbnailUrl": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
                "author": {"@id": f"{SITE_URL}/#person"},
            }
            if upload_date:
                schema["uploadDate"] = upload_date

            schema_tag = f'    <script type="application/ld+json">\n    {json.dumps(schema, ensure_ascii=False)}\n    </script>'

            if "</head>" in content:
                content = content.replace("</head>", f"{schema_tag}\n</head>")
                stats["modified"] += 1
                count += 1
                if dry_run:
                    print(f"  [DRY RUN] Would add VideoObject: {html_file.relative_to(PUBLIC)}")
                else:
                    html_file.write_text(content, encoding="utf-8")

    return count


def add_meta_descriptions_to_youtube(dry_run: bool):
    """5d: Add meta descriptions to YouTube video pages missing them."""
    count = 0
    for year_dir in sorted(YOUTUBE_DIR.iterdir()):
        if not year_dir.is_dir():
            continue
        for html_file in sorted(year_dir.glob("*.html")):
            if html_file.name == "index.html":
                continue
            stats["checked"] += 1
            content = html_file.read_text(encoding="utf-8")
            if 'name="description"' in content or 'name=description' in content:
                stats["skipped"] += 1
                continue

            title = _extract_title(content) or _extract_h1(content)
            if not title:
                stats["skipped"] += 1
                continue

            desc_tag = f'    <meta name="description" content="{html_mod.escape(title)} - YouTube video by Julien Simon">'
            if "</head>" in content:
                content = content.replace("</head>", f"{desc_tag}\n</head>")
                stats["modified"] += 1
                count += 1
                if dry_run:
                    print(f"  [DRY RUN] Would add description: {html_file.relative_to(PUBLIC)}")
                else:
                    html_file.write_text(content, encoding="utf-8")

    return count


# ── Round 3 fixes (remaining SEO gaps) ─────────


def fix_arcee_pages(dry_run: bool):
    """6a: Add canonical/OG/favicon/analytics to Arcee pages missing them."""
    count = 0
    for html_file in sorted(ARCEE_DIR.rglob("*.html")):
        stats["checked"] += 1
        content = html_file.read_text(encoding="utf-8")
        original = content

        if "</head>" not in content:
            stats["skipped"] += 1
            continue

        title = _extract_title(content) or _extract_h1(content)
        description = _extract_description(content) or title
        rel_path = html_file.relative_to(PUBLIC)
        url = f"{SITE_URL}/{rel_path}"

        # Extract date from directory name
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', html_file.parent.name)
        date_str = date_match.group(1) if date_match else ""

        additions = []

        if "favicon" not in content:
            additions.append(f"    {FAVICON_TAG}")

        if "umami" not in content:
            additions.append(f"    {UMAMI_SCRIPT}")

        if 'rel="canonical"' not in content:
            additions.append(f'    <link rel="canonical" href="{url}">')

        if 'name="description"' not in content and title:
            additions.append(f'    <meta name="description" content="{html_mod.escape(description[:200])}">')

        if "og:title" not in content and title:
            og = f'''    <meta property="og:type" content="article">
    <meta property="og:title" content="{html_mod.escape(title)}">
    <meta property="og:description" content="{html_mod.escape(description[:200])}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{OG_IMAGE}">
    <meta property="article:author" content="Julien Simon">'''
            if date_str:
                og += f'\n    <meta property="article:published_time" content="{date_str}T00:00:00Z">'
            og += f'''
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{html_mod.escape(title)}">
    <meta name="twitter:description" content="{html_mod.escape(description[:200])}">
    <meta name="twitter:creator" content="@julsimon">'''
            additions.append(og)

        if additions:
            insert = "\n".join(additions)
            content = content.replace("</head>", f"{insert}\n</head>")

        if _write_if_changed(html_file, content, original, "arcee SEO", dry_run):
            count += 1

    return count


def add_og_tags_to_legacy_blog(dry_run: bool):
    """6b: Add OG tags to legacy blog pages missing them."""
    count = 0
    for html_file in sorted(LEGACY_DIR.rglob("*.html")):
        if html_file.name == "index.html":
            continue
        stats["checked"] += 1
        content = html_file.read_text(encoding="utf-8")
        if "og:title" in content:
            stats["skipped"] += 1
            continue
        if "</head>" not in content:
            stats["skipped"] += 1
            continue

        title = _extract_title(content) or _extract_h1(content)
        if not title:
            stats["skipped"] += 1
            continue

        description = _extract_description(content) or f"{title} - Blog post by Julien Simon"
        rel_path = html_file.relative_to(PUBLIC)
        url = f"{SITE_URL}/{rel_path}"

        # Extract date from filename (YYYY-MM-DD prefix)
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', html_file.stem)
        date_str = date_match.group(1) if date_match else ""

        og_tags = f'''    <meta property="og:type" content="article">
    <meta property="og:title" content="{html_mod.escape(title)}">
    <meta property="og:description" content="{html_mod.escape(description[:200])}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{OG_IMAGE}">
    <meta property="article:author" content="Julien Simon">'''
        if date_str:
            og_tags += f'\n    <meta property="article:published_time" content="{date_str}T00:00:00Z">'
        og_tags += f'''
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{html_mod.escape(title)}">
    <meta name="twitter:creator" content="@julsimon">'''

        content = content.replace("</head>", f"{og_tags}\n</head>")
        stats["modified"] += 1
        count += 1
        if dry_run:
            print(f"  [DRY RUN] Would add OG tags: {rel_path}")
        else:
            html_file.write_text(content, encoding="utf-8")

    return count


def add_blogposting_schema_to_industry_perspectives(dry_run: bool):
    """6c: Add BlogPosting JSON-LD to industry-perspectives posts missing it."""
    count = 0
    for post_dir in sorted(INDUSTRY_DIR.iterdir()):
        if not post_dir.is_dir():
            continue
        index_file = post_dir / "index.html"
        if not index_file.exists():
            continue
        stats["checked"] += 1
        content = index_file.read_text(encoding="utf-8")
        if "BlogPosting" in content:
            stats["skipped"] += 1
            continue
        if "</head>" not in content:
            stats["skipped"] += 1
            continue

        title = _extract_title(content) or _extract_h1(content)
        if not title:
            stats["skipped"] += 1
            continue

        description = _extract_description(content) or title
        rel_path = index_file.relative_to(PUBLIC)
        url = f"{SITE_URL}/{rel_path}"

        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', post_dir.name)
        date_str = date_match.group(1) if date_match else ""

        schema = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": title.replace(" - Julien Simon", ""),
            "description": description[:200],
            "url": url,
            "image": OG_IMAGE,
            "author": {"@id": f"{SITE_URL}/#person"},
            "publisher": {"@id": f"{SITE_URL}/#person"},
        }
        if date_str:
            schema["datePublished"] = f"{date_str}T00:00:00Z"
            schema["dateModified"] = f"{date_str}T00:00:00Z"

        schema_tag = f'    <script type="application/ld+json">\n    {json.dumps(schema, ensure_ascii=False)}\n    </script>'

        content = content.replace("</head>", f"{schema_tag}\n</head>")
        stats["modified"] += 1
        count += 1
        if dry_run:
            print(f"  [DRY RUN] Would add BlogPosting: {rel_path}")
        else:
            index_file.write_text(content, encoding="utf-8")

    return count


def add_meta_descriptions_to_legacy_blog(dry_run: bool):
    """6d: Add meta descriptions to legacy blog pages missing them."""
    count = 0
    for html_file in sorted(LEGACY_DIR.rglob("*.html")):
        if html_file.name == "index.html":
            continue
        stats["checked"] += 1
        content = html_file.read_text(encoding="utf-8")
        if 'name="description"' in content:
            stats["skipped"] += 1
            continue
        if "</head>" not in content:
            stats["skipped"] += 1
            continue

        title = _extract_title(content) or _extract_h1(content)
        if not title:
            stats["skipped"] += 1
            continue

        desc_tag = f'    <meta name="description" content="{html_mod.escape(title)} - Blog post by Julien Simon">'
        content = content.replace("</head>", f"{desc_tag}\n</head>")
        stats["modified"] += 1
        count += 1
        if dry_run:
            print(f"  [DRY RUN] Would add description: {html_file.relative_to(PUBLIC)}")
        else:
            html_file.write_text(content, encoding="utf-8")

    return count


# ── Round 4 fixes (full coverage) ──────────────


def add_og_tags_to_youtube(dry_run: bool):
    """7a: Add OG/Twitter tags to YouTube video pages missing them."""
    count = 0
    for year_dir in sorted(YOUTUBE_DIR.iterdir()):
        if not year_dir.is_dir():
            continue
        for html_file in sorted(year_dir.glob("*.html")):
            if html_file.name == "index.html":
                continue
            stats["checked"] += 1
            content = html_file.read_text(encoding="utf-8")
            if "og:title" in content:
                stats["skipped"] += 1
                continue
            if "</head>" not in content:
                stats["skipped"] += 1
                continue

            title = _extract_title(content) or _extract_h1(content)
            if not title:
                stats["skipped"] += 1
                continue

            vid_match = re.search(r'youtube\.com/embed/([a-zA-Z0-9_-]+)', content)
            if not vid_match:
                stats["skipped"] += 1
                continue
            video_id = vid_match.group(1)
            thumbnail = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

            description = f"{title} - YouTube video by Julien Simon"
            rel_path = html_file.relative_to(PUBLIC)
            url = f"{SITE_URL}/{rel_path}"

            date_match = re.match(r'(\d{4})(\d{2})(\d{2})', html_file.stem)
            date_str = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}" if date_match else ""

            og_tags = f'''    <meta property="og:type" content="video.other">
    <meta property="og:title" content="{html_mod.escape(title)}">
    <meta property="og:description" content="{html_mod.escape(description)}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{thumbnail}">'''
            if date_str:
                og_tags += f'\n    <meta property="og:video:release_date" content="{date_str}T00:00:00Z">'
            og_tags += f'''
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{html_mod.escape(title)}">
    <meta name="twitter:description" content="{html_mod.escape(description)}">
    <meta name="twitter:image" content="{thumbnail}">
    <meta name="twitter:creator" content="@julsimon">'''

            content = content.replace("</head>", f"{og_tags}\n</head>")
            stats["modified"] += 1
            count += 1
            if dry_run:
                print(f"  [DRY RUN] Would add OG tags: {rel_path}")
            else:
                html_file.write_text(content, encoding="utf-8")

    return count


def add_favicon_to_legacy_blog(dry_run: bool):
    """7b: Add favicon to legacy blog pages missing it."""
    count = 0
    for html_file in sorted(LEGACY_DIR.rglob("*.html")):
        stats["checked"] += 1
        content = html_file.read_text(encoding="utf-8")
        if "favicon" in content:
            stats["skipped"] += 1
            continue
        if "</head>" not in content:
            stats["skipped"] += 1
            continue

        content = content.replace("</head>", f"    {FAVICON_TAG}\n</head>")
        stats["modified"] += 1
        count += 1
        if dry_run:
            print(f"  [DRY RUN] Would add favicon: {html_file.relative_to(PUBLIC)}")
        else:
            html_file.write_text(content, encoding="utf-8")

    return count


def fix_industry_perspectives_meta_descriptions(dry_run: bool):
    """7c: Fix industry-perspectives posts with missing/malformed meta descriptions."""
    count = 0
    for post_dir in sorted(INDUSTRY_DIR.iterdir()):
        if not post_dir.is_dir():
            continue
        index_file = post_dir / "index.html"
        if not index_file.exists():
            continue
        stats["checked"] += 1
        content = index_file.read_text(encoding="utf-8")
        if 'name="description"' in content:
            stats["skipped"] += 1
            continue
        if "</head>" not in content:
            stats["skipped"] += 1
            continue

        title = _extract_title(content) or _extract_h1(content)
        if not title:
            stats["skipped"] += 1
            continue

        desc_tag = f'    <meta name="description" content="{html_mod.escape(title)} - Industry perspectives by Julien Simon">'
        content = content.replace("</head>", f"{desc_tag}\n</head>")
        stats["modified"] += 1
        count += 1
        if dry_run:
            print(f"  [DRY RUN] Would add description: {index_file.relative_to(PUBLIC)}")
        else:
            index_file.write_text(content, encoding="utf-8")

    return count


def add_article_schema_to_arcee(dry_run: bool):
    """7d: Add Article schema to Arcee pages missing structured data."""
    count = 0
    for html_file in sorted(ARCEE_DIR.rglob("*.html")):
        stats["checked"] += 1
        content = html_file.read_text(encoding="utf-8")
        if "schema.org" in content:
            stats["skipped"] += 1
            continue
        if "</head>" not in content:
            stats["skipped"] += 1
            continue

        title = _extract_title(content) or _extract_h1(content)
        if not title:
            stats["skipped"] += 1
            continue

        description = _extract_description(content) or title
        rel_path = html_file.relative_to(PUBLIC)
        url = f"{SITE_URL}/{rel_path}"

        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', html_file.parent.name)
        date_str = date_match.group(1) if date_match else ""

        schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": description[:200],
            "url": url,
            "image": OG_IMAGE,
            "author": {"@id": f"{SITE_URL}/#person"},
            "publisher": {"@id": f"{SITE_URL}/#person"},
        }
        if date_str:
            schema["datePublished"] = f"{date_str}T00:00:00Z"

        schema_tag = f'    <script type="application/ld+json">\n    {json.dumps(schema, ensure_ascii=False)}\n    </script>'
        content = content.replace("</head>", f"{schema_tag}\n</head>")
        stats["modified"] += 1
        count += 1
        if dry_run:
            print(f"  [DRY RUN] Would add Article schema: {rel_path}")
        else:
            html_file.write_text(content, encoding="utf-8")

    return count


def add_og_tags_to_legacy_listing_pages(dry_run: bool):
    """8a: Add OG tags to legacy blog listing/index pages."""
    count = 0
    for html_file in sorted(LEGACY_DIR.rglob("index.html")):
        stats["checked"] += 1
        content = html_file.read_text(encoding="utf-8")
        if "og:title" in content:
            stats["skipped"] += 1
            continue
        if "</head>" not in content:
            stats["skipped"] += 1
            continue

        title = _extract_title(content) or _extract_h1(content)
        if not title:
            stats["skipped"] += 1
            continue

        description = _extract_description(content) or f"{title} - Julien Simon"
        rel_path = html_file.relative_to(PUBLIC)
        url = f"{SITE_URL}/{rel_path}"

        og_tags = f'''    <meta property="og:type" content="website">
    <meta property="og:title" content="{html_mod.escape(title)}">
    <meta property="og:description" content="{html_mod.escape(description[:200])}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{OG_IMAGE}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{html_mod.escape(title)}">
    <meta name="twitter:creator" content="@julsimon">'''

        content = content.replace("</head>", f"{og_tags}\n</head>")
        stats["modified"] += 1
        count += 1
        if dry_run:
            print(f"  [DRY RUN] Would add OG tags: {rel_path}")
        else:
            html_file.write_text(content, encoding="utf-8")

    return count


# ── Main ───────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Fix HTML page consistency across the site")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying files")
    args = parser.parse_args()

    mode = "DRY RUN" if args.dry_run else "APPLYING"
    print(f"\n=== Page Consistency Fix ({mode}) ===\n")

    print("── Round 1: Structure & consistency ──\n")

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

    print("── Round 2: SEO enhancements ──\n")

    print("5a: Adding canonical URLs to pages missing them...")
    n = add_canonical_urls(args.dry_run)
    print(f"    -> {n} pages\n")

    print("5b: Adding OG/Twitter tags to industry-perspectives...")
    n = add_og_tags_to_industry_perspectives(args.dry_run)
    print(f"    -> {n} pages\n")

    print("5c: Adding VideoObject schema to YouTube video pages...")
    n = add_video_schema_to_youtube(args.dry_run)
    print(f"    -> {n} pages\n")

    print("5d: Adding meta descriptions to YouTube video pages...")
    n = add_meta_descriptions_to_youtube(args.dry_run)
    print(f"    -> {n} pages\n")

    print("── Round 3: Remaining SEO gaps ──\n")

    print("6a: Fixing Arcee pages (canonical/OG/favicon/analytics)...")
    n = fix_arcee_pages(args.dry_run)
    print(f"    -> {n} pages\n")

    print("6b: Adding OG tags to legacy blog pages...")
    n = add_og_tags_to_legacy_blog(args.dry_run)
    print(f"    -> {n} pages\n")

    print("6c: Adding BlogPosting schema to industry-perspectives...")
    n = add_blogposting_schema_to_industry_perspectives(args.dry_run)
    print(f"    -> {n} pages\n")

    print("6d: Adding meta descriptions to legacy blog pages...")
    n = add_meta_descriptions_to_legacy_blog(args.dry_run)
    print(f"    -> {n} pages\n")

    print("── Round 4: Full coverage ──\n")

    print("7a: Adding OG/Twitter tags to YouTube video pages...")
    n = add_og_tags_to_youtube(args.dry_run)
    print(f"    -> {n} pages\n")

    print("7b: Adding favicon to legacy blog pages...")
    n = add_favicon_to_legacy_blog(args.dry_run)
    print(f"    -> {n} pages\n")

    print("7c: Fixing industry-perspectives meta descriptions...")
    n = fix_industry_perspectives_meta_descriptions(args.dry_run)
    print(f"    -> {n} pages\n")

    print("7d: Adding Article schema to Arcee pages...")
    n = add_article_schema_to_arcee(args.dry_run)
    print(f"    -> {n} pages\n")

    print("── Round 5: Cleanup ──\n")

    print("8a: Adding OG tags to legacy blog listing pages...")
    n = add_og_tags_to_legacy_listing_pages(args.dry_run)
    print(f"    -> {n} pages\n")

    print(f"=== Summary ===")
    print(f"  Checked:  {stats['checked']}")
    print(f"  Modified: {stats['modified']}")
    print(f"  Skipped:  {stats['skipped']}")
    if args.dry_run:
        print(f"\n  (No files were modified — run without --dry-run to apply)\n")


if __name__ == "__main__":
    main()
