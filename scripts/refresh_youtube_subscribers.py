#!/usr/bin/env python3
"""Refresh the YouTube subscriber count across the site.

Scrapes the public @juliensimonfr channel page (no API key), extracts the
rounded subscriber count (e.g. "508K subscribers"), and rewrites all known
references across the Next.js source tree.

Source of truth: YOUTUBE_STATS.subscriberCount in next-site/src/data/youtube.ts.
All other files reference the same value as literals (prose or metric cards);
this script does a targeted regex sweep anchored on the old numeric value.

Usage:
    python3 scripts/refresh_youtube_subscribers.py            # apply changes
    python3 scripts/refresh_youtube_subscribers.py --dry-run  # preview only
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from pathlib import Path

CHANNEL_URL = "https://www.youtube.com/@juliensimonfr?hl=en&persist_hl=1"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

REPO_ROOT = Path(__file__).resolve().parent.parent
YOUTUBE_DATA = REPO_ROOT / "next-site/src/data/youtube.ts"

# Files containing literal "<N>K subscribers" / "<N>K YouTube subscribers"
# or a raw numeric value we need to bump. Anchored on the OLD value read from
# youtube.ts so the sweep is precise and idempotent.
TARGET_FILES = [
    "next-site/src/data/youtube.ts",
    "next-site/src/data/experience.ts",
    "next-site/src/lib/constants.ts",
    "next-site/src/lib/structured-data.ts",
    "next-site/src/app/page.tsx",
    "next-site/src/app/speaking/SpeakingContent.tsx",
    "next-site/src/app/datasets/DatasetsContent.tsx",
    "next-site/src/app/code/CodeContent.tsx",
    "next-site/src/app/publications/PublicationsContent.tsx",
    "next-site/src/app/youtube-videos/page.tsx",
    "next-site/src/app/youtube-videos/YouTubeContent.tsx",
]


def fetch_subscriber_count() -> int:
    """Return the rounded subscriber count in thousands (e.g. 508)."""
    req = urllib.request.Request(
        CHANNEL_URL,
        headers={
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
            "Cookie": "PREF=hl=en&gl=US",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode("utf-8", errors="replace")

    # Match "508K subscribers", "1.2M subscribers", etc.
    m = re.search(r"(\d+(?:\.\d+)?)\s*([KMB])\s*subscribers", html)
    if not m:
        raise RuntimeError(
            "Could not find subscriber count in channel page HTML. "
            "YouTube may have changed markup or localized the response."
        )

    value = float(m.group(1))
    unit = m.group(2)
    if unit == "K":
        return int(round(value))
    if unit == "M":
        return int(round(value * 1000))
    if unit == "B":
        return int(round(value * 1_000_000))
    raise RuntimeError(f"Unexpected unit: {unit}")


def read_current_count() -> int:
    content = YOUTUBE_DATA.read_text()
    m = re.search(r"subscriberCount:\s*(\d+)", content)
    if not m:
        raise RuntimeError(f"Could not read subscriberCount from {YOUTUBE_DATA}")
    return int(m.group(1))


def replace_in_file(path: Path, old: int, new: int, dry_run: bool) -> int:
    """Rewrite `old` -> `new` in known patterns. Returns number of edits."""
    text = path.read_text()
    original = text

    patterns = [
        # youtube.ts: `subscriberCount: 494,`
        (rf"(subscriberCount:\s*){old}\b", rf"\g<1>{new}"),
        # constants.ts METRICS: `{ value: 494, suffix: 'K', label: 'YouTube Subscribers' }`
        (
            rf"(\{{\s*value:\s*){old}(,\s*suffix:\s*'K',\s*label:\s*'YouTube Subscribers'\s*\}})",
            rf"\g<1>{new}\g<2>",
        ),
        # Prose: "494K subscribers", "494K+ subscribers", "494K YouTube subscribers"
        (rf"\b{old}(K\+?\s+(?:YouTube\s+)?subscribers)", rf"{new}\g<1>"),
        # experience.ts: "(494K subscribers)"
        (rf"\({old}(K subscribers\))", rf"({new}\g<1>"),
    ]

    for pat, repl in patterns:
        text = re.sub(pat, repl, text)

    if text == original:
        return 0

    # Count changed lines for reporting
    edits = sum(1 for a, b in zip(original.splitlines(), text.splitlines()) if a != b)
    edits += abs(len(original.splitlines()) - len(text.splitlines()))

    if not dry_run:
        path.write_text(text)
    return edits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    current = read_current_count()
    print(f"Current subscriberCount (youtube.ts): {current}K")

    try:
        fetched = fetch_subscriber_count()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Fetched from YouTube:                {fetched}K")

    if fetched == current:
        print("No change — already up to date.")
        return 0

    if fetched < current:
        print(
            f"WARNING: fetched value ({fetched}K) is LOWER than current ({current}K). "
            "Refusing to downgrade automatically. Use git if you want to force it."
        )
        return 2

    print(f"\nUpdating {current}K -> {fetched}K across {len(TARGET_FILES)} files"
          f"{' (dry-run)' if args.dry_run else ''}...\n")

    total_edits = 0
    for rel in TARGET_FILES:
        path = REPO_ROOT / rel
        if not path.exists():
            print(f"  SKIP (missing): {rel}")
            continue
        n = replace_in_file(path, current, fetched, args.dry_run)
        status = "  -" if n == 0 else f"  ✓ {n} edit{'s' if n != 1 else ''}"
        print(f"{status:>6}  {rel}")
        total_edits += n

    print(f"\nTotal edits: {total_edits}")
    if args.dry_run:
        print("Dry-run complete — no files modified.")
    else:
        print("Done. Next: cd next-site && npm run build, then commit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
