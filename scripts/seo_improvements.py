#!/usr/bin/env python3
"""
Script to implement comprehensive SEO improvements for YouTube pages.
"""

import os
from pathlib import Path
from bs4 import BeautifulSoup
import re

def add_meta_tags_to_index_pages():
    """Add comprehensive meta tags to index pages."""
    youtube_dir = Path('youtube')
    year_dirs = [d for d in youtube_dir.iterdir() if d.is_dir() and d.name.isdigit()]
    
    for year_dir in year_dirs:
        year = year_dir.name
        index_file = year_dir / 'index.html'
        
        if not index_file.exists():
            continue
            
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Add meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            meta_desc = soup.new_tag('meta', attrs={'name': 'description'})
            head = soup.find('head')
            head.insert(1, meta_desc)
        
        meta_desc['content'] = f"Browse {year} YouTube videos by Julien Simon - AI tutorials, technical demos, and educational content with embedded videos, descriptions, tags, and complete transcripts."
        
        # Add Open Graph tags
        og_title = soup.find('meta', attrs={'property': 'og:title'})
        if not og_title:
            og_title = soup.new_tag('meta', attrs={'property': 'og:title'})
            head.insert(2, og_title)
        og_title['content'] = f"YouTube Videos {year} - Julien Simon"
        
        og_desc = soup.find('meta', attrs={'property': 'og:description'})
        if not og_desc:
            og_desc = soup.new_tag('meta', attrs={'property': 'og:description'})
            head.insert(3, og_desc)
        og_desc['content'] = f"Complete collection of {year} YouTube videos by Julien Simon featuring AI tutorials, technical demonstrations, and educational content."
        
        og_url = soup.find('meta', attrs={'property': 'og:url'})
        if not og_url:
            og_url = soup.new_tag('meta', attrs={'property': 'og:url'})
            head.insert(4, og_url)
        og_url['content'] = f"https://www.julien.org/youtube/{year}/index.html"
        
        og_type = soup.find('meta', attrs={'property': 'og:type'})
        if not og_type:
            og_type = soup.new_tag('meta', attrs={'property': 'og:type'})
            head.insert(5, og_type)
        og_type['content'] = 'website'
        
        # Add Twitter Card tags
        twitter_card = soup.find('meta', attrs={'name': 'twitter:card'})
        if not twitter_card:
            twitter_card = soup.new_tag('meta', attrs={'name': 'twitter:card'})
            head.insert(6, twitter_card)
        twitter_card['content'] = 'summary_large_image'
        
        twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
        if not twitter_title:
            twitter_title = soup.new_tag('meta', attrs={'name': 'twitter:title'})
            head.insert(7, twitter_title)
        twitter_title['content'] = f"YouTube Videos {year} - Julien Simon"
        
        twitter_desc = soup.find('meta', attrs={'name': 'twitter:description'})
        if not twitter_desc:
            twitter_desc = soup.new_tag('meta', attrs={'name': 'twitter:description'})
            head.insert(8, twitter_desc)
        twitter_desc['content'] = f"Complete collection of {year} YouTube videos by Julien Simon featuring AI tutorials, technical demonstrations, and educational content."
        
        # Add canonical URL
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if not canonical:
            canonical = soup.new_tag('link', attrs={'rel': 'canonical'})
            head.insert(9, canonical)
        canonical['href'] = f"https://www.julien.org/youtube/{year}/index.html"
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"Updated SEO meta tags for {year} index page")

