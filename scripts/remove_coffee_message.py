#!/usr/bin/env python3
"""
Remove coffee donation message from all video files.

This script removes the "Want to buy me a coffee?" message from all video HTML files.
"""

import re
import shutil
from pathlib import Path

def remove_coffee_message_from_file(file_path):
    """Remove coffee donation message from a single file."""
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match the coffee donation message
        # This pattern matches the entire message including the HTML link
        coffee_pattern = r'⭐️⭐️⭐️ Want to buy me a coffee\? I can always use more :\) <a href="https://www\.buymeacoffee\.com/julsimon" rel="noopener noreferrer" target="_blank">https://www\.buymeacoffee\.com/julsimon</a> ⭐️⭐️⭐️'
        
        # Check if the pattern exists in the file
        if re.search(coffee_pattern, content):
            # Create backup
            backup_path = str(file_path) + '.coffee_backup'
            shutil.copy2(file_path, backup_path)
            
            # Remove the coffee message
            new_content = re.sub(coffee_pattern, '', content)
            
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
    
    # Scan all HTML files in youtube subdirectories
    youtube_dir = Path('youtube')
    if youtube_dir.exists():
        for html_file in youtube_dir.rglob('*.html'):
            if html_file.is_file():
                video_files.append(html_file)
    
    return video_files

def main():
    """Main function to remove coffee messages from all video files."""
    print("🔍 Scanning for video files...")
    video_files = scan_video_files()
    print(f"Found {len(video_files)} video files")
    
    print("\n🗑️  Removing coffee donation messages...")
    files_processed = 0
    files_modified = 0
    
    for file_path in video_files:
        files_processed += 1
        if remove_coffee_message_from_file(file_path):
            files_modified += 1
            print(f"✅ Modified: {file_path}")
        
        # Progress indicator
        if files_processed % 10 == 0:
            print(f"Progress: {files_processed}/{len(video_files)} files processed")
    
    print(f"\n🎉 Complete!")
    print(f"📊 Results:")
    print(f"   - Files processed: {files_processed}")
    print(f"   - Files modified: {files_modified}")
    print(f"   - Files unchanged: {files_processed - files_modified}")
    
    if files_modified > 0:
        print(f"\n💾 Backup files created with '.coffee_backup' extension")
        print("   You can restore files if needed by removing the '.coffee_backup' extension")

if __name__ == "__main__":
    main() 