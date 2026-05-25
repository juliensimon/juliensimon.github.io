#!/usr/bin/env python3
"""Parse archive/media-analysts.html + archive/podcasts.html into next-site/src/data/media.ts.

Each archive entry is a <div class="speaking-event"> with:
  <h3>{title}</h3>
  <div class="event-details">
    <strong>{outlet}</strong> • {type} • {date} [ • <a href="...">{label}</a>]
  </div>
  <div class="description">{html}</div>
  <div class="tags"><span class="tag">{tag}</span>...</div>
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_FILES = [
    ROOT / "archive" / "media-analysts.html",
    ROOT / "archive" / "podcasts.html",
]
OUTPUT = ROOT / "next-site" / "src" / "data" / "media.ts"

MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
}

DATE_FULL = re.compile(r"(?i)\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{1,2}),\s*(\d{4})\b")
DATE_MONTH_YEAR = re.compile(r"(?i)\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})\b")
DATE_YEAR = re.compile(r"\b(20\d{2})\b")


def parse_date(text: str) -> tuple[Optional[str], int, int, int]:
    """Return (display, year, month, day). Missing fields become 0."""
    if m := DATE_FULL.search(text):
        month = MONTHS[m.group(1).lower()]
        day = int(m.group(2))
        year = int(m.group(3))
        display = f"{m.group(1).title()} {day}, {year}"
        return display, year, month, day
    if m := DATE_MONTH_YEAR.search(text):
        month = MONTHS[m.group(1).lower()]
        year = int(m.group(2))
        display = f"{m.group(1).title()} {year}"
        return display, year, month, 0
    if m := DATE_YEAR.search(text):
        year = int(m.group(1))
        return str(year), year, 0, 0
    return None, 0, 0, 0


def parse_entry(div) -> Optional[dict]:
    h3 = div.find("h3")
    details = div.find("div", class_="event-details")
    desc_div = div.find("div", class_="description")
    tags_div = div.find("div", class_="tags")
    if not h3 or not details:
        return None

    title = h3.get_text(strip=True)

    strong = details.find("strong")
    outlet = strong.get_text(strip=True) if strong else ""

    # event-details text segments separated by '•'
    details_text = details.get_text(" ", strip=True)
    # Strip the outlet from the front (it appears as text too)
    if outlet and details_text.startswith(outlet):
        details_text = details_text[len(outlet):].lstrip(" •")

    # The first segment after outlet is type, second is date
    segments = [s.strip() for s in details_text.split("•")]
    item_type = segments[0] if segments else ""
    date_text = segments[1] if len(segments) > 1 else ""

    display_date, year, month, day = parse_date(date_text or details_text)

    a = details.find("a", href=True)
    url = a["href"] if a else None
    link_label = a.get_text(strip=True) if a else None

    description = ""
    if desc_div:
        # Preserve <br> as newlines, collapse other whitespace
        for br in desc_div.find_all("br"):
            br.replace_with("\n")
        description = re.sub(r"\s+\n", "\n", desc_div.get_text(" ", strip=True))
        description = re.sub(r"\n\s+", "\n", description)
        description = re.sub(r"[ \t]+", " ", description).strip()

    tags = []
    if tags_div:
        tags = [t.get_text(strip=True) for t in tags_div.find_all("span", class_="tag")]

    return {
        "title": title,
        "outlet": outlet,
        "type": item_type,
        "date": display_date or "",
        "year": year,
        "month": month,
        "day": day,
        "url": url,
        "linkLabel": link_label,
        "description": description,
        "tags": tags,
    }


def sort_key(item: dict) -> tuple:
    # Desc by year, month, day
    return (-item["year"], -item["month"], -item["day"])


def ts_string(s: Optional[str]) -> str:
    if s is None:
        return "undefined"
    # Use JSON encoding for safe escaping then convert "..." to '...'
    # Actually, just use JSON.dumps which produces valid TS too.
    return json.dumps(s, ensure_ascii=False)


def emit_ts(items: list[dict]) -> str:
    lines: list[str] = []
    lines.append("// AUTO-GENERATED from archive/media-analysts.html + archive/podcasts.html")
    lines.append("// by scripts/parse_media_archive.py. Hand-edits at the top of MEDIA_ITEMS")
    lines.append("// (new entries) are safe; re-running the script preserves manual additions")
    lines.append("// only if you re-merge them. Treat this file as source of truth after edits.")
    lines.append("")
    lines.append("export interface MediaItem {")
    lines.append("  title: string;")
    lines.append("  outlet: string;")
    lines.append("  type: string;")
    lines.append("  date: string;")
    lines.append("  year: number;")
    lines.append("  url?: string;")
    lines.append("  linkLabel?: string;")
    lines.append("  description: string;")
    lines.append("  tags: string[];")
    lines.append("}")
    lines.append("")
    lines.append("export const MEDIA_ITEMS: MediaItem[] = [")
    for it in items:
        lines.append("  {")
        lines.append(f"    title: {ts_string(it['title'])},")
        lines.append(f"    outlet: {ts_string(it['outlet'])},")
        lines.append(f"    type: {ts_string(it['type'])},")
        lines.append(f"    date: {ts_string(it['date'])},")
        lines.append(f"    year: {it['year']},")
        if it["url"]:
            lines.append(f"    url: {ts_string(it['url'])},")
        if it["linkLabel"]:
            lines.append(f"    linkLabel: {ts_string(it['linkLabel'])},")
        lines.append(f"    description: {ts_string(it['description'])},")
        tags_inline = ", ".join(ts_string(t) for t in it["tags"])
        lines.append(f"    tags: [{tags_inline}],")
        lines.append("  },")
    lines.append("];")
    lines.append("")
    lines.append("export const MEDIA_STATS = {")
    lines.append(f"  total: {len(items)},")
    years = sorted({i['year'] for i in items if i['year']}, reverse=True)
    if years:
        lines.append(f"  yearSpan: '{years[-1]}–{years[0]}',")
        lines.append(f"  earliestYear: {years[-1]},")
        lines.append(f"  latestYear: {years[0]},")
    type_counts: dict[str, int] = {}
    for it in items:
        t = it["type"] or "Other"
        type_counts[t] = type_counts.get(t, 0) + 1
    lines.append("  byType: {")
    for k, v in sorted(type_counts.items(), key=lambda kv: -kv[1]):
        lines.append(f"    {ts_string(k)}: {v},")
    lines.append("  } as Record<string, number>,")
    lines.append("} as const;")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    items: list[dict] = []
    for path in ARCHIVE_FILES:
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        for div in soup.find_all("div", class_="speaking-event"):
            entry = parse_entry(div)
            if entry:
                items.append(entry)

    # Dedupe by (title, outlet, year, month, day) — keep first occurrence
    seen = set()
    deduped = []
    for it in items:
        key = (it["title"], it["outlet"], it["year"], it["month"], it["day"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(it)

    deduped.sort(key=sort_key)
    OUTPUT.write_text(emit_ts(deduped), encoding="utf-8")
    print(f"Wrote {len(deduped)} items to {OUTPUT.relative_to(ROOT)}")
    print(f"  Source items: {len(items)}, duplicates removed: {len(items) - len(deduped)}")


if __name__ == "__main__":
    main()
