#!/usr/bin/env python3
"""
Script to add "About the Author" sections to Hugging Face blog posts.
"""

import os
import re
import glob

def add_about_author_section(file_path):
    """Add About the Author section to a single HTML file."""
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if About the Author section already exists
    if 'About the Author' in content:
        print(f"About the Author section already exists in {file_path}")
        return False
    
    # Find the end of the body content (before closing body tag)
    body_end_pattern = r'(\s*</body>\s*</html>\s*)$'
    match = re.search(body_end_pattern, content, re.MULTILINE)
    
    if not match:
        print(f"Could not find body end in {file_path}")
        return False
    
    # Create the About the Author section
    about_author_section = '''
  <hr/>
  <h3>
   About the Author
  </h3>
  <p>
   <img alt="Julien Simon" class="alignleft size-full wp-image-3134" height="115" loading="lazy" src="image01.webp" width="100"/>
   <strong>
    Julien Simon is the Chief Evangelist at Hugging Face
   </strong>
   , where he focuses on democratizing AI and making transformers accessible to everyone. A leading voice in open-source AI and small language models, he helps developers and enterprises bring their AI ideas to life. In his spare time, he reads the works of JRR Tolkien again and again.
  </p>
  <p>
  </p>
  <p>
  </p>
  <p>
  </p>
  <!-- '"` -->
 
  
  </body>
 </html>'''
    
    # Insert the About the Author section before the closing body tag
    new_content = re.sub(body_end_pattern, about_author_section, content, flags=re.MULTILINE)
    
    # Write the updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Added About the Author section to {file_path}")
    return True

def main():
    """Main function to add About the Author sections to all Hugging Face posts."""
    
    # Find all index.html files in huggingface-posts-and-images
    pattern = "blog/huggingface-posts-and-images/*/index.html"
    files = glob.glob(pattern)
    
    if not files:
        print("No Hugging Face post files found!")
        return
    
    print(f"Found {len(files)} Hugging Face post files")
    
    updated_count = 0
    for file_path in files:
        if add_about_author_section(file_path):
            updated_count += 1
    
    print(f"\nAdded About the Author sections to {updated_count} out of {len(files)} files")

if __name__ == "__main__":
    main() 