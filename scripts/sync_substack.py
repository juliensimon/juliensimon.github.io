#!/usr/bin/env python3
"""
Sync Substack posts to julien.org

Fetches the RSS feed from julsimon.substack.com, detects new posts,
and creates the appropriate files on the website.

Video posts go to: /youtube/YYYY/
Article posts go to: /blog/industry-perspectives/

Usage:
    python sync_substack.py --dry-run  # Preview changes
    python sync_substack.py            # Apply changes
"""

import argparse
import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import NamedTuple

import requests
import xml.etree.ElementTree as ET

RSS_URL = "https://julsimon.substack.com/feed"
BASE = Path(__file__).parent.parent / "next-site"
PUBLIC = BASE / "public"
SRC = BASE / "src"


class PostItem(NamedTuple):
    """Parsed RSS item."""
    title: str
    link: str
    pub_date: datetime
    description: str
    content: str
    post_type: str  # 'video' or 'article'
    youtube_id: str | None


def fetch_feed() -> list[PostItem]:
    """Fetch and parse the Substack RSS feed."""
    print(f"Fetching {RSS_URL}...")
    response = requests.get(RSS_URL, timeout=30)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    items = []

    for item in root.findall('.//item'):
        title = item.findtext('title', '').strip()
        link = item.findtext('link', '').strip()
        pub_date_str = item.findtext('pubDate', '')
        description = item.findtext('description', '').strip()

        # Get content:encoded if available
        content = ''
        for child in item:
            if child.tag.endswith('encoded'):
                content = child.text or ''
                break

        # Parse date (format: "Wed, 04 Dec 2025 12:00:00 GMT")
        try:
            pub_date = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %Z")
        except ValueError:
            try:
                pub_date = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %z")
            except ValueError:
                pub_date = datetime.now()

        # Classify the post
        post_type, youtube_id = classify_post(content or description)

        items.append(PostItem(
            title=html.unescape(title),
            link=link,
            pub_date=pub_date,
            description=html.unescape(description),
            content=content,
            post_type=post_type,
            youtube_id=youtube_id,
        ))

    return items


