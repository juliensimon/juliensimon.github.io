#!/usr/bin/env python3
"""
Script to apply modern styling to legacy blog posts.
This script will:
1. Find all legacy blog posts
2. Replace the old basic CSS with modern styling
3. Add container divs for better layout
4. Apply different gradient backgrounds for visual variety
"""

import os
import re
import glob
from pathlib import Path

def get_gradient_theme(index):
    """Get a different gradient theme based on index for visual variety."""
    gradients = [
        "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",  # Purple
        "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",  # Pink
        "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",  # Blue
        "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",  # Green
        "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",  # Orange
        "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)",  # Soft
        "linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)",  # Rose
        "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)",  # Warm
    ]
    return gradients[index % len(gradients)]

def apply_modern_styling(file_path, theme_index):
    """Apply modern styling to a single blog post file."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get gradient theme
    gradient = get_gradient_theme(theme_index)
    
    # Replace the old CSS with modern styling
    old_css_pattern = r'<style>\s*body\s*\{[^}]*\}\s*img\s*\{[^}]*\}\s*a\[style\*="float"\]\s*\{[^}]*\}\s*\.separator\s*\{[^}]*\}\s*code\s*\{[^}]*\}\s*pre\s*\{[^}]*\}\s*h1\s*\{[^}]*\}\s*\.date\s*\{[^}]*\}\s*\.content\s*\{[^}]*\}\s*a\s*\{[^}]*\}\s*a:hover\s*\{[^}]*\}\s*</style>'
    
    new_css = f'''    <link rel="stylesheet" href="../../../css/modern-blog-styles.css">
    <style>
        /* Additional custom styles for this specific post */
        body {{
            background: {gradient};
            min-height: 100vh;
        }}
        
        .container {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
        }}
    </style>'''
    
    # Replace the CSS
    content = re.sub(old_css_pattern, new_css, content, flags=re.DOTALL)
    
    # Add container div around content
    # Find the body tag and add container div
    body_pattern = r'(<body>)\s*(<h1>)'
    container_replacement = r'\1\n    <div class="container">\n        \2'
    content = re.sub(body_pattern, container_replacement, content)
    
    # Close the container div before the closing body tag
    # Find the content div and close container after it
    content_div_pattern = r'(</div>)\s*(<hr/>)'
    container_close_replacement = r'\1\n        \2'
    content = re.sub(content_div_pattern, container_close_replacement, content)
    
    # Add proper closing div before body
    body_close_pattern = r'(<!--.*?-->)\s*(</body>)'
    final_close_replacement = r'\1\n    </div>\n    \2'
    content = re.sub(body_close_pattern, final_close_replacement, content)
    
    # Write the updated content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated: {file_path}")

def main():
    """Main function to process all legacy blog posts."""
    
    # Find all legacy blog posts
    legacy_dir = Path("blog/legacy-posts-and-images")
    
    if not legacy_dir.exists():
        print("❌ Legacy posts directory not found!")
        return
    
    # Find all HTML files in subdirectories
    html_files = []
    for year_dir in legacy_dir.iterdir():
        if year_dir.is_dir():
            html_files.extend(year_dir.glob("*.html"))
    
    print(f"📁 Found {len(html_files)} legacy blog posts to update")
    
    # Process each file
    for i, file_path in enumerate(html_files):
        try:
            apply_modern_styling(file_path, i)
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    print(f"\n🎉 Successfully updated {len(html_files)} blog posts with modern styling!")
    print("✨ The posts now feature:")
    print("   - Modern typography and spacing")
    print("   - Beautiful gradient backgrounds")
    print("   - Responsive design")
    print("   - Enhanced readability")
    print("   - Better code block styling")
    print("   - Improved image handling")

if __name__ == "__main__":
    main() 