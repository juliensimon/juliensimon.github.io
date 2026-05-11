#!/usr/bin/env python3
"""Backfill SEO-quality meta descriptions on legacy blog HTML pages.

These are 2008-2017 era posts under:
  - next-site/public/blog/legacy-posts-and-images/YYYY/*.html
  - next-site/public/blog/aws-medium-posts-and-images/YYYY/*/index.html

They originally received a templated description of the form
"{title} - Blog post by Julien Simon", which Bing flagged as both too
short and duplicated across the site. The bodies of these pages contain
real prose; we extract the first ~155 characters as the description.

Usage:
    python scripts/backfill_legacy_blog_descriptions.py [--dry-run] [--verbose]
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / 'scripts'))

from sync_youtube import build_meta_description, META_DESC_MIN  # noqa: E402

TARGET_GLOBS = [
    'next-site/public/blog/legacy-posts-and-images/*/*.html',
    'next-site/public/blog/aws-medium-posts-and-images/*/*/index.html',
    'blog/legacy-posts-and-images/*/*.html',
    'blog/aws-medium-posts-and-images/*/*/index.html',
]

LEGACY_MARKER = 'Blog post by Julien Simon'

META_DESC_RE = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"\s*/?>')
META_OG_DESC_RE = re.compile(r'<meta\s+property="og:description"\s+content="([^"]*)"\s*/?>')
META_TW_DESC_RE = re.compile(r'<meta\s+name="twitter:description"\s+content="([^"]*)"\s*/?>')
JSONLD_DESC_RE = re.compile(r'"description"\s*:\s*"((?:[^"\\]|\\.)*)"')
TITLE_RE = re.compile(r'<title>([^<]+)</title>')


def extract_prose(html_text: str) -> str:
    """Return the first prose text from the legacy post body."""
    soup = BeautifulSoup(html_text, 'html.parser')
    container = (
        soup.find('div', class_='content')
        or soup.find('section', class_='e-content')
        or soup.find('article')
        or soup.find('main')
    )
    if container is None:
        return ''
    # Drop figures, image tags, code blocks, links-only nodes from the
    # leading text — we want narrative prose, not "Image 1 of 2".
    for tag in container.find_all(['img', 'figure', 'pre', 'code',
                                   'textarea', 'script', 'style']):
        tag.decompose()
    text = container.get_text(separator=' ', strip=True)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def replace_attr(html_text: str, pattern: re.Pattern[str], new_value: str) -> str:
    escaped = html.escape(new_value, quote=True)

    def _sub(match: re.Match[str]) -> str:
        return match.group(0).replace(
            f'content="{match.group(1)}"',
            f'content="{escaped}"',
        )

    return pattern.sub(_sub, html_text, count=1)


def replace_jsonld_description(html_text: str, new_value: str) -> str:
    encoded = json.dumps(new_value)[1:-1].replace('</', '<\\/')

    def _sub(_match: re.Match[str]) -> str:
        return f'"description": "{encoded}"'

    return JSONLD_DESC_RE.sub(_sub, html_text, count=1)


def needs_update(html_text: str) -> bool:
    m = META_DESC_RE.search(html_text)
    if not m:
        return False  # No meta tag at all — different fix needed.
    current = html.unescape(m.group(1))
    if LEGACY_MARKER in current:
        return True
    return len(current) < META_DESC_MIN


def process_file(path: Path, dry_run: bool, verbose: bool) -> tuple[bool, str]:
    original = path.read_text(encoding='utf-8')
    if not needs_update(original):
        return False, 'description already non-templated and long enough'

    title_match = TITLE_RE.search(original)
    title = html.unescape(title_match.group(1).strip()) if title_match else ''
    # Strip a trailing " - Julien Simon | ..." suffix some posts have.
    title = re.sub(r'\s+[-–—|]\s+Julien Simon.*$', '', title).strip()

    prose = extract_prose(original)
    new_desc = build_meta_description(
        title, prose,
        fallback_suffix='an article by Julien Simon on AI, ML, and engineering.',
    )
    if not new_desc:
        return False, 'no description could be derived'

    current_match = META_DESC_RE.search(original)
    current = html.unescape(current_match.group(1)) if current_match else ''
    if new_desc == current:
        return False, 'derived description equals existing'

    updated = replace_attr(original, META_DESC_RE, new_desc)
    if META_OG_DESC_RE.search(updated):
        updated = replace_attr(updated, META_OG_DESC_RE, new_desc)
    if META_TW_DESC_RE.search(updated):
        updated = replace_attr(updated, META_TW_DESC_RE, new_desc)
    if JSONLD_DESC_RE.search(updated):
        updated = replace_jsonld_description(updated, new_desc)

    if updated == original:
        return False, 'no replacements applied'

    if verbose:
        print(f'  {len(current):3d} → {len(new_desc):3d}: {new_desc[:90]}{"…" if len(new_desc) > 90 else ""}')
    if not dry_run:
        path.write_text(updated, encoding='utf-8')
    return True, ''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    total_changed = 0
    total_seen = 0
    skipped: dict[str, int] = {}

    files: list[Path] = []
    for pattern in TARGET_GLOBS:
        files.extend(sorted(REPO_ROOT.glob(pattern)))
    # Deduplicate while preserving order.
    seen_paths: set[Path] = set()
    unique_files = []
    for f in files:
        if f not in seen_paths:
            seen_paths.add(f)
            unique_files.append(f)

    for path in unique_files:
        total_seen += 1
        changed, reason = process_file(path, args.dry_run, args.verbose)
        if changed:
            total_changed += 1
        else:
            skipped[reason] = skipped.get(reason, 0) + 1

    print()
    print(f'Files scanned: {total_seen}')
    print(f'Files updated: {total_changed}{" (dry-run)" if args.dry_run else ""}')
    for reason, count in sorted(skipped.items(), key=lambda x: -x[1]):
        print(f'  skipped ({count}): {reason}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
