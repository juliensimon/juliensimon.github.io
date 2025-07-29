#!/usr/bin/env python3
"""
Simple Fix Script
Addresses critical issues with basic regex patterns.
"""

import os
import re
import glob

def add_missing_alt_to_main_pages():
    """Add alt attributes to images in main pages only."""
    print("🖼️  Adding missing alt attributes to main pages...")
    
    main_files = ['index.html', 'experience.html', 'publications.html', 'speaking.html', 'computers.html']
    fixed_count = 0
    
    for file_path in main_files:
        if not os.path.exists(file_path):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple pattern to find img tags without alt
            original_content = content
            
            # Replace common patterns
            content = re.sub(r'<img([^>]*?)src="([^"]*)"([^>]*?)>', 
                           lambda m: add_alt_if_missing(m, 'Image'), content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += 1
                print(f"  ✅ Fixed alt attributes in {file_path}")
        
        except Exception as e:
            print(f"  ❌ Error processing {file_path}: {e}")
    
    print(f"Fixed alt attributes in {fixed_count} main files")

def add_alt_if_missing(match, default_alt):
    """Add alt attribute if missing from img tag."""
    full_match = match.group(0)
    if 'alt=' in full_match:
        return full_match
    
    # Extract the parts
    before_src = match.group(1)
    src_value = match.group(2)
    after_src = match.group(3)
    
    # Generate appropriate alt text
    filename = os.path.basename(src_value)
    if 'julien' in filename.lower():
        alt_text = "Julien Simon"
    elif 'logo' in filename.lower():
        alt_text = "Logo"
    elif 'icon' in filename.lower():
        alt_text = "Icon"
    else:
        alt_text = default_alt
    
    # Reconstruct with alt attribute
    return f'<img{before_src}src="{src_value}" alt="{alt_text}"{after_src}>'

def add_lang_to_arcee_posts():
    """Add lang attributes to Arcee posts."""
    print("🔧 Adding lang attributes to Arcee posts...")
    
    arcee_files = glob.glob("blog/arcee-posts/*/index.html")
    fixed_count = 0
    
    for file_path in arcee_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'lang=' not in content and '<html>' in content:
                content = content.replace('<html>', '<html lang="en">')
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += 1
                print(f"  ✅ Added lang attribute to {file_path}")
        
        except Exception as e:
            print(f"  ❌ Error processing {file_path}: {e}")
    
    print(f"Fixed lang attributes in {fixed_count} Arcee files")

def main():
    """Main function to apply simple fixes."""
    print("🚀 Starting Simple Issues Fix")
    print("=" * 50)
    
    add_missing_alt_to_main_pages()
    print()
    
    add_lang_to_arcee_posts()
    
    print("\n✅ Simple fixes completed!")

if __name__ == "__main__":
    main() 