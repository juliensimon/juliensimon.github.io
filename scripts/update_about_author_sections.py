#!/usr/bin/env python3
"""
Script to update "About the Author" sections in both AWS and Hugging Face posts.
Removes images and ensures consistent formatting.
"""

import os
import re
import glob

def update_aws_about_author(file_path):
    """Update About the Author section in AWS posts - remove image."""
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if About the Author section exists
    if 'About the Author' not in content:
        print(f"No About the Author section found in {file_path}")
        return False
    
    # Pattern to match the About the Author section with image
    pattern = r'(<hr/>\s*<h3>\s*About the Author\s*</h3>\s*<p>\s*<img[^>]*/>\s*<strong>\s*Julien is the Artificial Intelligence &amp; Machine Learning Evangelist for EMEA\s*</strong>\s*\. He focuses on helping developers and enterprises bring their ideas to life\. In his spare time, he reads the works of JRR Tolkien again and again\.\s*</p>)'
    
    # Replacement without image
    replacement = '''<hr/>
  <h3>
   About the Author
  </h3>
  <p>
   <strong>
    Julien is the Artificial Intelligence &amp; Machine Learning Evangelist for EMEA
   </strong>
   . He focuses on helping developers and enterprises bring their ideas to life. In his spare time, he reads the works of JRR Tolkien again and again.
  </p>'''
    
    # Apply the replacement
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content == content:
        print(f"No changes needed for {file_path}")
        return False
    
    # Write the updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated AWS About the Author section in {file_path}")
    return True

def update_huggingface_about_author(file_path):
    """Update About the Author section in Hugging Face posts - remove image."""
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if About the Author section exists
    if 'About the Author' not in content:
        print(f"No About the Author section found in {file_path}")
        return False
    
    # Pattern to match the About the Author section with image
    pattern = r'(<hr/>\s*<h3>\s*About the Author\s*</h3>\s*<p>\s*<img[^>]*/>\s*<strong>\s*Julien Simon is the Chief Evangelist at Hugging Face\s*</strong>\s*,[^<]*\. A leading voice in open-source AI and small language models, he helps developers and enterprises bring their AI ideas to life\. In his spare time, he reads the works of JRR Tolkien again and again\.\s*</p>)'
    
    # Replacement without image
    replacement = '''<hr/>
  <h3>
   About the Author
  </h3>
  <p>
   <strong>
    Julien Simon is the Chief Evangelist at Hugging Face
   </strong>
   , where he focuses on democratizing AI and making transformers accessible to everyone. A leading voice in open-source AI and small language models, he helps developers and enterprises bring their AI ideas to life. In his spare time, he reads the works of JRR Tolkien again and again.
  </p>'''
    
    # Apply the replacement
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content == content:
        print(f"No changes needed for {file_path}")
        return False
    
    # Write the updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated Hugging Face About the Author section in {file_path}")
    return True

def main():
    """Main function to update About the Author sections in both AWS and Hugging Face posts."""
    
    # Find all index.html files in aws-posts-and-images
    aws_pattern = "blog/aws-posts-and-images/*/index.html"
    aws_files = glob.glob(aws_pattern)
    
    # Find all index.html files in huggingface-posts-and-images
    hf_pattern = "blog/huggingface-posts-and-images/*/index.html"
    hf_files = glob.glob(hf_pattern)
    
    print(f"Found {len(aws_files)} AWS post files")
    print(f"Found {len(hf_files)} Hugging Face post files")
    
    # Update AWS posts
    aws_updated = 0
    for file_path in aws_files:
        if update_aws_about_author(file_path):
            aws_updated += 1
    
    # Update Hugging Face posts
    hf_updated = 0
    for file_path in hf_files:
        if update_huggingface_about_author(file_path):
            hf_updated += 1
    
    print(f"\nUpdated {aws_updated} out of {len(aws_files)} AWS files")
    print(f"Updated {hf_updated} out of {len(hf_files)} Hugging Face files")

if __name__ == "__main__":
    main() 