#!/usr/bin/env python3
"""
Add a "Listen" player to the Industry Perspectives articles that have a podcast episode.

The AI Realist podcast (AI-narrated audio of each Substack piece) is produced by a separate
pipeline in the sibling workspace, ../research/podcast/. This script shares no code with it. It
reads the one public thing that pipeline publishes, the RSS feed, and for every episode whose
link is an article archived here it inserts an audio player above the article body.

Each player sits between two HTML comments, so a rerun replaces it in place: a changed audio
address (a re-rendered episode) or duration updates the page, an unchanged one leaves the file
untouched. The player is placed BEFORE <div class="article-content">, never inside it: the
research workspace reads everything inside that div as the text of the piece.

Usage (stdlib only, any Python 3.9+):
    python3 scripts/sync_podcast.py --dry-run   # Preview changes
    python3 scripts/sync_podcast.py             # Apply changes
    python3 scripts/sync_podcast.py --selftest
"""

import argparse
import html
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

FEED_URL = "https://podcast.julien.org/feed.xml"
AUDIO_HOST = "podcast.julien.org"
MAX_FEED_BYTES = 5 * 1024 * 1024
REPO_ROOT = Path(__file__).resolve().parent.parent
ARTICLES = REPO_ROOT / "next-site" / "public" / "blog" / "industry-perspectives"
ITUNES = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"
BODY = '<div class="article-content">'
START, END = "<!-- podcast:start -->", "<!-- podcast:end -->"
BLOCK = re.compile(r"[ \t]*" + re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.S)


def fetch_feed(url: str = FEED_URL) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "julien.org sync_podcast"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def episodes(feed_xml: str) -> dict[str, dict]:
    """Article URL -> {"audio": url, "minutes": int} for every episode in the feed."""
    # Stdlib XML parsing expands entities. This feed is ours, but it arrives over the network: refuse
    # anything that declares a DTD or an entity, and anything far larger than a feed should be.
    if len(feed_xml) > MAX_FEED_BYTES or "<!DOCTYPE" in feed_xml or "<!ENTITY" in feed_xml:
        raise ValueError("not a feed this script reads: too large, or it carries a DTD")
    out = {}
    channel = ET.fromstring(feed_xml).find("channel")
    for item in channel.findall("item") if channel is not None else []:
        link = (item.findtext("link") or "").strip().rstrip("/")
        enclosure = item.find("enclosure")
        audio = enclosure.get("url", "") if enclosure is not None else ""
        parts = urllib.parse.urlsplit(audio)
        # Only an https MP3 on the podcast's own host is ever written into a page.
        if not link or parts.scheme != "https" or parts.hostname != AUDIO_HOST or not parts.path.endswith(".mp3"):
            continue
        try:
            seconds = int(float(item.findtext(ITUNES + "duration") or 0))
        except ValueError:
            seconds = 0
        out[link] = {"audio": audio, "minutes": max(1, round(seconds / 60))}
    return out


def player(episode: dict) -> str:
    audio = html.escape(episode["audio"], quote=True)
    return (
        f"        {START}\n"
        '        <div class="podcast-player" style="margin: 1.5em 0; padding: 1em 1.2em; '
        'border: 1px solid #e5e7eb; border-radius: 8px;">\n'
        f'            <p style="margin: 0 0 0.6em 0;"><strong>Listen:</strong> AI-narrated audio of this piece, '
        f'{episode["minutes"]} min. From <a href="{FEED_URL}" style="color: #6366f1;">The AI Realist podcast</a>.</p>\n'
        f'            <audio controls preload="none" style="width: 100%;" src="{audio}"></audio>\n'
        "        </div>\n"
        f"        {END}\n"
    )


def with_player(page: str, episode: dict | None) -> str:
    """The page with its player set to `episode`, or removed when there is none."""
    page = BLOCK.sub("", page)
    if episode is None or BODY not in page:
        return page
    at = page.index(BODY)
    at = page.rfind("\n", 0, at) + 1          # keep the body div's own indentation
    return page[:at] + player(episode) + page[at:]


def article_url(folder: Path) -> str:
    try:
        meta = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ""
    return (meta.get("original_url") or "").strip().rstrip("/")


