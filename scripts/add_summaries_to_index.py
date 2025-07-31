#!/usr/bin/env python3
"""
Generic script to add summaries to index pages.
Can process any index page and add AI-generated summaries to video/blog entries.
"""

import os
import re
import glob
import json
import sys
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

class IndexSummarizer:
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
    
    def generate_summary(self, content: str, content_type: str = "video") -> str:
        """Generate a 2-sentence summary using the AFM-4.5B model."""
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
    

    
    def parse_index_page(self, index_file: str) -> List[Dict]:
        """Parse an index page to extract video/blog entries."""
        entries = []
        
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all video-item divs
            video_items = re.findall(r'<div class="video-item">(.*?)</div>', content, re.DOTALL)
            
            for item in video_items:
                # Extract title and link
                title_match = re.search(r'<a class="video-title" href="([^"]+)">([^<]+)</a>', item)
                if title_match:
                    link = title_match.group(1)
                    title = title_match.group(2)
                    
                    # Extract date
                    date_match = re.search(r'<div class="video-date">([^<]+)</div>', item)
                    date = date_match.group(1) if date_match else ""
                    
                    # Extract existing tags
                    tags_match = re.search(r'<div class="video-tags">(.*?)</div>', item, re.DOTALL)
                    existing_tags = []
                    if tags_match:
                        tag_matches = re.findall(r'<span class="video-tag">([^<]+)</span>', tags_match.group(1))
                        existing_tags = tag_matches
                    
                    entries.append({
                        'title': title,
                        'link': link,
                        'date': date,
                        'existing_tags': existing_tags,
                        'full_html': item
                    })
            
            return entries
            
        except Exception as e:
            print(f"Error parsing index file {index_file}: {e}")
            return []
    
    def get_video_file_path(self, link: str, index_dir: str) -> str:
        """Get the full path to the video file based on the link."""
        # Remove .html extension if present
        if link.endswith('.html'):
            link = link[:-5]
        
        # Construct the full path
        video_file = os.path.join(index_dir, link + '.html')
        return video_file
    
    def process_index_page(self, index_file: str) -> Dict[str, Dict]:
        """Process an index page and generate summaries for all entries."""
        results = {}
        
        print(f"Processing index page: {index_file}")
        
        # Parse the index page
        entries = self.parse_index_page(index_file)
        print(f"Found {len(entries)} entries in index page")
        
        index_dir = os.path.dirname(index_file)
        
        for i, entry in enumerate(entries):
            print(f"Processing entry {i+1}/{len(entries)}: {entry['title']}")
            
            # Get the video file path
            video_file = self.get_video_file_path(entry['link'], index_dir)
            
            if os.path.exists(video_file):
                # Extract transcript content
                content = self.extract_video_transcript(video_file)
                if content:
                    # Generate summary only
                    summary = self.generate_summary(content, "video")
                    
                    results[entry['link']] = {
                        'title': entry['title'],
                        'date': entry['date'],
                        'summary': summary,
                        'existing_tags': entry['existing_tags']
                    }
                    
                    print(f"  Summary: {summary}")
                    
                    # Update the index page after each entry
                    self.update_and_save_index(index_file, results)
                else:
                    print(f"  No transcript found for {video_file}")
            else:
                print(f"  Video file not found: {video_file}")
            
            # Small delay to avoid overwhelming the model
            time.sleep(0.5)
        
        return results
    
    def update_index_page(self, index_file: str, summaries: Dict[str, Dict]) -> str:
        """Update the index page with summaries."""
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Process each video item
            for link, data in summaries.items():
                # Find the video item div
                pattern = rf'<div class="video-item">(.*?<a class="video-title" href="{re.escape(link)}".*?)</div>'
                match = re.search(pattern, content, re.DOTALL)
                
                if match:
                    video_item = match.group(1)
                    
                    # Add summary after the date
                    date_pattern = r'(<div class="video-date">[^<]+</div>)'
                    date_match = re.search(date_pattern, video_item)
                    
                    if date_match:
                        date_div = date_match.group(1)
                        summary_div = f'\n<div class="video-summary">{data["summary"]}</div>'
                        
                        # Replace the video item with the updated one
                        new_video_item = video_item.replace(date_div, date_div + summary_div)
                        new_video_item = f'<div class="video-item">{new_video_item}</div>'
                        
                        # Update the content
                        content = content.replace(match.group(0), new_video_item)
            
            return content
            
        except Exception as e:
            print(f"Error updating index file {index_file}: {e}")
            return None
    
    def update_and_save_index(self, index_file: str, summaries: Dict[str, Dict]):
        """Update the index page with summaries and save immediately."""
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Process each video item
            for link, data in summaries.items():
                # Find the video item div
                pattern = rf'<div class="video-item">(.*?<a class="video-title" href="{re.escape(link)}".*?)</div>'
                match = re.search(pattern, content, re.DOTALL)
                
                if match:
                    video_item = match.group(1)
                    
                    # Check if summary already exists
                    if '<div class="video-summary">' not in video_item:
                        # Add summary after the date
                        date_pattern = r'(<div class="video-date">[^<]+</div>)'
                        date_match = re.search(date_pattern, video_item)
                        
                        if date_match:
                            date_div = date_match.group(1)
                            summary_div = f'\n<div class="video-summary">{data["summary"]}</div>'
                            
                            # Replace the video item with the updated one
                            new_video_item = video_item.replace(date_div, date_div + summary_div)
                            new_video_item = f'<div class="video-item">{new_video_item}</div>'
                            
                            # Update the content
                            content = content.replace(match.group(0), new_video_item)
            
            # Save the updated content
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Index page updated and saved")
            
        except Exception as e:
            print(f"Error updating index file {index_file}: {e}")
    
    def save_updated_index(self, index_file: str, updated_content: str):
        """Save the updated index content."""
        try:
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Updated index page saved: {index_file}")
        except Exception as e:
            print(f"Error saving updated index file: {e}")

def main():
    """Main function to process an index page."""
    if len(sys.argv) != 2:
        print("Usage: python add_summaries_to_index.py <index_file>")
        print("Example: python add_summaries_to_index.py youtube/2024/index.html")
        return
    
    index_file = sys.argv[1]
    
    if not os.path.exists(index_file):
        print(f"Index file not found: {index_file}")
        return
    
    print(f"Processing index file: {index_file}")
    
    # Initialize summarizer
    summarizer = IndexSummarizer()
    
    # Load model
    print("\n" + "="*50)
    print("LOADING MODEL")
    print("="*50)
    summarizer.load_model()
    
    # Process the index page
    print("\n" + "="*50)
    print("PROCESSING INDEX PAGE")
    print("="*50)
    summaries = summarizer.process_index_page(index_file)
    
    print(f"\nProcessing complete!")
    print(f"Generated summaries for {len(summaries)} entries")
    print(f"Updated index page: {index_file}")

if __name__ == "__main__":
    main() 