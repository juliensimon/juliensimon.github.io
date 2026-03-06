#!/usr/bin/env python3
"""Generate redirect HTML files for old canonical URLs that Google indexed.

Old patterns → actual file paths:
- Arcee: /blog/YYYY-MM-DD-slug/ → /blog/arcee-posts/YYYY-MM-DD_slug/index.html
- HF:    /blog/YYYY-MM-DD-slug/ → /blog/huggingface-posts-and-images/YYYY-MM-DD_slug/index.html
- AWS:   /blog/slug/            → /blog/aws-posts-and-images/YYYY-MM-DD_slug/index.html
"""

import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
PUBLIC_DIR = BASE_DIR / 'next-site' / 'public'

def redirect_html(target_url: str, canonical_url: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0;url={target_url}">
<link rel="canonical" href="{canonical_url}">
<title>Redirecting...</title>
</head>
<body>
<p>Redirecting to <a href="{target_url}">{target_url}</a></p>
</body>
</html>"""


def get_old_url_patterns():
    """Map old (wrong) URLs to correct URLs for each post."""
    redirects = []

    # Arcee posts: old pattern /blog/YYYY-MM-DD-slug/
    arcee_dir = PUBLIC_DIR / 'blog' / 'arcee-posts'
    if arcee_dir.exists():
        for post_dir in sorted(arcee_dir.iterdir()):
            if not post_dir.is_dir() or post_dir.name.startswith('.'):
                continue
            # Extract date and slug from folder name like "2025-07-09_is-running-language-models-on-cpu-really-viable"
            match = re.match(r'(\d{4}-\d{2}-\d{2})_(.*)', post_dir.name)
            if match:
                date, slug = match.groups()
                old_path = f'blog/{date}-{slug}'
                new_path = f'/blog/arcee-posts/{post_dir.name}/index.html'
                canonical = f'https://www.julien.org{new_path}'
                redirects.append((old_path, new_path, canonical))

    # HuggingFace posts: old pattern /blog/YYYY-MM-DD-slug/
    hf_dir = PUBLIC_DIR / 'blog' / 'huggingface-posts-and-images'
    if hf_dir.exists():
        for post_dir in sorted(hf_dir.iterdir()):
            if not post_dir.is_dir() or post_dir.name.startswith('.'):
                continue
            match = re.match(r'(\d{4}-\d{2}-\d{2})_(.*)', post_dir.name)
            if match:
                date, slug = match.groups()
                old_path = f'blog/{date}-{slug}'
                new_path = f'/blog/huggingface-posts-and-images/{post_dir.name}/index.html'
                canonical = f'https://www.julien.org{new_path}'
                redirects.append((old_path, new_path, canonical))

    # AWS posts: old pattern /blog/slug/ (no date prefix!)
    aws_dir = PUBLIC_DIR / 'blog' / 'aws-posts-and-images'
    if aws_dir.exists():
        for post_dir in sorted(aws_dir.iterdir()):
            if not post_dir.is_dir() or post_dir.name.startswith('.'):
                continue
            match = re.match(r'(\d{4}-\d{2}-\d{2})_(.*)', post_dir.name)
            if match:
                date, slug = match.groups()
                # AWS old canonical had no date
                old_path = f'blog/{slug}'
                new_path = f'/blog/aws-posts-and-images/{post_dir.name}/index.html'
                canonical = f'https://www.julien.org{new_path}'
                redirects.append((old_path, new_path, canonical))
                # Also add with date prefix (some may have been indexed both ways)
                old_path_with_date = f'blog/{date}-{slug}'
                redirects.append((old_path_with_date, new_path, canonical))

    return redirects


def main():
    redirects = get_old_url_patterns()
    created = 0
    skipped = 0

    for old_path, new_path, canonical in redirects:
        # Create redirect as /old_path/index.html
        redirect_dir = PUBLIC_DIR / old_path
        redirect_file = redirect_dir / 'index.html'

        # Don't overwrite existing content
        if redirect_file.exists():
            skipped += 1
            continue

        redirect_dir.mkdir(parents=True, exist_ok=True)
        redirect_file.write_text(redirect_html(new_path, canonical))
        created += 1

    print(f"Created {created} redirect files, skipped {skipped} (already exist)")


if __name__ == '__main__':
    main()
