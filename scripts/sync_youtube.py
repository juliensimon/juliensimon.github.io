#!/usr/bin/env python3
"""
Sync YouTube videos to julien.org

Fetches the latest videos from the YouTube channel feed
and creates the appropriate HTML files on the website.

Usage:
    python sync_youtube.py --dry-run  # Preview changes
    python sync_youtube.py            # Apply changes
"""

import argparse
import html
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import NamedTuple

import requests
import xml.etree.ElementTree as ET

# YouTube channel
CHANNEL_HANDLE = "juliensimonfr"
CHANNEL_ID = "UCVonoXm3SI_Q0ZNHd5JPawA"

# Paths
REPO_ROOT = Path(__file__).parent.parent
BASE = REPO_ROOT / "next-site"
PUBLIC = BASE / "public"
SRC = BASE / "src"
REPO_YOUTUBE = REPO_ROOT / "youtube"

# Namespaces for YouTube Atom feed
NS = {
    'atom': 'http://www.w3.org/2005/Atom',
    'yt': 'http://www.youtube.com/xml/schemas/2015',
    'media': 'http://search.yahoo.com/mrss/',
}


class VideoItem(NamedTuple):
    """Parsed YouTube video entry."""
    video_id: str
    title: str
    published: datetime
    description: str


def resolve_channel_id(handle: str) -> str:
    """Resolve a YouTube @handle to a channel ID by fetching the channel page."""
    url = f"https://www.youtube.com/@{handle}"
    print(f"Resolving channel ID for @{handle}...")
    response = requests.get(url, timeout=15, headers={
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0'
        ),
        'Accept-Language': 'en-US,en;q=0.9',
    })
    response.raise_for_status()

    # Extract channel ID from page source (broad match)
    match = re.search(r'(UC[a-zA-Z0-9_-]{22})', response.text)
    if match:
        return match.group(1)

    raise ValueError(f"Could not resolve channel ID for @{handle}")


def fetch_feed(channel_id: str) -> list[VideoItem]:
    """Fetch and parse the YouTube Atom feed (returns ~15 most recent videos)."""
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    print(f"Fetching {url}...")
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    videos = []

    for entry in root.findall('atom:entry', NS):
        video_id = entry.findtext('yt:videoId', '', NS)
        title = entry.findtext('atom:title', '', NS).strip()
        pub_str = entry.findtext('atom:published', '', NS)

        # Get description from media:group/media:description
        media_group = entry.find('media:group', NS)
        description = ''
        if media_group is not None:
            description = media_group.findtext(
                'media:description', '', NS
            ).strip()

        # Parse ISO 8601 date
        try:
            published = datetime.fromisoformat(pub_str.replace('Z', '+00:00'))
            published = published.replace(tzinfo=None)
        except ValueError:
            published = datetime.now()

        if video_id and title:
            videos.append(VideoItem(
                video_id=video_id,
                title=title,
                published=published,
                description=description,
            ))

    return videos


def is_short(video_id: str) -> bool:
    """Check if a video is a YouTube Short by probing the /shorts/ URL.
    If /shorts/<id> stays on /shorts/, it's a Short. If it redirects to
    /watch, it's a regular video."""
    try:
        resp = requests.head(
            f"https://www.youtube.com/shorts/{video_id}",
            allow_redirects=True,
            timeout=10,
            headers={
                'User-Agent': (
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                    'AppleWebKit/537.36'
                ),
            },
        )
        return '/shorts/' in resp.url
    except requests.RequestException:
        return False


def filter_shorts(videos: list[VideoItem]) -> list[VideoItem]:
    """Remove YouTube Shorts from the video list."""
    filtered = []
    for video in videos:
        if is_short(video.video_id):
            print(f"  Skipping Short: {video.title}")
        else:
            filtered.append(video)
    return filtered


def title_to_filename(title: str) -> str:
    """Convert title to filename format (Title_Words_Here)."""
    clean = re.sub(r'[^\w\s-]', '', title)
    return re.sub(r'\s+', '_', clean.strip())


def is_video_existing(year: int, youtube_id: str) -> bool:
    """Check if a video with this YouTube ID already exists on the site."""
    # Check both locations
    for base_dir in [PUBLIC / "youtube", REPO_YOUTUBE]:
        year_dir = base_dir / str(year)
        if not year_dir.exists():
            continue
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


