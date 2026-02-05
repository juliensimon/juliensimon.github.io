#!/usr/bin/env python3
"""
Substack Image Handler

Downloads images from Substack posts, unwrapping CDN URLs and converting
to WebP format for efficient local hosting.

Usage:
    from substack_image_handler import process_images_for_post

    url_mapping = process_images_for_post(images, output_dir, slug)
"""

import io
import re
import time
from pathlib import Path
from urllib.parse import unquote, urlparse

import requests
from PIL import Image


# User agent for image downloads
USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/120.0.0.0 Safari/537.36'
)

# Default delay between downloads (seconds)
DOWNLOAD_DELAY = 0.2

# WebP quality setting (matches existing pattern in download_images.py)
WEBP_QUALITY = 85


def unwrap_substack_cdn_url(url: str) -> str:
    """
    Unwrap a Substack CDN URL to get the original image URL.

    Substack wraps images like:
    https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media...

    Args:
        url: The Substack CDN URL

    Returns:
        The unwrapped original URL, or the input URL if not a CDN URL
    """
    # Check if this is a Substack CDN URL
    if 'substackcdn.com/image/fetch/' not in url:
        return url

    # Find the actual URL after the fetch parameters
    # Pattern: ...fetch/{params}/{encoded_url}
    match = re.search(r'/fetch/[^/]+/(https?[^?\s]+)', url)
    if match:
        # URL decode the actual image URL
        return unquote(match.group(1))

    return url


def download_image(url: str, timeout: int = 30) -> bytes | None:
    """
    Download an image from a URL.

    Args:
        url: The image URL
        timeout: Request timeout in seconds

    Returns:
        Image bytes or None if download failed
    """
    headers = {
        'User-Agent': USER_AGENT,
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': 'https://substack.com/',
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        # Verify it's actually an image
        content_type = response.headers.get('content-type', '').lower()
        if not any(t in content_type for t in ['image/', 'jpeg', 'png', 'gif', 'webp']):
            print(f"    Warning: Non-image content type: {content_type}")
            return None

        return response.content

    except requests.RequestException as e:
        print(f"    Error downloading {url}: {e}")
        return None


def convert_to_webp(image_data: bytes, quality: int = WEBP_QUALITY) -> bytes | None:
    """
    Convert image data to WebP format.

    Args:
        image_data: Raw image bytes
        quality: WebP quality (0-100)

    Returns:
        WebP bytes or None if conversion failed
    """
    try:
        image = Image.open(io.BytesIO(image_data))

        # Convert to RGB if necessary (for WebP compatibility)
        if image.mode in ('RGBA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            if image.mode == 'RGBA':
                background.paste(image, mask=image.split()[-1])
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        # Save as WebP
        output = io.BytesIO()
        image.save(output, 'WEBP', quality=quality, optimize=True)
        return output.getvalue()

    except Exception as e:
        print(f"    Error converting to WebP: {e}")
        return None


def process_images_for_post(
    images: list[dict],
    output_dir: Path,
    slug: str,
    delay: float = DOWNLOAD_DELAY,
) -> dict[str, str]:
    """
    Download and process images for a post.

    Args:
        images: List of image dicts with 'src' and 'alt' keys
        output_dir: Directory to save images
        slug: Post slug for naming images
        delay: Delay between downloads in seconds

    Returns:
        Mapping of original URL to local filename
    """
    url_mapping = {}

    if not images:
        return url_mapping

    print(f"  Processing {len(images)} images...")
    output_dir.mkdir(parents=True, exist_ok=True)

    for idx, img in enumerate(images, start=1):
        original_url = img['src']

        # Generate local filename
        local_filename = f"image-{idx:02d}.webp"
        local_path = output_dir / local_filename

        # Skip if already exists
        if local_path.exists():
            print(f"    [{idx}/{len(images)}] Already exists: {local_filename}")
            url_mapping[original_url] = local_filename
            continue

        # Unwrap CDN URL
        actual_url = unwrap_substack_cdn_url(original_url)
        if actual_url != original_url:
            print(f"    [{idx}/{len(images)}] Unwrapped CDN URL")

        # Download
        print(f"    [{idx}/{len(images)}] Downloading...")
        image_data = download_image(actual_url)

        if not image_data:
            # Try original URL if unwrapped URL failed
            if actual_url != original_url:
                print(f"    [{idx}/{len(images)}] Trying original URL...")
                image_data = download_image(original_url)

        if not image_data:
            print(f"    [{idx}/{len(images)}] Failed to download")
            continue

        # Convert to WebP
        webp_data = convert_to_webp(image_data)

        if not webp_data:
            print(f"    [{idx}/{len(images)}] Failed to convert")
            continue

        # Save
        local_path.write_bytes(webp_data)
        print(f"    [{idx}/{len(images)}] Saved: {local_filename} ({len(webp_data):,} bytes)")

        url_mapping[original_url] = local_filename

        # Rate limiting
        if idx < len(images) and delay > 0:
            time.sleep(delay)

    print(f"  Downloaded {len(url_mapping)}/{len(images)} images")
    return url_mapping


def update_html_image_refs(html: str, url_mapping: dict[str, str]) -> str:
    """
    Update image references in HTML to use local paths.

    Args:
        html: HTML content with original image URLs
        url_mapping: Mapping of original URL to local filename

    Returns:
        HTML with updated image references
    """
    for original_url, local_filename in url_mapping.items():
        html = html.replace(original_url, local_filename)

    return html


if __name__ == '__main__':
    # Simple test
    print("Testing URL unwrapping...")

    test_urls = [
        'https://substackcdn.com/image/fetch/f_auto,q_auto:good/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ftest.jpg',
        'https://substack-post-media.s3.amazonaws.com/public/images/test.jpg',
        'https://example.com/image.png',
    ]

    for url in test_urls:
        result = unwrap_substack_cdn_url(url)
        print(f"  Input:  {url[:80]}...")
        print(f"  Output: {result[:80]}...")
        print()
