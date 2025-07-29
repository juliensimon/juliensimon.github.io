#!/usr/bin/env python3
"""
Fix Critical Issues Script
Addresses critical issues found in the website review without breaking content.
"""

import os
import re
import glob
from typing import List

def fix_missing_lang_attributes():
    """Add missing lang attributes to HTML files."""
    print("🔧 Fixing missing lang attributes...")
    
    html_files = glob.glob("**/*.html", recursive=True)
    fixed_count = 0
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if lang attribute is missing
            if 'lang=' not in content and '<html' in content:
                # Find and replace the html tag to add lang="en"
                html_pattern = r'<html([^>]*)>'
                
                def add_lang(match):
                    existing_attrs = match.group(1)
                    if 'lang=' not in existing_attrs:
                        if existing_attrs.strip():
                            return f'<html{existing_attrs} lang="en">'
                        else:
                            return '<html lang="en">'
                    return match.group(0)
                
                new_content = re.sub(html_pattern, add_lang, content, count=1)
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    fixed_count += 1
                    print(f"  ✅ Added lang attribute to {file_path}")
        
        except Exception as e:
            print(f"  ❌ Error processing {file_path}: {e}")
    
    print(f"Fixed lang attributes in {fixed_count} files")

def fix_missing_alt_attributes():
    """Add missing alt attributes to images."""
    print("🖼️  Fixing missing alt attributes...")
    
    html_files = glob.glob("**/*.html", recursive=True)
    fixed_count = 0
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find images without alt attributes
            img_pattern = r'<img([^>]*?)(?<!alt=")(?<!alt=\')(?<!alt=["\'][^"\']*["\'])>'
            
            def add_alt(match):
                img_attrs = match.group(1)
                
                # Check if alt attribute is already present
                if 'alt=' in img_attrs:
                    return match.group(0)
                
                # Generate appropriate alt text based on src or context
                alt_text = ""
                
                # Extract src for context
                src_match = re.search(r'src=["\']([^"\']*)["\']', img_attrs)
                if src_match:
                    src = src_match.group(1)
                    filename = os.path.basename(src)
                    
                    # Generate contextual alt text
                    if 'julien' in filename.lower():
                        alt_text = "Julien Simon"
                    elif 'logo' in filename.lower():
                        alt_text = "Logo"
                    elif 'icon' in filename.lower():
                        alt_text = "Icon"
                    elif any(word in filename.lower() for word in ['chart', 'graph', 'plot']):
                        alt_text = "Chart or graph"
                    elif any(word in filename.lower() for word in ['diagram', 'architecture']):
                        alt_text = "Technical diagram"
                    elif any(word in filename.lower() for word in ['screenshot', 'screen']):
                        alt_text = "Screenshot"
                    elif 'image' in filename.lower():
                        alt_text = "Image"
                    else:
                        # Use filename without extension as alt text
                        alt_text = os.path.splitext(filename)[0].replace('-', ' ').replace('_', ' ').title()
                
                if not alt_text:
                    alt_text = "Image"
                
                # Add alt attribute
                if img_attrs.strip():
                    return f'<img{img_attrs} alt="{alt_text}">'
                else:
                    return f'<img alt="{alt_text}">'
            
            # Apply the fix
            new_content = re.sub(img_pattern, add_alt, content)
            
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                fixed_count += 1
                print(f"  ✅ Added alt attributes to images in {file_path}")
        
        except Exception as e:
            print(f"  ❌ Error processing {file_path}: {e}")
    
    print(f"Fixed alt attributes in {fixed_count} files")

