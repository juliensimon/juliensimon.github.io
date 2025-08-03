#!/usr/bin/env python3
"""
Script to fix outdated "About the Author" sections in Hugging Face blog posts.
This script targets the old Hugging Face-style "About the Author" sections.
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
  <!-- '"` -->'''

def fix_huggingface_about_author_section(file_path):
    """Fix outdated About the Author section in a single Hugging Face blog post file."""

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if file already has the correct content
        if 'Julien Simon is the Chief Evangelist at Arcee AI' in content:
            print(f"  ✅ Already has correct content: {file_path}")
            return False

        # Look for the outdated pattern with flexible matching
        # Pattern: About the Author section with "Julien Simon is the Chief Evangelist at Hugging Face"
        pattern = r'(<hr/>\s*<h3>\s*About the Author\s*</h3>\s*<p>\s*<strong>\s*Julien Simon is the Chief Evangelist at Hugging Face\s*</strong>\s*,\s*where he focuses on democratizing AI and making transformers accessible to everyone\.\s*A leading voice in open-source AI and small language models, he helps developers and enterprises bring their AI ideas to life\.\s*In his spare time, he reads the works of JRR Tolkien again and again\.\s*</p>\s*<p>\s*</p>\s*<p>\s*</p>\s*<p>\s*</p>\s*<!-- \'"` -->)'
        
        match = re.search(pattern, content, re.DOTALL)
        if match:
            # Replace the outdated section with the new content
            new_content = content.replace(match.group(1), ABOUT_AUTHOR_CONTENT)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"  ➕ Fixed outdated 'About the Author' section in {file_path}")
            return True
        else:
            # Try a simpler pattern that just looks for the key phrase
            if 'Julien Simon is the Chief Evangelist at Hugging Face' in content:
                # Replace the specific outdated phrase
                new_content = content.replace('Julien Simon is the Chief Evangelist at Hugging Face', 'Julien Simon is the Chief Evangelist at Arcee AI')
                
                # Also replace the rest of the outdated content
                old_content_pattern = r'(where he focuses on democratizing AI and making transformers accessible to everyone\.\s*A leading voice in open-source AI and small language models, he helps developers and enterprises bring their AI ideas to life\.\s*In his spare time, he reads the works of JRR Tolkien again and again\.)'
                new_content = re.sub(old_content_pattern, 'specializing in Small Language Models and enterprise AI solutions. Recognized as the #1 AI Evangelist globally by AI Magazine in 2021, he brings over 30 years of technology leadership experience to his role.', new_content, flags=re.DOTALL)
                
                # Add the additional paragraphs
                additional_content = '''  <p>
   With 650+ speaking engagements worldwide and 350+ technical blog posts, Julien is a leading voice in practical AI implementation, cost-effective AI solutions, and the democratization of artificial intelligence. His expertise spans open-source AI, Small Language Models, enterprise AI strategy, and edge computing optimization.
  </p>
  <p>
   Previously serving as Principal Evangelist at AWS and Chief Evangelist at Hugging Face, Julien has authored books on Amazon SageMaker and contributed to the open-source AI ecosystem. His mission is to make AI accessible, understandable, and controllable for everyone.
  </p>'''
                
                # Find the position to insert the additional content
                insert_pos = new_content.find('<!-- \'"` -->')
                if insert_pos != -1:
                    new_content = new_content[:insert_pos] + additional_content + '\n  ' + new_content[insert_pos:]
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"  ➕ Fixed outdated 'About the Author' section in {file_path}")
                return True
            else:
                print(f"  ❌ No outdated pattern found in {file_path}")
                return False

    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {str(e)}")
        return False

def main():
    """Main function to fix outdated About the Author sections in Hugging Face blog posts."""

    print("🎯 Fixing outdated 'About the Author' sections in Hugging Face blog posts...")
    print("📋 This will replace old Hugging Face content with current Arcee AI messaging")
    print()

    # Find all Hugging Face blog posts
    huggingface_files = glob.glob("blog/huggingface-posts-and-images/**/*.html", recursive=True)

    print(f"📄 Found {len(huggingface_files)} Hugging Face blog posts to check")
    print()

    # Process each file
    fixed_count = 0
    skipped_count = 0
    error_count = 0

    for file_path in huggingface_files:
        print(f"Processing: {file_path}")

        if fix_huggingface_about_author_section(file_path):
            fixed_count += 1
        else:
            skipped_count += 1

        print()

    print("🎉 Hugging Face About the Author section fixes complete!")
    print(f"➕ Fixed: {fixed_count} files")
    print(f"✅ Skipped: {skipped_count} files (already correct or no pattern found)")
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