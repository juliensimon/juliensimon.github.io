#!/usr/bin/env python3
"""
Script to update individual video pages to replace the 2 buttons at the bottom 
with a single back link to the main YouTube page.
"""

import os
from pathlib import Path
from bs4 import BeautifulSoup
import glob

def update_video_page(video_file_path):
    """Update a single video page to replace the bottom buttons with a back link."""
    try:
        with open(video_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the links div
        links_div = soup.find('div', class_='links')
        if links_div:
            # Clear existing links and add only the back link
            links_div.clear()
            back_link = soup.new_tag('a', href='../../youtube.html', attrs={'class': 'link'})
            back_link.string = '← Back to YouTube Overview'
            links_div.append(back_link)
        
        # Write the updated content
        with open(video_file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        return True
    except Exception as e:
        print(f"Error updating {video_file_path}: {e}")
        return False

def main():
    """Update all video pages in all year directories."""
    # Get all year directories
    youtube_dir = Path('youtube')
    year_dirs = [d for d in youtube_dir.iterdir() if d.is_dir() and d.name.isdigit()]
    
    total_updated = 0
    total_files = 0
    
    for year_dir in year_dirs:
        print(f"Processing {year_dir.name}...")
        
        # Get all HTML files in the year directory (excluding index.html)
        html_files = [f for f in year_dir.glob('*.html') if f.name != 'index.html']
        
        for html_file in html_files:
            total_files += 1
            if update_video_page(html_file):
                total_updated += 1
                print(f"  Updated: {html_file.name}")
            else:
                print(f"  Failed: {html_file.name}")
    
    print(f"\nSummary:")
    print(f"  Total files processed: {total_files}")
    print(f"  Successfully updated: {total_updated}")
    print(f"  Failed: {total_files - total_updated}")

if __name__ == "__main__":
    main() 