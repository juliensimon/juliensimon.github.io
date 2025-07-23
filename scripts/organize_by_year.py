#!/usr/bin/env python3
"""
Organize blog posts by year and create index pages.

This script organizes extracted blog posts into year-based folders and creates
beautiful index pages for easy navigation.

Features:
- Organizes posts by year (2007-2018)
- Moves associated images to correct year folders
- Creates index.html for each year with post listings
- Generates main archive index with year overview
- Responsive design with modern CSS styling

Usage:
    python organize_by_year.py

Requirements:
    - Python 3.6+
    - Blog posts already extracted in blog/legacy-posts-and-images/

Output:
    - Year-based folder structure
    - Index pages with navigation
    - Clean, organized archive
"""

import os
import shutil
from pathlib import Path
import re

def extract_date_and_title(filename):
    """Extract date and title from filename."""
    # Pattern: YYYY-MM-DD-title.html
    match = re.match(r'(\d{4})-(\d{2})-(\d{2})-(.+)\.html$', filename)
    if match:
        year, month, day, title_slug = match.groups()
        # Convert slug to readable title
        title = title_slug.replace('-', ' ').title()
        # Clean up common words
        title = title.replace(' And ', ' and ').replace(' The ', ' the ')
        title = title.replace(' Of ', ' of ').replace(' In ', ' in ')
        title = title.replace(' On ', ' on ').replace(' For ', ' for ')
        title = title.replace(' With ', ' with ').replace(' To ', ' to ')
        return f"{year}-{month}-{day}", title, year
    return None, None, None

