#!/usr/bin/env python3
"""Backfill SEO-quality meta descriptions on existing Substack/industry
perspectives HTML pages.

Bing Webmaster Tools flagged several pages under
/blog/industry-perspectives/ for having meta descriptions shorter than
~80 characters. The original sync used the Substack subtitle verbatim;
when the subtitle was a short teaser ("What Four Products in Five
Months Tell You."), the resulting description fell below the SEO
threshold.

This script extends short descriptions by appending the first body
paragraph, using the same `_build_excerpt` logic that the live sync
script (`sync_substack.py`) now uses for new posts.

Usage:
    python scripts/backfill_substack_descriptions.py [--dry-run] [--verbose]
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

from sync_substack import _build_excerpt, EXCERPT_MIN  # noqa: E402

POSTS_DIR = REPO_ROOT / 'next-site' / 'public' / 'blog' / 'industry-perspectives'

META_DESC_RE = re.compile(
    r'<meta\s+name="description"\s+content="([^"]*)"\s*/?>'
)
META_OG_DESC_RE = re.compile(
    r'<meta\s+property="og:description"\s+content="([^"]*)"\s*/?>'
)
META_TW_DESC_RE = re.compile(
    r'<meta\s+name="twitter:description"\s+content="([^"]*)"\s*/?>'
)
JSONLD_DESC_RE = re.compile(r'"description"\s*:\s*"((?:[^"\\]|\\.)*)"')

# Article body lives in <main class="article-body"> or similar; fall back
# to first <p> after the title if the structure changes.


def extract_body_soup(html_text: str) -> BeautifulSoup:
    """Return a soup limited to the article prose, excluding the metadata
    header (<div class="meta"> with Author/Date/Source lines)."""
    full = BeautifulSoup(html_text, 'html.parser')
    body = (
        full.find('div', class_='article-content')
        or full.find('article')
        or full.find('main')
        or full
    )
    return body


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


def process_file(path: Path, dry_run: bool, verbose: bool) -> tuple[bool, str]:
    original = path.read_text(encoding='utf-8')
    m = META_DESC_RE.search(original)
    if not m:
        return False, 'no meta description tag'

    current = html.unescape(m.group(1)).strip()
    if len(current) >= EXCERPT_MIN:
        return False, 'description already meets minimum length'

    soup = extract_body_soup(original)
    new_excerpt = _build_excerpt(current, soup)
    if not new_excerpt or new_excerpt == current:
        return False, 'no improved excerpt produced'
    if len(new_excerpt) < len(current):
        return False, 'rebuilt excerpt is shorter than original'

    updated = replace_attr(original, META_DESC_RE, new_excerpt)
    updated = replace_attr(updated, META_OG_DESC_RE, new_excerpt)
    updated = replace_attr(updated, META_TW_DESC_RE, new_excerpt)
    updated = replace_jsonld_description(updated, new_excerpt)

    if updated == original:
        return False, 'no replacements applied'

    if verbose:
        print(f'  {len(current):3d} → {len(new_excerpt):3d}: {new_excerpt}')
    if not dry_run:
        path.write_text(updated, encoding='utf-8')
    return True, ''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    if not POSTS_DIR.exists():
        print(f'[error] {POSTS_DIR} does not exist', file=sys.stderr)
        return 1

    total_changed = 0
    total_seen = 0
    skipped: dict[str, int] = {}

    for path in sorted(POSTS_DIR.glob('*/index.html')):
        total_seen += 1
        changed, reason = process_file(path, args.dry_run, args.verbose)
        if changed:
            total_changed += 1
            if args.verbose:
                print(f'  ✓ {path.relative_to(REPO_ROOT)}')
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
