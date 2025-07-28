#!/usr/bin/env python3
"""
Simulation script to validate GitLab to GitHub URL migration.
This script will:
1. Extract all GitLab URLs from HTML files
2. Generate their GitHub equivalents
3. Validate that GitHub URLs resolve correctly
4. Provide a detailed report
"""

import re
import requests
import time
from pathlib import Path
from urllib.parse import urlparse, unquote
from collections import defaultdict

# Workshop repository mapping
WORKSHOP_MAPPING = {
    'aim410': 'reinvent-workshops/aim410',
    'aim307': 'reinvent-workshops/aim307', 
    'ent321': 'reinvent-workshops/ent321',
    'aim361': 'reinvent-workshops/aim361'
}

# GitLab URL patterns to match
GITLAB_PATTERNS = [
    r'https://gitlab\.com/juliensimon/([^/\s"<>]+)/-/tree/([^/\s"<>]+)/([^"\s<>]+)',
    r'https://gitlab\.com/juliensimon/([^/\s"<>]+)/-/blob/([^/\s"<>]+)/([^"\s<>]+)',
    r'https://gitlab\.com/juliensimon/([^/\s"<>]+)/-/tree/([^/\s"<>]+)',
    r'https://gitlab\.com/juliensimon/([^/\s"<>]+)/-/blob/([^/\s"<>]+)',
    r'https://gitlab\.com/juliensimon/([^/\s"<>]+)/blob/([^/\s"<>]+)/([^"\s<>]+)',
    r'https://gitlab\.com/juliensimon/([^/\s"<>]+)/tree/([^/\s"<>]+)/([^"\s<>]+)',
    r'https://gitlab\.com/juliensimon/([^/\s"<>]+)/blob/([^/\s"<>]+)',
    r'https://gitlab\.com/juliensimon/([^/\s"<>]+)/tree/([^/\s"<>]+)',
    r'https://gitlab\.com/juliensimon/([^/\s"<>]+)(?![^"\s<>]*[/])'
]

def extract_gitlab_urls_from_file(file_path):
    """Extract all GitLab URLs from a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        urls = []
        for i, pattern in enumerate(GITLAB_PATTERNS):
            matches = re.findall(pattern, content)
            for match in matches:
                if len(match) == 1:
                    # Repository root
                    repo = match[0]
                    if repo == 'awsmlmap':  # Skip awsmlmap
                        continue
                    urls.append({
                        'type': 'repo_root',
                        'repo': repo,
                        'branch': None,
                        'path': None,
                        'original_url': f'https://gitlab.com/juliensimon/{repo}',
                        'file_path': str(file_path)
                    })
                elif len(match) == 2:
                    # Repository with branch
                    repo, branch = match
                    if repo == 'awsmlmap':  # Skip awsmlmap
                        continue
                    urls.append({
                        'type': 'repo_branch',
                        'repo': repo,
                        'branch': branch,
                        'path': None,
                        'original_url': f'https://gitlab.com/juliensimon/{repo}/-/tree/{branch}',
                        'file_path': str(file_path)
                    })
                elif len(match) == 3:
                    # Repository with branch and path
                    repo, branch, path = match
                    if repo == 'awsmlmap':  # Skip awsmlmap
                        continue
                    
                    # Determine if this is a blob or tree URL based on the pattern index
                    # Patterns 0, 2, 4, 6 are tree patterns, patterns 1, 3, 5, 7 are blob patterns
                    is_blob = i in [1, 3, 5, 7]  # blob patterns
                    url_type = 'blob' if is_blob else 'tree'
                    
                    urls.append({
                        'type': 'repo_branch_path',
                        'repo': repo,
                        'branch': branch,
                        'path': path,
                        'url_type': url_type,
                        'original_url': f'https://gitlab.com/juliensimon/{repo}/-/{url_type}/{branch}/{path}',
                        'file_path': str(file_path)
                    })
        
        return urls
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return []

def generate_github_url(gitlab_url_info):
    """Generate GitHub URL from GitLab URL info."""
    repo = gitlab_url_info['repo']
    branch = gitlab_url_info['branch']
    path = gitlab_url_info['path']
    url_type = gitlab_url_info.get('url_type', 'tree')
    
    # Handle workshop repositories
    if repo in WORKSHOP_MAPPING:
        github_repo = WORKSHOP_MAPPING[repo]
        # Workshop repositories use 'main' branch, not 'master'
        if branch == 'master':
            branch = 'main'
    else:
        github_repo = repo
        # Some repositories use 'main' instead of 'master'
        if repo in ['amazon-studio-demos'] and branch == 'master':
            branch = 'main'
    
    # Build GitHub URL
    if path:
        github_url = f"https://github.com/juliensimon/{github_repo}/{url_type}/{branch}/{path}"
    elif branch:
        github_url = f"https://github.com/juliensimon/{github_repo}/tree/{branch}"
    else:
        github_url = f"https://github.com/juliensimon/{github_repo}"
    
    return github_url

def validate_github_url(url):
    """Validate that a GitHub URL resolves correctly."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; GitLabMigrationBot/1.0)'
        }
        response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
        return response.status_code == 200
    except Exception as e:
        return False

