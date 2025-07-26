#!/usr/bin/env python3
"""
Script to remove author information from all local Hugging Face blog posts.
"""

import os
import glob
import re

def remove_author_info_from_file(file_path):
    """Remove author information from a Hugging Face blog post."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if author information exists
    if 'Authors:' not in content:
        print(f"No author information found in {file_path}")
        return False
    
    # Pattern to match the author paragraph
    # This matches the entire paragraph containing "Authors:"
    author_pattern = r'<p style="color: #666; font-style: italic; margin-bottom: 1em;">\s*Authors:.*?</p>'
    
    # Remove the author information
    new_content = re.sub(author_pattern, '', content, flags=re.DOTALL)
    
    # If no change was made, try a more specific pattern
    if new_content == content:
        # Try to match just the line with "Authors:"
        author_line_pattern = r'\s*<p style="color: #666; font-style: italic; margin-bottom: 1em;">\s*Authors:.*?</p>\s*'
        new_content = re.sub(author_line_pattern, '', content, flags=re.DOTALL)
    
    # If still no change, try a simpler approach
    if new_content == content:
        lines = content.split('\n')
        new_lines = []
        skip_next = False
        
        for i, line in enumerate(lines):
            if 'Authors:' in line:
                print(f"Found author line in {file_path}: {line.strip()}")
                skip_next = True
                continue
            if skip_next and line.strip() == '':
                skip_next = False
                continue
            new_lines.append(line)
        
        new_content = '\n'.join(new_lines)
    
    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Removed author information from {file_path}")
    return True

def main():
    """Main function to process all Hugging Face blog posts."""
    # Get all index.html files in the huggingface-posts-and-images directory
    pattern = "blog/huggingface-posts-and-images/*/index.html"
    files = glob.glob(pattern)
    
    print(f"Found {len(files)} Hugging Face blog post files")
    
    updated_count = 0
    for file_path in files:
        if remove_author_info_from_file(file_path):
            updated_count += 1
    
    print(f"\nUpdated {updated_count} files by removing author information")

if __name__ == "__main__":
    main() 