#!/usr/bin/env python3
"""Rebuild blog/arcee-posts/index.html as a real section hub.

That URL is linked from the three sibling hubs (AWS, Hugging Face, Industry
Perspectives) as a peer listing, but it held a stray full copy of the MCP
article instead — wrong <title>, og:type=article, 11 <h1>s, and duplicate
content against the copy under industry-perspectives.

Clones the Hugging Face hub as the template so the styling stays in one place,
and fills it from the arcee post folders' own metadata.
"""
import html
import pathlib
import re
from collections import defaultdict
from datetime import datetime

PUBLIC = pathlib.Path(__file__).resolve().parent.parent / "next-site" / "public"
BLOG = PUBLIC / "blog"
TEMPLATE = BLOG / "huggingface-posts-and-images" / "index.html"
TARGET = BLOG / "arcee-posts" / "index.html"
URL = "https://www.julien.org/blog/arcee-posts/"
TITLE = "Arcee AI Blog Posts – Julien Simon"
HEADING = "Arcee AI Blog Posts"
BLURB = ("Technical articles written at Arcee AI on small language models, CPU and "
         "Arm inference, model routing, and the Arcee Foundation Model family.")


def post_meta(folder):
    """Title and publication date, read from the post's own page."""
    doc = (folder / "index.html").read_text(encoding="utf-8", errors="ignore")
    t = re.search(r"<title>(.*?)</title>", doc, re.S | re.I)
    title = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", t.group(1)))).strip() if t else folder.name
    title = re.sub(r"\s+[-–]\s+Julien Simon$", "", title)
    d = re.search(r'article:published_time"[^>]*content="([^"]+)"', doc) or \
        re.search(r'content="([^"]+)"[^>]*property="article:published_time"', doc)
    raw = d.group(1) if d else folder.name[:10]
    try:
        date = datetime.fromisoformat(raw.replace("Z", "+00:00")).date()
    except ValueError:
        date = datetime.strptime(folder.name[:10], "%Y-%m-%d").date()
    return title, date


def main():
    folders = sorted((p for p in (BLOG / "arcee-posts").iterdir()
                      if p.is_dir() and (p / "index.html").exists()),
                     key=lambda p: p.name, reverse=True)
    posts = [(f, *post_meta(f)) for f in folders]

    by_year = defaultdict(list)
    for folder, title, date in posts:
        by_year[date.year].append((folder, title, date))

    sections = []
    for year in sorted(by_year, reverse=True):
        items = sorted(by_year[year], key=lambda x: x[2], reverse=True)
        lis = "\n".join(
            f'                    <li class="post-item">\n'
            f'                        <a href="{html.escape(f.name)}/">{html.escape(t)}</a>\n'
            f'                        <div class="post-date">{d.strftime("%B %-d, %Y")}</div>\n'
            f'                    </li>' for f, t, d in items)
        sections.append(
            f'            <!-- {year} - {len(items)} posts -->\n'
            f'            <div class="year-section">\n'
            f'                <div class="year-header">\n'
            f'                    <div class="year-number">{year}</div>\n'
            f'                    <div class="year-count">{len(items)} post{"s" if len(items) != 1 else ""}</div>\n'
            f'                </div>\n'
            f'                <ul class="post-list">\n{lis}\n'
            f'                </ul>\n'
            f'            </div>')

    years = sorted(by_year)
    span = f"{years[0]} - {years[-1]}" if years[0] != years[-1] else str(years[0])
    doc = TEMPLATE.read_text(encoding="utf-8")

    # Head: retarget every URL and label, leaving the shared <style> untouched.
    doc = doc.replace("https://www.julien.org/blog/huggingface-posts-and-images/", URL)
    doc = re.sub(r"<title>.*?</title>", f"<title>{html.escape(TITLE)}</title>", doc, flags=re.S)
    doc = re.sub(r'(<meta name="description" content=")[^"]*(")',
                 lambda m: m.group(1) + html.escape(f"{BLURB} {len(posts)} posts by Julien Simon, {span}.") + m.group(2), doc)
    doc = re.sub(r'(<meta name="keywords" content=")[^"]*(")',
                 r"\1Julien Simon, Arcee AI, small language models, AFM, CPU inference, Arm, model routing\2", doc)
    for attr in ("property=\"og:title\"", "name=\"twitter:title\""):
        doc = re.sub(rf'(<meta {attr} content=")[^"]*(")', lambda m: m.group(1) + html.escape(TITLE) + m.group(2), doc)
    doc = re.sub(r'(<meta property="og:description" content=")[^"]*(")',
                 lambda m: m.group(1) + html.escape(f"{BLURB} {len(posts)} posts by Julien Simon, {span}.") + m.group(2), doc)

    # Body: breadcrumb, hero, listing, and the cross-links to sibling sections.
    doc = doc.replace('<span class="current">Hugging Face Blog Posts</span>',
                      f'<span class="current">{html.escape(HEADING)}</span>')
    doc = re.sub(r'<section class="hero">.*?</section>',
                 f'<section class="hero">\n            <h1>{html.escape(HEADING)}</h1>\n'
                 f'            <p>{html.escape(BLURB)}</p>\n'
                 f'            <div class="hero-stats">\n'
                 f'                <div class="hero-stat">{len(posts)} Total Posts</div>\n'
                 f'                <div class="hero-stat">{span}</div>\n'
                 f'            </div>\n        </section>', doc, flags=re.S)
    doc = re.sub(r'(<div class="content-wrap">\n).*?(\n\s*</div>\n\s*</main>)',
                 lambda m: m.group(1) + "\n" + "\n\n".join(sections) + m.group(2), doc, flags=re.S)
    doc = doc.replace('<a href="/blog/arcee-posts/">Arcee Blog Posts</a>',
                      '<a href="/blog/huggingface-posts-and-images/">Hugging Face Blog Posts</a>')

    TARGET.write_text(doc, encoding="utf-8")
    print(f"Wrote {TARGET.relative_to(PUBLIC)}: {len(posts)} posts across {len(by_year)} year(s)")


if __name__ == "__main__":
    main()
