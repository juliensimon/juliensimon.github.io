#!/usr/bin/env python3
"""
Script to apply minimal styling to Medium and Arcee blog posts.
Just improves readability without fancy effects.
"""

import os
import re
import glob
from pathlib import Path

def apply_minimal_styling_to_medium_arcee(file_path):
    """Apply minimal styling to a single blog post file."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if it already has CSS link
    if 'css/minimal-blog-styles.css' in content:
        return False
    
    # Find the head tag and add CSS link before closing head
    head_pattern = r'(</head>)'
    css_link = '''    <link rel="stylesheet" href="../../../css/minimal-blog-styles.css">
'''
    
    # Add CSS link before closing head tag
    content = re.sub(head_pattern, css_link + r'\1', content)
    
    # Write the updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """Apply minimal styling to all Medium and Arcee posts."""
    
    # Find all Medium posts
    medium_posts = glob.glob('blog/aws-medium-posts-and-images/**/*.html', recursive=True)
    
    # Find all Arcee posts
    arcee_posts = glob.glob('blog/arcee-posts/**/*.html', recursive=True)
    
    all_posts = medium_posts + arcee_posts
    
    updated_count = 0
    
    for file_path in all_posts:
        if apply_minimal_styling_to_medium_arcee(file_path):
            updated_count += 1
            print(f"Updated: {file_path}")
    
    print(f"\nTotal posts updated: {updated_count}")
    print(f"Medium posts: {len(medium_posts)}")
    print(f"Arcee posts: {len(arcee_posts)}")

if __name__ == "__main__":
    main() 