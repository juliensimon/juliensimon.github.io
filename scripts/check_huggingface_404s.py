#!/usr/bin/env python3
"""
Script to check for 404 errors in Hugging Face blog posts.
"""

import requests
import os
import glob
from urllib.parse import urljoin

def check_url(url, timeout=10):
    """Check if a URL returns a 404 error."""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        if response.status_code == 404:
            return False, f"404 Error: {response.status_code}"
        elif response.status_code >= 400:
            return False, f"HTTP Error: {response.status_code}"
        else:
            return True, f"OK: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"Request Error: {str(e)}"

def check_local_file(file_path):
    """Check if a local file exists."""
    if os.path.exists(file_path):
        return True, "File exists"
    else:
        return False, "File not found"

def main():
    """Main function to check for 404s."""
    print("Checking Hugging Face blog posts for 404 errors...\n")
    
    # Read the mapping file
    mapping_file = "blog/huggingface-posts-and-images/huggingface-blog-urls.txt"
    if not os.path.exists(mapping_file):
        print(f"Mapping file not found: {mapping_file}")
        return
    
    with open(mapping_file, 'r') as f:
        lines = f.readlines()
    
    print("=== ORIGINAL URLS ===")
    original_404s = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        original_url, local_path = line.split('|')
        print(f"Checking: {original_url}")
        success, message = check_url(original_url)
        if not success:
            original_404s.append((original_url, message))
            print(f"  ❌ {message}")
        else:
            print(f"  ✅ {message}")
    
    print(f"\n=== LOCAL COPIES ===")
    local_404s = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        original_url, local_path = line.split('|')
        local_file = f"blog/huggingface-posts-and-images/{local_path}/index.html"
        print(f"Checking: {local_file}")
        success, message = check_local_file(local_file)
        if not success:
            local_404s.append((local_file, message))
            print(f"  ❌ {message}")
        else:
            print(f"  ✅ {message}")
    
    # Summary
    print(f"\n=== SUMMARY ===")
    print(f"Original URLs with 404s: {len(original_404s)}")
    print(f"Local copies with 404s: {len(local_404s)}")
    
    if original_404s:
        print(f"\nOriginal URLs with issues:")
        for url, error in original_404s:
            print(f"  {url}: {error}")
    
    if local_404s:
        print(f"\nLocal copies with issues:")
        for file_path, error in local_404s:
            print(f"  {file_path}: {error}")

if __name__ == "__main__":
    main() 