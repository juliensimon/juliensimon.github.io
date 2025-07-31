#!/usr/bin/env python3
"""
Script to add Umami analytics to all HTML pages that don't already have it.
"""

import os
import glob
import re

def add_umami_to_file(file_path):
    """Add Umami analytics to a single HTML file."""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if Umami is already present
        if 'umami' in content.lower():
            return False  # Already has Umami
        
        # Find the head section
        head_match = re.search(r'(<head[^>]*>)', content, re.IGNORECASE)
        if not head_match:
            print(f"  ❌ No <head> tag found in {file_path}")
            return False
        
        head_start = head_match.start()
        
        # Find the closing head tag
        head_end_match = re.search(r'</head>', content, re.IGNORECASE)
        if not head_end_match:
            print(f"  ❌ No closing </head> tag found in {file_path}")
            return False
        
        head_end = head_end_match.end()
        
        # Extract head content
        head_content = content[head_start:head_end]
        
        # Check if title exists
        title_match = re.search(r'<title[^>]*>', head_content, re.IGNORECASE)
        if not title_match:
            print(f"  ❌ No <title> tag found in {file_path}")
            return False
        
        # Add Umami after the title
        title_end = title_match.end()
        umami_script = '''
<!-- Umami Analytics -->
<script defer src="https://cloud.umami.is/script.js" data-website-id="27550dad-d418-4f5d-ad1b-dab573da1020"></script>
<link rel="dns-prefetch" href="//cloud.umami.is">'''
        
        # Insert Umami after title
        new_head_content = head_content[:title_end] + umami_script + head_content[title_end:]
        
        # Replace the head section
        new_content = content[:head_start] + new_head_content + content[head_end:]
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {e}")
        return False

def main():
    """Add Umami to all HTML files."""
    
    print("Adding Umami analytics to all HTML pages...")
    
    # Find all HTML files
    html_files = glob.glob("**/*.html", recursive=True)
    
    # Filter out webp files and get unique files
    html_files = [f for f in html_files if not f.endswith('.webp')]
    
    print(f"Found {len(html_files)} HTML files")
    
    added_count = 0
    skipped_count = 0
    
    for file_path in html_files:
        print(f"Processing: {file_path}")
        
        if add_umami_to_file(file_path):
            print(f"  ✅ Added Umami to {file_path}")
            added_count += 1
        else:
            print(f"  ⏭️  Skipped {file_path} (already has Umami or error)")
            skipped_count += 1
    
    print(f"\n✅ Umami analytics addition completed!")
    print(f"📊 Summary:")
    print(f"   • Files processed: {len(html_files)}")
    print(f"   • Umami added: {added_count}")
    print(f"   • Skipped: {skipped_count}")
    print(f"\n🎯 Benefits:")
    print(f"   • Comprehensive analytics coverage")
    print(f"   • Better understanding of content performance")
    print(f"   • Privacy-focused analytics")

if __name__ == "__main__":
    main() 