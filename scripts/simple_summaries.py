#!/usr/bin/env python3
"""
Simple script to add summaries to index pages.
Processes one item at a time: generate summary, save page, move to next.
"""

import os
import re
import sys
from pathlib import Path

# Try to import llama-cpp-python
try:
    from llama_cpp import Llama
except ImportError:
    print("Installing llama-cpp-python...")
    import subprocess
    subprocess.check_call(["pip", "install", "llama-cpp-python"])
    from llama_cpp import Llama

def load_model():
    """Load the AFM-4.5B model."""
    model_path = "/Users/julien/models/AFM-4.5B-Q8_0.gguf"
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}")
        return None
    
    print("Loading model...")
    llm = Llama(
        model_path=model_path,
        n_ctx=2048,
        n_threads=4,
        verbose=False
    )
    print("Model loaded successfully!")
    return llm

def extract_transcript(file_path):
    """Extract transcript from video file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for transcript div
        transcript_match = re.search(r'<div class="transcript">(.*?)</div>', content, re.DOTALL | re.IGNORECASE)
        if not transcript_match:
            return None
        
        transcript_content = transcript_match.group(1)
        
        # Clean up HTML
        text = re.sub(r'<[^>]+>', ' ', transcript_content)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text[:2000] if text else None
        
    except Exception as e:
        print(f"Error extracting transcript: {e}")
        return None

def generate_summary(llm, content):
    """Generate a 2-sentence summary."""
    if not content or len(content.strip()) < 50:
        return "Content too short to summarize."
    
    prompt = f"""Write a 2-sentence summary of this video that explains what it's about and what problem it's solving:

{content}

Summary:"""
    
    try:
        response = llm(
            prompt,
            max_tokens=100,
            temperature=0.3,
            stop=["\n", "###", "---"]
        )
        
        summary = response['choices'][0]['text'].strip()
        summary = re.sub(r'^Summary:\s*', '', summary)
        summary = summary.strip()
        
        # Ensure it's 2 sentences maximum
        sentences = summary.split('.')
        if len(sentences) > 3:
            summary = '.'.join(sentences[:2]) + '.'
        
        return summary if summary else "Unable to generate summary."
        
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Error generating summary."

def parse_index_page(index_file):
    """Parse index page to get video entries."""
    try:
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all video-item divs
        video_items = re.findall(r'<div class="video-item">(.*?)</div>', content, re.DOTALL)
        
        entries = []
        for item in video_items:
            # Extract title and link
            title_match = re.search(r'<a class="video-title" href="([^"]+)">([^<]+)</a>', item)
            if title_match:
                link = title_match.group(1)
                title = title_match.group(2)
                
                # Extract date
                date_match = re.search(r'<div class="video-date">([^<]+)</div>', item)
                date = date_match.group(1) if date_match else ""
                
                entries.append({
                    'title': title,
                    'link': link,
                    'date': date,
                    'full_html': item
                })
        
        return entries, content
        
    except Exception as e:
        print(f"Error parsing index file: {e}")
        return [], None

def update_single_entry(content, link, summary):
    """Update a single video entry with summary."""
    # Find the video item div - make it more specific
    pattern = rf'<div class="video-item">(.*?<a class="video-title" href="{re.escape(link)}"[^>]*>.*?</a>.*?)</div>'
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
                summary_div = f'\n<div class="video-summary">{summary}</div>'
                
                # Replace the video item with the updated one
                new_video_item = video_item.replace(date_div, date_div + summary_div)
                new_video_item = f'<div class="video-item">{new_video_item}</div>'
                
                # Update the content - replace the specific match
                content = content.replace(match.group(0), new_video_item)
                return content
    
    return content

def save_index_page(index_file, content):
    """Save the updated index content."""
    try:
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  ✓ Page saved")
    except Exception as e:
        print(f"Error saving file: {e}")

def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python simple_summaries.py <index_file>")
        return
    
    index_file = sys.argv[1]
    
    if not os.path.exists(index_file):
        print(f"Index file not found: {index_file}")
        return
    
    print(f"Processing: {index_file}")
    
    # Load model
    llm = load_model()
    if not llm:
        return
    
    # Parse index page
    entries, content = parse_index_page(index_file)
    print(f"Found {len(entries)} entries")
    
    if not content:
        print("Failed to parse index page")
        return
    
    index_dir = os.path.dirname(index_file)
    
    # Process each entry one by one
    for i, entry in enumerate(entries):
        print(f"\nProcessing {i+1}/{len(entries)}: {entry['title']}")
        
        # Get video file path
        video_file = os.path.join(index_dir, entry['link'])
        
        if os.path.exists(video_file):
            # Extract transcript
            transcript = extract_transcript(video_file)
            
            if transcript:
                # Generate summary
                summary = generate_summary(llm, transcript)
                print(f"  Summary: {summary}")
                
                # Update content
                content = update_single_entry(content, entry['link'], summary)
                
                # Save immediately
                save_index_page(index_file, content)
            else:
                print(f"  No transcript found")
        else:
            print(f"  Video file not found: {video_file}")
    
    print(f"\nCompleted! Processed {len(entries)} entries.")

if __name__ == "__main__":
    main() 