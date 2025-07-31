#!/usr/bin/env python3
"""
Script to fix AI/ML capitalization throughout the codebase.
Replaces "AI" with "AI" and "ML" with "ML".
"""

import glob
import re
import os

def fix_capitalization_in_file(file_path):
    """Fix AI/ML capitalization in a single file."""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Track if any changes were made
        original_content = content
        
        # Replace "AI" with "AI" (word boundary to avoid false positives)
        content = re.sub(r'\bAi\b', 'AI', content)
        
        # Replace "ML" with "ML" (word boundary to avoid false positives)
        content = re.sub(r'\bMl\b', 'ML', content)
        
        # Check if any changes were made
        if content != original_content:
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {e}")
        return False

def main():
    """Fix AI/ML capitalization in all files."""
    
    print("Fixing AI/ML capitalization throughout the codebase...")
    
    # Find all files that might contain text
    file_extensions = ['*.html', '*.md', '*.txt', '*.py', '*.js', '*.css', '*.xml']
    all_files = []
    
    for ext in file_extensions:
        all_files.extend(glob.glob(f"**/{ext}", recursive=True))
    
    # Remove duplicates and filter out webp files
    all_files = list(set([f for f in all_files if not f.endswith('.webp')]))
    
    print(f"Found {len(all_files)} files to process")
    
    fixed_count = 0
    skipped_count = 0
    
    for file_path in all_files:
        print(f"Processing: {file_path}")
        
        if fix_capitalization_in_file(file_path):
            print(f"  ✅ Fixed capitalization in {file_path}")
            fixed_count += 1
        else:
            print(f"  ⏭️  Skipped {file_path} (no changes needed)")
            skipped_count += 1
    
    print(f"\n✅ AI/ML capitalization fix completed!")
    print(f"📊 Summary:")
    print(f"   • Files processed: {len(all_files)}")
    print(f"   • Fixed: {fixed_count}")
    print(f"   • Skipped: {skipped_count}")
    print(f"\n🎯 Benefits:")
    print(f"   • Consistent AI/ML terminology")
    print(f"   • Professional presentation")
    print(f"   • Better readability")

if __name__ == "__main__":
    main() 