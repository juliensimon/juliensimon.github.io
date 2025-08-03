#!/usr/bin/env python3
"""
Script to add "About the Author" sections to specific missing Arcee blog posts.
"""

import os
import re

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

# List of missing Arcee blog posts
MISSING_ARCEE_POSTS = [
    "blog/arcee-posts/2025-06-30_arcee-ai-releases-five-new-open-weights-models/index.html",
    "blog/arcee-posts/2025-06-07_building-an-ai-retail-assistant-at-the-edge-with-small-language-models-and-intel-xeon-cpus/index.html",
    "blog/arcee-posts/2025-07-09_is-running-language-models-on-cpu-really-viable/index.html",
    "blog/arcee-posts/2025-06-10_breaking-down-model-vocabulary-barriers-with-tokenizer-transplantation/index.html",
    "blog/arcee-posts/2025-06-25_arcee-conductor-wins-llm-application-of-the-year-at-2025-ai-breakthrough-awards/index.html",
    "blog/arcee-posts/2025-06-18_announcing-arcee-foundation-models/index.html",
    "blog/arcee-posts/2025-04-17_the-case-for-small-language-model-inference-on-arm-cpus/index.html",
    "blog/arcee-posts/2025-07-18_arcee-ai-small-language-models-excel-across-yuppai-leaderboards/index.html"
]

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
    """Main function to add About the Author sections to missing Arcee blog posts."""
    
    print("🎯 Adding 'About the Author' sections to missing Arcee blog posts...")
    print("📋 This will add sections to specific Arcee blog posts that don't have them")
    print()
    
    # Process each file
    added_count = 0
    skipped_count = 0
    error_count = 0
    
    for file_path in MISSING_ARCEE_POSTS:
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