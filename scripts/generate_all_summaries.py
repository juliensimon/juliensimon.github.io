#!/usr/bin/env python3
"""
Script to generate summaries for all blog posts and video transcripts using AFM-4.5B model.
This version processes all files automatically without user input.
"""

import os
import sys
sys.path.append('scripts')
from generate_content_summaries import ContentSummarizer

def main():
    """Main function to run the summarization process on all files."""
    print("Initializing Content Summarizer...")
    
    summarizer = ContentSummarizer()
    
    # Load model
    print("\n" + "="*50)
    print("LOADING MODEL")
    print("="*50)
    summarizer.load_model()
    
    # Process all blog posts
    print("\n" + "="*50)
    print("PROCESSING ALL BLOG POSTS")
    print("="*50)
    blog_results = summarizer.process_blog_posts()
    
    # Process all video transcripts
    print("\n" + "="*50)
    print("PROCESSING ALL VIDEO TRANSCRIPTS")
    print("="*50)
    video_results = summarizer.process_video_transcripts()
    
    # Combine all results
    all_results = {**blog_results, **video_results}
    
    # Save results
    summarizer.save_summaries(all_results)
    
    print(f"\nProcessing complete!")
    print(f"Generated {len(blog_results)} blog post summaries and tags")
    print(f"Generated {len(video_results)} video transcript summaries and tags")
    print(f"Total processed: {len(all_results)}")
    
    # Print summary statistics
    print(f"\nSummary statistics:")
    print(f"- Blog posts processed: {len(blog_results)}")
    print(f"- Video transcripts processed: {len(video_results)}")
    print(f"- Total files processed: {len(all_results)}")
    print(f"- Results saved to: content_summaries.json")

if __name__ == "__main__":
    main() 