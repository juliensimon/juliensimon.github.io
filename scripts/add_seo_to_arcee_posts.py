#!/usr/bin/env python3
"""
Script to add comprehensive SEO metadata to Arcee blog posts.
Positions Julien Simon as an expert on small language models and edge AI.
"""

import os
import re
import glob
import json
from datetime import datetime

def extract_title_from_filename(filename):
    """Extract title from directory name."""
    # Remove date prefix and convert to title case
    name = filename.replace('_', ' ').title()
    # Remove date pattern (YYYY-MM-DD_)
    name = re.sub(r'^\d{4}-\d{2}-\d{2}\s+', '', name)
    
    # Fix common title formatting issues
    name = name.replace('AI', 'AI')
    name = name.replace('ML', 'ML')
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

def generate_seo_metadata(title, date, post_url, original_url=None):
    """Generate comprehensive SEO metadata for Arcee posts."""
    
    # Convert title to lowercase for description
    title_lower = title.lower()
    
    # Extract key terms for keywords
    keywords = [
        "Arcee AI", "Small Language Models", "SLMs", "Edge AI", "CPU Inference",
        "Machine Learning", "AI", "Natural Language Processing", "NLP",
        "Julien Simon", "AI Expert", "Small Language Model Expert", "Edge AI Expert",
        "CPU AI", "ARM CPUs", "Intel Xeon", "AI at the Edge", "Local AI"
    ]
    
    # Add title-specific keywords
    title_words = title.split()
    keywords.extend([word for word in title_words if len(word) > 3])
    
    # Remove duplicates and join
    keywords = list(dict.fromkeys(keywords))
    keywords_str = ", ".join(keywords)
    
    # Generate description
    description = f"Expert analysis and technical deep-dive on {title_lower} by Julien Simon, leading voice in small language models and edge AI. Comprehensive insights on CPU inference, local AI deployment, and Arcee AI's innovative approaches."
    
    # Generate canonical URL
    canonical_url = f"https://julien.org/blog/{post_url}/"
    
    seo_metadata = f"""  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  
  <!-- Primary Meta Tags -->
  <title>{title} - Julien Simon | Small Language Model Expert</title>
  <meta name="title" content="{title} - Julien Simon | Small Language Model Expert"/>
  <meta name="description" content="{description}"/>
  <meta name="keywords" content="{keywords_str}"/>
  <meta name="author" content="Julien Simon"/>
  <meta name="robots" content="index, follow"/>
  
  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="article"/>
  <meta property="og:url" content="{canonical_url}"/>
  <meta property="og:title" content="{title} - Julien Simon | Small Language Model Expert"/>
  <meta property="og:description" content="{description}"/>
  <meta property="og:image" content="https://julien.org/assets/julien-simon-arcee-expert.jpg"/>
  <meta property="og:site_name" content="Julien Simon - Small Language Model Expert"/>
  <meta property="article:author" content="Julien Simon"/>
  <meta property="article:published_time" content="{date}T00:00:00Z"/>
  <meta property="article:section" content="Arcee AI"/>
  <meta property="article:tag" content="Arcee AI, Small Language Models, Edge AI, CPU Inference"/>
  
  <!-- Twitter -->
  <meta property="twitter:card" content="summary_large_image"/>
  <meta property="twitter:url" content="{canonical_url}"/>
  <meta property="twitter:title" content="{title} - Julien Simon | Small Language Model Expert"/>
  <meta property="twitter:description" content="{description}"/>
  <meta property="twitter:image" content="https://julien.org/assets/julien-simon-arcee-expert.jpg"/>
  <meta property="twitter:creator" content="@julsimon"/>
  
  <!-- Canonical URL -->
  <link rel="canonical" href="{canonical_url}"/>
  
  <!-- Author and Publisher -->
  <link rel="author" href="https://julien.org/"/>
  <link rel="publisher" href="https://julien.org/"/>
  
  <!-- Structured Data -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{title}",
    "description": "{description}",
    "image": "https://julien.org/assets/julien-simon-arcee-expert.jpg",
    "author": {{
      "@type": "Person",
      "name": "Julien Simon",
      "url": "https://julien.org/",
      "jobTitle": "Small Language Model Expert & AI Evangelist",
      "worksFor": {{
        "@type": "Organization",
        "name": "Arcee AI"
      }},
      "sameAs": [
        "https://twitter.com/julsimon",
        "https://linkedin.com/in/juliensimon",
        "https://github.com/juliensimon"
      ]
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "Julien Simon",
      "url": "https://julien.org/",
      "logo": {{
        "@type": "ImageObject",
        "url": "https://julien.org/assets/julien-simon-logo.jpg"
      }}
    }},
    "datePublished": "{date}T00:00:00Z",
    "dateModified": "{date}T00:00:00Z",
    "mainEntityOfPage": {{
      "@type": "WebPage",
      "@id": "{canonical_url}"
    }},
    "url": "{canonical_url}",
    "keywords": "{keywords_str}",
    "articleSection": "Arcee AI",
    "inLanguage": "en-US",
    "isPartOf": {{
      "@type": "Blog",
      "name": "Julien Simon - Small Language Model Expert Blog",
      "url": "https://julien.org/blog/"
    }}
  }}
  </script>
  
  <!-- Additional SEO Meta Tags -->
  <meta name="twitter:site" content="@julsimon"/>
  <meta name="twitter:creator" content="@julsimon"/>
  <meta name="theme-color" content="#FF6B35"/>
  <meta name="msapplication-TileColor" content="#FF6B35"/>
  <meta name="apple-mobile-web-app-capable" content="yes"/>
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"/>
  
  <!-- Preconnect to external domains -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  
  <!-- Favicon -->
  <link rel="icon" type="image/x-icon" href="https://julien.org/assets/favicon.ico">
  
  <!-- Security Headers -->
  <meta http-equiv="X-Content-Type-Options" content="nosniff">
  <meta http-equiv="X-Frame-Options" content="DENY">
  <meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">
  <meta http-equiv="X-XSS-Protection" content="1; mode=block">
  <meta http-equiv="Permissions-Policy" content="camera=(), microphone=(), geolocation=(), interest-cohort=()">
  <meta http-equiv="Cross-Origin-Opener-Policy" content="same-origin">
  <meta http-equiv="Cross-Origin-Embedder-Policy" content="require-corp">"""
    
    return seo_metadata

