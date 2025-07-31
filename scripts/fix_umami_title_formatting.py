#!/usr/bin/env python3
"""
Script to fix Umami analytics formatting in HTML files.
Fixes the issue where HTML comments appear in Firefox tab names.
"""

import glob
import re

def fix_umami_formatting(file_path):
    """Fix Umami analytics formatting in a single HTML file."""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match title tag followed immediately by Umami comment
        # This matches: </title><!-- Umami Analytics -->
        pattern = r'(</title>)<!-- Umami Analytics -->'
        
        # Check if the problematic pattern exists
        if not re.search(pattern, content):
            return False  # No fix needed
        
        # Replace with properly formatted version
        replacement = r'\1\n\n<!-- Umami Analytics -->'
        new_content = re.sub(pattern, replacement, content)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {e}")
        return False

def main():
    """Fix Umami formatting in all HTML files."""
    
    print("Fixing Umami analytics formatting in HTML pages...")
    
    # Find all HTML files
    html_files = glob.glob("**/*.html", recursive=True)
    
    # Filter out webp files and get unique files
    html_files = [f for f in html_files if not f.endswith('.webp')]
    
    print(f"Found {len(html_files)} HTML files")
    
    fixed_count = 0
    skipped_count = 0
    
    for file_path in html_files:
        print(f"Processing: {file_path}")
        
        if fix_umami_formatting(file_path):
            print(f"  ✅ Fixed Umami formatting in {file_path}")
            fixed_count += 1
        else:
            print(f"  ⏭️  Skipped {file_path} (no fix needed)")
            skipped_count += 1
    
    print(f"\n✅ Umami formatting fix completed!")
    print(f"📊 Summary:")
    print(f"   • Files processed: {len(html_files)}")
    print(f"   • Fixed: {fixed_count}")
    print(f"   • Skipped: {skipped_count}")
    print(f"\n🎯 Benefits:")
    print(f"   • Firefox tabs will show proper titles")
    print(f"   • No more HTML comments in tab names")
    print(f"   • Better user experience")

if __name__ == "__main__":
    main() 