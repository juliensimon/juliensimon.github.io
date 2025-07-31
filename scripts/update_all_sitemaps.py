#!/usr/bin/env python3
"""
Comprehensive script to update all sitemaps with all content including:
- Blog posts (Arcee, HuggingFace, AWS, Medium, Legacy)
- Video transcripts
- All pages
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

def create_comprehensive_blog_sitemap():
    """Create a comprehensive blog sitemap including all blog content."""
    
    sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
"""
    
    total_posts = 0
    
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
        total_posts += 1
    
    # Add HuggingFace posts
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
        total_posts += 1
    
    # Add AWS posts
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
      <image:title>Julien Simon - AWS AI Expert</image:title>
      <image:caption>Expert analysis on {dir_name.replace('_', ' ').title()}</image:caption>
    </image:image>
  </url>
"""
        total_posts += 1
    
    # Add Medium posts
    medium_pattern = "blog/aws-medium-posts-and-images/*/*/index.html"
    medium_files = glob.glob(medium_pattern)
    
    print(f"Found {len(medium_files)} Medium posts")
    
    for file_path in medium_files:
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
      <image:loc>https://www.julien.org/assets/julien-simon-medium-expert.jpg</image:loc>
      <image:title>Julien Simon - Medium AI Expert</image:title>
      <image:caption>Expert analysis on {dir_name.replace('_', ' ').title()}</image:caption>
    </image:image>
  </url>
"""
        total_posts += 1
    
    # Add Legacy posts
    legacy_pattern = "blog/legacy-posts-and-images/*/*.html"
    legacy_files = glob.glob(legacy_pattern)
    
    # Filter out index.html and image files
    legacy_files = [f for f in legacy_files if not f.endswith('index.html') and not f.endswith('.webp')]
    
    print(f"Found {len(legacy_files)} Legacy posts")
    
    for file_path in legacy_files:
        # Extract year and filename
        parts = file_path.split('/')
        year = parts[2]  # year directory
        filename = parts[3].replace('.html', '')
        
        # Extract date from filename
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
        if date_match:
            date = date_match.group(1)
        else:
            # Use year as fallback
            date = f"{year}-01-01"
        
        # Generate URL
        post_url = filename.replace('_', '-')
        canonical_url = f"https://www.julien.org/blog/{post_url}/"
        
        sitemap_content += f"""  <url>
    <loc>{canonical_url}</loc>
    <lastmod>{date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
    <image:image>
      <image:loc>https://www.julien.org/assets/julien-simon-legacy-expert.jpg</image:loc>
      <image:title>Julien Simon - Legacy Content</image:title>
      <image:caption>Legacy content on {filename.replace('_', ' ').title()}</image:caption>
    </image:image>
  </url>
"""
        total_posts += 1
    
    sitemap_content += """</urlset>"""
    
    # Write the sitemap
    with open('sitemap-blog.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    print(f"Created sitemap-blog.xml with {total_posts} total blog posts")
    return total_posts

def create_video_sitemap():
    """Create a sitemap for all video transcripts."""
    
    sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
"""
    
    total_videos = 0
    
    # Find all video transcript HTML files
    video_pattern = "youtube/*/*.html"
    video_files = glob.glob(video_pattern)
    
    # Filter out index.html files
    video_files = [f for f in video_files if not f.endswith('index.html')]
    
    print(f"Found {len(video_files)} video transcripts")
    
    for file_path in video_files:
        # Extract year and filename
        parts = file_path.split('/')
        year = parts[1]
        filename = parts[2].replace('.html', '')
        
        # Generate URL
        video_url = f"https://www.julien.org/youtube/{year}/{filename}.html"
        
        # Extract date from filename if possible
        date_match = re.search(r'(\d{8})', filename)
        if date_match:
            date_str = date_match.group(1)
            date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
        else:
            date = "2025-07-31"  # Default date
        
        sitemap_content += f"""  <url>
    <loc>{video_url}</loc>
    <lastmod>{date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
    <image:image>
      <image:loc>https://www.julien.org/assets/julien.webp</image:loc>
      <image:title>Julien Simon - Video Transcript</image:title>
      <image:caption>Video transcript: {filename.replace('_', ' ').title()}</image:caption>
    </image:image>
  </url>
"""
        total_videos += 1
    
    sitemap_content += """</urlset>"""
    
    # Write the sitemap
    with open('sitemap-videos.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    print(f"Created sitemap-videos.xml with {total_videos} video transcripts")
    return total_videos

def update_sitemap_index():
    """Update the sitemap index to include all sitemaps."""
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    sitemap_index_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <!-- Main sitemap -->
  <sitemap>
    <loc>https://www.julien.org/sitemap.xml</loc>
    <lastmod>{today}</lastmod>
  </sitemap>
  
  <!-- Blog posts sitemap -->
  <sitemap>
    <loc>https://www.julien.org/sitemap-blog.xml</loc>
    <lastmod>{today}</lastmod>
  </sitemap>
  
  <!-- Speaking engagements sitemap -->
  <sitemap>
    <loc>https://www.julien.org/sitemap-speaking.xml</loc>
    <lastmod>{today}</lastmod>
  </sitemap>
  
  <!-- Video transcripts sitemap -->
  <sitemap>
    <loc>https://www.julien.org/sitemap-videos.xml</loc>
    <lastmod>{today}</lastmod>
  </sitemap>
</sitemapindex>"""
    
    with open('sitemap-index.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_index_content)
    
    print("Updated sitemap-index.xml")

def main():
    """Main function to create all sitemaps."""
    print("Creating comprehensive sitemaps...")
    
    # Create blog sitemap
    blog_count = create_comprehensive_blog_sitemap()
    
    # Create video sitemap
    video_count = create_video_sitemap()
    
    # Update sitemap index
    update_sitemap_index()
    
    print(f"\n✅ Sitemap creation completed!")
    print(f"📊 Summary:")
    print(f"   • Blog posts: {blog_count}")
    print(f"   • Video transcripts: {video_count}")
    print(f"   • Total content: {blog_count + video_count} items")
    print(f"\n📝 Submit to Google: https://www.julien.org/sitemap-index.xml")

if __name__ == "__main__":
    main() 