def fix_meta_description_lengths():
    """Fix meta descriptions that are too long."""
    print("📝 Fixing meta description lengths...")
    
    main_files = ['index.html', 'experience.html', 'publications.html']
    fixed_count = 0
    
    for file_path in main_files:
        if not os.path.exists(file_path):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find meta description
            desc_pattern = r'<meta name="description" content="([^"]*)"[^>]*>'
            desc_match = re.search(desc_pattern, content)
            
            if desc_match:
                current_desc = desc_match.group(1)
                if len(current_desc) > 160:
                    # Truncate to 150 characters and add ellipsis if needed
                    new_desc = current_desc[:150].rsplit(' ', 1)[0]
                    if len(new_desc) < len(current_desc):
                        new_desc += "..."
                    
                    # Replace in content
                    new_content = content.replace(
                        f'content="{current_desc}"',
                        f'content="{new_desc}"'
                    )
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    fixed_count += 1
                    print(f"  ✅ Fixed meta description length in {file_path}")
                    print(f"     Old length: {len(current_desc)} chars")
                    print(f"     New length: {len(new_desc)} chars")
        
        except Exception as e:
            print(f"  ❌ Error processing {file_path}: {e}")
    
    print(f"Fixed meta descriptions in {fixed_count} files")

def add_missing_canonical_urls():
    """Add missing canonical URLs to main pages."""
    print("🔗 Adding missing canonical URLs...")
    
    main_files = {
        'index.html': 'https://julien.org/',
        'experience.html': 'https://julien.org/experience.html',
        'speaking.html': 'https://julien.org/speaking.html',
        'publications.html': 'https://julien.org/publications.html',
        'code.html': 'https://julien.org/code.html',
        'youtube.html': 'https://julien.org/youtube.html',
        'books.html': 'https://julien.org/books.html',
        'computers.html': 'https://julien.org/computers.html',
        'podcasts.html': 'https://julien.org/podcasts.html'
    }
    
    fixed_count = 0
    
    for file_path, canonical_url in main_files.items():
        if not os.path.exists(file_path):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if canonical URL is missing
            if 'rel="canonical"' not in content:
                # Find the head section and add canonical URL
                head_pattern = r'(<head[^>]*>)'
                
                def add_canonical(match):
                    return f'{match.group(1)}\n  <link rel="canonical" href="{canonical_url}"/>'
                
                new_content = re.sub(head_pattern, add_canonical, content, count=1)
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    fixed_count += 1
                    print(f"  ✅ Added canonical URL to {file_path}")
        
        except Exception as e:
            print(f"  ❌ Error processing {file_path}: {e}")
    
    print(f"Added canonical URLs to {fixed_count} files")

def validate_fixes():
    """Validate that fixes were applied correctly."""
    print("✅ Validating fixes...")
    
    # Check a sample of files for lang attributes
    sample_files = ['index.html', 'blog/arcee-posts/2025-07-18_arcee-ai-small-language-models-excel-across-yuppai-leaderboards/index.html']
    
    for file_path in sample_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check lang attribute
                if 'lang="en"' in content:
                    print(f"  ✅ Lang attribute validated in {file_path}")
                else:
                    print(f"  ⚠️  Lang attribute missing in {file_path}")
                
                # Check for images without alt
                img_no_alt = re.findall(r'<img[^>]*(?<!alt=")(?<!alt=\')>', content)
                if not img_no_alt:
                    print(f"  ✅ All images have alt attributes in {file_path}")
                else:
                    print(f"  ⚠️  Found {len(img_no_alt)} images without alt in {file_path}")
            
            except Exception as e:
                print(f"  ❌ Error validating {file_path}: {e}")

def main():
    """Main function to fix critical issues."""
    print("🚀 Starting Critical Issues Fix")
    print("=" * 50)
    
    # Apply fixes
    fix_missing_lang_attributes()
    print()
    
    fix_missing_alt_attributes()
    print()
    
    fix_meta_description_lengths()
    print()
    
    add_missing_canonical_urls()
    print()
    
    # Validate fixes
    validate_fixes()
    
    print("\n🎉 Critical issues fix completed!")
    print("   Re-run the website review to see improvements.")

if __name__ == "__main__":
    main() 