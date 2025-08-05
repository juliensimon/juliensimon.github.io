#!/usr/bin/env python3
"""
Script to apply simple, clean styling to legacy blog posts.
Just improves readability without fancy effects.
"""

import os
import re
import glob
from pathlib import Path

def apply_simple_styling(file_path):
    """Apply simple styling to a single blog post file."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the old CSS with simple styling
    old_css_pattern = r'<style>\s*body\s*\{[^}]*\}\s*img\s*\{[^}]*\}\s*a\[style\*="float"\]\s*\{[^}]*\}\s*\.separator\s*\{[^}]*\}\s*code\s*\{[^}]*\}\s*pre\s*\{[^}]*\}\s*h1\s*\{[^}]*\}\s*\.date\s*\{[^}]*\}\s*\.content\s*\{[^}]*\}\s*a\s*\{[^}]*\}\s*a:hover\s*\{[^}]*\}\s*</style>'
    
    new_css = '''    <link rel="stylesheet" href="../../../css/simple-blog-styles.css">'''
    
    # Replace the CSS
    content = re.sub(old_css_pattern, new_css, content, flags=re.DOTALL)
    
    # Remove any container divs that were added
    content = re.sub(r'<div class="container">\s*', '', content)
    content = re.sub(r'\s*</div>\s*<!--.*?-->', '<!--.*?-->', content)
    
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
            apply_simple_styling(file_path)
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    print(f"\n🎉 Successfully updated {len(html_files)} blog posts with simple styling!")
    print("✨ The posts now feature:")
    print("   - Clean, readable typography")
    print("   - Simple, professional layout")
    print("   - Better code block styling")
    print("   - Responsive design")
    print("   - No fancy effects - just readability")

if __name__ == "__main__":
    main() 