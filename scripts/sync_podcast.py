#!/usr/bin/env python3
"""
Put The AI Realist podcast on the site: a "Listen" player on each article that has an episode, the
episode list behind the /podcast page, and the podcast section of llms.txt and llms-full.txt.

The AI Realist podcast (AI-narrated audio of each Substack piece) is produced by a separate
pipeline in the sibling workspace, ../research/podcast/. This script shares no code with it. It
reads the one public thing that pipeline publishes, the RSS feed, and for every episode whose
link is an article archived here it inserts an audio player above the article body.

Each player sits between two HTML comments, so a rerun replaces it in place: a changed audio
address (a re-rendered episode) or duration updates the page, an unchanged one leaves the file
untouched. The player is placed BEFORE <div class="article-content">, never inside it: the
research workspace reads everything inside that div as the text of the piece. Each player carries
a schema.org PodcastEpisode block, so a search engine knows the article has an audio version.

The same feed read also writes next-site/src/data/podcast-episodes.json, which the /podcast page
renders, and the "## Podcast: The AI Realist" section of the two llms files. Everything written
comes from the feed, so nothing here is edited by hand and a rerun with an unchanged feed writes
nothing.

Usage (stdlib only, any Python 3.9+):
    python3 scripts/sync_podcast.py --dry-run   # Preview changes
    python3 scripts/sync_podcast.py             # Apply changes
    python3 scripts/sync_podcast.py --selftest
"""

import argparse
import email.utils
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
DATA = REPO_ROOT / "next-site" / "src" / "data" / "podcast-episodes.json"
LLMS = (REPO_ROOT / "next-site" / "public" / "llms.txt", REPO_ROOT / "next-site" / "public" / "llms-full.txt")
LLMS_BRIEF = 5                      # episodes listed in llms.txt; llms-full.txt lists them all
SITE_URL = "https://www.julien.org"
SHOW_NAME = "The AI Realist"
SHOW_PAGE = f"{SITE_URL}/podcast"
SERIES_ID = f"{SHOW_PAGE}/#series"   # the PodcastSeries the /podcast page declares
APPLE = "https://podcasts.apple.com/podcast/the-ai-realist/id6819758071"
SPOTIFY = "https://open.spotify.com/show/78U6RiqMDd0wnY3FmJFZGF"
SECTION = "## Podcast: The AI Realist"
ITUNES = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"
BODY = '<div class="article-content">'
START, END = "<!-- podcast:start -->", "<!-- podcast:end -->"
BLOCK = re.compile(r"[ \t]*" + re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.S)


def fetch_feed(url: str = FEED_URL) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "julien.org sync_podcast"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def _ours(url: str, suffix: str) -> bool:
    """True for an https address on the podcast's own host ending in `suffix`: all that is ever written."""
    parts = urllib.parse.urlsplit(url)
    return parts.scheme == "https" and parts.hostname == AUDIO_HOST and parts.path.endswith(suffix)


def _line(text: str, limit: int) -> str:
    """The first line of a feed text, on one line and no longer than `limit`."""
    first = html.unescape(text or "").strip().split("\n", 1)[0]   # a feed text may carry "&#8217;" as written
    return " ".join(first.split())[:limit]


def episodes(feed_xml: str) -> dict[str, dict]:
    """Article URL -> the episode (audio, minutes, seconds, title, date, image, summary), newest first."""
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
        # Only an https MP3 on the podcast's own host is ever written into a page.
        if not link.startswith("https://") or not _ours(audio, ".mp3"):
            continue
        try:
            seconds = int(float(item.findtext(ITUNES + "duration") or 0))
        except ValueError:
            seconds = 0
        try:
            date = email.utils.parsedate_to_datetime(item.findtext("pubDate") or "").date().isoformat()
        except (TypeError, ValueError):
            date = ""
        image = item.find(ITUNES + "image")
        image = image.get("href", "") if image is not None else ""
        out[link] = {"audio": audio, "minutes": max(1, round(seconds / 60)), "seconds": seconds,
                     "title": _line(item.findtext("title"), 200), "date": date,
                     "image": image if _ours(image, ".jpg") else "",
                     "summary": _line(item.findtext("description"), 300)}
    return out


def _json_ld(data: dict) -> str:
    # "<" is written as an escape, so no title can close the script element it sits in.
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")


