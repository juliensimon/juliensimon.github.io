#!/usr/bin/env python3
"""Fix truncated meta descriptions (ending in '...') across all blog posts.

For each file with a truncated description, extracts the first 1-2 complete
sentences from the post body and replaces all description meta tags.
"""

import os
import re
import html
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "next-site" / "public" / "blog"
MAX_DESC_LEN = 155  # Google typically shows ~155-160 chars


def extract_body_text(content: str) -> str:
    """Extract visible text from the post body, stripping HTML tags."""
    # Find the main content area - try common patterns
    # Industry perspectives use <div class="article-content">
    body_match = re.search(r'<div class="article-content">(.*?)</article>', content, re.DOTALL)
    if not body_match:
        # Industry perspectives alt: <div class="body markup">
        body_match = re.search(r'<div class="body markup">(.*?)</div>\s*</div>', content, re.DOTALL)
    if not body_match:
        # AWS Medium posts use <section class="e-content"
        body_match = re.search(r'<section class="e-content"[^>]*>(.*?)</section>\s*</article>', content, re.DOTALL)
    if not body_match:
        # Fallback: find first <p> tags after the title (greedy across long lines)
        body_match = re.search(r'</h[1-4]>\s*(.*?)</section>', content, re.DOTALL)
    if not body_match:
        return ""

    body_html = body_match.group(1)

    # Remove script/style tags
    body_html = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', body_html, flags=re.DOTALL)
    # Remove figure/img/iframe tags (not text content)
    body_html = re.sub(r'<(figure|img|iframe)[^>]*>.*?</\1>', '', body_html, flags=re.DOTALL)
    body_html = re.sub(r'<(figure|img|iframe)[^>]*/?>', '', body_html)
    # Remove all remaining HTML tags
    text = re.sub(r'<[^>]+>', ' ', body_html)
    # Decode HTML entities
    text = html.unescape(text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_sentences(text: str, max_len: int = MAX_DESC_LEN) -> str:
    """Extract first complete sentence(s) that fit within max_len."""
    if not text:
        return ""

    # Split on sentence boundaries (period/exclamation/question followed by space or end)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    result = ""
    for sentence in sentences:
        candidate = (result + " " + sentence).strip() if result else sentence
        if len(candidate) <= max_len:
            result = candidate
        else:
            break

    # If even the first sentence is too long, truncate it cleanly
    if not result and sentences:
        first = sentences[0]
        if len(first) > max_len:
            # Try to cut at last word boundary before max_len
            cut = first[:max_len].rsplit(' ', 1)[0]
            # End with period if it doesn't already
            if not cut.endswith(('.', '!', '?')):
                cut = cut.rstrip('.,;:!? ') + '.'
            result = cut
        else:
            result = first

    return result


def fix_file(filepath: Path) -> bool:
    """Fix truncated descriptions in a single HTML file. Returns True if modified."""
    content = filepath.read_text(encoding='utf-8')

    # Check if any description ends with "..."
    if not re.search(r'(name|property)="(description|og:description|twitter:description)" content="[^"]*\.\.\."', content):
        return False

    # Extract body text and build new description
    body_text = extract_body_text(content)
    if not body_text:
        return False

    new_desc = extract_sentences(body_text)
    if not new_desc or len(new_desc) < 30:
        return False

    # Escape for HTML attribute
    new_desc_escaped = new_desc.replace('"', '&quot;').replace('&', '&amp;')

    modified = False

    # Replace all truncated description attributes
    for attr in ['name="description"', 'property="og:description"', 'name="twitter:description"']:
        pattern = rf'({attr} content=")[^"]*\.\.\.(")'
        if re.search(pattern, content):
            content = re.sub(pattern, rf'\g<1>{new_desc_escaped}\2', content)
            modified = True

    if modified:
        filepath.write_text(content, encoding='utf-8')

    return modified


def main():
    fixed = 0
    skipped = 0
    errors = []

    for html_file in sorted(BLOG_DIR.rglob("index.html")):
        try:
            if fix_file(html_file):
                rel = html_file.relative_to(BLOG_DIR)
                print(f"  Fixed: {rel}")
                fixed += 1
            else:
                skipped += 1
        except Exception as e:
            errors.append((html_file, str(e)))

    print(f"\nDone: {fixed} fixed, {skipped} skipped, {len(errors)} errors")
    for path, err in errors:
        print(f"  ERROR {path.relative_to(BLOG_DIR)}: {err}")


if __name__ == "__main__":
    main()