def classify_post(content: str) -> tuple[str, str | None]:
    """
    Classify post as video or article.
    Returns ('video', youtube_id) or ('article', None)
    """
    patterns = [
        r'youtube-nocookie\.com/embed/([a-zA-Z0-9_-]{11})',
        r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',
        r'youtu\.be/([a-zA-Z0-9_-]{11})',
        r'youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        if match := re.search(pattern, content):
            return ('video', match.group(1))
    return ('article', None)


def slugify(text: str) -> str:
    """Create a URL-friendly slug from text."""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Convert to lowercase
    text = text.lower()
    # Replace special characters with hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    # Replace spaces and multiple hyphens with single hyphen
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def title_to_filename(title: str) -> str:
    """Convert title to filename format (Title_Words_Here)."""
    # Remove special characters but keep spaces
    clean = re.sub(r'[^\w\s-]', '', title)
    # Replace spaces with underscores
    return re.sub(r'\s+', '_', clean.strip())


def is_video_existing(year: int, youtube_id: str) -> bool:
    """Check if a video with this YouTube ID already exists."""
    year_dir = PUBLIC / "youtube" / str(year)
    if not year_dir.exists():
        return False

    # Search for YouTube ID in any HTML file in this year's directory
    for html_file in year_dir.glob("*.html"):
        if html_file.name == "index.html":
            continue
        try:
            content = html_file.read_text(encoding='utf-8')
            if youtube_id in content:
                return True
        except Exception:
            continue

    return False


def is_article_existing(date_str: str, slug: str) -> bool:
    """Check if an article folder already exists."""
    path = PUBLIC / "blog" / "industry-perspectives" / f"{date_str}_{slug}"
    return path.exists()


def get_new_posts(items: list[PostItem], force: bool = False) -> list[PostItem]:
    """Filter to only new posts not yet on the site."""
    if force:
        return items  # Return all posts when forcing

    new_posts = []

    for item in items:
        if item.post_type == 'video':
            year = item.pub_date.year
            # Use YouTube ID for deduplication (more robust than filename)
            if item.youtube_id and not is_video_existing(year, item.youtube_id):
                new_posts.append(item)
        else:
            date_str = item.pub_date.strftime('%Y-%m-%d')
            slug = slugify(item.title)
            if not is_article_existing(date_str, slug):
                new_posts.append(item)

    return new_posts


def create_video_page(item: PostItem, dry_run: bool) -> Path:
    """Create a video HTML page."""
    year = item.pub_date.year
    date_str = item.pub_date.strftime('%Y%m%d')
    filename = f"{date_str}_{title_to_filename(item.title)}"

    year_dir = PUBLIC / "youtube" / str(year)
    filepath = year_dir / f"{filename}.html"

    # Format date for display
    display_date = item.pub_date.strftime('%B %d, %Y').replace(' 0', ' ')

    # Extract description (first paragraph from content or use description)
    description = item.description
    if item.content:
        # Try to get meaningful content
        desc_match = re.search(r'<p[^>]*>(.+?)</p>', item.content, re.DOTALL)
        if desc_match:
            description = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip()

    html_content = f'''<!DOCTYPE html><html lang="en"><head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(item.title)}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2.2em;
        }}
        .date {{
            color: #7f8c8d;
            font-size: 1.1em;
            margin-bottom: 30px;
            font-weight: 500;
        }}
        .video-container {{
            position: relative;
            width: 100%;
            height: 0;
            padding-bottom: 56.25%;
            margin-bottom: 30px;
        }}
        .video-container iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
            border-radius: 8px;
        }}
        .description {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            white-space: pre-wrap;
            font-size: 1em;
        }}
        .description a {{
            color: #3498db;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }}
        .description a:hover {{
            color: #2980b9;
            text-decoration: underline;
        }}
        .tags {{
            margin-bottom: 30px;
        }}
        .tags h2 {{
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.5em;
        }}
        .tag {{
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 6px 12px;
            margin: 4px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 500;
        }}
        .links {{
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }}
        .link {{
            display: inline-block;
            padding: 12px 24px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 500;
            transition: background-color 0.3s;
        }}
        .link:hover {{
            background: #2980b9;
        }}
        .link.youtube {{
            background: #e74c3c;
        }}
        .link.youtube:hover {{
            background: #c0392b;
        }}
        @media (max-width: 600px) {{
            .container {{
                padding: 20px;
                margin: 10px;
            }}
            h1 {{
                font-size: 1.8em;
            }}
            .links {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body><p style="margin-bottom: 1.5em;"><a href="https://www.julien.org" style="color: #6366f1; text-decoration: none;">&larr; julien.org</a></p>
    <div class="container">
        <h1>{html.escape(item.title)}</h1>
        <div class="date">{display_date}</div>

        <div class="video-container">
            <iframe src="https://www.youtube.com/embed/{item.youtube_id}" allowfullscreen="" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture">
            </iframe>
        </div>

        <div class="description">{html.escape(description)}

<a href="{item.link}" target="_blank" rel="noopener noreferrer">Read full post on Substack &rarr;</a></div>

        <div class="tags">
            <h2>Tags</h2>
            <span class="tag">AI</span><span class="tag">Machine Learning</span><span class="tag">Technology</span>
        </div>

        <div class="links">

        </div>
    </div>


</body></html>'''

    if not dry_run:
        year_dir.mkdir(parents=True, exist_ok=True)
        filepath.write_text(html_content, encoding='utf-8')

    return filepath


def create_article_page(item: PostItem, dry_run: bool) -> Path:
    """Create an article folder with index.html and metadata.json."""
    date_str = item.pub_date.strftime('%Y-%m-%d')
    slug = slugify(item.title)
    folder_name = f"{date_str}_{slug}"

    folder_path = PUBLIC / "blog" / "industry-perspectives" / folder_name
    index_path = folder_path / "index.html"
    metadata_path = folder_path / "metadata.json"

    # Format date for display
    display_date = item.pub_date.strftime('%B %d, %Y').replace(' 0', ' ')

    # Get first paragraph as excerpt
    excerpt = item.description
    if len(excerpt) > 200:
        excerpt = excerpt[:197] + '...'

    # Create HTML
    html_content = f'''<!DOCTYPE html><html lang="en"><head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(item.title)} - Julien Simon</title>
    <meta name="author" content="Julien Simon">
    <meta name="date" content="{date_str}">
    <meta name="source" content="{item.link}">
    <link rel="stylesheet" href="../../../css/minimal-blog-styles.css">
</head>
<body><p style="margin-bottom: 1.5em;"><a href="https://www.julien.org" style="color: #6366f1; text-decoration: none;">&larr; julien.org</a></p>
    <h1>{html.escape(item.title)}</h1>
    <div class="meta">
        <p><strong>Author:</strong> Julien Simon</p>
        <p><strong>Date:</strong> {display_date}</p>
        <p><strong>Source:</strong> <a href="{item.link}">{item.link}</a></p>
    </div>
    <div class="content">
        <p>{html.escape(excerpt)}</p>
        <p><a href="{item.link}" target="_blank" rel="noopener noreferrer">Read the full article on Substack &rarr;</a></p>
    </div>



</body></html>'''

    # Create metadata
    metadata = {
        "title": item.title,
        "author": "Julien Simon",
        "date": date_str,
        "description": excerpt,
        "read_time": "5 min read",
        "tags": ["AI", "Technology"],
        "category": "Industry Perspectives",
        "original_url": item.link
    }

    if not dry_run:
        folder_path.mkdir(parents=True, exist_ok=True)
        index_path.write_text(html_content, encoding='utf-8')
        metadata_path.write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')

    return folder_path


def update_year_index(year: int, item: PostItem, dry_run: bool) -> bool:
    """Update the youtube/YYYY/index.html with new video entry.
    Returns True if entry was added, False if it already existed."""
    index_path = PUBLIC / "youtube" / str(year) / "index.html"

    if not index_path.exists():
        print(f"  Warning: Year index not found: {index_path}")
        return False

    content = index_path.read_text(encoding='utf-8')

    # Format date for display
    display_date = item.pub_date.strftime('%B %-d, %Y')
    date_str = item.pub_date.strftime('%Y%m%d')
    filename = f"{date_str}_{title_to_filename(item.title)}"

    # Check if this video is already in the index (by YouTube ID or filename)
    if item.youtube_id and item.youtube_id in content:
        print(f"  Skipped (already in index by YouTube ID): {item.title}")
        return False
    if f'href="{filename}.html"' in content:
        print(f"  Skipped (already in index by filename): {item.title}")
        return False

    # Parse current count
    count_match = re.search(r'(\d+) videos? from', content)
    current_count = int(count_match.group(1)) if count_match else 0
    new_count = current_count + 1

    # Update subtitle count
    new_subtitle = f'{new_count} video{"s" if new_count != 1 else ""} from {year}'
    content = re.sub(
        r'<div class="subtitle">[^<]+</div>',
        f'<div class="subtitle">{new_subtitle}</div>',
        content
    )

    # Create new video entry
    new_entry = f'''<div class="video-item">
<a class="video-title" href="{filename}.html">{html.escape(item.title)}</a>
<div class="video-date">{display_date}</div><div class="video-tags"><span class="video-tag">AI</span><span class="video-tag">Tutorial</span></div>
</div>
'''

    # Insert after video-list opening
    content = re.sub(
        r'(<div class="video-list">)\n',
        f'\\1\n{new_entry}',
        content
    )

    if not dry_run:
        index_path.write_text(content, encoding='utf-8')

    print(f"  Updated {index_path.name}: {current_count} -> {new_count} videos")
    return True


def update_youtube_ts(year: int, videos_to_add: int, dry_run: bool):
    """Update src/data/youtube.ts with new counts."""
    ts_path = SRC / "data" / "youtube.ts"

    if not ts_path.exists():
        print(f"  Warning: youtube.ts not found: {ts_path}")
        return

    content = ts_path.read_text(encoding='utf-8')

    # Update VIDEO_YEARS count for this year
    year_pattern = rf'(\{{\s*year:\s*{year},\s*count:\s*)(\d+)'
    year_match = re.search(year_pattern, content)

    if year_match:
        old_count = int(year_match.group(2))
        new_count = old_count + videos_to_add
        content = re.sub(
            year_pattern,
            f'\\g<1>{new_count}',
            content
        )
        print(f"  Updated VIDEO_YEARS[{year}]: {old_count} -> {new_count}")
    else:
        print(f"  Warning: Year {year} not found in VIDEO_YEARS")

    # Update totalVideos
    total_pattern = r'(totalVideos:\s*)(\d+)'
    total_match = re.search(total_pattern, content)

    if total_match:
        old_total = int(total_match.group(2))
        new_total = old_total + videos_to_add
        content = re.sub(
            total_pattern,
            f'\\g<1>{new_total}',
            content
        )
        print(f"  Updated totalVideos: {old_total} -> {new_total}")

    if not dry_run:
        ts_path.write_text(content, encoding='utf-8')


def update_latest_updates(items: list[PostItem], dry_run: bool):
    """Update LATEST_UPDATES in HomeContent.tsx."""
    home_path = SRC / "app" / "HomeContent.tsx"

    if not home_path.exists():
        print(f"  Warning: HomeContent.tsx not found: {home_path}")
        return

    content = home_path.read_text(encoding='utf-8')

    # Find the LATEST_UPDATES array
    updates_match = re.search(
        r'const LATEST_UPDATES = \[(.*?)\];',
        content,
        re.DOTALL
    )

    if not updates_match:
        print("  Warning: Could not find LATEST_UPDATES array")
        return

    # Parse existing entries
    existing_entries = []
    entry_pattern = r"\{\s*title:\s*['\"](.+?)['\"],\s*href:\s*['\"](.+?)['\"],\s*date:\s*['\"](.+?)['\"],\s*icon:\s*['\"](.+?)['\"],?\s*\}"
    for match in re.finditer(entry_pattern, updates_match.group(1)):
        existing_entries.append({
            'title': match.group(1),
            'href': match.group(2),
            'date': match.group(3),
            'icon': match.group(4),
        })

    # Add new entries at the beginning
    new_entries = []
    for item in sorted(items, key=lambda x: x.pub_date, reverse=True):
        if item.post_type == 'video':
            date_str = item.pub_date.strftime('%Y%m%d')
            filename = f"{date_str}_{title_to_filename(item.title)}"
            href = f"/youtube/{item.pub_date.year}/{filename}.html"
            icon = 'video'
        else:
            date_str = item.pub_date.strftime('%Y-%m-%d')
            slug = slugify(item.title)
            href = f"/blog/industry-perspectives/{date_str}_{slug}/index.html"
            icon = 'article'

        display_date = item.pub_date.strftime('%B %-d, %Y')

        new_entries.append({
            'title': item.title.replace("'", "\\'"),
            'href': href,
            'date': display_date,
            'icon': icon,
        })

    # Merge: new entries first, then existing, keep top 5
    all_entries = new_entries + existing_entries
    all_entries = all_entries[:5]

    # Generate new array content
    entries_str = ',\n  '.join([
        f"{{\n    title: '{e['title']}',\n    href: '{e['href']}',\n    date: '{e['date']}',\n    icon: '{e['icon']}',\n  }}"
        for e in all_entries
    ])

    new_array = f"const LATEST_UPDATES = [\n  {entries_str},\n];"

    # Match the entire LATEST_UPDATES array - from declaration to closing ];
    # Use a lookahead to ensure we stop at the closing ]; followed by whitespace and next const
    content = re.sub(
        r'const LATEST_UPDATES = \[[\s\S]*?\];(?=\s*\nconst )',
        new_array,
        content
    )

    if not dry_run:
        home_path.write_text(content, encoding='utf-8')

    print(f"  Updated LATEST_UPDATES with {len(new_entries)} new items")


def print_summary(new_posts: list[PostItem]):
    """Print summary of detected new posts."""
    print(f"\nNEW POSTS DETECTED ({len(new_posts)}):\n")

    for item in new_posts:
        if item.post_type == 'video':
            date_str = item.pub_date.strftime('%Y%m%d')
            filename = f"{date_str}_{title_to_filename(item.title)}"
            print(f"[VIDEO] {item.title}")
            print(f"  YouTube ID: {item.youtube_id}")
            print(f"  Date: {item.pub_date.strftime('%B %-d, %Y')}")
            print(f"  -> /youtube/{item.pub_date.year}/{filename}.html")
        else:
            date_str = item.pub_date.strftime('%Y-%m-%d')
            slug = slugify(item.title)
            print(f"[ARTICLE] {item.title}")
            print(f"  Date: {item.pub_date.strftime('%B %-d, %Y')}")
            print(f"  -> /blog/industry-perspectives/{date_str}_{slug}/")
        print()


def run(dry_run: bool = False, force: bool = False):
    """Main execution."""
    # Fetch feed
    items = fetch_feed()
    print(f"Found {len(items)} items in feed")

    # Find new posts
    new_posts = get_new_posts(items, force=force)

    if not new_posts:
        print("\nNo new posts detected. Site is up to date!")
        return

    print_summary(new_posts)

    if dry_run:
        print("DRY RUN - No files were modified")
        print("\nRun without --dry-run to apply changes")
        return

    # Process each new post
    videos_added = []
    articles_added = []

    for item in new_posts:
        if item.post_type == 'video':
            filepath = create_video_page(item, dry_run)
            print(f"Created: {filepath}")
            videos_added.append(item)
        else:
            filepath = create_article_page(item, dry_run)
            print(f"Created: {filepath}")
            articles_added.append(item)

    # Update indexes for videos - only count those actually added
    year_video_counts = {}
    for item in videos_added:
        year = item.pub_date.year
        # Add each video to the year index, only count if actually added
        if update_year_index(year, item, dry_run):
            year_video_counts[year] = year_video_counts.get(year, 0) + 1

    # Update youtube.ts with the total count changes per year
    for year, count in year_video_counts.items():
        update_youtube_ts(year, count, dry_run)

    # Update LATEST_UPDATES
    if new_posts:
        update_latest_updates(new_posts, dry_run)

    print(f"\nSync complete!")
    print(f"  Videos added: {len(videos_added)}")
    print(f"  Articles added: {len(articles_added)}")
    print("\nNext steps:")
    print("  1. cd next-site && npm run build")
    print("  2. Verify the build succeeds")
    print("  3. Commit and push changes")


def main():
    parser = argparse.ArgumentParser(
        description='Sync Substack posts to julien.org'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying files'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-sync of all posts, ignoring existing files'
    )
    args = parser.parse_args()

    try:
        run(dry_run=args.dry_run, force=args.force)
    except requests.RequestException as e:
        print(f"Error fetching feed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
