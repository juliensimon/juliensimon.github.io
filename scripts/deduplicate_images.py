#!/usr/bin/env python3
"""
Deduplicate images in blog posts.

This script identifies images that are duplicated between SRC and HREF attributes
in HTML files. It computes SHA256 hashes to verify if images are identical and
offers to remove duplicates while updating HTML references.

Features:
- Scans all HTML files for image references
- Computes hashes to identify identical images
- Finds cases where SRC and HREF point to different files of same image
- Shows preview of changes before applying
- Updates HTML files to use single image reference
- Removes duplicate image files

Usage:
    python deduplicate_images.py

Requirements:
    - Python 3.6+
    - hashlib (built-in)
    - Blog posts already organized in year folders
"""

import os
import re
import hashlib
from pathlib import Path
from collections import defaultdict
import html

def compute_file_hash(file_path):
    """Compute SHA256 hash of a file."""
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"   ❌ Error computing hash for {file_path}: {e}")
        return None

def extract_image_references(html_content):
    """Extract all image references from HTML content."""
    references = []
    
    # Pattern to match <a href="..."><img src="..."></a> structures
    pattern = r'<a[^>]+href="([^"]+)"[^>]*>\s*<img[^>]+src="([^"]+)"[^>]*>\s*</a>'
    matches = re.findall(pattern, html_content, re.IGNORECASE)
    
    for href, src in matches:
        # Only process if both are local image files
        if (href.endswith(('.webp', '.jpg', '.jpeg', '.png', '.gif')) and 
            src.endswith(('.webp', '.jpg', '.jpeg', '.png', '.gif')) and
            not href.startswith('http') and not src.startswith('http')):
            references.append({
                'href': href,
                'src': src,
                'type': 'linked_image'
            })
    
    # Also find standalone images
    standalone_pattern = r'<img[^>]+src="([^"]+)"[^>]*>'
    standalone_matches = re.findall(standalone_pattern, html_content, re.IGNORECASE)
    
    for src in standalone_matches:
        if (src.endswith(('.webp', '.jpg', '.jpeg', '.png', '.gif')) and 
            not src.startswith('http')):
            # Check if this is already part of a linked image
            is_linked = any(ref['src'] == src for ref in references)
            if not is_linked:
                references.append({
                    'src': src,
                    'type': 'standalone_image'
                })
    
    return references

def analyze_duplicates():
    """Analyze all images to find duplicates."""
    posts_dir = Path('blog/legacy-posts-and-images')
    
    # Find all HTML files
    html_files = []
    for year_dir in posts_dir.iterdir():
        if year_dir.is_dir() and year_dir.name.isdigit():
            for html_file in year_dir.glob('*.html'):
                if html_file.name != 'index.html':
                    html_files.append(html_file)
    
    print(f"📄 Scanning {len(html_files)} HTML files for image references...")
    
    # Collect all image references
    all_references = []
    image_hashes = {}  # file_path -> hash
    hash_to_files = defaultdict(list)  # hash -> [file_paths]
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            references = extract_image_references(content)
            
            for ref in references:
                ref['html_file'] = html_file
                all_references.append(ref)
                
                # Compute hashes for all referenced images
                for img_key in ['href', 'src']:
                    if img_key in ref:
                        img_path = html_file.parent / ref[img_key]
                        if img_path.exists() and str(img_path) not in image_hashes:
                            img_hash = compute_file_hash(img_path)
                            if img_hash:
                                image_hashes[str(img_path)] = img_hash
                                hash_to_files[img_hash].append(str(img_path))
                            
        except Exception as e:
            print(f"   ❌ Error processing {html_file}: {e}")
    
    print(f"🔍 Found {len(all_references)} image references")
    print(f"🖼️  Computed hashes for {len(image_hashes)} unique image files")
    
    # Find duplicates
    duplicates = {h: files for h, files in hash_to_files.items() if len(files) > 1}
    
    print(f"📊 Found {len(duplicates)} groups of duplicate images")
    
    # Analyze specific cases where href and src in same HTML point to duplicates
    duplicate_cases = []
    
    for ref in all_references:
        if ref['type'] == 'linked_image':
            href_path = str(ref['html_file'].parent / ref['href'])
            src_path = str(ref['html_file'].parent / ref['src'])
            
            href_hash = image_hashes.get(href_path)
            src_hash = image_hashes.get(src_path)
            
            if (href_hash and src_hash and href_hash == src_hash and 
                href_path != src_path):
                duplicate_cases.append({
                    'html_file': ref['html_file'],
                    'href_file': href_path,
                    'src_file': src_path,
                    'href_name': ref['href'],
                    'src_name': ref['src'],
                    'hash': href_hash
                })
    
    return duplicate_cases, duplicates, all_references

