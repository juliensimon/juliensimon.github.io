#!/usr/bin/env python3
"""
Extract all blog posts from Atom feed to HTML files.

This script processes an Atom XML feed and extracts all blog posts into individual
HTML files with proper formatting, CSS styling, and clean filenames.

Usage:
    python extract_blog_posts.py

Requirements:
    - feed.atom file in blog/legacy-posts/ directory
    - Python 3.6+

Output:
    - Individual HTML files in blog/legacy-posts-and-images/
    - Files named as YYYY-MM-DD-title.html
    - Clean HTML with embedded CSS styling
    - Code blocks wrapped in <code> tags
"""

import os
import re
from datetime import datetime
import xml.etree.ElementTree as ET

def clean_filename(text):
    """Create a clean filename from text."""
    # Remove HTML tags first
    text = re.sub(r'<[^>]+>', '', text)
    # Replace special characters with hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    # Replace spaces and multiple hyphens with single hyphen
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-').lower()

def clean_html_content(content):
    """Clean HTML content and wrap code blocks."""
    if not content:
        return ""
    
    # Decode HTML entities
    content = content.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    content = content.replace('&quot;', '"').replace('&#39;', "'")
    
    # Simple code block detection - wrap command lines in <code> tags
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        stripped = line.strip()
        # Check if line looks like a command
        if (stripped.startswith('$') or 
            stripped.startswith('#') or
            stripped.startswith('sudo ') or
            stripped.startswith('apt-get ') or
            stripped.startswith('make ') or
            stripped.startswith('./configure') or
            stripped.startswith('git ') or
            stripped.startswith('npm ') or
            stripped.startswith('docker ') or
            stripped.startswith('aws ') or
            any(stripped.startswith(cmd + ' ') for cmd in ['cd', 'ls', 'mv', 'cp', 'rm'])):
            cleaned_lines.append(f"<code>{line}</code>")
        else:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def create_html_template(title, date_str, content):
    """Create a complete HTML document with embedded styling."""
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        img {{
            display: block;
            margin: 1.5rem auto;
            max-width: 100%;
            height: auto;
            border-radius: 5px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            clear: both;
        }}
        
        /* Override any inline float styles on image links */
        a[style*="float"] {{
            float: none !important;
            clear: both !important;
            display: block !important;
            text-align: center !important;
            margin: 1.5rem auto !important;
        }}
        
        /* Center image containers */
        .separator {{
            text-align: center !important;
            clear: both !important;
            margin: 1.5rem 0 !important;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', Monaco, monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: 'Courier New', Monaco, monospace;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        .date {{
            color: #7f8c8d;
            font-style: italic;
            margin-bottom: 20px;
        }}
        .content {{
            margin-top: 30px;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="date">Published: {date_str}</div>
    <div class="content">
        {content}
    </div>
</body>
</html>'''

def extract_posts_from_atom(atom_file_path, output_dir):
    """Extract all posts from atom feed and save as HTML files."""
    
    # Parse the XML
    print(f"📖 Reading Atom feed: {atom_file_path}")
    tree = ET.parse(atom_file_path)
    root = tree.getroot()
    
    # Define namespace
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    
    # Find all entries
    entries = root.findall('atom:entry', ns)
    print(f"Found {len(entries)} entries in the feed")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    saved_count = 0
    
    for entry in entries:
        try:
            # Extract title
            title_elem = entry.find('atom:title', ns)
            title = title_elem.text if title_elem is not None else 'Untitled'
            
            # Extract content
            content_elem = entry.find('atom:content', ns)
            content = ''
            if content_elem is not None:
                content = content_elem.text or ''
            
            # Extract published date
            published_elem = entry.find('atom:published', ns)
            if published_elem is not None:
                published_str = published_elem.text
                # Parse the date (format: 2015-04-14T10:30:00.000-07:00)
                published_dt = datetime.fromisoformat(published_str.replace('Z', '+00:00'))
                date_str = published_dt.strftime('%Y-%m-%d')
                formatted_date = published_dt.strftime('%Y-%m-%d')
            else:
                date_str = '1970-01-01'
                formatted_date = '1970-01-01'
            
            # Clean the content
            cleaned_content = clean_html_content(content)
            
            # Create filename
            clean_title = clean_filename(title)
            filename = f"{date_str}-{clean_title}.html"
            filepath = os.path.join(output_dir, filename)
            
            # Create HTML content
            html_content = create_html_template(title, formatted_date, cleaned_content)
            
            # Save file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            saved_count += 1
            print(f"✅ Saved: {filename}")
            
        except Exception as e:
            print(f"❌ Error processing entry: {e}")
            continue
    
    print(f"\n🎉 Successfully extracted {saved_count} blog posts!")
    return saved_count

def main():
    """Main function."""
    atom_file = 'blog/legacy-posts/feed.atom'
    output_dir = 'blog/legacy-posts-and-images'
    
    if not os.path.exists(atom_file):
        print(f"❌ Atom file not found: {atom_file}")
        print("Please ensure the feed.atom file exists in blog/legacy-posts/")
        return
    
    print("🚀 Starting blog post extraction...")
    extract_posts_from_atom(atom_file, output_dir)

if __name__ == "__main__":
    main() 