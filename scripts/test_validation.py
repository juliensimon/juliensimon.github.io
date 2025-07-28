#!/usr/bin/env python3
"""
Test script to validate specific GitHub URLs that were failing in the simulation.
"""

import requests
import time

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

def test_workshop_urls():
    """Test the workshop repository URLs that were failing."""
    test_urls = [
        "https://github.com/juliensimon/reinvent-workshops/blob/main/aim410/local_training.ipynb",
        "https://github.com/juliensimon/reinvent-workshops/tree/main/aim410",
        "https://github.com/juliensimon/reinvent-workshops/tree/main/aim361/Lab2.ipynb",
        "https://github.com/juliensimon/reinvent-workshops/tree/main/aim361",
        "https://github.com/juliensimon/amazon-studio-demos/tree/main/sagemaker_fridays/season3/s03e03",
        "https://github.com/juliensimon/amazon-studio-demos/tree/main/sagemaker_fridays/season3/s03e04",
        "https://github.com/juliensimon/amazon-studio-demos/tree/main/sagemaker_fridays/season3/s03e05"
    ]
    
    print("Testing workshop repository URLs...")
    for i, url in enumerate(test_urls, 1):
        print(f"Testing {i}/{len(test_urls)}: {url}")
        is_valid = validate_github_url(url)
        status = "✅ Valid" if is_valid else "❌ Invalid"
        print(f"  {status}")
        time.sleep(0.5)  # Rate limiting

if __name__ == "__main__":
    test_workshop_urls() 