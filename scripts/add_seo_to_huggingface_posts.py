#!/usr/bin/env python3
"""
Script to add comprehensive SEO metadata to Hugging Face blog posts.
Positions Julien Simon as an expert on open-source AI and small language models.
"""

import os
import re
import glob
from datetime import datetime

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
    name = name.replace('Phi-2', 'Phi-2')
    name = name.replace('Protst', 'ProtST')
    name = name.replace('Q8-Chat', 'Q8-Chat')
    name = name.replace('Watsonxai', 'WatsonX.ai')
    name = name.replace('Watsonx', 'WatsonX')
    
    return name

def extract_date_from_filename(filename):
    """Extract date from directory name."""
    match = re.search(r'^(\d{4}-\d{2}-\d{2})_', filename)
    if match:
        return match.group(1)
    return None

def generate_seo_metadata(title, date, post_url):
    """Generate comprehensive SEO metadata for Hugging Face posts."""
    
    # Convert title to lowercase for description
    title_lower = title.lower()
    
    # Extract key terms for keywords
    keywords = [
        "Hugging Face", "Transformers", "Open Source AI", "Small Language Models",
        "Machine Learning", "AI", "Natural Language Processing", "NLP",
        "Julien Simon", "AI Expert", "Open Source Expert", "Hugging Face Expert"
    ]
    
    # Add title-specific keywords
    title_words = title.split()
    keywords.extend([word for word in title_words if len(word) > 3])
    
    # Remove duplicates and join
    keywords = list(dict.fromkeys(keywords))
    keywords_str = ", ".join(keywords)
    
    # Generate description
    description = f"Expert analysis and technical deep-dive on {title_lower} by Julien Simon, leading voice in open-source AI and former Chief Evangelist at Hugging Face. Comprehensive insights on transformers, small language models, and AI accessibility."
    
    # Generate canonical URL
    canonical_url = f"https://julien.org/blog/{post_url}/"
    
    seo_metadata = f"""  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  
  <!-- Primary Meta Tags -->
  <title>{title} - Julien Simon | Open Source AI Expert</title>
  <meta name="title" content="{title} - Julien Simon | Open Source AI Expert"/>
  <meta name="description" content="{description}"/>
  <meta name="keywords" content="{keywords_str}"/>
  <meta name="author" content="Julien Simon"/>
  <meta name="robots" content="index, follow"/>
  
  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="article"/>
  <meta property="og:url" content="{canonical_url}"/>
  <meta property="og:title" content="{title} - Julien Simon | Open Source AI Expert"/>
  <meta property="og:description" content="{description}"/>
  <meta property="og:image" content="https://julien.org/assets/julien-simon-huggingface-expert.jpg"/>
  <meta property="og:site_name" content="Julien Simon - Open Source AI Expert"/>
  <meta property="article:author" content="Julien Simon"/>
  <meta property="article:published_time" content="{date}T00:00:00Z"/>
  <meta property="article:section" content="Hugging Face"/>
  <meta property="article:tag" content="Hugging Face, Open Source AI, Transformers, Small Language Models"/>
  
  <!-- Twitter -->
  <meta property="twitter:card" content="summary_large_image"/>
  <meta property="twitter:url" content="{canonical_url}"/>
  <meta property="twitter:title" content="{title} - Julien Simon | Open Source AI Expert"/>
  <meta property="twitter:description" content="{description}"/>
  <meta property="twitter:image" content="https://julien.org/assets/julien-simon-huggingface-expert.jpg"/>
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
    "image": "https://julien.org/assets/julien-simon-huggingface-expert.jpg",
    "author": {{
      "@type": "Person",
      "name": "Julien Simon",
      "url": "https://julien.org/",
      "jobTitle": "Open Source AI Expert & Former Chief Evangelist",
      "worksFor": {{
        "@type": "Organization",
        "name": "Hugging Face"
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
    "articleSection": "Hugging Face",
    "inLanguage": "en-US",
    "isPartOf": {{
      "@type": "Blog",
      "name": "Julien Simon - Open Source AI Expert Blog",
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
    
    if not date:
        print(f"Warning: Could not extract date from {dir_name}")
        return False
    
    # Generate post URL for canonical link
    post_url = dir_name.replace('_', '-')
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if SEO is already present
    if 'Open Source AI Expert' in content:
        print(f"SEO already present in {file_path}")
        return False
    
    # Generate SEO metadata
    seo_metadata = generate_seo_metadata(title, date, post_url)
    
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
    """Main function to process all Hugging Face posts."""
    
    # Find all index.html files in huggingface-posts-and-images
    pattern = "blog/huggingface-posts-and-images/*/index.html"
    files = glob.glob(pattern)
    
    if not files:
        print("No Hugging Face post files found!")
        return
    
    print(f"Found {len(files)} Hugging Face post files")
    
    updated_count = 0
    for file_path in files:
        if add_seo_to_file(file_path):
            updated_count += 1
    
    print(f"\nUpdated {updated_count} out of {len(files)} files")

if __name__ == "__main__":
    main() 