def episode_schema(article: str, episode: dict) -> dict:
    duration = f"PT{episode['seconds'] // 60}M{episode['seconds'] % 60}S"
    data = {
        "@context": "https://schema.org", "@type": "PodcastEpisode", "name": episode["title"],
        "description": episode["summary"], "datePublished": episode["date"], "timeRequired": duration,
        "inLanguage": "en", "isBasedOn": article, "image": episode["image"],
        "associatedMedia": {"@type": "AudioObject", "contentUrl": episode["audio"],
                            "encodingFormat": "audio/mpeg", "duration": duration},
        "partOfSeries": {"@type": "PodcastSeries", "@id": SERIES_ID, "name": SHOW_NAME,
                         "url": SHOW_PAGE, "webFeed": FEED_URL},
    }
    return {k: v for k, v in data.items() if v}


def player(episode: dict, article: str = "") -> str:
    audio = html.escape(episode["audio"], quote=True)
    link = 'style="color: #6366f1;"'
    return (
        f"        {START}\n"
        '        <div class="podcast-player" style="margin: 1.5em 0; padding: 1em 1.2em; '
        'border: 1px solid #e5e7eb; border-radius: 8px;">\n'
        f'            <p style="margin: 0 0 0.6em 0;"><strong>Listen:</strong> AI-narrated audio of this piece, '
        f'{episode["minutes"]} min. From <a href="{SHOW_PAGE}" {link}>The AI Realist podcast</a>, also on '
        f'<a href="{APPLE}" {link}>Apple Podcasts</a> and <a href="{SPOTIFY}" {link}>Spotify</a>.</p>\n'
        f'            <audio controls preload="none" style="width: 100%;" src="{audio}"></audio>\n'
        f'            <script type="application/ld+json">{_json_ld(episode_schema(article, episode))}</script>\n'
        "        </div>\n"
        f"        {END}\n"
    )


def with_player(page: str, episode: dict | None, article: str = "") -> str:
    """The page with its player set to `episode`, or removed when there is none."""
    page = BLOCK.sub("", page)
    if episode is None or BODY not in page:
        return page
    at = page.index(BODY)
    at = page.rfind("\n", 0, at) + 1          # keep the body div's own indentation
    return page[:at] + player(episode, article) + page[at:]


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
        article = article_url(folder)
        episode = by_url.get(article)
        if episode is None and START not in page:
            continue
        new = with_player(page, episode, article)
        if new != page:
            changed.append(folder.name)
            if not dry_run:
                page_path.write_text(new, encoding="utf-8")
    return changed


def listing(feed_xml: str, articles: Path) -> list[dict]:
    """The episodes as the /podcast page lists them, newest first. `page` is the article's own page
    on this site when it is archived here, where the player is."""
    local = {article_url(p): p.name for p in sorted(articles.iterdir()) if (p / "index.html").is_file()}
    return [{"title": e["title"], "date": e["date"], "minutes": e["minutes"], "seconds": e["seconds"],
             "summary": e["summary"], "audio": e["audio"], "image": e["image"], "article": url,
             "page": f"/blog/industry-perspectives/{local[url]}/" if url in local else ""}
            for url, e in episodes(feed_xml).items()]


def write_if_changed(path: Path, text: str, dry_run: bool) -> bool:
    if path.is_file() and path.read_text(encoding="utf-8") == text:
        return False
    if not dry_run:
        path.write_text(text, encoding="utf-8")
    return True


def llms_section(rows: list[dict], limit: int | None = None) -> str:
    """The podcast as the llms files describe it. Dated by its newest episode, so a rerun is a no-op."""
    shown = rows[:limit] if limit else rows
    lines = [SECTION, "",
             f"The AI Realist podcast is the audio edition of Julien Simon's newsletter on the AI industry. Each "
             f"episode is one written piece, narrated by an AI voice. {len(rows)} episodes as of "
             f"{rows[0]['date'] if rows else 'launch'}.", "",
             f"- [Podcast page]({SHOW_PAGE}): every episode, with a player and a link to the written piece",
             f"- [RSS feed]({FEED_URL}): audio, chapters and a WebVTT transcript for each episode",
             f"- [Apple Podcasts]({APPLE})", f"- [Spotify]({SPOTIFY})", "",
             "Latest episodes:" if limit and len(rows) > limit else "Episodes:"]
    lines += [f"- **{e['title']}** ({e['date']}, {e['minutes']} min): {e['summary']} Written piece: {e['article']}"
              for e in shown]
    return "\n".join(lines) + "\n"


def with_section(text: str, section: str) -> str:
    """`text` with its podcast section replaced, or added before the blog or YouTube section."""
    found = re.search(r"^" + re.escape(SECTION) + r"\n.*?(?=^## |\Z)", text, re.S | re.M)
    if found:
        return text[:found.start()] + section + "\n" + text[found.end():]
    for anchor in ("## Blog Categories\n", "## YouTube\n"):
        at = text.find("\n" + anchor)
        if at != -1:
            return text[:at + 1] + section + "\n" + text[at + 1:]
    return text.rstrip("\n") + "\n\n" + section


