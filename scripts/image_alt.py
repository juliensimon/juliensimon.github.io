#!/usr/bin/env python3
"""Alt-text fallback for article images. Stdlib only, so the backfill can run
without the scraping dependencies the sync scripts need."""
import html as html_lib
import re


def ensure_image_alt(html_fragment: str, title: str) -> str:
    """Give every <img> an alt attribute.

    Preferred alt text comes from the source markup or its figcaption (see
    SubstackHTMLCleaner._simplify_images). Anything still bare gets a
    title-derived fallback so screen readers and image search have something
    to work with rather than an unlabelled image.
    """
    index = [0]

    def label(match):
        tag = match.group(0)
        if re.search(r"\balt=", tag):
            return tag
        index[0] += 1
        alt = html_lib.escape(f"Figure {index[0]} from {title}", quote=True)
        if tag.endswith("/>"):
            return tag[:-2].rstrip() + f' alt="{alt}"/>'
        return tag[:-1].rstrip() + f' alt="{alt}">'

    return re.sub(r"<img\b[^>]*>", label, html_fragment)


def demo():
    out = ensure_image_alt('<p><img src="a.webp"/><img src="b.png" alt="kept"></p>', 'My "Post"')
    assert 'alt="Figure 1 from My &quot;Post&quot;"' in out, out
    assert out.count('alt="kept"') == 1, out          # existing alt untouched
    assert out.count("alt=") == 2, out                # no double-tagging
    assert ensure_image_alt(out, "x") == out, "not idempotent"
    print("ok")


if __name__ == "__main__":
    demo()