def sync(feed_xml: str, articles: Path, dry_run: bool) -> list[str]:
    by_url = episodes(feed_xml)
    changed = []
    for folder in sorted(p for p in articles.iterdir() if (p / "index.html").is_file()):
        page_path = folder / "index.html"
        page = page_path.read_text(encoding="utf-8")
        episode = by_url.get(article_url(folder))
        if episode is None and START not in page:
            continue
        new = with_player(page, episode)
        if new != page:
            changed.append(folder.name)
            if not dry_run:
                page_path.write_text(new, encoding="utf-8")
    return changed


def selftest() -> None:
    import tempfile
    feed = f"""<?xml version="1.0"?><rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0"><channel>
<item><link>https://www.airealist.ai/p/a-piece</link><enclosure url="https://{AUDIO_HOST}/episodes/a.mp3" length="1" type="audio/mpeg"/><itunes:duration>687</itunes:duration></item>
<item><link>https://www.airealist.ai/p/evil</link><enclosure url="https://evil.example/x.mp3" length="1" type="audio/mpeg"/></item>
<item><link>https://www.airealist.ai/p/not-here</link><enclosure url="https://{AUDIO_HOST}/episodes/n.mp3" length="1" type="audio/mpeg"/></item>
</channel></rss>"""
    page = ('<html><body>\n    <article>\n        <h1>T</h1>\n        <div class="meta">\n            <p>m</p>\n        </div>\n'
            '        <div class="article-content">\n<p>Body text.</p>\n</div>\n    </article>\n</body></html>\n')
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for name, url in (("2026-01-01_a-piece", "https://www.airealist.ai/p/a-piece"),
                          ("2026-01-02_evil", "https://www.airealist.ai/p/evil"),
                          ("2026-01-03_no-episode", "https://www.airealist.ai/p/no-episode")):
            (root / name).mkdir()
            (root / name / "index.html").write_text(page, encoding="utf-8")
            (root / name / "metadata.json").write_text(json.dumps({"original_url": url}), encoding="utf-8")
        a = root / "2026-01-01_a-piece" / "index.html"

        assert sync(feed, root, dry_run=True) == ["2026-01-01_a-piece"] and a.read_text() == page, "dry run wrote"
        assert sync(feed, root, dry_run=False) == ["2026-01-01_a-piece"]
        out = a.read_text()
        assert f'src="https://{AUDIO_HOST}/episodes/a.mp3"' in out and "11 min" in out
        assert out.index(START) < out.index(BODY), "the player must sit before the article body"
        assert out[out.index(BODY):] == page[page.index(BODY):], "the article body changed"
        assert "evil.example" not in (root / "2026-01-02_evil" / "index.html").read_text(), "foreign audio host written"
        assert sync(feed, root, dry_run=False) == [], "second run is not a no-op"

        moved = feed.replace("episodes/a.mp3", "episodes/a.v2.mp3").replace(">687<", ">700<")
        assert sync(moved, root, dry_run=False) == ["2026-01-01_a-piece"]
        out = a.read_text()
        assert "a.v2.mp3" in out and "a.mp3\"" not in out and out.count(START) == 1 and "12 min" in out

        gone = feed.replace("https://www.airealist.ai/p/a-piece", "https://www.airealist.ai/p/other")
        assert sync(gone, root, dry_run=False) == ["2026-01-01_a-piece"] and a.read_text() == page, "player not removed cleanly"
    for bad in ('<?xml version="1.0"?><!DOCTYPE x [<!ENTITY a "aaaa">]><rss><channel/></rss>', "x" * (MAX_FEED_BYTES + 1)):
        try:
            episodes(bad)
        except ValueError:
            continue
        raise AssertionError("a feed with a DTD or of absurd size was parsed")
    print("ok: insert, idempotence, moved audio, removal, foreign host refused, body untouched, DTD refused")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    try:
        feed_xml = fetch_feed()
        count = len(episodes(feed_xml))
    except Exception as error:  # the podcast feed being down must not fail a site sync
        print(f"Podcast feed not read ({error}); article pages left as they are.")
        return
    changed = sync(feed_xml, ARTICLES, args.dry_run)
    verb = "Would update" if args.dry_run else "Updated"
    print(f"Podcast feed: {count} episode(s). {verb} {len(changed)} article page(s).")
    for name in changed:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
