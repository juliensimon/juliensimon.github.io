#!/usr/bin/env python3
"""
Test script to verify GitLab URL extraction
"""

import re

# Test URLs
test_urls = [
    'https://gitlab.com/juliensimon/huggingface-demos/-/tree/main/vision-transformer',
    'https://gitlab.com/juliensimon/aim410/-/blob/master/local_training.ipynb',
    'https://gitlab.com/juliensimon/dlnotebooks/blob/master/pytorch/Detectron2_Tutorial.ipynb',
    'https://gitlab.com/juliensimon/awsmlmap',  # Should be ignored
    'https://gitlab.com/juliensimon/ent321/-/tree/master',
]

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
    r'https://gitlab\.com/juliensimon/([^/\s"<>]+)'
]

def extract_gitlab_urls_from_text(text):
    """Extract all GitLab URLs from text."""
    urls = []
    for i, pattern in enumerate(GITLAB_PATTERNS):
        matches = re.findall(pattern, text)
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
                    'original_url': f'https://gitlab.com/juliensimon/{repo}'
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
                    'original_url': f'https://gitlab.com/juliensimon/{repo}/-/tree/{branch}'
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
                    'original_url': f'https://gitlab.com/juliensimon/{repo}/-/{url_type}/{branch}/{path}'
                })
    
    return urls

def main():
    print("Testing GitLab URL extraction...")
    
    for url in test_urls:
        print(f"\nTesting: {url}")
        urls = extract_gitlab_urls_from_text(url)
        for url_info in urls:
            print(f"  Extracted: {url_info}")

if __name__ == "__main__":
    main() 