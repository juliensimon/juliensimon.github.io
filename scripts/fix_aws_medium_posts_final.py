#!/usr/bin/env python3
"""
Script to add "About the Author" sections to all AWS Medium posts.
"""

import os
import re
import subprocess

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

def add_about_author_section(file_path):
    """Add About the Author section to a single HTML file if it doesn't have one."""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if "About the Author" section already exists
        if 'About the Author' in content:
            print(f"  ✅ Already has 'About the Author' section: {file_path}")
            return False
        
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
        
        print(f"  ➕ Added new 'About the Author' section to {file_path}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {str(e)}")
        return False

def main():
    """Main function to add About the Author sections to all AWS Medium posts."""
    
    print("🎯 Adding 'About the Author' sections to all AWS Medium posts...")
    print("📋 This will add sections to AWS Medium posts that don't have them")
    print()
    
    # Find ALL AWS Medium posts using find command
    result = subprocess.run(['find', 'blog/aws-medium-posts-and-images', '-name', '*.html'], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Error finding AWS Medium posts")
        return
    
    aws_medium_files = result.stdout.strip().split('\n')
    aws_medium_files = [f for f in aws_medium_files if f]  # Don't filter out index.html files
    
    print(f"📄 Found {len(aws_medium_files)} AWS Medium posts to process")
    print(f"First few files: {aws_medium_files[:3]}")
    print()
    
    # Process each file
    added_count = 0
    skipped_count = 0
    error_count = 0
    
    for file_path in aws_medium_files:
        print(f"Processing: {file_path}")
        
        if add_about_author_section(file_path):
            added_count += 1
        else:
            skipped_count += 1
        
        print()
    
    print("🎉 About the Author section addition complete!")
    print(f"➕ Added: {added_count} files")
    print(f"✅ Skipped: {skipped_count} files (already had sections)")
    print(f"❌ Errors: {error_count} files")
    print()
    print("📊 Added content includes:")
    print("  - Current role: Chief Evangelist at Arcee AI")
    print("  - Recognition: #1 AI Evangelist 2021")
    print("  - Experience: 30+ years technology leadership")
    print("  - Reach: 650+ speaking engagements, 350+ blog posts")
    print("  - Expertise: Small Language Models, enterprise AI")
    print("  - Mission: Making AI accessible and controllable")

if __name__ == "__main__":
    main() 