def is_substack_content(video: VideoItem) -> bool:
    """Check if a video's description indicates it's a Substack blog post
    rather than a genuine YouTube video. Substack posts sometimes appear
    in YouTube feeds when they contain embedded videos."""
    desc_lower = video.description.lower()
    substack_signals = [
        'airealist.ai',
        'read full post on substack',
        'substack.com',
    ]
    return any(signal in desc_lower for signal in substack_signals)


def get_new_videos(
    videos: list[VideoItem], force: bool = False,
) -> list[VideoItem]:
    """Filter to only new videos not yet on the site."""
    if force:
        return videos

    new_videos = []
    for video in videos:
        if is_substack_content(video):
            print(f"  Skipping Substack content: {video.title}")
            continue
        year = video.published.year
        if not is_video_existing(year, video.video_id):
            new_videos.append(video)

    return new_videos


def create_video_page(video: VideoItem, dry_run: bool) -> Path:
    """Create a video HTML page."""
    year = video.published.year
    date_str = video.published.strftime('%Y%m%d')
    filename = f"{date_str}_{title_to_filename(video.title)}"
    display_date = video.published.strftime('%B %d, %Y').replace(' 0', ' ')

    # Truncate description for display if very long
    description = video.description
    if len(description) > 2000:
        description = description[:2000] + '...'

    html_content = f'''<!DOCTYPE html><html lang="en"><head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(video.title)}</title>
    <meta name="description" content="{html.escape(video.title)} - YouTube video by Julien Simon">
    <meta property="og:title" content="{html.escape(video.title)}">
    <meta property="og:type" content="video.other">
    <meta property="og:url" content="https://www.julien.org/youtube/{year}/{date_str}_{title_to_filename(video.title)}.html">
    <link rel="canonical" href="https://www.julien.org/youtube/{year}/{date_str}_{title_to_filename(video.title)}.html">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../style.css">
    <script defer src="https://cloud.umami.is/script.js" data-website-id="27550dad-d418-4f5d-ad1b-dab573da1020"></script>
</head>
<body>
    <div class="back-link"><a href="https://www.julien.org">&larr; julien.org</a></div>
    <div class="container">
        <h1>{html.escape(video.title)}</h1>
        <div class="date">{display_date}</div>

        <div class="video-container">
            <iframe src="https://www.youtube.com/embed/{video.video_id}" allowfullscreen="" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture">
            </iframe>
        </div>

        <div class="description">{html.escape(description)}</div>

        <div class="tags">
            <h2>Tags</h2>
            <span class="tag">AI</span><span class="tag">Machine Learning</span><span class="tag">Technology</span>
        </div>

        <div class="links">

        </div>
    </div>


</body></html>'''

    # Write to both locations
    for base_dir in [PUBLIC / "youtube", REPO_YOUTUBE]:
        year_dir = base_dir / str(year)
        filepath = year_dir / f"{filename}.html"
        if not dry_run:
            year_dir.mkdir(parents=True, exist_ok=True)
            filepath.write_text(html_content, encoding='utf-8')

    return PUBLIC / "youtube" / str(year) / f"{filename}.html"


def _sort_video_entries(content: str) -> str:
    """Sort video-item entries in an index page by date (newest first).

    Splits the video-list div into individual video-item blocks,
    sorts them by the YYYYMMDD prefix in their href filename,
    and reassembles the HTML.
    """
    marker = '<div class="video-list">'
    end_marker = '<div class="links">'

    start = content.find(marker)
    end = content.find(end_marker)
    if start == -1 or end == -1:
        return content

    before = content[:start + len(marker)]
    after = content[end:]
    list_html = content[start + len(marker):end]

    # Split into individual items at each <div class="video-item"> boundary
    parts = re.split(r'(?=<div class="video-item">)', list_html.strip())
    items = [p.strip() for p in parts if p.strip()]

    if len(items) < 2:
        return content

    # Sort by date extracted from href filename (YYYYMMDD prefix)
    def sort_key(item_html: str) -> str:
        m = re.search(r'href="(\d{8})_', item_html)
        return m.group(1) if m else '00000000'

    items.sort(key=sort_key, reverse=True)

    return before + '\n' + '\n'.join(items) + '\n' + after


