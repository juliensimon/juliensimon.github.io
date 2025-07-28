#!/usr/bin/env python3
"""
Script to update yearly YouTube index pages to include tags and back links.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import glob

def extract_tags_from_video_page(video_file_path):
    """Extract tags from a video page."""
    try:
        with open(video_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        tags_div = soup.find('div', class_='tags')
        
        if tags_div:
            # Find all tag spans
            tag_spans = tags_div.find_all('span', class_='tag')
            tags = [span.text.strip() for span in tag_spans]
            return tags
        return []
    except Exception as e:
        print(f"Error extracting tags from {video_file_path}: {e}")
        return []

def update_yearly_index(year_dir):
    """Update the index.html file for a specific year."""
    index_file = year_dir / 'index.html'
    
    if not index_file.exists():
        print(f"Index file not found for {year_dir}")
        return
    
    # Read the current index file
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all video items
    video_items = soup.find_all('div', class_='video-item')
    
    for video_item in video_items:
        # Find the video link
        video_link = video_item.find('a', class_='video-title')
        if not video_link:
            continue
        
        video_href = video_link.get('href')
        if not video_href or video_href == 'index.html':
            continue
        
        # Extract tags from the video page
        video_file = year_dir / video_href
        if video_file.exists():
            tags = extract_tags_from_video_page(video_file)
            
            # Remove existing tags div if it exists
            existing_tags = video_item.find('div', class_='video-tags')
            if existing_tags:
                existing_tags.decompose()
            
            # Add tags if we found any
            if tags:
                tags_div = soup.new_tag('div', attrs={'class': 'video-tags'})
                for tag in tags:
                    tag_span = soup.new_tag('span', attrs={'class': 'video-tag'})
                    tag_span.string = tag
                    tags_div.append(tag_span)
                
                # Insert tags after the video date
                video_date = video_item.find('div', class_='video-date')
                if video_date:
                    video_date.insert_after(tags_div)
    
    # Remove the stats section (duplicated count)
    stats_div = soup.find('div', class_='stats')
    if stats_div:
        stats_div.decompose()
    
    # Update the back link section
    links_div = soup.find('div', class_='links')
    if links_div:
        # Clear existing links and add only the back link
        links_div.clear()
        back_link = soup.new_tag('a', href='../youtube.html', attrs={'class': 'link'})
        back_link.string = '← Back to YouTube Overview'
        links_div.append(back_link)
    
    # Add CSS for tags
    style_tag = soup.find('style')
    if style_tag:
        # Add tag styles to existing style
        tag_css = """
        .video-tags {
            margin-top: 8px;
        }
        .video-tag {
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 4px 8px;
            margin: 2px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 500;
        }
        """
        style_tag.string += tag_css
    
    # Write the updated content
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"Updated {index_file}")

def main():
    """Main function to update all yearly indexes."""
    youtube_dir = Path('youtube')
    
    if not youtube_dir.exists():
        print("YouTube directory not found")
        return
    
    # Find all year directories
    year_dirs = [d for d in youtube_dir.iterdir() if d.is_dir() and d.name.isdigit()]
    
    for year_dir in sorted(year_dirs, reverse=True):
        print(f"Processing {year_dir.name}...")
        update_yearly_index(year_dir)

if __name__ == "__main__":
    main() 