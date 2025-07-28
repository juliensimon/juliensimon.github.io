#!/usr/bin/env python3
"""
Fix incorrect YouTube links in year index pages.

This script fixes the "Back to YouTube Overview" links in year index pages
that incorrectly point to ../youtube.html instead of the correct paths.
"""

import re
import shutil
from pathlib import Path

def fix_year_index_links_in_file(file_path):
    """Fix YouTube links in a year index file."""
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match the incorrect YouTube link
        # This matches the "Back to YouTube Overview" link that points to ../youtube.html
        incorrect_pattern = r'href="../youtube\.html"'
        correct_replacement = 'href="../../youtube.html"'
        
        # Check if the pattern exists in the file
        if re.search(incorrect_pattern, content):
            # Create backup
            backup_path = str(file_path) + '.year_backup'
            shutil.copy2(file_path, backup_path)
            
            # Replace the incorrect link
            new_content = re.sub(incorrect_pattern, correct_replacement, content)
            
            # Write the updated content back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def scan_year_index_files():
    """Scan all year index files in the youtube directory."""
    year_index_files = []
    
    # Scan all index.html files in youtube year subdirectories
    youtube_dir = Path('youtube')
    if youtube_dir.exists():
        for year_dir in youtube_dir.iterdir():
            if year_dir.is_dir() and year_dir.name.isdigit():
                index_file = year_dir / 'index.html'
                if index_file.exists():
                    year_index_files.append(index_file)
    
    return year_index_files

def main():
    """Main function to fix YouTube links in all year index files."""
    print("🔍 Scanning for year index files...")
    year_index_files = scan_year_index_files()
    print(f"Found {len(year_index_files)} year index files")
    
    print("\n🔧 Fixing year index links...")
    files_processed = 0
    files_modified = 0
    
    for file_path in year_index_files:
        files_processed += 1
        if fix_year_index_links_in_file(file_path):
            files_modified += 1
            print(f"✅ Fixed: {file_path}")
        else:
            print(f"ℹ️  No changes needed: {file_path}")
    
    print(f"\n🎉 Complete!")
    print(f"📊 Results:")
    print(f"   - Files processed: {files_processed}")
    print(f"   - Files modified: {files_modified}")
    print(f"   - Files unchanged: {files_processed - files_modified}")
    
    if files_modified > 0:
        print(f"\n💾 Backup files created with '.year_backup' extension")
        print("   You can restore files if needed by removing the '.year_backup' extension")
        print(f"\n🔗 Fixed links:")
        print(f"   - Changed 'href=\"../youtube.html\"' to 'href=\"../../youtube.html\"'")
        print(f"   - This now correctly links to the main YouTube overview page at youtube.html")

if __name__ == "__main__":
    main() 