#!/usr/bin/env python3
"""
Script to safely update or add "About the Author" sections to all content pages.
This script handles both scenarios:
- Pages WITH existing "About the Author" sections (replace with updated content)
- Pages WITHOUT existing sections (add new section)
"""

import os
import glob
import re
from pathlib import Path

# Vetted "About the Author" content from homepage messaging
ABOUT_AUTHOR_CONTENT = '''  <hr/>
  <h3>
   About the Author
  </h3>
  <p>
   <strong>
    Julien Simon is the Chief Evangelist at Arcee AI
   </strong>
   , specializing in Small Language Models and enterprise AI solutions. Recognized as the #1 AI Evangelist globally by AI Magazine in 2021, he brings over 30 years of technology leadership experience to his role.
  </p>
  <p>
   With 650+ speaking engagements worldwide and 350+ technical blog posts, Julien is a leading voice in practical AI implementation, cost-effective AI solutions, and the democratization of artificial intelligence. His expertise spans open-source AI, Small Language Models, enterprise AI strategy, and edge computing optimization.
  </p>
  <p>
   Previously serving as Principal Evangelist at Amazon Web Services and Chief Evangelist at Hugging Face, Julien has helped thousands of organizations implement AI solutions that deliver real business value. He is the author of "Learn Amazon SageMaker," the first book ever published on AWS's flagship machine learning service.
  </p>
  <p>
   Julien's mission is to make AI accessible, understandable, and controllable for enterprises through transparent, open-weights models that organizations can deploy, customize, and trust.
  </p>
  <p>
  </p>
  <p>
  </p>
  <p>
  </p>
  <!-- '"` -->'''

def update_about_author_section(file_path):
    """Update or add About the Author section to a single HTML file."""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if "About the Author" section already exists
        if 'About the Author' in content:
            print(f"  🔄 Found existing 'About the Author' section in {file_path}")
            
            # Find the existing section and replace it
            # Look for the pattern: <hr/> followed by <h3>About the Author</h3>
            pattern = r'<hr/>\s*<h3>\s*About the Author\s*</h3>.*?<!-- \'"` -->'
            match = re.search(pattern, content, re.DOTALL)
            
            if not match:
                # Try alternative pattern without the comment
                pattern = r'<hr/>\s*<h3>\s*About the Author\s*</h3>.*?<p>\s*</p>\s*<p>\s*</p>\s*<p>\s*</p>'
                match = re.search(pattern, content, re.DOTALL)
            
            if match:
                # Replace the entire section
                new_content = content[:match.start()] + ABOUT_AUTHOR_CONTENT + content[match.end():]
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"  ✅ Updated existing 'About the Author' section in {file_path}")
                return True
            else:
                print(f"  ⚠️  Found 'About the Author' text but couldn't match pattern in {file_path}")
                return False
        else:
            print(f"  ➕ No existing 'About the Author' section found in {file_path}")
            
            # Find the closing body tag
            body_end_match = re.search(r'</body>', content, re.IGNORECASE)
            if not body_end_match:
                print(f"  ❌ No closing </body> tag found in {file_path}")
                return False
            
            # Add the section before the closing body tag
            body_end = body_end_match.start()
            new_content = content[:body_end] + ABOUT_AUTHOR_CONTENT + content[body_end:]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"  ✅ Added new 'About the Author' section to {file_path}")
            return True
        
    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {str(e)}")
        return False

def main():
    """Main function to update About the Author sections on all content pages."""
    
    print("🎯 Updating 'About the Author' sections with vetted messaging...")
    print("📋 This will replace outdated sections and add new ones where missing")
    print()
    
    # Find all HTML files
    html_files = []
    
    # Blog posts
    blog_patterns = [
        "blog/**/*.html",
        "blog/*.html",
        "youtube/**/*.html",
        "youtube/*.html"
    ]
    
    for pattern in blog_patterns:
        html_files.extend(glob.glob(pattern, recursive=True))
    
    # Main pages (skip these as they don't need About the Author sections)
    main_pages = [
        "index.html",
        "experience.html", 
        "speaking.html",
        "publications.html",
        "books.html",
        "youtube.html",
        "code.html",
        "computers.html",
        "media-analysts.html",
        "podcasts.html"
    ]
    
    # Remove main pages from the list
    html_files = [f for f in html_files if os.path.basename(f) not in main_pages]
    
    print(f"📄 Found {len(html_files)} HTML files to process")
    print()
    
    # Process each file
    updated_count = 0
    added_count = 0
    error_count = 0
    
    for file_path in html_files:
        print(f"Processing: {file_path}")
        
        if update_about_author_section(file_path):
            if 'About the Author' in open(file_path, 'r', encoding='utf-8').read():
                if 'Chief Evangelist at Arcee AI' in open(file_path, 'r', encoding='utf-8').read():
                    updated_count += 1
                else:
                    added_count += 1
            else:
                added_count += 1
        else:
            error_count += 1
        
        print()
    
    print("🎉 About the Author section update complete!")
    print(f"✅ Updated: {updated_count} files")
    print(f"➕ Added: {added_count} files") 
    print(f"❌ Errors: {error_count} files")
    print()
    print("📊 Updated content includes:")
    print("  - Current role: Chief Evangelist at Arcee AI")
    print("  - Recognition: #1 AI Evangelist 2021")
    print("  - Experience: 30+ years technology leadership")
    print("  - Reach: 650+ speaking engagements, 350+ blog posts")
    print("  - Expertise: Small Language Models, enterprise AI")
    print("  - Mission: Making AI accessible and controllable")

if __name__ == "__main__":
    main() 