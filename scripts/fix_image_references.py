#!/usr/bin/env python3
"""
Comprehensive Image Reference Fixer
Finds and fixes HREF/SRC mismatches across all blog posts and removes unused images.

This script is useful for maintaining blog image consistency and cleaning up
orphaned image files.

Usage: python scripts/fix_image_references.py
"""

import os
import re
import hashlib
from collections import defaultdict
from pathlib import Path

def find_all_html_files():
    """Find all HTML blog post files."""
    blog_dir = Path("blog/legacy-posts-and-images")
    if not blog_dir.exists():
        print(f"❌ Blog directory not found: {blog_dir}")
        return []
    
    html_files = []
    for root, dirs, files in os.walk(blog_dir):
        for file in files:
            if file.endswith('.html') and file != 'index.html':
                html_files.append(Path(root) / file)
    
    return sorted(html_files)

def find_all_images():
    """Find all image files."""
    blog_dir = Path("blog/legacy-posts-and-images")
    image_extensions = {'.webp', '.jpg', '.jpeg', '.png', '.gif'}
    images = []
    
    for root, dirs, files in os.walk(blog_dir):
        for file in files:
            if Path(file).suffix.lower() in image_extensions:
                images.append(Path(root) / file)
    
    return sorted(images)

def extract_image_references(html_content):
    """Extract all image references from HTML content."""
    # Pattern to match <a href="..."><img src="..."></a> structures
    pattern = r'<a[^>]*href="([^"]*(?:\.webp|\.jpg|\.jpeg|\.png|\.gif))"[^>]*>.*?<img[^>]*src="([^"]*(?:\.webp|\.jpg|\.jpeg|\.png|\.gif))"[^>]*>.*?</a>'
    matches = re.findall(pattern, html_content, re.IGNORECASE | re.DOTALL)
    
    # Also find standalone img tags without href
    img_pattern = r'<img[^>]*src="([^"]*(?:\.webp|\.jpg|\.jpeg|\.png|\.gif))"[^>]*>'
    img_matches = re.findall(img_pattern, html_content, re.IGNORECASE)
    
    return matches, img_matches

def analyze_html_file(html_file):
    """Analyze a single HTML file for image reference issues."""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        href_src_pairs, standalone_imgs = extract_image_references(content)
        
        issues = []
        all_referenced_images = set()
        
        # Check HREF/SRC mismatches
        for href, src in href_src_pairs:
            # Extract just the filename from paths
            href_file = os.path.basename(href)
            src_file = os.path.basename(src)
            
            all_referenced_images.add(src_file)
            
            if href_file != src_file:
                issues.append({
                    'type': 'mismatch',
                    'href': href,
                    'src': src,
                    'href_file': href_file,
                    'src_file': src_file
                })
        
        # Add standalone images
        for img_src in standalone_imgs:
            img_file = os.path.basename(img_src)
            all_referenced_images.add(img_file)
        
        return issues, all_referenced_images, content
        
    except Exception as e:
        print(f"❌ Error analyzing {html_file}: {e}")
        return [], set(), ""

def fix_html_file(html_file, issues, content, dry_run=False):
    """Fix HREF/SRC mismatches in HTML file."""
    if not issues:
        return content, False
    
    fixed_content = content
    changes_made = False
    
    for issue in issues:
        if issue['type'] == 'mismatch':
            # Replace href to match src
            old_pattern = f'href="{issue["href"]}"'
            new_pattern = f'href="{issue["src"]}"'
            
            if old_pattern in fixed_content:
                if not dry_run:
                    fixed_content = fixed_content.replace(old_pattern, new_pattern)
                changes_made = True
                action = "Would fix" if dry_run else "Fixed"
                print(f"   {action}: {issue['href_file']} → {issue['src_file']}")
    
    return fixed_content, changes_made

def find_unused_images(year_dir, referenced_images):
    """Find images in year directory that are not referenced."""
    if not year_dir.exists():
        return []
    
    image_extensions = {'.webp', '.jpg', '.jpeg', '.png', '.gif'}
    all_images = []
    
    for file in year_dir.iterdir():
        if file.is_file() and file.suffix.lower() in image_extensions:
            all_images.append(file.name)
    
    unused = []
    for img in all_images:
        if img not in referenced_images:
            unused.append(year_dir / img)
    
    return unused

