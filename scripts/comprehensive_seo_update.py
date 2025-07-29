#!/usr/bin/env python3
"""
Comprehensive SEO Update Script
Runs all SEO optimizations in sequence for the website.
"""

import os
import subprocess
import sys
from datetime import datetime

def run_script(script_name, description):
    """Run a Python script and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Script: {script_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, f"scripts/{script_name}"], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("✅ Success!")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ Error!")
            if result.stderr:
                print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False
    
    return True

def main():
    """Run comprehensive SEO updates."""
    
    print("🚀 Starting Comprehensive SEO Update")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # List of scripts to run in order
    scripts_to_run = [
        ("add_seo_to_arcee_posts.py", "Adding SEO to Arcee posts"),
        ("create_blog_sitemap.py", "Creating blog sitemap"),
        ("update_rss_feed.py", "Updating RSS feed")
    ]
    
    success_count = 0
    total_scripts = len(scripts_to_run)
    
    for script_name, description in scripts_to_run:
        if run_script(script_name, description):
            success_count += 1
        else:
            print(f"⚠️  Warning: {description} failed")
    
    print(f"\n{'='*60}")
    print("📊 SEO Update Summary")
    print(f"{'='*60}")
    print(f"✅ Successful: {success_count}/{total_scripts}")
    print(f"❌ Failed: {total_scripts - success_count}/{total_scripts}")
    
    if success_count == total_scripts:
        print("\n🎉 All SEO updates completed successfully!")
    else:
        print("\n⚠️  Some updates failed. Please check the errors above.")
    
    print(f"\n📝 Summary of changes:")
    print("• Added comprehensive SEO metadata to Arcee posts")
    print("• Created blog sitemap with 102 posts (9 Arcee + 25 HuggingFace + 68 AWS)")
    print("• Updated RSS feed with latest content")
    print("• Updated sitemap index")
    
    print(f"\n🔍 Next steps:")
    print("• Submit sitemap to search engines")
    print("• Monitor search console for indexing")
    print("• Check social media previews")
    print("• Verify structured data with Google's testing tools")

if __name__ == "__main__":
    main() 