def selftest() -> None:
    import tempfile
    feed = f"""<?xml version="1.0"?><rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0"><channel>
<item><title>A &lt;/script&gt; Piece</title><link>https://www.airealist.ai/p/a-piece</link><pubDate>Mon, 28 Sep 2026 16:04:13 +0000</pubDate>
<description>The piece&amp;#8217;s subtitle.

AI-generated narration of it.</description><itunes:image href="https://{AUDIO_HOST}/episodes/a.jpg"/>
<enclosure url="https://{AUDIO_HOST}/episodes/a.mp3" length="1" type="audio/mpeg"/><itunes:duration>687</itunes:duration></item>
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
        block = out[out.index(START):out.index(END)]
        assert block.count("</script>") == 1, "a title closed the structured-data script"
        ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', block, re.S).group(1))
        assert (ld["@type"], ld["name"], ld["datePublished"], ld["timeRequired"]) == ("PodcastEpisode", "A </script> Piece", "2026-09-28", "PT11M27S")
        assert ld["associatedMedia"]["contentUrl"].endswith("/episodes/a.mp3") and ld["isBasedOn"].endswith("/p/a-piece")
        assert ld["partOfSeries"]["@id"] == SERIES_ID and ld["image"].endswith("/episodes/a.jpg") and ld["description"] == "The piece\u2019s subtitle."
        assert out.index(START) < out.index(BODY), "the player must sit before the article body"
        assert out[out.index(BODY):] == page[page.index(BODY):], "the article body changed"
        assert "evil.example" not in (root / "2026-01-02_evil" / "index.html").read_text(), "foreign audio host written"
        assert sync(feed, root, dry_run=False) == [], "second run is not a no-op"

        moved = feed.replace("episodes/a.mp3", "episodes/a.v2.mp3").replace(">687<", ">700<")
        assert sync(moved, root, dry_run=False) == ["2026-01-01_a-piece"]
        out = a.read_text()
        assert "a.v2.mp3" in out and "a.mp3\"" not in out and out.count(START) == 1 and "12 min" in out

        rows = listing(feed, root)
        assert [(r["title"], r["page"], r["minutes"]) for r in rows] == [
            ("A </script> Piece", "/blog/industry-perspectives/2026-01-01_a-piece/", 11), ("", "", 1)], rows
        assert all("evil.example" not in json.dumps(r) for r in rows), "foreign audio host listed"
        data = root / "episodes.json"
        text = json.dumps(rows, ensure_ascii=False, indent=2) + "\n"
        assert write_if_changed(data, text, dry_run=True) and not data.exists(), "dry run wrote the data file"
        assert write_if_changed(data, text, dry_run=False) and not write_if_changed(data, text, dry_run=False)
        section = llms_section(rows, limit=1)
        assert "2 episodes as of 2026-09-28" in section and "Latest episodes:" in section and section.count("\n- **") == 1
        llms = "# Me\n\n## Pages\n\n- a\n\n## Blog Categories\n\n- b\n"
        once = with_section(llms, section)
        assert once.index(SECTION) < once.index("## Blog Categories") and once.endswith("## Blog Categories\n\n- b\n")
        assert with_section(once, section) == once, "the llms section is not idempotent"
        assert with_section(once, llms_section(rows)).count(SECTION) == 1 and with_section("# Me\n", section).endswith(section)

        gone = feed.replace("https://www.airealist.ai/p/a-piece", "https://www.airealist.ai/p/other")
        assert sync(gone, root, dry_run=False) == ["2026-01-01_a-piece"] and a.read_text() == page, "player not removed cleanly"
    for bad in ('<?xml version="1.0"?><!DOCTYPE x [<!ENTITY a "aaaa">]><rss><channel/></rss>', "x" * (MAX_FEED_BYTES + 1)):
        try:
            episodes(bad)
        except ValueError:
            continue
        raise AssertionError("a feed with a DTD or of absurd size was parsed")
    print("ok: insert, idempotence, moved audio, removal, foreign host refused, body untouched, DTD refused, "
          "structured data, episode list, llms section")


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
    rows = listing(feed_xml, ARTICLES)
    files = [(DATA, json.dumps(rows, ensure_ascii=False, indent=2) + "\n")]
    files += [(path, with_section(path.read_text(encoding="utf-8"), llms_section(rows, LLMS_BRIEF if path.name == "llms.txt" else None)))
              for path in LLMS if path.is_file()]
    for path, text in files:
        if write_if_changed(path, text, args.dry_run):
            print(f"  {verb.lower()} {path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
