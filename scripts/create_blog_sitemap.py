#!/usr/bin/env python3
"""
Script to create a comprehensive blog sitemap including Arcee posts and other blog content.
"""

import os
import glob
import re
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
            import json
            with open(json_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                return metadata.get('title'), metadata.get('date'), metadata.get('url')
        except:
            pass
    return None, None, None

def create_blog_sitemap():
    """Create a comprehensive blog sitemap."""
    
    sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
"""
    
    # Add Arcee posts
    arcee_pattern = "blog/arcee-posts/*/index.html"
    arcee_files = glob.glob(arcee_pattern)
    
    print(f"Found {len(arcee_files)} Arcee posts")
    
    for file_path in arcee_files:
        dir_name = os.path.basename(os.path.dirname(file_path))
        date = extract_date_from_filename(dir_name)
        
        # Try to get metadata from JSON file
        json_title, json_date, original_url = get_metadata_from_json(file_path)
        if json_date:
            date = json_date
        
        if not date:
            print(f"Warning: Could not extract date from {dir_name}")
            continue
        
        # Generate canonical URL
        post_url = dir_name.replace('_', '-')
        canonical_url = f"https://www.julien.org/blog/{post_url}/"
        
        # Add to sitemap
        sitemap_content += f"""  <url>
    <loc>{canonical_url}</loc>
    <lastmod>{date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
    <image:image>
      <image:loc>https://www.julien.org/assets/julien-simon-arcee-expert.jpg</image:loc>
      <image:title>Julien Simon - Small Language Model Expert</image:title>
      <image:caption>Expert analysis on {dir_name.replace('_', ' ').title()}</image:caption>
    </image:image>
  </url>
"""
    
    # Add other blog post types if they exist
    # HuggingFace posts
    hf_pattern = "blog/huggingface-posts-and-images/*/index.html"
    hf_files = glob.glob(hf_pattern)
    
    print(f"Found {len(hf_files)} HuggingFace posts")
    
    for file_path in hf_files:
        dir_name = os.path.basename(os.path.dirname(file_path))
        date = extract_date_from_filename(dir_name)
        
        if not date:
            continue
        
        post_url = dir_name.replace('_', '-')
        canonical_url = f"https://www.julien.org/blog/{post_url}/"
        
        sitemap_content += f"""  <url>
    <loc>{canonical_url}</loc>
    <lastmod>{date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
    <image:image>
      <image:loc>https://www.julien.org/assets/julien-simon-huggingface-expert.jpg</image:loc>
      <image:title>Julien Simon - Open Source AI Expert</image:title>
      <image:caption>Expert analysis on {dir_name.replace('_', ' ').title()}</image:caption>
    </image:image>
  </url>
"""
    
    # AWS posts
    aws_pattern = "blog/aws-posts-and-images/*/index.html"
    aws_files = glob.glob(aws_pattern)
    
    print(f"Found {len(aws_files)} AWS posts")
    
    for file_path in aws_files:
        dir_name = os.path.basename(os.path.dirname(file_path))
        date = extract_date_from_filename(dir_name)
        
        if not date:
            continue
        
        post_url = dir_name.replace('_', '-')
        canonical_url = f"https://www.julien.org/blog/{post_url}/"
        
        sitemap_content += f"""  <url>
    <loc>{canonical_url}</loc>
    <lastmod>{date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
    <image:image>
      <image:loc>https://www.julien.org/assets/julien-simon-aws-expert.jpg</image:loc>
      <image:title>Julien Simon - AWS Expert</image:title>
      <image:caption>Expert analysis on {dir_name.replace('_', ' ').title()}</image:caption>
    </image:image>
  </url>
"""
    
    sitemap_content += """</urlset>"""
    
    # Write the sitemap
    with open('sitemap-blog.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    print(f"Created sitemap-blog.xml with {len(arcee_files) + len(hf_files) + len(aws_files)} blog posts")

def update_sitemap_index():
    """Update the sitemap index to include the blog sitemap."""
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    sitemap_index_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <!-- Main sitemap -->
  <sitemap>
    <loc>https://www.julien.org/sitemap.xml</loc>
    <lastmod>{current_date}</lastmod>
  </sitemap>
  
  <!-- Blog posts sitemap -->
  <sitemap>
    <loc>https://www.julien.org/sitemap-blog.xml</loc>
    <lastmod>{current_date}</lastmod>
  </sitemap>
  
  <!-- Speaking engagements sitemap -->
  <sitemap>
    <loc>https://www.julien.org/sitemap-speaking.xml</loc>
    <lastmod>{current_date}</lastmod>
  </sitemap>
</sitemapindex>"""
    
    with open('sitemap-index.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_index_content)
    
    print("Updated sitemap-index.xml")

def main():
    """Main function to create blog sitemap and update index."""
    create_blog_sitemap()
    update_sitemap_index()
    print("Blog sitemap creation completed!")

if __name__ == "__main__":
    main() 