def add_seo_to_file(file_path):
    """Add SEO metadata to a single HTML file."""
    
    # Extract directory name for title and date
    dir_name = os.path.basename(os.path.dirname(file_path))
    title = extract_title_from_filename(dir_name)
    date = extract_date_from_filename(dir_name)
    
    # Try to get metadata from JSON file
    json_title, json_date, original_url = get_metadata_from_json(file_path)
    if json_title:
        title = json_title
    if json_date:
        date = json_date
    
    if not date:
        print(f"Warning: Could not extract date from {dir_name}")
        return False
    
    # Generate post URL for canonical link
    post_url = dir_name.replace('_', '-')
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if SEO is already present
    if 'Small Language Model Expert' in content:
        print(f"SEO already present in {file_path}")
        return False
    
    # Generate SEO metadata
    seo_metadata = generate_seo_metadata(title, date, post_url, original_url)
    
    # Find the head tag and insert SEO metadata
    head_pattern = r'(<head>\s*)(<meta charset="utf-8"/>)'
    replacement = r'\1' + seo_metadata + '\n\n  '
    
    new_content = re.sub(head_pattern, replacement, content, flags=re.DOTALL)
    
    if new_content == content:
        print(f"Warning: Could not find head tag in {file_path}")
        return False
    
    # Write the updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Added SEO to {file_path}")
    return True

def main():
    """Main function to process all Arcee posts."""
    
    # Find all index.html files in arcee-posts
    pattern = "blog/arcee-posts/*/index.html"
    files = glob.glob(pattern)
    
    if not files:
        print("No Arcee post files found!")
        return
    
    print(f"Found {len(files)} Arcee post files")
    
    updated_count = 0
    for file_path in files:
        if add_seo_to_file(file_path):
            updated_count += 1
    
    print(f"\nUpdated {updated_count} out of {len(files)} files")

if __name__ == "__main__":
    main() 