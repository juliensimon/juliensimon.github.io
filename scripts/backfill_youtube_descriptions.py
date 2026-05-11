#!/usr/bin/env python3
"""Backfill SEO-quality meta descriptions on existing YouTube HTML pages.

Bing Webmaster Tools flagged hundreds of YouTube pages for "too many pages
with identical/short meta descriptions." The root cause was a templated
"<title> - YouTube video by Julien Simon" string, plus some older pages
missing meta descriptions entirely.

This script reads each video page, extracts the body description (stored
in <div class="description">...</div>), and rewrites:
  - <meta name="description">
  - <meta property="og:description">
  - <meta name="twitter:description">
  - JSON-LD VideoObject "description" field

Tags that are missing are inserted near the rest of the head metadata.

Usage:
    python scripts/backfill_youtube_descriptions.py [--dry-run] [--verbose]
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / 'scripts'))

# Reuse the same description-building logic that the live sync uses
from sync_youtube import build_meta_description, META_DESC_MAX  # noqa: E402

TARGET_DIRS = [
    REPO_ROOT / 'next-site' / 'public' / 'youtube',
    REPO_ROOT / 'youtube',
]

# Marker substring on the legacy templated descriptions
LEGACY_MARKER = 'YouTube video by Julien Simon'

DESC_BLOCK_RE = re.compile(
    r'<div class="description">(.*?)</div>',
    re.DOTALL,
)
TITLE_RE = re.compile(r'<title>([^<]+)</title>')
META_DESC_RE = re.compile(
    r'<meta\s+name="description"\s+content="[^"]*"\s*/?>',
)
META_OG_DESC_RE = re.compile(
    r'<meta\s+property="og:description"\s+content="[^"]*"\s*/?>',
)
META_TW_DESC_RE = re.compile(
    r'<meta\s+name="twitter:description"\s+content="[^"]*"\s*/?>',
)
# JSON-LD description field: handle quoted string value, simple non-nested form.
JSONLD_DESC_RE = re.compile(
    r'"description"\s*:\s*"((?:[^"\\]|\\.)*)"'
)


def extract_body_description(html_text: str) -> str:
    """Return the plain-text body description from <div class="description">."""
    m = DESC_BLOCK_RE.search(html_text)
    if not m:
        return ''
    block = m.group(1)
    # Drop the "Read full post on Substack →" footer link if present.
    block = re.sub(r'<a [^>]*airealist[^>]*>.*?</a>', '', block, flags=re.DOTALL)
    # Strip remaining HTML tags.
    block = re.sub(r'<[^>]+>', ' ', block)
    # Unescape entities.
    block = html.unescape(block)
    # Normalize whitespace, preserving paragraph breaks for the line-by-line
    # filtering inside build_meta_description.
    paragraphs = [re.sub(r'\s+', ' ', p).strip() for p in block.split('\n\n')]
    return '\n\n'.join(p for p in paragraphs if p)


def extract_title(html_text: str) -> str:
    m = TITLE_RE.search(html_text)
    return html.unescape(m.group(1).strip()) if m else ''


def replace_or_insert_meta(html_text: str, meta_re: re.Pattern[str],
                           new_tag: str, anchor_re: re.Pattern[str]) -> str:
    """Replace the meta tag if present; otherwise insert after `anchor_re`."""
    if meta_re.search(html_text):
        return meta_re.sub(new_tag, html_text, count=1)
    anchor = anchor_re.search(html_text)
    if not anchor:
        return html_text  # No safe insertion point; skip silently.
    end = anchor.end()
    return html_text[:end] + '\n    ' + new_tag + html_text[end:]


def replace_jsonld_description(html_text: str, new_value: str) -> str:
    """Replace JSON-LD description string with the new value, preserving JSON
    escaping. Only operates on the first match (the video's structured data)."""
    encoded = json.dumps(new_value)[1:-1]  # encode then strip surrounding quotes
    # Escape `</` to keep JSON inside <script> tag safe.
    encoded = encoded.replace('</', '<\\/')

    def _sub(_match: re.Match[str]) -> str:
        return f'"description": "{encoded}"'

    return JSONLD_DESC_RE.sub(_sub, html_text, count=1)


def needs_update(html_text: str) -> bool:
    """Return True if this page has a missing or legacy/templated description."""
    m = META_DESC_RE.search(html_text)
    if not m:
        return True
    return LEGACY_MARKER in m.group(0)


def process_file(path: Path, dry_run: bool, verbose: bool) -> tuple[bool, str]:
    """Returns (changed, reason). reason is empty when changed."""
    original = path.read_text(encoding='utf-8')
    if not needs_update(original):
        return False, 'already has a non-templated description'

    title = extract_title(original)
    body = extract_body_description(original)
    if not title:
        return False, 'no <title> found'

    meta_description = build_meta_description(title, body)
    escaped = html.escape(meta_description, quote=True)

    updated = original
    updated = replace_or_insert_meta(
        updated, META_DESC_RE,
        f'<meta name="description" content="{escaped}">',
        TITLE_RE,
    )
    updated = replace_or_insert_meta(
        updated, META_OG_DESC_RE,
        f'<meta property="og:description" content="{escaped}">',
        META_DESC_RE,
    )
    updated = replace_or_insert_meta(
        updated, META_TW_DESC_RE,
        f'<meta name="twitter:description" content="{escaped}">',
        META_OG_DESC_RE,
    )
    updated = replace_jsonld_description(updated, meta_description)

    if updated == original:
        return False, 'no replacements applied'

    if verbose:
        print(f'  → {meta_description[:80]}{"…" if len(meta_description) > 80 else ""}')
    if not dry_run:
        path.write_text(updated, encoding='utf-8')
    return True, ''


def iter_video_files(base: Path):
    if not base.exists():
        return
    for path in sorted(base.glob('*/*.html')):
        if path.name == 'index.html':
            continue
        yield path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    total_changed = 0
    total_seen = 0
    skipped_reasons: dict[str, int] = {}

    for base in TARGET_DIRS:
        if not base.exists():
            print(f'[skip] {base} does not exist')
            continue
        print(f'[scan] {base.relative_to(REPO_ROOT)}')
        for path in iter_video_files(base):
            total_seen += 1
            changed, reason = process_file(path, args.dry_run, args.verbose)
            if changed:
                total_changed += 1
                if args.verbose:
                    print(f'  ✓ {path.relative_to(REPO_ROOT)}')
            else:
                skipped_reasons[reason] = skipped_reasons.get(reason, 0) + 1

    print()
    print(f'Files scanned: {total_seen}')
    print(f'Files updated: {total_changed}{" (dry-run)" if args.dry_run else ""}')
    for reason, count in sorted(skipped_reasons.items(), key=lambda x: -x[1]):
        print(f'  skipped ({count}): {reason}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
