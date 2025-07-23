#!/usr/bin/env python3
"""
Script to update Hugging Face emoji from 🤖 to 🤗 across all HTML files
"""

import os
import glob

def update_huggingface_emoji():
    """Update Hugging Face emoji in all HTML files"""
    
    # Find all HTML files in the current directory and subdirectories
    html_files = glob.glob("*.html") + glob.glob("blog/**/*.html")
    
    updated_count = 0
    
    for file_path in html_files:
        if os.path.isfile(file_path):
            try:
                # Read the file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if the file contains the old emoji
                if '🤖</span>Hugging Face' in content:
                    # Replace the old emoji with the new one
                    new_content = content.replace('🤖</span>Hugging Face', '🤗</span>Hugging Face')
                    
                    # Write the updated content back
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    print(f"✅ Updated: {file_path}")
                    updated_count += 1
                else:
                    print(f"⏭️  No change needed: {file_path}")
                    
            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")
    
    print(f"\n🎉 Update complete! Updated {updated_count} files.")

if __name__ == "__main__":
    update_huggingface_emoji() 