def create_year_index(year, posts, year_dir):
    """Create an index.html file for a specific year."""
    
    # Sort posts by date (newest first)
    posts.sort(key=lambda x: x[0], reverse=True)
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog Posts - {year}</title>
    <link rel="stylesheet" href="../../css/styles.css">
    <style>
        .year-header {{
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
            border-bottom: 1px solid #e2e8f0;
            margin-bottom: 2rem;
        }}
        
        .year-title {{
            font-size: 2.5rem;
            font-weight: 800;
            color: #1e40af;
            margin-bottom: 0.5rem;
        }}
        
        .year-subtitle {{
            color: #64748b;
            font-size: 1.125rem;
        }}
        
        .posts-grid {{
            display: grid;
            gap: 1.5rem;
            margin: 2rem 0;
        }}
        
        .post-card {{
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s ease;
            box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
        }}
        
        .post-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
            border-color: #1e40af;
        }}
        
        .post-date {{
            font-size: 0.875rem;
            color: #1e40af;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}
        
        .post-title {{
            font-size: 1.125rem;
            font-weight: 600;
            color: #0f172a;
            margin-bottom: 0.75rem;
        }}
        
        .post-title a {{
            color: inherit;
            text-decoration: none;
            transition: color 0.3s ease;
        }}
        
        .post-title a:hover {{
            color: #1e40af;
        }}
        
        .navigation {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 3rem 0;
            padding: 1rem;
            background: #f8fafc;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        }}
        
        .nav-link {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1.5rem;
            background: #1e40af;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.3s ease;
        }}
        
        .nav-link:hover {{
            background: #1e3a8a;
            transform: translateY(-1px);
        }}
        
        .stats {{
            text-align: center;
            color: #64748b;
            font-size: 0.875rem;
        }}
        
        @media (max-width: 768px) {{
            .year-title {{
                font-size: 2rem;
            }}
            
            .navigation {{
                flex-direction: column;
                gap: 1rem;
            }}
            
            .post-card {{
                padding: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="year-header">
            <h1 class="year-title">{year}</h1>
            <p class="year-subtitle">{len(posts)} blog posts from this year</p>
        </div>
        
        <div class="navigation">
            <a href="../index.html" class="nav-link">
                ← Back to All Years
            </a>
            <div class="stats">
                <strong>{len(posts)}</strong> posts in {year}
            </div>
            <a href="../../index.html" class="nav-link">
                🏠 Home
            </a>
        </div>
        
        <div class="posts-grid">'''
    
    for date, title, filename in posts:
        html_content += f'''
            <div class="post-card">
                <div class="post-date">{date}</div>
                <div class="post-title">
                    <a href="{filename}">{title}</a>
                </div>
            </div>'''
    
    html_content += f'''
        </div>
        
        <div class="navigation">
            <a href="../index.html" class="nav-link">
                ← Back to All Years
            </a>
            <div class="stats">
                End of {year} posts
            </div>
            <a href="../../index.html" class="nav-link">
                🏠 Home
            </a>
        </div>
    </div>
</body>
</html>'''
    
    index_path = year_dir / 'index.html'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Created index for {year} with {len(posts)} posts")

def create_main_index(year_stats):
    """Create main index.html for all years."""
    
    # Sort years in descending order
    sorted_years = sorted(year_stats.items(), key=lambda x: x[0], reverse=True)
    total_posts = sum(year_stats.values())
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Legacy Blog Posts Archive</title>
    <link rel="stylesheet" href="../css/styles.css">
    <style>
        .archive-header {{
            text-align: center;
            padding: 3rem 0;
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
            color: white;
            margin-bottom: 3rem;
            border-radius: 12px;
        }}
        
        .archive-title {{
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 1rem;
        }}
        
        .archive-subtitle {{
            font-size: 1.25rem;
            opacity: 0.9;
        }}
        
        .years-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }}
        
        .year-card {{
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 2rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
            position: relative;
            overflow: hidden;
        }}
        
        .year-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }}
        
        .year-card:hover::before {{
            transform: scaleX(1);
        }}
        
        .year-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1);
            border-color: #1e40af;
        }}
        
        .year-number {{
            font-size: 2.5rem;
            font-weight: 800;
            color: #1e40af;
            margin-bottom: 1rem;
        }}
        
        .year-stats {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }}
        
        .post-count {{
            font-size: 1.125rem;
            color: #64748b;
            font-weight: 600;
        }}
        
        .year-link {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1.5rem;
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
            width: 100%;
            justify-content: center;
        }}
        
        .year-link:hover {{
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
            transform: translateY(-1px);
        }}
        
        .navigation {{
            text-align: center;
            margin: 3rem 0;
        }}
        
        .home-link {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 1rem 2rem;
            background: #64748b;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .home-link:hover {{
            background: #475569;
            transform: translateY(-1px);
        }}
        
        .summary {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 2rem;
            margin: 2rem 0;
            text-align: center;
        }}
        
        @media (max-width: 768px) {{
            .archive-title {{
                font-size: 2rem;
            }}
            
            .years-grid {{
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }}
            
            .year-card {{
                padding: 1.5rem;
            }}
            
            .year-number {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="archive-header">
            <h1 class="archive-title">Blog Archive</h1>
            <p class="archive-subtitle">Legacy posts organized by year</p>
        </div>
        
        <div class="summary">
            <h2>Archive Summary</h2>
            <p>This archive contains <strong>{total_posts} blog posts</strong> spanning <strong>{sorted_years[-1][0]} - {sorted_years[0][0]}</strong>, covering topics from technology and programming to industry insights and personal experiences.</p>
        </div>
        
        <div class="years-grid">'''
    
    for year, count in sorted_years:
        html_content += f'''
            <div class="year-card">
                <div class="year-number">{year}</div>
                <div class="year-stats">
                    <span class="post-count">{count} posts</span>
                </div>
                <a href="{year}/index.html" class="year-link">
                    View {year} Posts →
                </a>
            </div>'''
    
    html_content += '''
        </div>
        
        <div class="navigation">
            <a href="../index.html" class="home-link">
                🏠 Back to Main Site
            </a>
        </div>
    </div>
</body>
</html>'''
    
    main_index_path = Path('blog/legacy-posts-and-images/index.html')
    with open(main_index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Created main index with {len(sorted_years)} years")

def move_images_to_year_folders():
    """Move images to their respective year folders."""
    posts_dir = Path('blog/legacy-posts-and-images')
    
    # Get all WebP image files
    image_files = list(posts_dir.glob('*.webp'))
    print(f"📸 Found {len(image_files)} image files to organize")
    
    moved_count = 0
    
    for image_file in image_files:
        # Extract year from filename (YYYY-MM-DD-...)
        match = re.match(r'(\d{4})-\d{2}-\d{2}-', image_file.name)
        
        if match:
            year = match.group(1)
            year_dir = posts_dir / year
            
            if year_dir.exists():
                dst_path = year_dir / image_file.name
                
                if not dst_path.exists():
                    shutil.move(str(image_file), str(dst_path))
                    moved_count += 1
                    print(f"   ✅ Moved {image_file.name} to {year}/")
    
    print(f"📸 Moved {moved_count} images to year folders")

def main():
    """Main function to organize posts and create indexes."""
    posts_dir = Path('blog/legacy-posts-and-images')
    
    if not posts_dir.exists():
        print(f"❌ Directory {posts_dir} does not exist!")
        print("Please run extract_blog_posts.py first")
        return
    
    # Get all HTML files (excluding any existing index files)
    html_files = [f for f in posts_dir.glob('*.html') if f.name != 'index.html']
    print(f"📄 Found {len(html_files)} HTML files to organize")
    
    if not html_files:
        print("❌ No blog post HTML files found to organize")
        return
    
    # Group by year
    year_posts = {}
    year_stats = {}
    
    for html_file in html_files:
        date, title, year = extract_date_and_title(html_file.name)
        
        if year:
            if year not in year_posts:
                year_posts[year] = []
                year_stats[year] = 0
            
            year_posts[year].append((date, title, html_file.name))
            year_stats[year] += 1
    
    print(f"📁 Organizing posts across {len(year_posts)} years...")
    
    # Create year directories and move files
    for year, posts in year_posts.items():
        year_dir = posts_dir / year
        year_dir.mkdir(exist_ok=True)
        
        # Move HTML files to year directory
        for date, title, filename in posts:
            src_path = posts_dir / filename
            dst_path = year_dir / filename
            
            if src_path.exists() and not dst_path.exists():
                shutil.move(str(src_path), str(dst_path))
        
        # Create year index
        create_year_index(year, posts, year_dir)
    
    # Move images to year folders
    move_images_to_year_folders()
    
    # Create main index
    create_main_index(year_stats)
    
    print(f"\n🎉 Successfully organized {len(html_files)} posts into {len(year_posts)} years")
    print("\n📁 Folder structure:")
    for year in sorted(year_stats.keys()):
        print(f"   blog/legacy-posts-and-images/{year}/ ({year_stats[year]} posts)")

if __name__ == "__main__":
    main() 