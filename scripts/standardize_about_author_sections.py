#!/usr/bin/env python3
"""
Script to standardize "About the Author" sections across all blog posts.
Removes top author-bio sections and ensures all posts have consistent end format.
"""

import os
import re
import glob

def remove_top_author_bio(file_path):
    """Remove the top author-bio section from a file."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if author-bio section exists
    if 'class="author-bio"' not in content:
        return False
    
    # Pattern to match the entire author-bio div
    pattern = r'<div class="author-bio">\s*<h3>About the Author</h3>\s*<p>.*?</p>\s*<p>.*?</p>\s*<p>.*?</p>\s*</div>'
    
    # Remove the author-bio section
    new_content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    if new_content == content:
        # Try a more flexible pattern if the first one didn't match
        pattern2 = r'<div class="author-bio">.*?</div>'
        new_content = re.sub(pattern2, '', content, flags=re.DOTALL)
    
    if new_content == content:
        print(f"No author-bio section found in {file_path}")
        return False
    
    # Write the updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Removed top author-bio section from {file_path}")
    return True

def ensure_end_about_author_aws(file_path):
    """Ensure AWS posts have the correct end format About the Author section."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if About the Author section exists at the end
    if 'About the Author' not in content:
        # Add the section at the end
        end_pattern = r'(\s*</body>\s*</html>\s*)$'
        about_author_section = '''
  <hr/>
  <h3>
   About the Author
  </h3>
  <p>
   <strong>
    Julien is the Artificial Intelligence &amp; Machine Learning Evangelist for EMEA
   </strong>
   . He focuses on helping developers and enterprises bring their ideas to life. In his spare time, he reads the works of JRR Tolkien again and again.
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
        
        new_content = re.sub(end_pattern, about_author_section, content, flags=re.MULTILINE)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Added end About the Author section to {file_path}")
        return True
    
    # Check if the existing section has the correct format
    if 'Julien is the Artificial Intelligence &amp; Machine Learning Evangelist for EMEA' in content:
        return False  # Already correct
    
    # Replace with correct format
    old_pattern = r'<hr/>\s*<h3>\s*About the Author\s*</h3>\s*<p>.*?</p>'
    replacement = '''<hr/>
  <h3>
   About the Author
  </h3>
  <p>
   <strong>
    Julien is the Artificial Intelligence &amp; Machine Learning Evangelist for EMEA
   </strong>
   . He focuses on helping developers and enterprises bring their ideas to life. In his spare time, he reads the works of JRR Tolkien again and again.
  </p>'''
    
    new_content = re.sub(old_pattern, replacement, content, flags=re.DOTALL)
    
    if new_content == content:
        return False
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated end About the Author section in {file_path}")
    return True

def ensure_end_about_author_huggingface(file_path):
    """Ensure Hugging Face posts have the correct end format About the Author section."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if About the Author section exists at the end
    if 'About the Author' not in content:
        # Add the section at the end
        end_pattern = r'(\s*</body>\s*</html>\s*)$'
        about_author_section = '''
  <hr/>
  <h3>
   About the Author
  </h3>
  <p>
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
        
        new_content = re.sub(end_pattern, about_author_section, content, flags=re.MULTILINE)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Added end About the Author section to {file_path}")
        return True
    
    # Check if the existing section has the correct format
    if 'Julien Simon is the Chief Evangelist at Hugging Face' in content:
        return False  # Already correct
    
    # Replace with correct format
    old_pattern = r'<hr/>\s*<h3>\s*About the Author\s*</h3>\s*<p>.*?</p>'
    replacement = '''<hr/>
  <h3>
   About the Author
  </h3>
  <p>
   <strong>
    Julien Simon is the Chief Evangelist at Hugging Face
   </strong>
   , where he focuses on democratizing AI and making transformers accessible to everyone. A leading voice in open-source AI and small language models, he helps developers and enterprises bring their AI ideas to life. In his spare time, he reads the works of JRR Tolkien again and again.
  </p>'''
    
    new_content = re.sub(old_pattern, replacement, content, flags=re.DOTALL)
    
    if new_content == content:
        return False
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated end About the Author section in {file_path}")
    return True

def main():
    """Main function to standardize About the Author sections in both AWS and Hugging Face posts."""
    
    # Find all index.html files in aws-posts-and-images
    aws_pattern = "blog/aws-posts-and-images/*/index.html"
    aws_files = glob.glob(aws_pattern)
    
    # Find all index.html files in huggingface-posts-and-images
    hf_pattern = "blog/huggingface-posts-and-images/*/index.html"
    hf_files = glob.glob(hf_pattern)
    
    print(f"Found {len(aws_files)} AWS post files")
    print(f"Found {len(hf_files)} Hugging Face post files")
    
    # Process AWS posts
    aws_top_removed = 0
    aws_end_updated = 0
    
    for file_path in aws_files:
        if remove_top_author_bio(file_path):
            aws_top_removed += 1
        if ensure_end_about_author_aws(file_path):
            aws_end_updated += 1
    
    # Process Hugging Face posts
    hf_end_updated = 0
    
    for file_path in hf_files:
        if ensure_end_about_author_huggingface(file_path):
            hf_end_updated += 1
    
    print(f"\nAWS Posts:")
    print(f"  - Removed top author-bio sections: {aws_top_removed}")
    print(f"  - Updated/added end sections: {aws_end_updated}")
    
    print(f"\nHugging Face Posts:")
    print(f"  - Updated/added end sections: {hf_end_updated}")
    
    print(f"\nAll posts now have consistent end format with company-appropriate bios!")

if __name__ == "__main__":
    main() 