def update_year_index(year: int, video: VideoItem, dry_run: bool) -> bool:
    """Update the youtube/YYYY/index.html with a new video entry.
    Returns True if the entry was added."""
    date_str = video.published.strftime('%Y%m%d')
    filename = f"{date_str}_{title_to_filename(video.title)}"
    display_date = video.published.strftime('%B %-d, %Y')

    added = False
    for base_dir in [PUBLIC / "youtube", REPO_YOUTUBE]:
        index_path = base_dir / str(year) / "index.html"
        if not index_path.exists():
            continue

        content = index_path.read_text(encoding='utf-8')

        # Skip if already present
        if video.video_id in content or f'href="{filename}.html"' in content:
            continue

        # Update video count in subtitle
        count_match = re.search(r'(\d+) videos? from', content)
        current_count = int(count_match.group(1)) if count_match else 0
        new_count = current_count + 1
        new_subtitle = (
            f'{new_count} video{"s" if new_count != 1 else ""} from {year}'
        )
        content = re.sub(
            r'<div class="subtitle">[^<]+</div>',
            f'<div class="subtitle">{new_subtitle}</div>',
            content,
        )

        # Create new video entry
        new_entry = (
            f'<div class="video-item">\n'
            f'<a class="video-title" href="{filename}.html">'
            f'{html.escape(video.title)}</a>\n'
            f'<div class="video-date">{display_date}</div>'
            f'<div class="video-tags">'
            f'<span class="video-tag">AI</span>'
            f'<span class="video-tag">Tutorial</span>'
            f'</div>\n'
            f'</div>\n'
        )

        # Insert after video-list opening tag
        content = re.sub(
            r'(<div class="video-list">)\n',
            f'\\1\n{new_entry}',
            content,
        )

        # Re-sort all entries by date (newest first)
        content = _sort_video_entries(content)

        if not dry_run:
            index_path.write_text(content, encoding='utf-8')

        added = True

    if added:
        print(f"  Updated year index for {year}")

    return added


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
        content = re.sub(year_pattern, f'\\g<1>{new_count}', content)
        print(f"  Updated VIDEO_YEARS[{year}]: {old_count} -> {new_count}")
    else:
        # Year not in list yet — add it at the top of VIDEO_YEARS
        new_entry = (
            f"  {{ year: {year}, count: {videos_to_add}, "
            f"href: '/youtube/{year}/index.html' }},\n"
        )
        content = content.replace(
            'export const VIDEO_YEARS: VideoYear[] = [\n',
            f'export const VIDEO_YEARS: VideoYear[] = [\n{new_entry}',
        )
        print(f"  Added new year {year} with {videos_to_add} videos")

    # Update totalVideos
    total_pattern = r'(totalVideos:\s*)(\d+)'
    total_match = re.search(total_pattern, content)
    if total_match:
        old_total = int(total_match.group(2))
        new_total = old_total + videos_to_add
        content = re.sub(total_pattern, f'\\g<1>{new_total}', content)
        print(f"  Updated totalVideos: {old_total} -> {new_total}")

    if not dry_run:
        ts_path.write_text(content, encoding='utf-8')


