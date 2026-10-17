#!/usr/bin/env python3
"""Rewrite meta descriptions that end in an ellipsis (one-off backfill).

Reads every blog and video page under next-site/public, and for each page whose
<meta name="description"> ends in "…" re-cuts that text with
meta_description.cut_description, then replaces the old string wherever it
appears on the page (description, og:description, twitter:description and the
JSON-LD copy). Dry run by default; pass --apply to write.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from meta_description import cut_description  # noqa: E402

PUBLIC = Path(__file__).resolve().parent.parent / "next-site" / "public"
RX = re.compile(r'<meta name="description" content="([^"]*…)"')
MINIMUM = 70


def spellings(s: str) -> list[str]:
    """The spellings of one text a page may carry: as in the meta tag, raw,
    HTML-escaped, and JSON-escaped with and without \\u escapes."""
    raw = html.unescape(s)
    return [s, raw, html.escape(raw, quote=True),
            json.dumps(raw, ensure_ascii=False)[1:-1], json.dumps(raw)[1:-1]]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    changed = missed = 0
    for sub in ("blog", "youtube"):
        for f in sorted((PUBLIC / sub).rglob("*.html")):
            h = f.read_text(encoding="utf-8", errors="surrogateescape")
            m = RX.search(h)
            if not m:
                continue
            old_attr = m.group(1)
            plain = html.unescape(old_attr).rstrip("…").rstrip()
            # The text was already cut at LIMIT; force one more cut so it ends cleanly.
            new_text = cut_description(plain, len(plain) - 1, MINIMUM)
            if new_text.endswith("…") or len(new_text) < MINIMUM:
                # The forced cut loses too much: keep the whole text, close it cleanly.
                new_text = plain.rstrip(" ,;:-") + "."
            if len(new_text) < MINIMUM:
                missed += 1
                print(f"SKIP {f.relative_to(PUBLIC)}: {new_text!r}")
                continue
            # Slot 0 is the meta-tag spelling: the new text must be HTML-escaped there.
            new_sp = spellings(new_text)
            new_sp[0] = html.escape(new_text, quote=True)
            pairs = list(zip(spellings(old_attr), new_sp))
            # variants(old) and variants(new) line up by spelling; the old text
            # keeps its "…", the new one does not.
            new_h = h
            for o, n in pairs:  # index-aligned: never de-duplicate one side only
                if o != n:
                    new_h = new_h.replace(o, n)
            if new_h == h:
                continue
            changed += 1
            print(f"{f.relative_to(PUBLIC)}\n  - {html.unescape(old_attr)[-70:]}\n  + {new_text[-70:]}")
            if args.apply:
                f.write_text(new_h, encoding="utf-8", errors="surrogateescape")
    print(f"\n{changed} pages {'rewritten' if args.apply else 'would change'}, {missed} skipped")


if __name__ == "__main__":
    main()
