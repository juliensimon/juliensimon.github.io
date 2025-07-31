#!/usr/bin/env python3
"""
Script to fix Umami analytics code that is incorrectly placed inside title tags.
This moves the Umami code outside the title tag to prevent it from appearing in tab names.
"""

import glob
import re

def fix_umami_inside_title(file_path):
    """Fix Umami analytics code that is incorrectly placed inside title tags."""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match title tag with Umami code inside it
        # This matches: <title>\n<!-- Umami Analytics -->\n<script...>\n<link...>\nActual Title</title>
        pattern = r'(<title>\s*)\n\s*(<!-- Umami Analytics -->\s*\n\s*<script[^>]*src="[^"]*umami[^"]*"[^>]*>\s*</script>\s*\n\s*<link[^>]*href="[^"]*umami[^"]*"[^>]*>\s*\n\s*)([^<]*</title>)'
        
        # Check if the problematic pattern exists
        if not re.search(pattern, content, re.DOTALL):
            return False  # No fix needed
        
        # Replace with properly formatted version
        # Move Umami code outside the title tag
        replacement = r'\1\3\n\n\2'
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {e}")
        return False

def main():
    """Fix Umami code inside title tags in all HTML files."""
    
    print("Fixing Umami analytics code inside title tags...")
    
    # Find all HTML files
    html_files = glob.glob("**/*.html", recursive=True)
    
    # Filter out webp files and get unique files
    html_files = [f for f in html_files if not f.endswith('.webp')]
    
    print(f"Found {len(html_files)} HTML files")
    
    fixed_count = 0
    skipped_count = 0
    
    for file_path in html_files:
        print(f"Processing: {file_path}")
        
        if fix_umami_inside_title(file_path):
            print(f"  ✅ Fixed Umami inside title in {file_path}")
            fixed_count += 1
        else:
            print(f"  ⏭️  Skipped {file_path} (no fix needed)")
            skipped_count += 1
    
    print(f"\n✅ Umami inside title fix completed!")
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