def update_latest_updates(videos: list[VideoItem], dry_run: bool):
    """Update LATEST_UPDATES in HomeContent.tsx."""
    home_path = SRC / "app" / "HomeContent.tsx"
    if not home_path.exists():
        print(f"  Warning: HomeContent.tsx not found: {home_path}")
        return

    content = home_path.read_text(encoding='utf-8')

    updates_match = re.search(
        r'const LATEST_UPDATES = \[(.*?)\];',
        content,
        re.DOTALL,
    )
    if not updates_match:
        print("  Warning: Could not find LATEST_UPDATES array")
        return

    # Parse existing entries
    existing_entries = []
    entry_pattern = (
        r"\{\s*title:\s*['\"](.+?)['\"],\s*href:\s*['\"](.+?)['\"],"
        r"\s*date:\s*['\"](.+?)['\"],\s*icon:\s*['\"](.+?)['\"],?\s*\}"
    )
    for match in re.finditer(entry_pattern, updates_match.group(1)):
        existing_entries.append({
            'title': match.group(1),
            'href': match.group(2),
            'date': match.group(3),
            'icon': match.group(4),
        })

    # Build new entries (newest first)
    new_entries = []
    for video in sorted(videos, key=lambda v: v.published, reverse=True):
        date_str = video.published.strftime('%Y%m%d')
        filename = f"{date_str}_{title_to_filename(video.title)}"
        href = f"/youtube/{video.published.year}/{filename}.html"
        display_date = video.published.strftime('%B %-d, %Y')

        new_entries.append({
            'title': video.title.replace("'", "\\'"),
            'href': href,
            'date': display_date,
            'icon': 'video',
        })

    # Merge: new first, then existing (no duplicates), keep top 5
    seen_hrefs = {e['href'] for e in new_entries}
    unique_existing = [e for e in existing_entries if e['href'] not in seen_hrefs]
    all_entries = (new_entries + unique_existing)[:5]

    entries_str = ',\n  '.join([
        f"{{\n    title: '{e['title']}',\n    href: '{e['href']}',"
        f"\n    date: '{e['date']}',\n    icon: '{e['icon']}',\n  }}"
        for e in all_entries
    ])
    new_array = f"const LATEST_UPDATES = [\n  {entries_str},\n];"

    content = re.sub(
        r'const LATEST_UPDATES = \[[\s\S]*?\];(?=\s*\nconst )',
        new_array,
        content,
    )

    if not dry_run:
        home_path.write_text(content, encoding='utf-8')

    print(f"  Updated LATEST_UPDATES with {len(new_entries)} new videos")


def print_summary(new_videos: list[VideoItem]):
    """Print summary of detected new videos."""
    print(f"\nNEW VIDEOS DETECTED ({len(new_videos)}):\n")

    for video in new_videos:
        date_str = video.published.strftime('%Y%m%d')
        filename = f"{date_str}_{title_to_filename(video.title)}"
        print(f"  {video.title}")
        print(f"    YouTube ID: {video.video_id}")
        print(f"    Date: {video.published.strftime('%B %-d, %Y')}")
        print(f"    -> /youtube/{video.published.year}/{filename}.html")
        print()


def run(
    dry_run: bool = False,
    force: bool = False,
    channel_id: str | None = None,
    include_shorts: bool = False,
):
    """Main execution."""
    # Use hardcoded channel ID, resolve from handle, or use provided value
    if not channel_id:
        channel_id = CHANNEL_ID
    print(f"Channel ID: {channel_id}")

    # Fetch feed
    videos = fetch_feed(channel_id)
    print(f"Found {len(videos)} videos in feed")

    # Filter out Shorts (unless --include-shorts)
    if not include_shorts:
        print("Checking for Shorts...")
        videos = filter_shorts(videos)
        print(f"{len(videos)} regular videos after filtering Shorts")

    # Find new videos
    new_videos = get_new_videos(videos, force=force)

    if not new_videos:
        print("\nNo new videos detected. Site is up to date!")
        return

    print_summary(new_videos)

    if dry_run:
        print("DRY RUN - No files were modified")
        print("\nRun without --dry-run to apply changes")
        return

    # Create video pages
    for video in new_videos:
        filepath = create_video_page(video, dry_run)
        print(f"Created: {filepath}")

    # Update year indexes and collect counts
    year_video_counts: dict[int, int] = {}
    for video in new_videos:
        year = video.published.year
        if update_year_index(year, video, dry_run):
            year_video_counts[year] = year_video_counts.get(year, 0) + 1

    # Update youtube.ts counts
    for year, count in year_video_counts.items():
        update_youtube_ts(year, count, dry_run)

    # Update LATEST_UPDATES
    update_latest_updates(new_videos, dry_run)

    print(f"\nSync complete! {len(new_videos)} videos added.")
    print("\nNext steps:")
    print("  1. cd next-site && npm run build")
    print("  2. Verify the build succeeds")
    print("  3. Commit and push changes")


def main():
    parser = argparse.ArgumentParser(
        description='Sync YouTube videos to julien.org',
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying files',
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-sync of all videos from the feed',
    )
    parser.add_argument(
        '--channel-id',
        type=str,
        default=None,
        help='YouTube channel ID (auto-resolved from handle if omitted)',
    )
    parser.add_argument(
        '--include-shorts',
        action='store_true',
        help='Include YouTube Shorts (excluded by default)',
    )
    args = parser.parse_args()

    try:
        run(
            dry_run=args.dry_run,
            force=args.force,
            channel_id=args.channel_id,
            include_shorts=args.include_shorts,
        )
    except requests.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
