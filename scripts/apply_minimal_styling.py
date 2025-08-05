#!/usr/bin/env python3
"""
Script to apply minimal styling to legacy blog posts.
Just white backgrounds and basic readability.
"""

import os
import re
import glob
from pathlib import Path

def apply_minimal_styling(file_path):
    """Apply minimal styling to a single blog post file."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace any existing CSS with minimal styling
    old_css_pattern = r'<link rel="stylesheet" href="../../../css/[^"]*">'
    new_css = '''    <link rel="stylesheet" href="../../../css/minimal-blog-styles.css">'''
    
    # Replace the CSS
    content = re.sub(old_css_pattern, new_css, content)
    
    # Remove any inline styles that were added
    content = re.sub(r'<style>[^<]*</style>', '', content)
    
    # Write the updated content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated: {file_path}")

def main():
    """Main function to process all legacy blog posts."""
    
    # Find all legacy blog posts
    legacy_dir = Path("blog/legacy-posts-and-images")
    
    if not legacy_dir.exists():
        print("❌ Legacy posts directory not found!")
        return
    
    # Find all HTML files in subdirectories
    html_files = []
    for year_dir in legacy_dir.iterdir():
        if year_dir.is_dir():
            html_files.extend(year_dir.glob("*.html"))
    
    print(f"📁 Found {len(html_files)} legacy blog posts to update")
    
    # Process each file
    for file_path in html_files:
        try:
            apply_minimal_styling(file_path)
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    print(f"\n🎉 Successfully updated {len(html_files)} blog posts with minimal styling!")
    print("✨ The posts now feature:")
    print("   - White backgrounds")
    print("   - Basic readability")
    print("   - Simple layout")
    print("   - No fancy effects")

if __name__ == "__main__":
    main() 