#!/usr/bin/env python3
"""
Fix incorrect YouTube links in video files.

This script fixes the "Back to YouTube Overview" links that incorrectly point to
youtube.html instead of the correct paths.
"""

import re
import shutil
from pathlib import Path

def fix_youtube_links_in_file(file_path):
    """Fix YouTube links in a single file."""
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match the incorrect YouTube link
        # This matches the "Back to YouTube Overview" link that points to ../../youtube.html
        incorrect_pattern = r'href="../../youtube\.html"'
        correct_replacement = 'href="../../index.html"'
        
        # Check if the pattern exists in the file
        if re.search(incorrect_pattern, content):
            # Create backup
            backup_path = str(file_path) + '.link_backup'
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

def scan_video_files():
    """Scan all video files in the youtube directory."""
    video_files = []
    
    # Scan all HTML files in youtube subdirectories (excluding index.html files)
    youtube_dir = Path('youtube')
    if youtube_dir.exists():
        for html_file in youtube_dir.rglob('*.html'):
            if html_file.is_file() and html_file.name != 'index.html':
                video_files.append(html_file)
    
    return video_files

def main():
    """Main function to fix YouTube links in all video files."""
    print("🔍 Scanning for video files...")
    video_files = scan_video_files()
    print(f"Found {len(video_files)} video files")
    
    print("\n🔧 Fixing YouTube links...")
    files_processed = 0
    files_modified = 0
    
    for file_path in video_files:
        files_processed += 1
        if fix_youtube_links_in_file(file_path):
            files_modified += 1
            print(f"✅ Fixed: {file_path}")
        
        # Progress indicator
        if files_processed % 50 == 0:
            print(f"Progress: {files_processed}/{len(video_files)} files processed")
    
    print(f"\n🎉 Complete!")
    print(f"📊 Results:")
    print(f"   - Files processed: {files_processed}")
    print(f"   - Files modified: {files_modified}")
    print(f"   - Files unchanged: {files_processed - files_modified}")
    
    if files_modified > 0:
        print(f"\n💾 Backup files created with '.link_backup' extension")
        print("   You can restore files if needed by removing the '.link_backup' extension")
        print(f"\n🔗 Fixed links:")
        print(f"   - Changed 'href=\"../../youtube.html\"' to 'href=\"../../index.html\"'")
        print(f"   - This now correctly links to the year overview page")

if __name__ == "__main__":
    main() 