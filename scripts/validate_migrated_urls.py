#!/usr/bin/env python3
"""
Validate Migrated GitHub URLs

This script checks that all migrated GitHub URLs work correctly.
"""

import re
import requests
import time
from pathlib import Path
from urllib.parse import urlparse

def extract_github_urls_from_content(content):
    """Extract GitHub URLs from HTML content."""
    # Pattern to match GitHub URLs
    github_pattern = r'https://github\.com/juliensimon/[^"\s<>]+'
    matches = re.findall(github_pattern, content)
    return list(set(matches))  # Remove duplicates

def validate_github_url(url):
    """Validate if a GitHub URL returns a 200 OK status."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
        return response.status_code == 200
    except Exception as e:
        print(f"Error validating {url}: {e}")
        return False

def scan_html_files():
    """Scan for HTML files in youtube/ and blog/ directories."""
    html_files = []
    
    # Scan youtube/ directory (by year)
    youtube_dir = Path('youtube')
    if youtube_dir.exists():
        for year_dir in youtube_dir.iterdir():
            if year_dir.is_dir():
                for html_file in year_dir.glob('*.html'):
                    html_files.append(html_file)
    
    # Scan blog/ directory recursively
    blog_dir = Path('blog')
    if blog_dir.exists():
        for html_file in blog_dir.rglob('*.html'):
            html_files.append(html_file)
    
    return html_files

def categorize_url(url):
    """Categorize URL by type for better reporting."""
    parsed = urlparse(url)
    path_parts = parsed.path.split('/')
    
    if len(path_parts) >= 4:
        repo = path_parts[2]
        branch = path_parts[3]
        if len(path_parts) > 4:
            path = '/'.join(path_parts[4:])
            return f"{repo}/{branch}/{path}"
        else:
            return f"{repo}/{branch}"
    elif len(path_parts) >= 3:
        repo = path_parts[2]
        return f"{repo}"
    else:
        return "root"

def main():
    """Main validation function."""
    print("🔍 Validating Migrated GitHub URLs")
    print("=" * 50)
    
    # Scan for HTML files
    html_files = scan_html_files()
    print(f"Found {len(html_files)} HTML files to scan")
    print()
    
    # Collect all GitHub URLs
    all_github_urls = []
    url_sources = {}
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            github_urls = extract_github_urls_from_content(content)
            
            if github_urls:
                print(f"Found {len(github_urls)} GitHub URLs in {file_path}")
                for url in github_urls:
                    all_github_urls.append(url)
                    if url not in url_sources:
                        url_sources[url] = []
                    url_sources[url].append(str(file_path))
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    # Remove duplicates
    unique_urls = list(set(all_github_urls))
    print(f"\nFound {len(unique_urls)} unique GitHub URLs to validate")
    print()
    
    # Validate URLs
    valid_urls = []
    invalid_urls = []
    
    print("🔍 Validating GitHub URLs...")
    print("-" * 50)
    
    for i, url in enumerate(unique_urls, 1):
        print(f"Validating {i}/{len(unique_urls)}: {url}")
        is_valid = validate_github_url(url)
        
        if is_valid:
            valid_urls.append(url)
            print(f"  ✅ Valid")
        else:
            invalid_urls.append(url)
            print(f"  ❌ Invalid")
        
        # Rate limiting
        time.sleep(0.1)
    
    # Print results
    print()
    print("📊 Validation Results")
    print("=" * 50)
    print(f"Total URLs found: {len(unique_urls)}")
    print(f"Valid URLs: {len(valid_urls)}")
    print(f"Invalid URLs: {len(invalid_urls)}")
    
    if len(unique_urls) > 0:
        success_rate = (len(valid_urls) / len(unique_urls)) * 100
        print(f"Success rate: {success_rate:.1f}%")
    
    # Categorize URLs for better reporting
    if valid_urls:
        print("\n✅ Valid URL Categories:")
        categories = {}
        for url in valid_urls:
            category = categorize_url(url)
            if category not in categories:
                categories[category] = 0
            categories[category] += 1
        
        for category, count in sorted(categories.items()):
            print(f"  {category}: {count} URLs")
    
    if invalid_urls:
        print("\n❌ Invalid URLs:")
        for url in invalid_urls:
            print(f"  {url}")
            if url in url_sources:
                print(f"    Found in: {', '.join(url_sources[url])}")
    
    # Summary
    print()
    if len(invalid_urls) == 0:
        print("🎉 All migrated GitHub URLs are working correctly!")
    else:
        print(f"⚠️  {len(invalid_urls)} URLs need attention")
    
    return {
        'total': len(unique_urls),
        'valid': len(valid_urls),
        'invalid': len(invalid_urls),
        'success_rate': (len(valid_urls) / len(unique_urls)) * 100 if len(unique_urls) > 0 else 0
    }

if __name__ == "__main__":
    main() 