def add_meta_tags_to_video_pages():
    """Add comprehensive meta tags to individual video pages."""
    youtube_dir = Path('youtube')
    year_dirs = [d for d in youtube_dir.iterdir() if d.is_dir() and d.name.isdigit()]
    
    for year_dir in year_dirs:
        year = year_dir.name
        html_files = [f for f in year_dir.glob('*.html') if f.name != 'index.html']
        
        for video_file in html_files:
            with open(video_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract video title
            title_elem = soup.find('h1')
            if not title_elem:
                continue
            video_title = title_elem.get_text().strip()
            
            # Extract description
            desc_elem = soup.find('div', class_='description')
            description = ""
            if desc_elem:
                description = desc_elem.get_text().strip()[:160] + "..." if len(desc_elem.get_text().strip()) > 160 else desc_elem.get_text().strip()
            
            # Update title
            title_tag = soup.find('title')
            if title_tag:
                title_tag.string = f"{video_title} - Julien Simon"
            
            # Add meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if not meta_desc:
                meta_desc = soup.new_tag('meta', attrs={'name': 'description'})
                head = soup.find('head')
                head.insert(1, meta_desc)
            
            meta_desc['content'] = f"{video_title} - {description}"
            
            # Add Open Graph tags
            og_title = soup.find('meta', attrs={'property': 'og:title'})
            if not og_title:
                og_title = soup.new_tag('meta', attrs={'property': 'og:title'})
                head.insert(2, og_title)
            og_title['content'] = f"{video_title} - Julien Simon"
            
            og_desc = soup.find('meta', attrs={'property': 'og:description'})
            if not og_desc:
                og_desc = soup.new_tag('meta', attrs={'property': 'og:description'})
                head.insert(3, og_desc)
            og_desc['content'] = f"{video_title} - {description}"
            
            og_url = soup.find('meta', attrs={'property': 'og:url'})
            if not og_url:
                og_url = soup.new_tag('meta', attrs={'property': 'og:url'})
                head.insert(4, og_url)
            og_url['content'] = f"https://www.julien.org/youtube/{year}/{video_file.name}"
            
            og_type = soup.find('meta', attrs={'property': 'og:type'})
            if not og_type:
                og_type = soup.new_tag('meta', attrs={'property': 'og:type'})
                head.insert(5, og_type)
            og_type['content'] = 'video'
            
            # Add Twitter Card tags
            twitter_card = soup.find('meta', attrs={'name': 'twitter:card'})
            if not twitter_card:
                twitter_card = soup.new_tag('meta', attrs={'name': 'twitter:card'})
                head.insert(6, twitter_card)
            twitter_card['content'] = 'summary_large_image'
            
            twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
            if not twitter_title:
                twitter_title = soup.new_tag('meta', attrs={'name': 'twitter:title'})
                head.insert(7, twitter_title)
            twitter_title['content'] = f"{video_title} - Julien Simon"
            
            twitter_desc = soup.find('meta', attrs={'name': 'twitter:description'})
            if not twitter_desc:
                twitter_desc = soup.new_tag('meta', attrs={'name': 'twitter:description'})
                head.insert(8, twitter_desc)
            twitter_desc['content'] = f"{video_title} - {description}"
            
            # Add canonical URL
            canonical = soup.find('link', attrs={'rel': 'canonical'})
            if not canonical:
                canonical = soup.new_tag('link', attrs={'rel': 'canonical'})
                head.insert(9, canonical)
            canonical['href'] = f"https://www.julien.org/youtube/{year}/{video_file.name}"
            
            with open(video_file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            print(f"Updated SEO meta tags for {video_file.name}")

def add_structured_data():
    """Add structured data to main YouTube page."""
    with open('youtube.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Add VideoObject structured data
    script_tag = soup.new_tag('script', type='application/ld+json')
    script_tag.string = '''
    {
      "@context": "https://schema.org",
      "@type": "ItemList",
      "name": "Julien Simon YouTube Videos",
      "description": "Collection of AI tutorials, technical demos, and educational content",
      "url": "https://www.julien.org/youtube.html",
      "numberOfItems": 256,
      "itemListElement": [
        {
          "@type": "VideoObject",
          "name": "AI Tutorials and Technical Demos",
          "description": "Comprehensive collection of AI tutorials, machine learning demos, and technical content",
          "uploadDate": "2019-2025",
          "creator": {
            "@type": "Person",
            "name": "Julien Simon",
            "url": "https://www.julien.org"
          },
          "publisher": {
            "@type": "Organization",
            "name": "Julien Simon",
            "url": "https://www.julien.org"
          }
        }
      ]
    }
    '''
    
    head = soup.find('head')
    head.append(script_tag)
    
    with open('youtube.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print("Added structured data to main YouTube page")

def main():
    """Run all SEO improvements."""
    print("Starting SEO improvements...")
    
    print("\n1. Adding meta tags to index pages...")
    add_meta_tags_to_index_pages()
    
    print("\n2. Adding meta tags to video pages...")
    add_meta_tags_to_video_pages()
    
    print("\n3. Adding structured data...")
    add_structured_data()
    
    print("\nSEO improvements completed!")

if __name__ == "__main__":
    main() 