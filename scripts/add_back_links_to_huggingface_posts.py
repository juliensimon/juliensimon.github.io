#!/usr/bin/env python3
"""
Script to add back links to all local Hugging Face blog posts.
"""

import os
import glob

def add_back_link_to_file(file_path):
    """Add a back link to the Hugging Face blog posts page."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if back link already exists
    if 'Back to Hugging Face Blog Posts' in content:
        print(f"Back link already exists in {file_path}")
        return False
    
    # Find the position to insert the back link (after <body> tag)
    body_pos = content.find('<body>')
    if body_pos == -1:
        print(f"Could not find <body> tag in {file_path}")
        return False
    
    # Insert the back link after the body tag
    back_link = '  <div style="margin-bottom: 2em;">\n   <a href="../../../../huggingface-blog-posts.html" style="color: #3498db; text-decoration: none; font-weight: 500;">← Back to Hugging Face Blog Posts</a>\n  </div>\n'
    
    new_content = content[:body_pos + 7] + '\n' + back_link + content[body_pos + 7:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Added back link to {file_path}")
    return True

def main():
    """Main function to process all Hugging Face blog posts."""
    # Get all index.html files in the huggingface-posts-and-images directory
    pattern = "blog/huggingface-posts-and-images/*/index.html"
    files = glob.glob(pattern)
    
    print(f"Found {len(files)} Hugging Face blog post files")
    
    updated_count = 0
    for file_path in files:
        if add_back_link_to_file(file_path):
            updated_count += 1
    
    print(f"\nUpdated {updated_count} files with back links")

if __name__ == "__main__":
    main() 