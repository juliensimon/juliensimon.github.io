#!/usr/bin/env python3
"""
Add the 3 most important video tags for each year on the YouTube overview page.

This script adds representative tags to each year card to show the key themes
covered in that year's videos.
"""

import re
import shutil
from pathlib import Path

def add_year_tags_to_youtube_page():
    """Add year tags to the YouTube overview page."""
    file_path = "youtube.html"
    
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Define the most important tags for each year based on content analysis
        year_tags = {
            "2025": ["Small Language Models", "Arcee AI", "Model Routing"],
            "2024": ["AWS SageMaker", "Arcee Models", "Open Source AI"],
            "2023": ["AWS Trainium", "Intel OpenVINO", "Stable Diffusion"],
            "2022": ["Transformers", "Hugging Face", "AWS Inferentia"],
            "2021": ["Machine Learning", "AWS", "Deep Learning"],
            "2020": ["AWS SageMaker", "Machine Learning", "Cloud Computing"],
            "2019": ["AWS SageMaker", "Machine Learning", "Deep Learning"]
        }
        
        # Pattern to match each year card and add tags
        for year, tags in year_tags.items():
            # Pattern to find the year card
            year_pattern = rf'<div class="year-card">\s*<div class="year-number">{year}</div>\s*<div class="year-stats">\s*<span class="video-count">(\d+) videos</span>\s*</div>'
            
            # Replacement with tags added
            replacement = f'''<div class="year-card">
<div class="year-number">{year}</div>
<div class="year-stats">
<span class="video-count">\\1 videos</span>
<div class="year-tags">
<span class="year-tag">{tags[0]}</span>
<span class="year-tag">{tags[1]}</span>
<span class="year-tag">{tags[2]}</span>
</div>
</div>'''
            
            # Apply the replacement
            content = re.sub(year_pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
        
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Successfully added year tags to {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Main function to add year tags."""
    print("🎯 Adding year tags to YouTube overview page...")
    
    success = add_year_tags_to_youtube_page()
    
    if success:
        print("🎉 Year tags added successfully!")
        print("\n📊 Tags added by year:")
        year_tags = {
            "2025": ["Small Language Models", "Arcee AI", "Model Routing"],
            "2024": ["AWS SageMaker", "Arcee Models", "Open Source AI"],
            "2023": ["AWS Trainium", "Intel OpenVINO", "Stable Diffusion"],
            "2022": ["Transformers", "Hugging Face", "AWS Inferentia"],
            "2021": ["Machine Learning", "AWS", "Deep Learning"],
            "2020": ["AWS SageMaker", "Machine Learning", "Cloud Computing"],
            "2019": ["AWS SageMaker", "Machine Learning", "Deep Learning"]
        }
        
        for year, tags in year_tags.items():
            print(f"  {year}: {', '.join(tags)}")
    else:
        print("❌ Failed to add year tags")

if __name__ == "__main__":
    main() 