#!/usr/bin/env python3
"""Fix SEO issues across HuggingFace and AWS blog posts.

Fixes:
1. Author/publisher schema → use #person ref
2. Canonical URLs → correct www.julien.org paths
3. OG URLs and images → correct paths and existing image
4. Add speakable to BlogPosting schema
5. Remove isPartOf from schema
6. Remove fake security headers (meta http-equiv)
7. Remove apple-mobile-web-app meta tags
8. Fix broken Python list syntax in keywords
9. Fix og:site_name
"""

import json
import os
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
OG_IMAGE = "https://www.julien.org/assets/og-image-1200x630.webp"

SECURITY_HEADERS = [
    'X-Content-Type-Options',
    'X-Frame-Options',
    'Referrer-Policy',
    'X-XSS-Protection',
    'Permissions-Policy',
    'Cross-Origin-Opener-Policy',
    'Cross-Origin-Embedder-Policy',
]

APPLE_META = [
    'apple-mobile-web-app-capable',
    'apple-mobile-web-app-status-bar-style',
]


def fix_json_ld(html: str, correct_url: str) -> str:
    """Fix the BlogPosting JSON-LD structured data."""
    # Find the JSON-LD block
    pattern = r'(<script type="application/ld\+json">\s*)(.*?)(</script>)'

    def replace_jsonld(match):
        prefix = match.group(1)
        json_str = match.group(2)
        suffix = match.group(3)

        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            return match.group(0)  # Leave unchanged if can't parse

        if data.get('@type') != 'BlogPosting':
            return match.group(0)

        # Fix author
        data['author'] = {"@id": "https://www.julien.org/#person"}

        # Fix publisher
        data['publisher'] = {"@id": "https://www.julien.org/#person"}

        # Fix URL
        data['url'] = correct_url

        # Fix mainEntityOfPage
        data['mainEntityOfPage'] = {
            "@type": "WebPage",
            "@id": correct_url
        }

        # Fix image
        data['image'] = OG_IMAGE

        # Add speakable
        data['speakable'] = {
            "@type": "SpeakableSpecification",
            "cssSelector": ["h1", "h2", "h3", "p"]
        }

        # Remove isPartOf
        data.pop('isPartOf', None)

        # Fix broken keywords (Python list syntax)
        if 'keywords' in data:
            kw = data['keywords']
            # Remove ['word', 'word'] patterns
            kw = re.sub(r"\['[^']*'(?:,\s*'[^']*')*\]", '', kw)
            kw = re.sub(r',\s*,', ',', kw)  # Fix double commas
            kw = kw.strip(', ')
            data['keywords'] = kw

        new_json = json.dumps(data, indent=2, ensure_ascii=False)
        return f'{prefix}\n{new_json}\n{suffix}'

    return re.sub(pattern, replace_jsonld, html, flags=re.DOTALL)


def fix_meta_tags(html: str, correct_url: str, folder_type: str) -> str:
    """Fix meta tags: canonical, OG, Twitter, etc."""

    # Fix canonical URL
    html = re.sub(
        r'<link rel="canonical" href="[^"]*">',
        f'<link rel="canonical" href="{correct_url}">',
        html
    )

    # Fix og:url
    html = re.sub(
        r'<meta property="og:url" content="[^"]*">',
        f'<meta property="og:url" content="{correct_url}">',
        html
    )

    # Fix twitter:url
    html = re.sub(
        r'<meta property="twitter:url" content="[^"]*">',
        f'<meta property="twitter:url" content="{correct_url}">',
        html
    )

    # Fix og:image
    html = re.sub(
        r'<meta property="og:image" content="[^"]*">',
        f'<meta property="og:image" content="{OG_IMAGE}">',
        html
    )

    # Fix twitter:image
    html = re.sub(
        r'<meta property="twitter:image" content="[^"]*">',
        f'<meta property="twitter:image" content="{OG_IMAGE}">',
        html
    )

    # Fix og:site_name
    html = re.sub(
        r'<meta property="og:site_name" content="[^"]*">',
        '<meta property="og:site_name" content="Julien Simon">',
        html
    )

    # Fix broken keywords in meta tag
    html = re.sub(
        r"""(<meta name="keywords" content="[^"]*)\['[^"]*?\]([^"]*">)""",
        lambda m: m.group(0).replace(
            re.search(r"\[.*?\]", m.group(0)).group(0),
            ''
        ),
        html
    )

    # Remove fake security headers
    for header in SECURITY_HEADERS:
        html = re.sub(
            rf'\s*<meta http-equiv="{header}" content="[^"]*">\s*\n?',
            '\n',
            html
        )

    # Remove apple mobile meta tags
    for meta in APPLE_META:
        html = re.sub(
            rf'\s*<meta name="{meta}" content="[^"]*">\s*\n?',
            '\n',
            html
        )

    # Clean up multiple blank lines
    html = re.sub(r'\n{3,}', '\n\n', html)

    return html


def get_correct_url(folder_name: str, post_type: str) -> str:
    """Build the correct canonical URL."""
    if post_type == 'huggingface':
        return f"https://www.julien.org/blog/huggingface-posts-and-images/{folder_name}/index.html"
    elif post_type == 'aws':
        return f"https://www.julien.org/blog/aws-posts-and-images/{folder_name}/index.html"
    return ""


def process_file(filepath: Path, post_type: str) -> bool:
    """Process a single HTML file. Returns True if modified."""
    folder_name = filepath.parent.name
    correct_url = get_correct_url(folder_name, post_type)

    html = filepath.read_text(encoding='utf-8')
    original = html

    html = fix_json_ld(html, correct_url)
    html = fix_meta_tags(html, correct_url, post_type)

    if html != original:
        filepath.write_text(html, encoding='utf-8')
        return True
    return False


def main():
    dirs_to_process = [
        # next-site/public copies
        (BASE_DIR / 'next-site' / 'public' / 'blog' / 'huggingface-posts-and-images', 'huggingface'),
        (BASE_DIR / 'next-site' / 'public' / 'blog' / 'aws-posts-and-images', 'aws'),
        # legacy copies
        (BASE_DIR / 'blog' / 'huggingface-posts-and-images', 'huggingface'),
        (BASE_DIR / 'blog' / 'aws-posts-and-images', 'aws'),
    ]

    total_modified = 0
    total_files = 0

    for base_path, post_type in dirs_to_process:
        if not base_path.exists():
            print(f"  Skipping {base_path} (not found)")
            continue

        for post_dir in sorted(base_path.iterdir()):
            index_file = post_dir / 'index.html'
            if not index_file.exists():
                continue

            total_files += 1
            if process_file(index_file, post_type):
                total_modified += 1
                print(f"  Fixed: {post_type}/{post_dir.name}")

    print(f"\nProcessed {total_files} files, modified {total_modified}")


if __name__ == '__main__':
    main()
