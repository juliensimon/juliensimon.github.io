#!/usr/bin/env python3
"""
Download blogger images and update HTML files with local references.

This script downloads all images from Blogger/Blogspot URLs found in HTML files,
converts them to WebP format, and updates the HTML files to use local references.

Features:
- Smart URL resolution for old blogger image formats
- WebP conversion for better compression
- Per-post image numbering (post-title-image-01.webp)
- Automatic HTML updating with local image paths
- Error handling and retry logic

Usage:
    python download_images.py

Requirements:
    - Python 3.6+
    - PIL (Pillow): pip install Pillow
    - requests: pip install requests

Input:
    - HTML files in blog/legacy-posts-and-images/ with blogger image URLs

Output:
    - WebP images saved locally alongside HTML files
    - Updated HTML files with local image references
"""

import os
import re
import requests
import time
from PIL import Image
import io
from pathlib import Path

def try_alternative_urls(original_url):
    """Generate alternative URL formats for old blogger images."""
    alternatives = [original_url]
    
    # Try removing -h suffix (common issue with old blogger URLs)
    if '/s1600-h/' in original_url:
        alternatives.append(original_url.replace('/s1600-h/', '/s1600/'))
    
    # Try different size formats
    if '/s1600/' in original_url:
        alternatives.extend([
            original_url.replace('/s1600/', '/s0/'),      # Original size
            original_url.replace('/s1600/', '/s1200/'),   # High quality
            original_url.replace('/s1600/', '/'),         # Root path
        ])
    
    return alternatives

def download_and_convert_image(url, local_path):
    """Download image and convert to WebP format."""
    
    # Try the original URL and alternatives
    urls_to_try = try_alternative_urls(url)
    
    for attempt, try_url in enumerate(urls_to_try):
        try:
            # Use browser-like headers to avoid blocking
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://blogger.com/',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8'
            }
            response = requests.get(try_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get('content-type', '').lower()
            if not any(img_type in content_type for img_type in ['image/', 'jpeg', 'png', 'gif', 'webp']):
                if attempt < len(urls_to_try) - 1:
                    print(f"   ⚠️  URL {attempt + 1} returned non-image content, trying alternative...")
                    continue
                else:
                    return False, f"Invalid content type: {content_type}"
            
            # Convert to WebP
            try:
                image = Image.open(io.BytesIO(response.content))
                
                # Convert to RGB if necessary (for WebP compatibility)
                if image.mode in ('RGBA', 'P'):
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    if image.mode == 'P':
                        image = image.convert('RGBA')
                    background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                    image = background
                elif image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Save as WebP with good quality
                image.save(local_path, 'WEBP', quality=85, optimize=True)
                
                file_size = os.path.getsize(local_path)
                print(f"   ✅ Downloaded and converted to WebP ({file_size:,} bytes)")
                return True, "Success"
                
            except Exception as img_error:
                if attempt < len(urls_to_try) - 1:
                    print(f"   ⚠️  Image processing failed for URL {attempt + 1}, trying alternative...")
                    continue
                else:
                    return False, f"Image processing failed: {str(img_error)}"
                
        except requests.RequestException as e:
            if attempt < len(urls_to_try) - 1:
                print(f"   ⚠️  Request failed for URL {attempt + 1}, trying alternative...")
                continue
            else:
                return False, f"Request failed: {str(e)}"
        except Exception as e:
            if attempt < len(urls_to_try) - 1:
                print(f"   ⚠️  Unexpected error for URL {attempt + 1}, trying alternative...")
                continue
            else:
                return False, f"Unexpected error: {str(e)}"
        
        # Small delay between attempts
        if attempt < len(urls_to_try) - 1:
            time.sleep(0.5)
    
    return False, "All URL alternatives failed"

def extract_post_title_from_filename(filename):
    """Extract post title from filename for image naming."""
    # Remove date prefix and extension
    base = os.path.splitext(filename)[0]
    if re.match(r'^\d{4}-\d{2}-\d{2}-', base):
        base = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', base)
    return base

def download_images_for_posts():
    """Download all blogger images and update HTML files."""
    
    posts_dir = Path('blog/legacy-posts-and-images')
    
    # Find all HTML files
    html_files = []
    for year_dir in posts_dir.iterdir():
        if year_dir.is_dir() and year_dir.name.isdigit():
            for html_file in year_dir.glob('*.html'):
                if html_file.name != 'index.html':
                    html_files.append(html_file)
    
    if not html_files:
        print("❌ No HTML files found in year directories")
        return
    
    print(f"📁 Found {len(html_files)} HTML files to process")
    
    # Pattern to match blogger image URLs
    blogger_pattern = r'https?://\d+\.bp\.blogspot\.com/[^"\s]+'
    
    total_images = 0
    successful_downloads = 0
    updated_files = 0
    
    for html_file in html_files:
        print(f"\n📄 Processing: {html_file.name}")
        
        # Read the HTML content
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all blogger URLs
        blogger_urls = re.findall(blogger_pattern, content)
        unique_urls = list(set(blogger_urls))  # Remove duplicates
        
        if not unique_urls:
            print("   ℹ️  No blogger images found")
            continue
        
        print(f"   🖼️  Found {len(unique_urls)} unique blogger images")
        
        # Extract post title for image naming
        post_title = extract_post_title_from_filename(html_file.name)
        
        # Download each image
        image_counter = 1
        content_updated = False
        
        for url in unique_urls:
            total_images += 1
            
            # Create local filename
            local_filename = f"{html_file.stem}-image-{image_counter:02d}.webp"
            local_path = html_file.parent / local_filename
            
            print(f"   📥 Downloading image {image_counter}: {local_filename}")
            
            # Skip if already exists
            if local_path.exists():
                print(f"   ⏭️  Already exists, skipping")
                # Still update HTML to use local reference
                content = content.replace(url, local_filename)
                content_updated = True
                image_counter += 1
                successful_downloads += 1
                continue
            
            # Download and convert
            success, message = download_and_convert_image(url, local_path)
            
            if success:
                successful_downloads += 1
                # Update HTML content to use local reference
                content = content.replace(url, local_filename)
                content_updated = True
                print(f"   ✅ Successfully replaced URL with {local_filename}")
            else:
                print(f"   ❌ Failed: {message}")
            
            image_counter += 1
            
            # Small delay to be respectful
            time.sleep(0.1)
        
        # Write updated HTML content
        if content_updated:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_files += 1
            print(f"   💾 Updated HTML file with local image references")
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"   • Total images found: {total_images}")
    print(f"   • Successfully downloaded: {successful_downloads}")
    print(f"   • HTML files updated: {updated_files}")
    print(f"   • Success rate: {(successful_downloads/total_images*100):.1f}%" if total_images > 0 else "   • No images to process")

def main():
    """Main function."""
    print("🚀 Starting image download and HTML update process...")
    
    # Check if posts directory exists
    posts_dir = Path('blog/legacy-posts-and-images')
    if not posts_dir.exists():
        print(f"❌ Directory not found: {posts_dir}")
        print("Please run the extract_blog_posts.py script first")
        return
    
    download_images_for_posts()
    print("\n🎉 Image download process completed!")

if __name__ == "__main__":
    main() 