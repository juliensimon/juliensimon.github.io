#!/usr/bin/env python3
"""One-time migration: replace inline CSS in YouTube HTML files with shared stylesheet.

Processes both youtube/ and next-site/public/youtube/ trees.
- Replaces <style>...</style> with <link rel="stylesheet" href="../style.css">
- Adds Google Fonts <link> if missing
- Adds Umami analytics if missing
- Wraps bare inline back-links in <div class="back-link">
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TREES = [
    REPO_ROOT / "youtube",
    REPO_ROOT / "next-site" / "public" / "youtube",
]

GOOGLE_FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600'
    '&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">'
)

STYLESHEET = '<link rel="stylesheet" href="../style.css">'

UMAMI = (
    '<script defer src="https://cloud.umami.is/script.js" '
    'data-website-id="27550dad-d418-4f5d-ad1b-dab573da1020"></script>'
)


def migrate_file(filepath: Path, dry_run: bool = False) -> bool:
    """Migrate a single HTML file. Returns True if changes were made."""
    content = filepath.read_text(encoding='utf-8')
    original = content

    # 1. Replace inline <style>...</style> with external stylesheet link
    style_pattern = re.compile(r'\s*<style>.*?</style>\s*', re.DOTALL)
    if style_pattern.search(content):
        content = style_pattern.sub(f'\n    {STYLESHEET}\n', content, count=1)

    # 2. Add Google Fonts if missing
    if 'fonts.googleapis.com' not in content:
        # Insert before the stylesheet link or before </head>
        if STYLESHEET in content:
            content = content.replace(
                STYLESHEET,
                f'{GOOGLE_FONTS}\n    {STYLESHEET}',
            )
        else:
            content = content.replace('</head>', f'    {GOOGLE_FONTS}\n</head>')

    # 3. Add Umami analytics if missing
    if 'umami.is/script.js' not in content:
        content = content.replace(
            STYLESHEET,
            f'{STYLESHEET}\n    {UMAMI}',
        )

    # 4. Wrap bare inline-styled back links in <div class="back-link">
    # Pattern: <p style="..."><a href="https://www.julien.org" style="...">← julien.org</a></p>
    back_link_pattern = re.compile(
        r'<p[^>]*>\s*<a\s+href="https?://(?:www\.)?julien\.org"[^>]*>'
        r'[^<]*julien\.org</a>\s*</p>',
        re.IGNORECASE,
    )
    match = back_link_pattern.search(content)
    if match:
        content = content.replace(
            match.group(0),
            '<div class="back-link"><a href="https://www.julien.org">&larr; julien.org</a></div>',
        )

    # 5. Add back-link if none exists (for older files)
    if 'back-link' not in content and 'julien.org' not in content.split('<div class="container">')[0]:
        content = content.replace(
            '<body>',
            '<body>\n    <div class="back-link"><a href="https://www.julien.org">&larr; julien.org</a></div>',
        )

    if content == original:
        return False

    if not dry_run:
        filepath.write_text(content, encoding='utf-8')
    return True


def main():
    dry_run = '--dry-run' in sys.argv
    if dry_run:
        print("DRY RUN — no files will be modified\n")

    total = 0
    modified = 0

    for tree in TREES:
        if not tree.exists():
            print(f"Skipping {tree} (not found)")
            continue

        # Process all HTML files in year subdirectories
        for html_file in sorted(tree.glob("*/[!.]*.html")):
            # Skip non-year directories
            if not html_file.parent.name.isdigit():
                continue
            total += 1
            if migrate_file(html_file, dry_run):
                modified += 1
                prefix = "[DRY RUN] " if dry_run else ""
                print(f"  {prefix}Updated: {html_file.relative_to(REPO_ROOT)}")

    print(f"\nProcessed {total} files, modified {modified}")


if __name__ == '__main__':
    main()
