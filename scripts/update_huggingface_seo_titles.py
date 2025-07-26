#!/usr/bin/env python3
"""
Script to update Hugging Face blog posts with better formatted titles.
"""

import os
import re
import glob

def extract_title_from_filename(filename):
    """Extract title from directory name with proper formatting."""
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

def update_file_titles(file_path):
    """Update titles in a single HTML file."""
    
    # Extract directory name for title
    dir_name = os.path.basename(os.path.dirname(file_path))
    title = extract_title_from_filename(dir_name)
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update title in meta tags
    content = re.sub(
        r'<title>.*?</title>',
        f'<title>{title} - Julien Simon | Open Source AI Expert</title>',
        content
    )
    
    content = re.sub(
        r'<meta name="title" content=".*?"/>',
        f'<meta name="title" content="{title} - Julien Simon | Open Source AI Expert"/>',
        content
    )
    
    content = re.sub(
        r'<meta property="og:title" content=".*?"/>',
        f'<meta property="og:title" content="{title} - Julien Simon | Open Source AI Expert"/>',
        content
    )
    
    content = re.sub(
        r'<meta property="twitter:title" content=".*?"/>',
        f'<meta property="twitter:title" content="{title} - Julien Simon | Open Source AI Expert"/>',
        content
    )
    
    # Update headline in structured data
    content = re.sub(
        r'"headline": ".*?"',
        f'"headline": "{title}"',
        content
    )
    
    # Update description to use proper title
    title_lower = title.lower()
    description = f"Expert analysis and technical deep-dive on {title_lower} by Julien Simon, leading voice in open-source AI and former Chief Evangelist at Hugging Face. Comprehensive insights on transformers, small language models, and AI accessibility."
    
    content = re.sub(
        r'<meta name="description" content=".*?"/>',
        f'<meta name="description" content="{description}"/>',
        content
    )
    
    content = re.sub(
        r'<meta property="og:description" content=".*?"/>',
        f'<meta property="og:description" content="{description}"/>',
        content
    )
    
    content = re.sub(
        r'<meta property="twitter:description" content=".*?"/>',
        f'<meta property="twitter:description" content="{description}"/>',
        content
    )
    
    # Update description in structured data
    content = re.sub(
        r'"description": ".*?"',
        f'"description": "{description}"',
        content
    )
    
    # Write the updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated titles in {file_path}")
    return True

def main():
    """Main function to update all Hugging Face posts."""
    
    # Find all index.html files in huggingface-posts-and-images
    pattern = "blog/huggingface-posts-and-images/*/index.html"
    files = glob.glob(pattern)
    
    if not files:
        print("No Hugging Face post files found!")
        return
    
    print(f"Found {len(files)} Hugging Face post files")
    
    updated_count = 0
    for file_path in files:
        if update_file_titles(file_path):
            updated_count += 1
    
    print(f"\nUpdated {updated_count} out of {len(files)} files")

if __name__ == "__main__":
    main() 