def compute_file_hash(filepath):
    """Compute SHA256 hash of a file for duplicate detection."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"❌ Error hashing {filepath}: {e}")
        return None

def find_duplicate_images():
    """Find duplicate images by SHA256 hash."""
    image_files = find_all_images()
    hash_to_files = defaultdict(list)
    
    print("🔢 Computing hashes for duplicate detection...")
    for i, image_path in enumerate(image_files, 1):
        if i % 20 == 0:
            print(f"   Progress: {i}/{len(image_files)} ({i/len(image_files)*100:.1f}%)")
        
        file_hash = compute_file_hash(image_path)
        if file_hash:
            hash_to_files[file_hash].append(image_path)
    
    duplicates = {h: files for h, files in hash_to_files.items() if len(files) > 1}
    return duplicates

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Fix image references and clean up unused images')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without making changes')
    parser.add_argument('--check-duplicates', action='store_true', help='Also check for duplicate images by hash')
    args = parser.parse_args()
    
    print("🔍 Comprehensive Image Reference Analysis")
    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
    print("=" * 60)
    
    # Find all HTML files
    html_files = find_all_html_files()
    print(f"📄 Found {len(html_files)} HTML files")
    
    if not html_files:
        print("❌ No HTML files found!")
        return
    
    total_issues = 0
    total_fixes = 0
    total_unused = 0
    year_stats = defaultdict(lambda: {'issues': 0, 'fixes': 0, 'unused': 0})
    
    # Group files by year
    files_by_year = defaultdict(list)
    for html_file in html_files:
        # Extract year from path
        year = None
        for part in html_file.parts:
            if part.isdigit() and len(part) == 4 and part.startswith('20'):
                year = part
                break
        if year:
            files_by_year[year].append(html_file)
    
    # Process each year
    for year in sorted(files_by_year.keys()):
        year_files = files_by_year[year]
        print(f"\n📅 Processing {year} ({len(year_files)} files)...")
        
        year_referenced_images = set()
        year_issues = []
        
        # Analyze all files in this year
        for html_file in year_files:
            issues, referenced_images, content = analyze_html_file(html_file)
            year_referenced_images.update(referenced_images)
            
            if issues:
                year_issues.append((html_file, issues, content))
                year_stats[year]['issues'] += len(issues)
                total_issues += len(issues)
        
        # Fix issues
        for html_file, issues, content in year_issues:
            action = "Would fix" if args.dry_run else "Fixing"
            print(f"   🔧 {action} {html_file.name}:")
            fixed_content, changes_made = fix_html_file(html_file, issues, content, args.dry_run)
            
            if changes_made and not args.dry_run:
                try:
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    year_stats[year]['fixes'] += len(issues)
                    total_fixes += len(issues)
                except Exception as e:
                    print(f"      ❌ Error writing {html_file}: {e}")
            elif changes_made:
                year_stats[year]['fixes'] += len(issues)
                total_fixes += len(issues)
        
        # Find and remove unused images
        year_dir = Path("blog/legacy-posts-and-images") / year
        unused_images = find_unused_images(year_dir, year_referenced_images)
        
        if unused_images:
            action = "Would remove" if args.dry_run else "Removing"
            print(f"   🗑️  {action} {len(unused_images)} unused images:")
            for unused_img in unused_images:
                try:
                    file_size = unused_img.stat().st_size
                    if not args.dry_run:
                        unused_img.unlink()
                    action_word = "Would delete" if args.dry_run else "Deleted"
                    print(f"      {action_word}: {unused_img.name} ({file_size:,} bytes)")
                    year_stats[year]['unused'] += 1
                    total_unused += 1
                except Exception as e:
                    print(f"      ❌ Error deleting {unused_img}: {e}")
    
    # Check for duplicates if requested
    if args.check_duplicates:
        print(f"\n🔍 Checking for duplicate images...")
        duplicates = find_duplicate_images()
        if duplicates:
            print(f"Found {len(duplicates)} groups of duplicate images:")
            for i, (hash_val, files) in enumerate(duplicates.items(), 1):
                print(f"  Group {i} (Hash: {hash_val[:12]}...):")
                for file in files:
                    file_size = file.stat().st_size
                    print(f"    📁 {file} ({file_size:,} bytes)")
        else:
            print("✅ No duplicate images found!")
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"   Total HREF/SRC mismatches found: {total_issues}")
    action_word = "would be fixed" if args.dry_run else "fixed"
    print(f"   Total mismatches {action_word}: {total_fixes}")
    action_word = "would be removed" if args.dry_run else "removed"
    print(f"   Total unused images {action_word}: {total_unused}")
    
    if year_stats:
        print(f"\n📅 By Year:")
        for year in sorted(year_stats.keys()):
            stats = year_stats[year]
            print(f"   {year}: {stats['fixes']} fixes, {stats['unused']} unused images")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main() 