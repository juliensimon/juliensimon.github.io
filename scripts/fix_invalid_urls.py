#!/usr/bin/env python3
"""
Fix Invalid GitHub URLs

This script fixes invalid GitHub URLs by updating them to valid repositories
or correcting paths based on what actually exists.
"""

import re
import shutil
from pathlib import Path

# URL fixes mapping
URL_FIXES = {
    # Workshop repositories that exist in reinvent-workshops
    'https://github.com/juliensimon/aim307': 'https://github.com/juliensimon/reinvent-workshops/tree/main/aim307',
    'https://github.com/juliensimon/aim410': 'https://github.com/juliensimon/reinvent-workshops/tree/main/aim410',
    'https://github.com/juliensimon/aim410/blob/main/local_training.ipynb': 'https://github.com/juliensimon/reinvent-workshops/blob/main/aim410/local_training.ipynb',
    
    # Legacy repositories that don't exist - point to main repositories
    'https://github.com/juliensimon/Arduino/tree/master/LCD_Temp': 'https://github.com/juliensimon/arduino-projects',
    'https://github.com/juliensimon/DataStuff': 'https://github.com/juliensimon/data-science-projects',
    'https://github.com/juliensimon/DataStuff/blob/master/SparkExamples/SparkTest5.txt': 'https://github.com/juliensimon/data-science-projects/blob/main/spark-examples',
    'https://github.com/juliensimon/DataStuff/blob/master/src/org/julien/datastuff/MLSample.java': 'https://github.com/juliensimon/data-science-projects/blob/main/java-examples',
    'https://github.com/juliensimon/NodeApp/blob/master/v5-server.c': 'https://github.com/juliensimon/nodejs-projects',
    
    # Amazon SageMaker examples - point to AWS samples
    'https://github.com/juliensimon/amazon-sagemaker-examples/tree/master/step-functions-data-science-sdk/machine_learning_workflow_abalone': 'https://github.com/aws/amazon-sagemaker-examples/tree/main/sagemaker-pipelines/tabular/abalone_build_train_deploy',
    'https://github.com/juliensimon/amazon-sagemaker-examples/tree/master/step...': 'https://github.com/aws/amazon-sagemaker-examples/tree/main/sagemaker-pipelines',
    
    # AWS repository issues - fix paths
    'https://github.com/juliensimon/aws/tree/master/rekognition': 'https://github.com/juliensimon/aws/tree/master/AmazonAI/rekognition',
    
    # Amazon Studio Demos - fix episode paths
    'https://github.com/juliensimon/amazon-studio-demos/tree/main/sagemaker_fridays/s03e03': 'https://github.com/juliensimon/amazon-studio-demos/tree/main/sagemaker_fridays/season3/s03e03',
    'https://github.com/juliensimon/amazon-studio-demos/tree/main/sagemaker_fridays/s03e04': 'https://github.com/juliensimon/amazon-studio-demos/tree/main/sagemaker_fridays/season3/s03e04',
    'https://github.com/juliensimon/amazon-studio-demos/tree/main/sagemaker_fridays/s03e05': 'https://github.com/juliensimon/amazon-studio-demos/tree/main/sagemaker_fridays/season3/s03e05',
    
    # DL Notebooks issues - fix paths
    'https://github.com/juliensimon/dlnotebooks/blob/master/spark/spam': 'https://github.com/juliensimon/dlnotebooks/blob/master/spark/spark-examples',
    'https://github.com/juliensimon/dlnotebooks/blob/master/spark/ham': 'https://github.com/juliensimon/dlnotebooks/blob/master/spark/spark-examples',
    
    # AWSMLMap - keep as is since it was requested to be ignored
    'https://github.com/juliensimon/awsmlmap': 'https://github.com/juliensimon/awsmlmap',
}

def backup_file(file_path):
    """Create a backup of the file before modification."""
    backup_path = file_path.with_suffix(file_path.suffix + '.fix_backup')
    shutil.copy2(file_path, backup_path)
    return backup_path

def fix_urls_in_file(file_path):
    """Fix invalid GitHub URLs in a single file."""
    print(f"Processing: {file_path}")
    
    # Read file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Track changes
    changes_made = 0
    new_content = content
    
    # Apply URL fixes
    for old_url, new_url in URL_FIXES.items():
        if old_url in new_content:
            new_content = new_content.replace(old_url, new_url)
            changes_made += 1
            print(f"  Fixed: {old_url}")
            print(f"  To: {new_url}")
    
    # Write updated content if changes were made
    if changes_made > 0:
        backup_path = backup_file(file_path)
        print(f"  Backup created: {backup_path}")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  File updated: {file_path}")
        print(f"  Changes made: {changes_made}")
    else:
        print(f"  No fixes needed")
    
    return changes_made

def scan_html_files():
    """Scan for HTML files in youtube/ and blog/ directories."""
    html_files = []
    
    # Scan youtube/ directory (by year)
    youtube_dir = Path('youtube')
    if youtube_dir.exists():
        for year_dir in youtube_dir.iterdir():
            if year_dir.is_dir():
                for html_file in year_dir.glob('*.html'):
                    html_files.append(html_file)
    
    # Scan blog/ directory recursively
    blog_dir = Path('blog')
    if blog_dir.exists():
        for html_file in blog_dir.rglob('*.html'):
            html_files.append(html_file)
    
    return html_files

def main():
    """Main fix function."""
    print("🔧 Fixing Invalid GitHub URLs")
    print("=" * 50)
    
    # Scan for HTML files
    html_files = scan_html_files()
    print(f"Found {len(html_files)} HTML files to scan")
    print()
    
    # Process files
    total_fixes = 0
    files_modified = 0
    
    for file_path in html_files:
        fixes = fix_urls_in_file(file_path)
        if fixes > 0:
            files_modified += 1
            total_fixes += fixes
    
    # Print summary
    print()
    print("📊 Fix Summary")
    print("=" * 50)
    print(f"Files processed: {len(html_files)}")
    print(f"Files modified: {files_modified}")
    print(f"Total URL fixes: {total_fixes}")
    
    if total_fixes > 0:
        print("\n✅ URL fixes completed successfully!")
        print("Backup files have been created with .fix_backup extension")
    else:
        print("\n✅ No fixes needed - all URLs are already valid!")

if __name__ == "__main__":
    main() 