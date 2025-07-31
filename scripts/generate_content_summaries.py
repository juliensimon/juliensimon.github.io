#!/usr/bin/env python3
"""
Script to generate summaries for blog posts and video transcripts using AFM-4.5B model.
Downloads the model from Hugging Face and generates short summaries for index pages.
"""

import os
import re
import glob
import json
import requests
import tempfile
from pathlib import Path
from typing import List, Dict, Optional
import time

# Try to import llama-cpp-python, install if not available
try:
    from llama_cpp import Llama
except ImportError:
    print("Installing llama-cpp-python...")
    import subprocess
    subprocess.check_call(["pip", "install", "llama-cpp-python"])
    from llama_cpp import Llama

class ContentSummarizer:
    def __init__(self, model_url: str = "https://huggingface.co/arcee-ai/AFM-4.5B-GGUF/resolve/main/AFM-4.5B-Q8_0.gguf?download=true"):
        self.model_url = model_url
        self.model_path = None
        self.llm = None
        
    def get_model_path(self) -> str:
        """Get the path to the AFM-4.5B model."""
        # Check if model exists in local models directory
        local_model_path = "/Users/julien/models/AFM-4.5B-Q8_0.gguf"
        if os.path.exists(local_model_path):
            print(f"Using local model at {local_model_path}")
            return local_model_path
        
        # Fallback to downloading if not found locally
        model_dir = Path("models")
        model_dir.mkdir(exist_ok=True)
        
        model_filename = "AFM-4.5B-Q8_0.gguf"
        model_path = model_dir / model_filename
        
        if model_path.exists():
            print(f"Model already exists at {model_path}")
            return str(model_path)
        
        print(f"Model not found locally. Please download it to {local_model_path}")
        print("or run the script from a directory with the model.")
        raise FileNotFoundError(f"Model not found at {local_model_path}")
    
    def load_model(self):
        """Load the AFM-4.5B model."""
        if self.llm is None:
            model_path = self.get_model_path()
            print("Loading model...")
            self.llm = Llama(
                model_path=model_path,
                n_ctx=2048,
                n_threads=4,
                verbose=False
            )
            print("Model loaded successfully!")
    
    def extract_text_from_html(self, html_content: str) -> str:
        """Extract clean text content from HTML."""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', html_content)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common HTML entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        
        return text.strip()
    
    def extract_blog_content(self, file_path: str) -> Optional[str]:
        """Extract content from blog post HTML."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract text between <body> and </body>
            body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
            if not body_match:
                return None
            
            body_content = body_match.group(1)
            
            # Remove navigation, headers, footers, etc.
            # Remove script and style tags
            body_content = re.sub(r'<script[^>]*>.*?</script>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
            body_content = re.sub(r'<style[^>]*>.*?</style>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
            
            # Extract main content (look for paragraphs, headings, etc.)
            text_content = self.extract_text_from_html(body_content)
            
            # Limit to first 2000 characters to avoid token limits
            return text_content[:2000] if text_content else None
            
        except Exception as e:
            print(f"Error extracting content from {file_path}: {e}")
            return None
    
    def extract_video_transcript(self, file_path: str) -> Optional[str]:
        """Extract transcript content from video HTML."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for transcript div
            transcript_match = re.search(r'<div class="transcript">(.*?)</div>', content, re.DOTALL | re.IGNORECASE)
            if not transcript_match:
                return None
            
            transcript_content = transcript_match.group(1)
            text_content = self.extract_text_from_html(transcript_content)
            
            # Limit to first 2000 characters
            return text_content[:2000] if text_content else None
            
        except Exception as e:
            print(f"Error extracting transcript from {file_path}: {e}")
            return None
    
    def generate_summary(self, content: str, content_type: str = "blog post") -> str:
        """Generate a one-liner summary using the AFM-4.5B model."""
        if not content or len(content.strip()) < 50:
            return "Content too short to summarize."
        
        prompt = f"""Write a 2-sentence summary of this {content_type} that explains what it's about and what problem it's solving:

{content}

Summary:"""
        
        try:
            response = self.llm(
                prompt,
                max_tokens=100,
                temperature=0.3,
                stop=["\n", "###", "---"]
            )
            
            summary = response['choices'][0]['text'].strip()
            
            # Clean up the summary
            summary = re.sub(r'^Summary:\s*', '', summary)
            summary = summary.strip()
            
            # Ensure it's 2 sentences maximum
            sentences = summary.split('.')
            if len(sentences) > 3:  # More than 2 sentences
                summary = '.'.join(sentences[:2]) + '.'
            
            return summary if summary else "Unable to generate summary."
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Error generating summary."
    
    def generate_tags(self, content: str, content_type: str = "blog post") -> List[str]:
        """Generate relevant tags using the AFM-4.5B model."""
        if not content or len(content.strip()) < 50:
            return []
        
        prompt = f"""Extract 3-5 relevant tags from this {content_type}. Return only the tags, separated by commas, no explanations:

{content}

Tags:"""
        
        try:
            response = self.llm(
                prompt,
                max_tokens=50,
                temperature=0.2,
                stop=["\n", "###", "---"]
            )
            
            tags_text = response['choices'][0]['text'].strip()
            
            # Clean up the tags
            tags_text = re.sub(r'^Tags:\s*', '', tags_text)
            tags = [tag.strip() for tag in tags_text.split(',') if tag.strip()]
            
            # Clean up tag formatting
            cleaned_tags = []
            for tag in tags:
                # Remove quotes and extra punctuation
                tag = re.sub(r'["\']', '', tag)
                tag = tag.strip()
                if tag and len(tag) > 1:
                    cleaned_tags.append(tag)
            
            return cleaned_tags[:5]  # Limit to 5 tags
            
        except Exception as e:
            print(f"Error generating tags: {e}")
            return []
    
    def process_blog_posts(self, blog_dir: str = "blog") -> Dict[str, Dict[str, any]]:
        """Process all blog posts and generate summaries and tags."""
        results = {}
        
        # Find all blog post directories
        blog_patterns = [
            "blog/aws-posts-and-images/*/index.html",
            "blog/arcee-posts/*/index.html",
            "blog/aws-medium-posts-and-images/*/*/index.html"
        ]
        
        for pattern in blog_patterns:
            files = glob.glob(pattern)
            print(f"Found {len(files)} files matching {pattern}")
            
            for file_path in files:
                print(f"Processing {file_path}...")
                
                content = self.extract_blog_content(file_path)
                if content:
                    summary = self.generate_summary(content, "blog post")
                    tags = self.generate_tags(content, "blog post")
                    results[file_path] = {
                        "summary": summary,
                        "tags": tags
                    }
                    print(f"Generated summary: {summary}")
                    print(f"Generated tags: {', '.join(tags)}")
                else:
                    print(f"No content extracted from {file_path}")
                
                # Small delay to avoid overwhelming the model
                time.sleep(0.5)
        
        return results
    
    def process_video_transcripts(self, youtube_dir: str = "youtube") -> Dict[str, Dict[str, any]]:
        """Process all video transcripts and generate summaries and tags."""
        results = {}
        
        # Find all video transcript files
        transcript_pattern = "youtube/*/*.html"
        files = glob.glob(transcript_pattern)
        print(f"Found {len(files)} video transcript files")
        
        for file_path in files:
            print(f"Processing {file_path}...")
            
            content = self.extract_video_transcript(file_path)
            if content:
                summary = self.generate_summary(content, "video transcript")
                tags = self.generate_tags(content, "video transcript")
                results[file_path] = {
                    "summary": summary,
                    "tags": tags
                }
                print(f"Generated summary: {summary}")
                print(f"Generated tags: {', '.join(tags)}")
            else:
                print(f"No transcript extracted from {file_path}")
            
            # Small delay to avoid overwhelming the model
            time.sleep(0.5)
        
        return results
    
    def save_summaries(self, results: Dict[str, Dict[str, any]], output_file: str = "content_summaries.json"):
        """Save summaries and tags to a JSON file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Summaries and tags saved to {output_file}")
    
    def test_on_samples(self, num_samples: int = 3):
        """Test the summarization on a few sample files."""
        print("Testing summarization on sample files...")
        
        # Test blog posts
        blog_files = glob.glob("blog/aws-posts-and-images/*/index.html")[:2]
        for file_path in blog_files:
            print(f"\n--- Testing blog post: {file_path} ---")
            content = self.extract_blog_content(file_path)
            if content:
                summary = self.generate_summary(content, "blog post")
                tags = self.generate_tags(content, "blog post")
                print(f"Content preview: {content[:200]}...")
                print(f"Summary: {summary}")
                print(f"Tags: {', '.join(tags)}")
            else:
                print("No content extracted")
        
        # Test video transcripts
        video_files = glob.glob("youtube/2025/*.html")[:1]
        for file_path in video_files:
            print(f"\n--- Testing video transcript: {file_path} ---")
            content = self.extract_video_transcript(file_path)
            if content:
                summary = self.generate_summary(content, "video transcript")
                tags = self.generate_tags(content, "video transcript")
                print(f"Content preview: {content[:200]}...")
                print(f"Summary: {summary}")
                print(f"Tags: {', '.join(tags)}")
            else:
                print("No transcript extracted")

def main():
    """Main function to run the summarization process."""
    print("Initializing Content Summarizer...")
    
    summarizer = ContentSummarizer()
    
    # Test on samples first
    print("\n" + "="*50)
    print("TESTING ON SAMPLE FILES")
    print("="*50)
    summarizer.load_model()
    summarizer.test_on_samples()
    
    # Ask user if they want to proceed with full processing
    response = input("\nDo you want to process all files? (y/n): ")
    if response.lower() != 'y':
        print("Exiting. Summaries saved for sample files only.")
        return
    
    print("\n" + "="*50)
    print("PROCESSING ALL BLOG POSTS")
    print("="*50)
    blog_results = summarizer.process_blog_posts()
    
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

if __name__ == "__main__":
    main() 