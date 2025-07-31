#!/usr/bin/env python3
"""
Debug script to find missing blog posts
"""

import os
import glob
import re

def extract_date_from_filename(filename):
    """Extract date from directory name."""
    match = re.search(r'^(\d{4}-\d{2}-\d{2})_', filename)
    if match:
        return match.group(1)
    return None

def debug_blog_posts():
    """Debug which blog posts are missing."""
    
    print("=== Debugging Blog Posts ===")
    
    # Check Arcee posts
    arcee_pattern = "blog/arcee-posts/*/index.html"
    arcee_files = glob.glob(arcee_pattern)
    print(f"Arcee posts found: {len(arcee_files)}")
    
    for file_path in arcee_files:
        dir_name = os.path.basename(os.path.dirname(file_path))
        date = extract_date_from_filename(dir_name)
        if not date:
            print(f"  ❌ No date found: {dir_name}")
        else:
            print(f"  ✅ {dir_name} -> {date}")
    
    # Check HuggingFace posts
    hf_pattern = "blog/huggingface-posts-and-images/*/index.html"
    hf_files = glob.glob(hf_pattern)
    print(f"\nHuggingFace posts found: {len(hf_files)}")
    
    for file_path in hf_files:
        dir_name = os.path.basename(os.path.dirname(file_path))
        date = extract_date_from_filename(dir_name)
        if not date:
            print(f"  ❌ No date found: {dir_name}")
        else:
            print(f"  ✅ {dir_name} -> {date}")
    
    # Check AWS posts
    aws_pattern = "blog/aws-posts-and-images/*/index.html"
    aws_files = glob.glob(aws_pattern)
    print(f"\nAWS posts found: {len(aws_files)}")
    
    for file_path in aws_files:
        dir_name = os.path.basename(os.path.dirname(file_path))
        date = extract_date_from_filename(dir_name)
        if not date:
            print(f"  ❌ No date found: {dir_name}")
        else:
            print(f"  ✅ {dir_name} -> {date}")
    
    # Check Medium posts
    medium_pattern = "blog/aws-medium-posts-and-images/*/*/index.html"
    medium_files = glob.glob(medium_pattern)
    print(f"\nMedium posts found: {len(medium_files)}")
    
    for file_path in medium_files:
        dir_name = os.path.basename(os.path.dirname(file_path))
        date = extract_date_from_filename(dir_name)
        if not date:
            print(f"  ❌ No date found: {dir_name}")
        else:
            print(f"  ✅ {dir_name} -> {date}")
    
    # Check Legacy posts
    legacy_pattern = "blog/legacy-posts-and-images/*/index.html"
    legacy_files = glob.glob(legacy_pattern)
    print(f"\nLegacy posts found: {len(legacy_files)}")
    
    for file_path in legacy_files:
        dir_name = os.path.basename(os.path.dirname(file_path))
        date = extract_date_from_filename(dir_name)
        if not date:
            print(f"  ❌ No date found: {dir_name}")
        else:
            print(f"  ✅ {dir_name} -> {date}")

if __name__ == "__main__":
    debug_blog_posts() 