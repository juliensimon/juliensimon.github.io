#!/usr/bin/env python3
"""
GitLab to GitHub URL Migration Script

This script migrates all GitLab URLs to GitHub URLs in HTML files.
It includes safety measures like backups and dry-run mode.
"""

import re
import os
import shutil
from pathlib import Path
from datetime import datetime
import requests
import time

# Repository mappings
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

def extract_gitlab_urls_from_content(content):
    """Extract GitLab URLs from HTML content."""
    urls = []
    
    for i, pattern in enumerate(GITLAB_PATTERNS):
        matches = re.finditer(pattern, content)
        for match in matches:
            if i in [0, 1, 4, 5]:  # Patterns with repo/branch/path
                repo = match.group(1)
                branch = match.group(2)
                path = match.group(3)
                is_blob = i in [1, 5]  # blob patterns
                url_type = 'blob' if is_blob else 'tree'
                urls.append({
                    'type': 'repo_branch_path',
                    'repo': repo,
                    'branch': branch,
                    'path': path,
                    'url_type': url_type,
                    'original_url': f'https://gitlab.com/juliensimon/{repo}/-/{url_type}/{branch}/{path}',
                    'match': match.group(0)
                })
            elif i in [2, 3, 6, 7]:  # Patterns with repo/branch only
                repo = match.group(1)
                branch = match.group(2)
                is_blob = i in [3, 6]  # blob patterns
                url_type = 'blob' if is_blob else 'tree'
                urls.append({
                    'type': 'repo_branch',
                    'repo': repo,
                    'branch': branch,
                    'path': None,
                    'url_type': url_type,
                    'original_url': f'https://gitlab.com/juliensimon/{repo}/-/{url_type}/{branch}',
                    'match': match.group(0)
                })
            elif i == 8:  # Root repository pattern
                repo = match.group(1)
                urls.append({
                    'type': 'repo_only',
                    'repo': repo,
                    'branch': None,
                    'path': None,
                    'url_type': 'tree',
                    'original_url': f'https://gitlab.com/juliensimon/{repo}',
                    'match': match.group(0)
                })
    
    return urls

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

def backup_file(file_path):
    """Create a backup of the file before modification."""
    backup_path = file_path.with_suffix(file_path.suffix + '.backup')
    shutil.copy2(file_path, backup_path)
    return backup_path

def migrate_urls_in_file(file_path, dry_run=True):
    """Migrate GitLab URLs to GitHub URLs in a single file."""
    print(f"Processing: {file_path}")
    
    # Read file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract GitLab URLs
    gitlab_urls = extract_gitlab_urls_from_content(content)
    
    if not gitlab_urls:
        print(f"  No GitLab URLs found")
        return {'processed': False, 'urls_found': 0, 'urls_migrated': 0}
    
    print(f"  Found {len(gitlab_urls)} GitLab URLs")
    
    # Create backup if not in dry-run mode
    if not dry_run:
        backup_path = backup_file(file_path)
        print(f"  Backup created: {backup_path}")
    
    # Replace URLs
    new_content = content
    migrated_count = 0
    
    for url_info in gitlab_urls:
        original_url = url_info['original_url']
        github_url = generate_github_url(url_info)
        
        # Replace the URL in content
        new_content = new_content.replace(original_url, github_url)
        migrated_count += 1
        
        if dry_run:
            print(f"    Would migrate: {original_url}")
            print(f"    To: {github_url}")
        else:
            print(f"    Migrated: {original_url} → {github_url}")
    
    # Write updated content if not in dry-run mode
    if not dry_run:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  File updated: {file_path}")
    
    return {
        'processed': True,
        'urls_found': len(gitlab_urls),
        'urls_migrated': migrated_count
    }

def main():
    """Main migration function."""
    print("🔄 GitLab to GitHub URL Migration")
    print("=" * 50)
    
    # Configuration
    dry_run = False  # Set to True for testing
    
    if dry_run:
        print("⚠️  DRY RUN MODE - No files will be modified")
    else:
        print("🚀 LIVE MIGRATION MODE - Files will be updated")
    
    print()
    
    # Scan for HTML files
    html_files = scan_html_files()
    print(f"Found {len(html_files)} HTML files to process")
    print()
    
    # Process files
    stats = {
        'files_processed': 0,
        'files_modified': 0,
        'total_urls_found': 0,
        'total_urls_migrated': 0
    }
    
    for file_path in html_files:
        result = migrate_urls_in_file(file_path, dry_run=dry_run)
        
        if result['processed']:
            stats['files_processed'] += 1
            if result['urls_migrated'] > 0:
                stats['files_modified'] += 1
            stats['total_urls_found'] += result['urls_found']
            stats['total_urls_migrated'] += result['urls_migrated']
    
    # Print summary
    print()
    print("📊 Migration Summary")
    print("=" * 50)
    print(f"Files processed: {stats['files_processed']}")
    print(f"Files modified: {stats['files_modified']}")
    print(f"Total GitLab URLs found: {stats['total_urls_found']}")
    print(f"Total URLs migrated: {stats['total_urls_migrated']}")
    
    if dry_run:
        print("\n✅ Dry run completed successfully!")
        print("To perform the actual migration, set dry_run = False")
    else:
        print("\n✅ Migration completed successfully!")
        print("All GitLab URLs have been migrated to GitHub URLs")
        print("Backup files have been created with .backup extension")

if __name__ == "__main__":
    main() 