def scan_html_files(sample_mode=False):
    """Scan all HTML files for GitLab URLs."""
    html_files = []
    
    # Scan youtube directory
    youtube_dir = Path('youtube')
    if youtube_dir.exists():
        for year_dir in youtube_dir.iterdir():
            if year_dir.is_dir() and year_dir.name.isdigit():
                year_files = list(year_dir.glob('*.html'))
                if sample_mode:
                    # Take only first 3 files from each year for testing
                    year_files = year_files[:3]
                html_files.extend(year_files)
    
    # Scan blog directory
    blog_dir = Path('blog')
    if blog_dir.exists():
        blog_files = list(blog_dir.rglob('*.html'))
        if sample_mode:
            # Take only first 5 blog files for testing
            blog_files = blog_files[:5]
        html_files.extend(blog_files)
    
    return html_files

def main():
    """Main simulation function."""
    print("🔍 GitLab to GitHub URL Migration Simulation")
    print("=" * 50)
    
    # Use sample mode for testing
    sample_mode = True  # Set to False for full run
    html_files = scan_html_files(sample_mode=sample_mode)
    print(f"Found {len(html_files)} HTML files to scan" + (" (SAMPLE MODE)" if sample_mode else ""))
    
    # Extract all GitLab URLs
    all_gitlab_urls = []
    for file_path in html_files:
        urls = extract_gitlab_urls_from_file(file_path)
        all_gitlab_urls.extend(urls)
    
    print(f"Found {len(all_gitlab_urls)} GitLab URLs")
    
    # Generate GitHub URLs and validate
    results = {
        'valid': [],
        'invalid': [],
        'workshop_repos': [],
        'standard_repos': [],
        'ignored': []
    }
    
    print("\n📋 URL Analysis:")
    print("-" * 30)
    
    for url_info in all_gitlab_urls:
        github_url = generate_github_url(url_info)
        
        # Categorize
        if url_info['repo'] in WORKSHOP_MAPPING:
            results['workshop_repos'].append({
                'gitlab_url': url_info['original_url'],
                'github_url': github_url,
                'repo': url_info['repo'],
                'file_path': url_info['file_path']
            })
        else:
            results['standard_repos'].append({
                'gitlab_url': url_info['original_url'],
                'github_url': github_url,
                'repo': url_info['repo'],
                'file_path': url_info['file_path']
            })
    
    # Validate GitHub URLs
    print("\n🔍 Validating GitHub URLs...")
    print("-" * 30)
    
    all_urls_to_validate = results['workshop_repos'] + results['standard_repos']
    
    for i, url_info in enumerate(all_urls_to_validate):
        print(f"Validating {i+1}/{len(all_urls_to_validate)}: {url_info['github_url']}")
        
        is_valid = validate_github_url(url_info['github_url'])
        
        if is_valid:
            results['valid'].append(url_info)
            print(f"  ✅ Valid")
        else:
            results['invalid'].append(url_info)
            print(f"  ❌ Invalid")
        
        # Rate limiting
        time.sleep(0.1)
    
    # Generate report
    print("\n📊 Migration Simulation Report")
    print("=" * 50)
    
    print(f"\n📁 Repository Breakdown:")
    print(f"  Standard repositories: {len(results['standard_repos'])}")
    print(f"  Workshop repositories: {len(results['workshop_repos'])}")
    print(f"  Ignored (awsmlmap): {len(results['ignored'])}")
    
    print(f"\n✅ Validation Results:")
    print(f"  Valid GitHub URLs: {len(results['valid'])}")
    print(f"  Invalid GitHub URLs: {len(results['invalid'])}")
    total_urls = len(results['valid']) + len(results['invalid'])
    success_rate = (len(results['valid']) / total_urls * 100) if total_urls > 0 else 0
    print(f"  Success rate: {success_rate:.1f}%")
    
    # Show workshop repository mappings
    print(f"\n🏗️ Workshop Repository Mappings:")
    for repo, github_path in WORKSHOP_MAPPING.items():
        print(f"  {repo} → {github_path}")
    
    # Show invalid URLs
    if results['invalid']:
        print(f"\n❌ Invalid GitHub URLs:")
        for url_info in results['invalid']:
            print(f"  {url_info['github_url']} (from {url_info['file_path']})")
    
    # Show sample transformations
    print(f"\n🔄 Sample URL Transformations:")
    print("Standard repositories:")
    for url_info in results['standard_repos'][:3]:
        print(f"  {url_info['gitlab_url']}")
        print(f"  → {url_info['github_url']}")
        print()
    
    print("Workshop repositories:")
    for url_info in results['workshop_repos'][:3]:
        print(f"  {url_info['gitlab_url']}")
        print(f"  → {url_info['github_url']}")
        print()
    
    # Save detailed results to file
    with open('gitlab_migration_simulation_results.txt', 'w') as f:
        f.write("GitLab to GitHub Migration Simulation Results\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"Total URLs found: {len(all_gitlab_urls)}\n")
        f.write(f"Valid GitHub URLs: {len(results['valid'])}\n")
        f.write(f"Invalid GitHub URLs: {len(results['invalid'])}\n\n")
        
        f.write("Invalid URLs:\n")
        for url_info in results['invalid']:
            f.write(f"  {url_info['github_url']} (from {url_info['file_path']})\n")
    
    print(f"\n📄 Detailed results saved to: gitlab_migration_simulation_results.txt")
    
    return results

if __name__ == "__main__":
    main() 