def preview_changes(duplicate_cases):
    """Show preview of what will be changed."""
    if not duplicate_cases:
        print("✅ No duplicate image cases found where SRC and HREF point to the same image!")
        return False
    
    print(f"\n🔍 Found {len(duplicate_cases)} cases where SRC and HREF point to identical images:")
    print("=" * 80)
    
    for i, case in enumerate(duplicate_cases, 1):
        print(f"\n📄 Case {i}: {case['html_file'].name}")
        print(f"   🔗 HREF: {case['href_name']} -> {Path(case['href_file']).name}")
        print(f"   🖼️  SRC:  {case['src_name']} -> {Path(case['src_file']).name}")
        print(f"   🔑 Hash: {case['hash'][:16]}...")
        
        # Show file sizes
        try:
            href_size = Path(case['href_file']).stat().st_size
            src_size = Path(case['src_file']).stat().st_size
            print(f"   📏 Sizes: HREF={href_size:,} bytes, SRC={src_size:,} bytes")
        except:
            pass
    
    print("\n" + "=" * 80)
    print("\n💡 Proposed changes:")
    print("   • Keep one image file (typically the larger/better quality one)")
    print("   • Update HTML to use the kept image for both SRC and HREF")
    print("   • Delete the duplicate image file")
    print("   • This will reduce storage and improve consistency")
    
    return True

def apply_deduplication(duplicate_cases):
    """Apply the deduplication changes."""
    if not duplicate_cases:
        return
    
    print(f"\n🔧 Applying deduplication to {len(duplicate_cases)} cases...")
    
    updated_files = set()
    deleted_files = []
    
    for i, case in enumerate(duplicate_cases, 1):
        print(f"\n📄 Processing case {i}: {case['html_file'].name}")
        
        # Determine which file to keep (prefer larger file)
        href_path = Path(case['href_file'])
        src_path = Path(case['src_file'])
        
        try:
            href_size = href_path.stat().st_size if href_path.exists() else 0
            src_size = src_path.stat().st_size if src_path.exists() else 0
            
            if href_size >= src_size:
                keep_file = case['href_name']
                delete_file = case['src_file']
                delete_name = case['src_name']
                print(f"   ✅ Keeping HREF image: {keep_file} ({href_size:,} bytes)")
            else:
                keep_file = case['src_name']
                delete_file = case['href_file']
                delete_name = case['href_name']
                print(f"   ✅ Keeping SRC image: {keep_file} ({src_size:,} bytes)")
            
            # Update HTML content
            html_file = case['html_file']
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace the pattern to use the same image for both href and src
            old_pattern = f'href="{case["href_name"]}"([^>]*>\\s*<img[^>]+)src="{case["src_name"]}"'
            new_pattern = f'href="{keep_file}"\\1src="{keep_file}"'
            
            updated_content = re.sub(old_pattern, new_pattern, content)
            
            if updated_content != content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                updated_files.add(str(html_file))
                print(f"   📝 Updated HTML file")
            
            # Delete the duplicate file
            if Path(delete_file).exists():
                os.remove(delete_file)
                deleted_files.append(delete_file)
                print(f"   🗑️  Deleted duplicate: {delete_name}")
            
        except Exception as e:
            print(f"   ❌ Error processing case: {e}")
    
    print(f"\n📊 Summary:")
    print(f"   • Updated {len(updated_files)} HTML files")
    print(f"   • Deleted {len(deleted_files)} duplicate image files")
    
    if deleted_files:
        total_saved = sum(Path(f).stat().st_size for f in deleted_files if Path(f).exists())
        print(f"   • Saved ~{total_saved:,} bytes of storage")

def main():
    """Main function."""
    print("🔍 Image Deduplication Analysis")
    print("=" * 50)
    
    # Check if posts directory exists
    posts_dir = Path('blog/legacy-posts-and-images')
    if not posts_dir.exists():
        print(f"❌ Directory not found: {posts_dir}")
        print("Please ensure blog posts are organized first")
        return
    
    # Analyze duplicates
    duplicate_cases, all_duplicates, all_references = analyze_duplicates()
    
    # Show general duplicate statistics
    if all_duplicates:
        print(f"\n📈 General duplicate statistics:")
        for hash_val, files in all_duplicates.items():
            if len(files) > 1:
                file_names = [Path(f).name for f in files]
                print(f"   🔑 {hash_val[:16]}... -> {len(files)} files: {', '.join(file_names[:3])}")
                if len(file_names) > 3:
                    print(f"      ... and {len(file_names) - 3} more")
    
    # Preview changes for href/src duplicates
    if preview_changes(duplicate_cases):
        print("\n" + "=" * 80)
        response = input("\n❓ Do you want to apply these changes? (y/N): ").strip().lower()
        
        if response in ['y', 'yes']:
            apply_deduplication(duplicate_cases)
            print("\n✅ Deduplication completed!")
        else:
            print("\n❌ Operation cancelled. No changes made.")
    else:
        print("\n✅ No deduplication needed for SRC/HREF pairs!")
        
        if all_duplicates:
            print(f"\nℹ️  Note: There are {len(all_duplicates)} groups of duplicate images")
            print("   but they don't appear to be SRC/HREF pairs in the same HTML.")
            print("   These might be legitimate copies used in different contexts.")

if __name__ == "__main__":
    main() 