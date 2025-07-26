#!/usr/bin/env python3
"""
Script to remove breadcrumb navigation from AWS blog post files and replace with a simple back link.
"""

import os
import re
import glob

def remove_breadcrumbs_and_add_back_link():
    """Remove breadcrumb navigation and add a simple back link to aws-blog-posts.html"""
    
    # Find all index.html files in aws-posts-and-images subdirectories
    pattern = "blog/aws-posts-and-images/*/index.html"
    files = glob.glob(pattern)
    
    print(f"Found {len(files)} blog post files to process")
    
    for file_path in files:
        print(f"Processing: {file_path}")
        
        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove the breadcrumb CSS styles
            breadcrumb_css_pattern = r'\.breadcrumb \{[^}]*\}\s*\.breadcrumb a \{[^}]*\}'
            content = re.sub(breadcrumb_css_pattern, '', content, flags=re.DOTALL)
            
            # Remove the breadcrumb HTML and replace with back link
            breadcrumb_html_pattern = r'<div class="breadcrumb">\s*<a href="[^"]*">Home</a> &gt;\s*<a href="[^"]*">Blog</a> &gt;\s*<a href="[^"]*">AWS</a> &gt;\s*AWS Blog Post\s*</div>'
            
            back_link_html = '''<div style="margin-bottom: 1em;">
  <a href="../../../aws-blog-posts.html" style="color: #FF9900; text-decoration: none; font-size: 0.9em;">← Back to AWS Blog Posts</a>
</div>'''
            
            content = re.sub(breadcrumb_html_pattern, back_link_html, content, flags=re.DOTALL)
            
            # Write the modified content back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"  ✓ Updated {file_path}")
            
        except Exception as e:
            print(f"  ✗ Error processing {file_path}: {e}")
    
    print(f"\nCompleted processing {len(files)} files")

if __name__ == "__main__":
    remove_breadcrumbs_and_add_back_link() 