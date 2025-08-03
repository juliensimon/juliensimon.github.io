#!/usr/bin/env python3
"""
Script to fix outdated "About the Author" sections that don't mention Arcee AI.
This script specifically targets the old AWS-style "About the Author" sections.
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
   Previously serving as Principal Evangelist at AWS and Chief Evangelist at Hugging Face, Julien has authored books on Amazon SageMaker and contributed to the open-source AI ecosystem. His mission is to make AI accessible, understandable, and controllable for everyone.
  </p>
  <!-- '` -->'''

def fix_outdated_about_author_section(file_path):
    """Fix outdated About the Author section in a single HTML file."""

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if file has the outdated AWS-style "About the Author" section
        # Look for the old pattern: "Julien is the Artificial Intelligence & Machine Learning Evangelist for EMEA"
        if 'Julien is the Artificial Intelligence & Machine Learning Evangelist for EMEA' in content:
            print(f"  🔧 Found outdated AWS-style 'About the Author' section in {file_path}")
            
            # Find the old section and replace it
            # Pattern to match the exact content structure found in AWS blog posts
            old_pattern = r'<hr/>\s*<h3>\s*About the Author\s*</h3>\s*<p>\s*<strong>\s*Julien is the Artificial Intelligence &amp; Machine Learning Evangelist for EMEA\s*</strong>\s*\.\s*He focuses on helping developers and enterprises bring their ideas to life\.\s*In his spare time, he reads the works of JRR Tolkien again and again\.\s*</p>\s*<p>\s*</p>\s*<p>\s*</p>\s*<p>\s*</p>\s*<!--\s*[\'"`]\s*-->'
            
            # Replace with new content
            new_content = re.sub(old_pattern, ABOUT_AUTHOR_CONTENT, content, flags=re.DOTALL)
            
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  ✅ Fixed outdated 'About the Author' section in {file_path}")
                return True
            else:
                print(f"  ⚠️  Pattern not found or no changes made in {file_path}")
                return False
        else:
            print(f"  ✅ Already has correct 'About the Author' section: {file_path}")
            return False

    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {str(e)}")
        return False

def main():
    """Main function to fix outdated About the Author sections."""

    print("🎯 Fixing outdated 'About the Author' sections...")
    print("📋 This will replace old AWS-style sections with current Arcee AI content")
    print()

    # Find ALL HTML files
    html_files = glob.glob("**/*.html", recursive=True)

    # Skip main pages that don't need About the Author sections
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
        "podcasts.html",
        "speaking-2024.html",
        "speaking-2023.html",
        "speaking-2022.html",
        "speaking-2021.html",
        "speaking-2020.html",
        "speaking-2019.html",
        "speaking-2018.html",
        "speaking-2017.html",
        "speaking-2016.html",
        "arcee-blog-posts.html",
        "aws-blog-posts.html",
        "huggingface-blog-posts.html",
        "medium-blog-posts.html",
        "aws-medium-posts.html",
        "yandex_2ec4ded54cdb437b.html",
        "404.html",
        "500.html"
    ]

    # Remove main pages from the list
    html_files = [f for f in html_files if os.path.basename(f) not in main_pages]

    print(f"📄 Found {len(html_files)} HTML files to process")
    print()

    # Process each file
    fixed_count = 0
    skipped_count = 0
    error_count = 0

    for file_path in html_files:
        print(f"Processing: {file_path}")

        if fix_outdated_about_author_section(file_path):
            fixed_count += 1
        else:
            skipped_count += 1

        print()

    print("🎉 About the Author section fixes complete!")
    print(f"🔧 Fixed: {fixed_count} files")
    print(f"✅ Skipped: {skipped_count} files (already correct)")
    print(f"❌ Errors: {error_count} files")
    print()
    print("📊 Fixed content includes:")
    print("  - Current role: Chief Evangelist at Arcee AI")
    print("  - Recognition: #1 AI Evangelist 2021")
    print("  - Experience: 30+ years technology leadership")
    print("  - Reach: 650+ speaking engagements, 350+ blog posts")
    print("  - Expertise: Small Language Models, enterprise AI")
    print("  - Mission: Making AI accessible and controllable")

if __name__ == "__main__":
    main() 