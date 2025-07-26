#!/usr/bin/env python3
"""
Script to fix Hugging Face blog post titles with proper formatting.
"""

import os
import re
import glob

def format_title_properly(title):
    """Format title with proper spacing and capitalization."""
    # Replace hyphens with spaces
    title = title.replace('-', ' ')
    
    # Apply title case
    title = title.title()
    
    # Fix common technical terms
    title = title.replace('Ai', 'AI')
    title = title.replace('Ml', 'ML')
    title = title.replace('Nlp', 'NLP')
    title = title.replace('Cpu', 'CPU')
    title = title.replace('Cpus', 'CPUs')
    title = title.replace('Gpu', 'GPU')
    title = title.replace('Gpus', 'GPUs')
    title = title.replace('Api', 'API')
    title = title.replace('Sdk', 'SDK')
    title = title.replace('Iot', 'IoT')
    title = title.replace('Rag', 'RAG')
    title = title.replace('Phi-2', 'Phi-2')
    title = title.replace('Protst', 'ProtST')
    title = title.replace('Q8-Chat', 'Q8-Chat')
    title = title.replace('Watsonxai', 'WatsonX.ai')
    title = title.replace('Watsonx', 'WatsonX')
    title = title.replace('Xeon', 'Xeon')
    title = title.replace('Intel', 'Intel')
    title = title.replace('Amd', 'AMD')
    title = title.replace('Ibm', 'IBM')
    title = title.replace('Azure', 'Azure')
    title = title.replace('Aws', 'AWS')
    title = title.replace('PyTorch', 'PyTorch')
    title = title.replace('Stable Diffusion', 'Stable Diffusion')
    title = title.replace('Habana', 'Habana')
    title = title.replace('Gaudi', 'Gaudi')
    title = title.replace('Meteor Lake', 'Meteor Lake')
    title = title.replace('Sapphire Rapids', 'Sapphire Rapids')
    title = title.replace('Inferentia2', 'Inferentia2')
    title = title.replace('OpenVINO', 'OpenVINO')
    title = title.replace('Graphcore', 'Graphcore')
    title = title.replace('IPUs', 'IPUs')
    title = title.replace('IPU', 'IPU')
    
    return title

def fix_file_titles(file_path):
    """Fix titles in a single HTML file."""
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract current title from meta tags
    title_match = re.search(r'<title>(.*?) - Julien Simon', content)
    if not title_match:
        print(f"Could not find title in {file_path}")
        return False
    
    current_title = title_match.group(1)
    formatted_title = format_title_properly(current_title)
    
    # Update title in meta tags
    content = re.sub(
        r'<title>.*?</title>',
        f'<title>{formatted_title} - Julien Simon | Open Source AI Expert</title>',
        content
    )
    
    content = re.sub(
        r'<meta name="title" content=".*?"/>',
        f'<meta name="title" content="{formatted_title} - Julien Simon | Open Source AI Expert"/>',
        content
    )
    
    content = re.sub(
        r'<meta property="og:title" content=".*?"/>',
        f'<meta property="og:title" content="{formatted_title} - Julien Simon | Open Source AI Expert"/>',
        content
    )
    
    content = re.sub(
        r'<meta property="twitter:title" content=".*?"/>',
        f'<meta property="twitter:title" content="{formatted_title} - Julien Simon | Open Source AI Expert"/>',
        content
    )
    
    # Update headline in structured data
    content = re.sub(
        r'"headline": ".*?"',
        f'"headline": "{formatted_title}"',
        content
    )
    
    # Update description to use proper title
    title_lower = formatted_title.lower()
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
    
    # Update keywords to include formatted title
    keywords_match = re.search(r'<meta name="keywords" content="(.*?)"/>', content)
    if keywords_match:
        keywords = keywords_match.group(1)
        # Remove the old title from keywords and add the new one
        keywords = re.sub(r', [^,]*?(?:-|$)', '', keywords)  # Remove last keyword (old title)
        keywords = f"{keywords}, {formatted_title}"
        content = re.sub(
            r'<meta name="keywords" content=".*?"/>',
            f'<meta name="keywords" content="{keywords}"/>',
            content
        )
    
    # Write the updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed title in {file_path}: {current_title} → {formatted_title}")
    return True

def main():
    """Main function to fix all Hugging Face posts."""
    
    # Find all index.html files in huggingface-posts-and-images
    pattern = "blog/huggingface-posts-and-images/*/index.html"
    files = glob.glob(pattern)
    
    if not files:
        print("No Hugging Face post files found!")
        return
    
    print(f"Found {len(files)} Hugging Face post files")
    
    updated_count = 0
    for file_path in files:
        if fix_file_titles(file_path):
            updated_count += 1
    
    print(f"\nFixed {updated_count} out of {len(files)} files")

if __name__ == "__main__":
    main() 