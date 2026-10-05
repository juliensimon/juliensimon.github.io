#!/usr/bin/env python3
"""Refresh count claims, article lists and the Last-updated stamp in llms.txt / llms-full.txt.

Source of truth is next-site/src/data/*.ts (publications, youtube, speaking,
datasets). The sync scripts keep those data files current but historically
left the AI-facing llms files behind; this script closes that gap. It is
idempotent and safe to run at any time.

Usage:
  python3 scripts/refresh_llms_txt.py            # apply fixes
  python3 scripts/refresh_llms_txt.py --dry-run  # report drift, change nothing
  python3 scripts/refresh_llms_txt.py --check    # exit 1 if drift found
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
BASE = REPO_ROOT / "next-site"
SRC = BASE / "src"
DATA = SRC / "data"

LLMS_FILES = [
    BASE / "public" / "llms.txt",
    BASE / "public" / "llms-full.txt",
]

# publications.ts category name -> label used in the llms-full.txt table and
# in the llms.txt link list (None where a surface has no per-category line).
CATEGORY_LABELS = {
    'The AI Realist (Industry Perspectives)': ('Industry Perspectives', None),
    'Arcee AI': ('Arcee AI', 'Arcee AI Blog Posts'),
    'Hugging Face': ('Hugging Face', 'Hugging Face Blog Posts'),
    'AWS Blog Posts': ('AWS Blog Posts', 'AWS Blog Posts'),
    'AWS Medium Posts': ('AWS Medium Posts', 'AWS Medium Posts'),
    'Medium Articles': ('Medium Articles', 'Medium Posts'),
    'Legacy Blog Posts': ('Legacy Blog Posts', 'Legacy Blog Posts'),
}


def _extract(pattern: str, text: str, source: Path) -> int:
    match = re.search(pattern, text)
    if not match:
        sys.exit(f"ERROR: pattern {pattern!r} not found in {source}")
    return int(match.group(1))


def load_stats() -> dict:
    """Read authoritative counts from the TypeScript data files."""
    pubs = (DATA / "publications.ts").read_text(encoding='utf-8')
    youtube = (DATA / "youtube.ts").read_text(encoding='utf-8')
    speaking = (DATA / "speaking.ts").read_text(encoding='utf-8')
    datasets = (DATA / "datasets.ts").read_text(encoding='utf-8')

    categories = {
        name: int(count)
        for name, count in re.findall(
            r"name:\s*'([^']+)',\s*count:\s*(\d+)", pubs
        )
    }
    total_articles = _extract(r"TOTAL_ARTICLES = (\d+)", pubs, DATA / "publications.ts")
    if sum(categories.values()) != total_articles:
        sys.exit(
            f"ERROR: publications.ts category counts sum to "
            f"{sum(categories.values())} but TOTAL_ARTICLES is {total_articles}. "
            "Fix publications.ts before refreshing llms files."
        )

    return {
        'total_articles': total_articles,
        'categories': categories,
        'industry_perspectives': categories.get('The AI Realist (Industry Perspectives)', 0),
        'videos': _extract(r"totalVideos:\s*(\d+)", youtube, DATA / "youtube.ts"),
        'subscribers': _extract(r"subscriberCount:\s*(\d+)", youtube, DATA / "youtube.ts"),
        'events': _extract(r"totalEvents:\s*(\d+)", speaking, DATA / "speaking.ts"),
        'countries': _extract(r"countries:\s*(\d+)", speaking, DATA / "speaking.ts"),
        'cities': _extract(r"cities:\s*(\d+)", speaking, DATA / "speaking.ts"),
        'datasets': _extract(r"TOTAL_DATASETS = (\d+)", datasets, DATA / "datasets.ts"),
    }


def build_rules(stats: dict) -> list[tuple[str, str, str]]:
    """(pattern, replacement, label) tuples. Patterns are anchored to the exact
    phrasings used in llms.txt / llms-full.txt so that historical narrative
    (e.g. "650+ talks in nearly 40 countries" about the Hugging Face years)
    is never rewritten."""
    a = stats['total_articles']
    ip = stats['industry_perspectives']
    v = stats['videos']
    s = stats['subscribers']
    e = stats['events']
    c = stats['countries']
    ci = stats['cities']
    d = stats['datasets']

    rules = [
        (r"\d+\+ technical articles", f"{a}+ technical articles", "total articles"),
        (r"\d+\+ technical blog posts", f"{a}+ technical blog posts", "total articles"),
        (r"\d+\+ technical posts published", f"{a}+ technical posts published", "total articles"),
        (r"\d+ company-agnostic", f"{ip} company-agnostic", "industry perspectives"),
        (r"\d+\+ speaking engagements", f"{e}+ speaking engagements", "speaking events"),
        (r"(\| Total events \| )\d+\+", rf"\g<1>{e}+", "speaking events"),
        (r"(/speaking\): )\d+\+ talks", rf"\g<1>{e}+ talks", "speaking events"),
        (r"(across )\d+( countries and )\d+( cities)", rf"\g<1>{c}\g<2>{ci}\g<3>", "countries/cities"),
        (r"(across )\d+( countries)", rf"\g<1>{c}\g<2>", "countries"),
        (r"(\| Countries \| )\d+", rf"\g<1>{c}", "countries"),
        (r"(\| Cities \| )\d+", rf"\g<1>{ci}", "cities"),
        (r"\d+K\+ YouTube subscribers", f"{s}K+ YouTube subscribers", "subscribers"),
        (r"\d+K\+ subscribers", f"{s}K+ subscribers", "subscribers"),
        (r"(\| Subscribers \| )\d+K\+", rf"\g<1>{s}K+", "subscribers"),
        (r"\d+\+ videos", f"{v}+ videos", "videos"),
        (r"\d+\+ YouTube video transcript pages", f"{v}+ YouTube video transcript pages", "videos"),
        (r"(\| Total videos \| )\d+\+", rf"\g<1>{v}+", "videos"),
        (r"\d+ open datasets", f"{d} open datasets", "datasets"),
    ]

    for ts_name, (table_label, link_label) in CATEGORY_LABELS.items():
        count = stats['categories'].get(ts_name)
        if count is None:
            continue
        rules.append((
            rf"(\| {re.escape(table_label)} \| )\d+( \|)",
            rf"\g<1>{count}\g<2>",
            f"category table: {table_label}",
        ))
        if link_label:
            rules.append((
                rf"(\[{re.escape(link_label)}\]\([^)]+\): )\d+\+",
                rf"\g<1>{count}+",
                f"category link: {link_label}",
            ))

    return rules


ARTICLES_TS = DATA / "blog-listings" / "industry-perspectives.ts"
ARCHIVE_URL = "https://www.julien.org/blog/industry-perspectives"
RECENT_COUNT = 5
KEY_ARTICLES_HEADING = "## Industry Perspectives — Key Articles"


def load_articles() -> list[dict]:
    """Industry Perspectives entries from the TypeScript listing, newest first."""
    text = ARTICLES_TS.read_text(encoding='utf-8')
    string = r"'((?:[^'\\]|\\.)*)'"
    entry = re.compile(
        rf"title: {string},\s*slug: {string},\s*date: {string},\s*"
        rf"description: {string},\s*originalUrl: {string}"
    )

    def unescape(value: str) -> str:
        value = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), value)
        return re.sub(r"\\(.)", r"\1", value)

    articles = [
        dict(zip(('title', 'slug', 'date', 'description', 'original'), map(unescape, m.groups())))
        for m in entry.finditer(text)
    ]
    if not articles:
        sys.exit(f"ERROR: no articles parsed from {ARTICLES_TS}")
    return sorted(articles, key=lambda a: a['date'], reverse=True)


def _month_year(iso_date: str) -> str:
    return datetime.strptime(iso_date, '%Y-%m-%d').strftime('%B %Y')


def refresh_recent_articles(text: str, articles: list[dict]) -> str:
    """llms.txt: rebuild the "Recent Articles" list from the newest entries."""
    section = re.search(r"(## Recent Articles\n\n)(.*?)(\n\n## )", text, re.DOTALL)
    if not section:
        return text
    lines = [
        f"- **{a['title']}** ({_month_year(a['date'])}) — {a['description']}"
        for a in articles[:RECENT_COUNT]
    ]
    return text[:section.start(2)] + '\n'.join(lines) + text[section.end(2):]


def add_missing_key_articles(text: str, articles: list[dict]) -> str:
    """llms-full.txt: add an entry for every article the file does not list yet.

    Existing entries carry hand-written summaries and are left alone; new ones
    start from the listing description and go in above them, newest first.
    """
    start = text.find(KEY_ARTICLES_HEADING)
    if start == -1:
        return text
    first_entry = text.find('\n### ', start)
    if first_entry == -1:
        return text
    missing = [a for a in articles if f"{ARCHIVE_URL}/{a['slug']}/" not in text]
    if not missing:
        return text
    blocks = ''.join(
        f"\n### {a['title']} ({_month_year(a['date'])})\n{a['description']}\n"
        f"- URL: {ARCHIVE_URL}/{a['slug']}/\n- Original: {a['original']}\n"
        for a in missing
    )
    return text[:first_entry] + blocks + text[first_entry:]



def refresh_llms_files(dry_run: bool = False) -> bool:
    """Rewrite stale counts in the llms files. Returns True if drift was found."""
    stats = load_stats()
    rules = build_rules(stats)
    articles = load_articles()
    today = datetime.now().strftime('%Y-%m-%d')
    drift_found = False

    print("Refreshing llms.txt / llms-full.txt from data files...")
    for path in LLMS_FILES:
        if not path.exists():
            print(f"  Warning: {path} not found, skipping")
            continue
        original = path.read_text(encoding='utf-8')
        text = original
        changed_labels = []
        for pattern, replacement, label in rules:
            updated = re.sub(pattern, replacement, text)
            if updated != text:
                changed_labels.append(label)
                text = updated

        for refresh, label in (
            (refresh_recent_articles, "recent articles"),
            (add_missing_key_articles, "key articles"),
        ):
            updated = refresh(text, articles)
            if updated != text:
                changed_labels.append(label)
                text = updated

        if text != original:
            drift_found = True
            # Only bump the freshness stamp when something actually changed.
            text = re.sub(
                r"(Last updated:\s*)\d{4}-\d{2}-\d{2}", rf"\g<1>{today}", text
            )
            rel = path.relative_to(REPO_ROOT)
            print(f"  {rel}: updated {', '.join(sorted(set(changed_labels)))}")
            if not dry_run:
                path.write_text(text, encoding='utf-8')
        else:
            print(f"  {path.name}: up to date")

    if drift_found and dry_run:
        print("  DRY RUN - no files were modified")
    return drift_found


def main():
    parser = argparse.ArgumentParser(
        description='Sync llms.txt / llms-full.txt counts with src/data/*.ts'
    )
    parser.add_argument('--dry-run', action='store_true',
                        help='Report drift without modifying files')
    parser.add_argument('--check', action='store_true',
                        help='Exit 1 if drift is found (implies --dry-run)')
    args = parser.parse_args()

    drift = refresh_llms_files(dry_run=args.dry_run or args.check)
    if args.check and drift:
        sys.exit(1)


if __name__ == "__main__":
    main()
