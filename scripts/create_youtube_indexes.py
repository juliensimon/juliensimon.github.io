#!/usr/bin/env python3
"""
Script to create index.html files for YouTube year directories.
"""

import os
import re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

def extract_date_from_filename(filename):
    """Extract date from filename like 20250103_..."""
    match = re.match(r'(\d{8})_', filename)
    if match:
        date_str = match.group(1)
        try:
            date_obj = datetime.strptime(date_str, '%Y%m%d')
            return date_obj.strftime('%B %d, %Y')
        except ValueError:
            pass
    return "Unknown Date"

def create_index_for_year(year_dir):
    """Create an index.html file for a specific year directory."""
    year = year_dir.name
    
    # Get all HTML files in the directory
    html_files = list(year_dir.glob('*.html'))
    
    # Filter out index.html if it exists
    html_files = [f for f in html_files if f.name != 'index.html']
    
    if not html_files:
        print(f"No HTML files found in {year_dir}")
        return
    
    # Sort files by date (newest first)
    html_files.sort(key=lambda x: x.name, reverse=True)
    
    # Create the HTML content
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Julien Simon - YouTube Videos {year}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2.5em;
            text-align: center;
        }}
        .subtitle {{
            color: #7f8c8d;
            font-size: 1.2em;
            text-align: center;
            margin-bottom: 40px;
        }}
        .video-list {{
            display: grid;
            gap: 20px;
        }}
        .video-item {{
            border: 1px solid #e1e8ed;
            border-radius: 8px;
            padding: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .video-item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .video-title {{
            color: #2c3e50;
            font-size: 1.3em;
            font-weight: 600;
            margin-bottom: 8px;
            text-decoration: none;
        }}
        .video-title:hover {{
            color: #3498db;
        }}
        .video-date {{
            color: #7f8c8d;
            font-size: 0.95em;
            font-weight: 500;
        }}
        .video-tags {{
            margin-top: 8px;
        }}
        .video-tag {{
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 4px 8px;
            margin: 2px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 500;
        }}
        .stats {{
            text-align: center;
            color: #7f8c8d;
            font-size: 1.1em;
            margin-bottom: 30px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 6px;
        }}
        .links {{
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-top: 40px;
            flex-wrap: wrap;
        }}
        .link {{
            display: inline-block;
            padding: 12px 24px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 500;
            transition: background-color 0.3s;
        }}
        .link:hover {{
            background: #2980b9;
        }}
        .link.youtube {{
            background: #e74c3c;
        }}
        .link.youtube:hover {{
            background: #c0392b;
        }}
        @media (max-width: 600px) {{
            .container {{
                padding: 20px;
            }}
            h1 {{
                font-size: 2em;
            }}
            .video-item {{
                padding: 15px;
            }}
            .links {{
                flex-direction: column;
                align-items: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>YouTube Videos - {year}</h1>
        <div class="subtitle">{len(html_files)} videos from {year}</div>
        
        <div class="stats">
            <strong>{len(html_files)}</strong> videos in {year}
        </div>
        
        <div class="video-list">'''
    
    # Add video items
    for html_file in html_files:
        # Skip index.html file
        if html_file.name == 'index.html':
            continue
            
        # Extract title from filename and remove YYYYMMDD timestamp
        title = html_file.stem.replace('_', ' ').replace('-', ' ')
        # Remove the YYYYMMDD_ prefix from the title
        title = re.sub(r'^\d{8}_', '', title)
        # Also remove any remaining YYYYMMDD patterns that might be in the middle
        title = re.sub(r'\d{8}', '', title)
        
        # Extract date
        date = extract_date_from_filename(html_file.name)
        
        html_content += f'''
            <div class="video-item">
                <a href="{html_file.name}" class="video-title">{title}</a>
                <div class="video-date">{date}</div>
            </div>'''
    
    html_content += '''
        </div>
        
        <div class="links">
            <a href="../youtube.html" class="link">← Back to YouTube Overview</a>
        </div>
    </div>
</body>
</html>'''
    
    # Write the index file
    index_file = year_dir / 'index.html'
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Created {index_file} with {len(html_files)} videos")

def main():
    """Main function to create indexes for all year directories."""
    youtube_dir = Path('youtube')
    
    if not youtube_dir.exists():
        print("YouTube directory not found")
        return
    
    # Find all year directories
    year_dirs = [d for d in youtube_dir.iterdir() if d.is_dir() and d.name.isdigit()]
    
    for year_dir in sorted(year_dirs, reverse=True):
        index_file = year_dir / 'index.html'
        if not index_file.exists():
            print(f"Creating index for {year_dir.name}...")
            create_index_for_year(year_dir)
        else:
            print(f"Index already exists for {year_dir.name}")

if __name__ == "__main__":
    main() 