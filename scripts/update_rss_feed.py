#!/usr/bin/env python3
"""
Script to update the RSS feed with latest Arcee posts and other blog content.
"""

import os
import glob
import re
import json
from datetime import datetime

def extract_date_from_filename(filename):
    """Extract date from directory name."""
    match = re.search(r'^(\d{4}-\d{2}-\d{2})_', filename)
    if match:
        return match.group(1)
    return None

def get_metadata_from_json(file_path):
    """Extract metadata from the JSON file if it exists."""
    json_path = file_path.replace('index.html', 'metadata.json')
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                return metadata.get('title'), metadata.get('date'), metadata.get('url')
        except:
            pass
    return None, None, None

def extract_title_from_filename(filename):
    """Extract title from directory name."""
    # Remove date prefix and convert to title case
    name = filename.replace('_', ' ').title()
    # Remove date pattern (YYYY-MM-DD_)
    name = re.sub(r'^\d{4}-\d{2}-\d{2}\s+', '', name)
    
    # Fix common title formatting issues
    name = name.replace('Ai', 'AI')
    name = name.replace('Ml', 'ML')
    name = name.replace('Nlp', 'NLP')
    name = name.replace('Cpu', 'CPU')
    name = name.replace('Gpu', 'GPU')
    name = name.replace('Api', 'API')
    name = name.replace('Sdk', 'SDK')
    name = name.replace('Iot', 'IoT')
    name = name.replace('Rag', 'RAG')
    name = name.replace('Llms', 'LLMs')
    name = name.replace('Slms', 'SLMs')
    name = name.replace('Arcee', 'Arcee')
    name = name.replace('Yuppai', 'Yupp.ai')
    name = name.replace('Togetherai', 'Together AI')
    name = name.replace('Openrouter', 'OpenRouter')
    name = name.replace('Xeon', 'Xeon')
    name = name.replace('Arm', 'ARM')
    
    return name

def format_rss_date(date_str):
    """Convert date string to RSS format."""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%a, %d %b %Y 12:00:00 +0000')
    except:
        return "Sat, 18 Jan 2025 12:00:00 +0000"

def create_rss_items():
    """Create RSS items for blog posts."""
    items = []
    
    # Add Arcee posts
    arcee_pattern = "blog/arcee-posts/*/index.html"
    arcee_files = glob.glob(arcee_pattern)
    
    for file_path in arcee_files:
        dir_name = os.path.basename(os.path.dirname(file_path))
        date = extract_date_from_filename(dir_name)
        
        # Try to get metadata from JSON file
        json_title, json_date, original_url = get_metadata_from_json(file_path)
        if json_title:
            title = json_title
        else:
            title = extract_title_from_filename(dir_name)
        
        if json_date:
            date = json_date
        
        if not date:
            continue
        
        # Generate canonical URL
        post_url = dir_name.replace('_', '-')
        canonical_url = f"https://www.julien.org/blog/{post_url}/"
        
        # Create description
        description = f"Expert analysis and technical deep-dive on {title.lower()} by Julien Simon, leading voice in small language models and edge AI."
        
        items.append({
            'title': title,
            'link': canonical_url,
            'guid': canonical_url,
            'pubDate': format_rss_date(date),
            'description': description,
            'categories': ['Arcee AI', 'Small Language Models', 'AI', 'Technical Analysis']
        })
    
    # Add HuggingFace posts (recent ones)
    hf_pattern = "blog/huggingface-posts-and-images/*/index.html"
    hf_files = glob.glob(hf_pattern)
    
    # Sort by date and take recent ones
    hf_files_with_dates = []
    for file_path in hf_files:
        dir_name = os.path.basename(os.path.dirname(file_path))
        date = extract_date_from_filename(dir_name)
        if date:
            hf_files_with_dates.append((file_path, date))
    
    # Sort by date (newest first) and take top 5
    hf_files_with_dates.sort(key=lambda x: x[1], reverse=True)
    
    for file_path, date in hf_files_with_dates[:5]:
        dir_name = os.path.basename(os.path.dirname(file_path))
        title = extract_title_from_filename(dir_name)
        
        post_url = dir_name.replace('_', '-')
        canonical_url = f"https://www.julien.org/blog/{post_url}/"
        
        description = f"Expert analysis on {title.lower()} by Julien Simon, former Chief Evangelist at Hugging Face and leading voice in open-source AI."
        
        items.append({
            'title': title,
            'link': canonical_url,
            'guid': canonical_url,
            'pubDate': format_rss_date(date),
            'description': description,
            'categories': ['Hugging Face', 'Open Source AI', 'AI', 'Technical Analysis']
        })
    
    # Sort all items by date (newest first)
    items.sort(key=lambda x: x['pubDate'], reverse=True)
    
    return items

def update_rss_feed():
    """Update the RSS feed with latest content."""
    
    current_date = datetime.now().strftime('%a, %d %b %Y 12:00:00 +0000')
    items = create_rss_items()
    
    rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:sy="http://purl.org/rss/1.0/modules/syndication/">
  <channel>
    <title>Julien Simon - AI Expert & Technical Evangelist</title>
    <link>https://www.julien.org/</link>
    <description>Leading voice in Practical AI, Chief Evangelist at Arcee AI, specializing in Small Language Models and enterprise AI solutions</description>
    <language>en-us</language>
    <lastBuildDate>{current_date}</lastBuildDate>
    <generator>Julien Simon's Website</generator>
    <webMaster>julien@julien.org</webMaster>
    <managingEditor>julien@julien.org</managingEditor>
    <category>Technology</category>
    <category>Artificial Intelligence</category>
    <category>Machine Learning</category>
    <category>Small Language Models</category>
    <image>
      <url>https://www.julien.org/assets/julien.webp</url>
      <title>Julien Simon</title>
      <link>https://www.julien.org/</link>
      <width>200</width>
      <height>200</height>
    </image>
    <atom:link href="https://www.julien.org/feed.xml" rel="self" type="application/rss+xml"/>
    <sy:updatePeriod>weekly</sy:updatePeriod>
    <sy:updateFrequency>1</sy:updateFrequency>
"""
    
    # Add items
    for item in items:
        categories_xml = '\n'.join([f'    <category>{cat}</category>' for cat in item['categories']])
        
        rss_content += f"""
    <item>
      <title>{item['title']}</title>
      <link>{item['link']}</link>
      <guid>{item['guid']}</guid>
      <pubDate>{item['pubDate']}</pubDate>
      <description>{item['description']}</description>
{categories_xml}
    </item>"""
    
    rss_content += """
  </channel>
</rss>"""
    
    # Write the updated RSS feed
    with open('feed.xml', 'w', encoding='utf-8') as f:
        f.write(rss_content)
    
    print(f"Updated RSS feed with {len(items)} items")

def main():
    """Main function to update RSS feed."""
    update_rss_feed()
    print("RSS feed update completed!")

if __name__ == "__main__":
    main() 