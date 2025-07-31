#!/usr/bin/env python3
"""
Intelligent Alt Text Generator
Uses multi-layer context analysis to generate meaningful alt text descriptions.
"""

import os
import re
import glob
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

class IntelligentAltGenerator:
    def __init__(self):
        self.domain_patterns = {
            'sagemaker': {
                'keywords': ['sagemaker', 'training', 'model', 'endpoint', 'studio'],
                'template': 'Amazon SageMaker {context}'
            },
            'performance': {
                'keywords': ['benchmark', 'speed', 'latency', 'throughput', 'chart', 'graph'],
                'template': '{context} performance chart'
            },
            'architecture': {
                'keywords': ['architecture', 'diagram', 'flow', 'pipeline', 'system'],
                'template': '{context} architecture diagram'
            },
            'aws_service': {
                'keywords': ['aws', 'amazon', 'console', 'dashboard', 'interface'],
                'template': 'AWS {context} console'
            },
            'ai_model': {
                'keywords': ['model', 'inference', 'training', 'neural', 'ai', 'ml'],
                'template': '{context} AI model demonstration'
            }
        }
        
        self.book_titles = {
            '4.3bsd-book': '4.3BSD Unix System',
            '4.4bsd-design-implementation': '4.4BSD Design and Implementation',
            '4.4bsd-french': '4.4BSD French Edition',
            'advanced-programming': 'Advanced Programming',
            'unix-programming': 'Unix Programming',
            'linux-programming': 'Linux Programming',
            'network-programming': 'Network Programming',
            'system-programming': 'System Programming'
        }
        
        self.stats = {
            'processed': 0,
            'improved': 0,
            'added': 0,
            'skipped': 0
        }
    
    def analyze_filename(self, src: str) -> Tuple[str, str]:
        """Analyze filename to determine image type and context."""
        filename = os.path.basename(src).lower()
        name_without_ext = os.path.splitext(filename)[0]
        
        # Book covers
        if any(book_key in name_without_ext for book_key in self.book_titles.keys()):
            for book_key, title in self.book_titles.items():
                if book_key in name_without_ext:
                    return "book", f"{title} book cover"
        
        # Technical screenshots
        if any(term in filename for term in ['screenshot', 'console', 'dashboard', 'interface']):
            return "interface", "Technical interface screenshot"
        
        # Performance charts
        if any(term in filename for term in ['chart', 'graph', 'performance', 'benchmark', 'comparison']):
            return "chart", "Performance comparison chart"
        
        # Architecture diagrams
        if any(term in filename for term in ['architecture', 'diagram', 'flow', 'pipeline']):
            return "diagram", "System architecture diagram"
        
        # Profile images
        if 'julien' in filename:
            return "profile", "Julien Simon"
        
        # Logo and branding
        if any(term in filename for term in ['logo', 'brand', 'icon']):
            return "logo", "Company logo"
        
        # Awards and achievements
        if any(term in filename for term in ['award', 'achievement', 'recognition', 'trophy']):
            return "award", "Achievement award"
        
        # Sequential images (image01, image02, etc.)
        if re.match(r'image\d+', filename):
            return "sequence", "Tutorial step illustration"
        
        return "generic", "Illustration"
    
    def get_directory_context(self, file_path: str) -> Dict[str, str]:
        """Extract context from directory structure."""
        path_lower = file_path.lower()
        
        if 'arcee-posts' in path_lower:
            return {
                'domain': 'Small Language Models',
                'context': 'AI performance and capabilities',
                'prefix': 'Small language model',
                'topic': 'AI/ML'
            }
        
        elif 'aws-posts' in path_lower:
            return {
                'domain': 'AWS Cloud Services',
                'context': 'Cloud computing and services',
                'prefix': 'AWS',
                'topic': 'Cloud'
            }
        
        elif 'huggingface-posts' in path_lower:
            return {
                'domain': 'Hugging Face AI',
                'context': 'Machine learning models',
                'prefix': 'Hugging Face',
                'topic': 'AI/ML'
            }
        
        elif 'computers' in path_lower:
            return {
                'domain': 'Computer Books',
                'context': 'Technical literature',
                'prefix': 'Computer science',
                'topic': 'Books'
            }
        
        elif 'youtube' in path_lower:
            return {
                'domain': 'Video Content',
                'context': 'Educational videos',
                'prefix': 'Video',
                'topic': 'Media'
            }
        
        return {
            'domain': 'Technical Content',
            'context': 'Technology',
            'prefix': 'Technical',
            'topic': 'Tech'
        }
    
    def analyze_surrounding_content(self, html_content: str, img_position: int) -> Optional[str]:
        """Analyze content around the image for context clues."""
        # Extract context window around image
        start = max(0, img_position - 1000)
        end = min(len(html_content), img_position + 1000)
        context_window = html_content[start:end]
        
        # Look for figure captions
        caption_match = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', context_window, re.IGNORECASE | re.DOTALL)
        if caption_match:
            caption = re.sub(r'<[^>]+>', '', caption_match.group(1)).strip()
            if caption and len(caption) < 100:
                return caption
        
        # Look for nearby headings
        heading_patterns = [
            r'<h[1-6][^>]*>(.*?)</h[1-6]>',
            r'<title[^>]*>(.*?)</title>'
        ]
        
        for pattern in heading_patterns:
            heading_match = re.search(pattern, context_window, re.IGNORECASE | re.DOTALL)
            if heading_match:
                heading = re.sub(r'<[^>]+>', '', heading_match.group(1)).strip()
                if heading and len(heading) < 80:
                    return f"Illustration for {heading}"
        
        return None
    
    def extract_post_title(self, file_path: str) -> Optional[str]:
        """Extract post title from directory name or metadata."""
        dir_name = os.path.basename(os.path.dirname(file_path))
        
        # Remove date prefix and clean up
        title_part = re.sub(r'^\d{4}-\d{2}-\d{2}_', '', dir_name)
        title_part = title_part.replace('-', ' ').replace('_', ' ')
        
        # Convert to title case and clean up
        title = title_part.title()
        title = re.sub(r'\b(And|Or|The|A|An|In|On|At|To|For|Of|With|By)\b', 
                      lambda m: m.group().lower(), title)
        title = title.replace('AI', 'AI').replace('ML', 'ML').replace('Aws', 'AWS')
        
        return title if len(title) < 80 else None
    
    def generate_smart_alt(self, img_src: str, file_path: str, html_content: str, img_position: int) -> str:
        """Generate intelligent alt text using all available context."""
        
        # Analyze different context layers
        filename_type, filename_desc = self.analyze_filename(img_src)
        directory_context = self.get_directory_context(file_path)
        post_title = self.extract_post_title(file_path)
        
        # Try to get surrounding content context
        img_position_in_content = html_content.find(f'src="{img_src}"')
        if img_position_in_content == -1:
            img_position_in_content = img_position
        
        surrounding_context = self.analyze_surrounding_content(html_content, img_position_in_content)
        
        # Build intelligent description
        if surrounding_context:
            return surrounding_context
        
        # Book covers get special treatment
        if filename_type == "book":
            return filename_desc
        
        # Profile images
        if filename_type == "profile":
            return "Julien Simon"
        
        # Technical content with domain context
        if filename_type in ["interface", "chart", "diagram"]:
            prefix = directory_context.get('prefix', 'Technical')
            
            if filename_type == "interface":
                return f"{prefix} user interface screenshot"
            elif filename_type == "chart":
                return f"{prefix} performance metrics chart"
            elif filename_type == "diagram":
                return f"{prefix} system architecture diagram"
        
        # Sequential images with post context
        if filename_type == "sequence" and post_title:
            sequence_match = re.search(r'image(\d+)', img_src)
            if sequence_match:
                step_num = int(sequence_match.group(1))
                if step_num == 1:
                    return f"Screenshot from {post_title} tutorial"
                else:
                    return f"Step {step_num} screenshot from {post_title}"
        
        # Domain-specific defaults
        domain_prefix = directory_context.get('prefix', 'Technical')
        
        if 'arcee' in file_path.lower():
            return f"Small language model {filename_desc.lower()}"
        elif 'aws' in file_path.lower():
            return f"AWS {filename_desc.lower()}"
        elif 'huggingface' in file_path.lower():
            return f"Hugging Face {filename_desc.lower()}"
        
        # Generic but contextual fallback
        return f"{domain_prefix} {filename_desc.lower()}"
    
    def process_html_file(self, file_path: str) -> bool:
        """Process a single HTML file to fix alt attributes."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            modified = False
            
            # Find all img tags
            img_pattern = r'<img([^>]*?)>'
            img_matches = list(re.finditer(img_pattern, content, re.IGNORECASE))
            
            # Process images in reverse order to maintain positions
            for match in reversed(img_matches):
                img_tag = match.group(0)
                img_attrs = match.group(1)
                
                # Extract src attribute
                src_match = re.search(r'src=["\']([^"\']+)["\']', img_attrs, re.IGNORECASE)
                if not src_match:
                    continue
                
                img_src = src_match.group(1)
                
                # Check if alt attribute exists and is meaningful
                alt_match = re.search(r'alt=["\']([^"\']*)["\']', img_attrs, re.IGNORECASE)
                
                needs_alt = False
                if not alt_match:
                    # No alt attribute
                    needs_alt = True
                    action = "added"
                elif alt_match.group(1).strip() == "":
                    # Empty alt attribute
                    needs_alt = True
                    action = "improved"
                elif len(alt_match.group(1).strip()) < 3:
                    # Very short/generic alt text
                    needs_alt = True
                    action = "improved"
                
                if needs_alt:
                    # Generate smart alt text
                    smart_alt = self.generate_smart_alt(img_src, file_path, content, match.start())
                    
                    if alt_match:
                        # Replace existing alt attribute
                        new_img_tag = img_tag.replace(alt_match.group(0), f'alt="{smart_alt}"')
                    else:
                        # Add alt attribute
                        # Insert before the closing >
                        new_img_tag = img_tag[:-1] + f' alt="{smart_alt}">'
                    
                    content = content[:match.start()] + new_img_tag + content[match.end():]
                    modified = True
                    
                    if action == "added":
                        self.stats['added'] += 1
                    else:
                        self.stats['improved'] += 1
                    
                    print(f"  ✅ {action.title()} alt text: {img_src} → '{smart_alt}'")
                else:
                    self.stats['skipped'] += 1
            
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            
            return False
            
        except Exception as e:
            print(f"  ❌ Error processing {file_path}: {e}")
            return False
    
    def process_all_files(self):
        """Process all HTML files in the website."""
        print("🚀 Starting Intelligent Alt Text Generation")
        print("=" * 60)
        
        # Find all HTML files
        html_files = glob.glob("**/*.html", recursive=True)
        html_files = [f for f in html_files if not f.startswith('.git')]
        
        print(f"Found {len(html_files)} HTML files to process")
        print()
        
        processed_files = 0
        
        for file_path in html_files:
            self.stats['processed'] += 1
            
            # Skip certain files
            if any(skip in file_path for skip in ['.git', 'node_modules', 'vendor']):
                continue
            
            print(f"📄 Processing: {file_path}")
            
            if self.process_html_file(file_path):
                processed_files += 1
                print(f"  ✅ Updated {file_path}")
            else:
                print(f"  ⏭️  No changes needed for {file_path}")
            
            print()
        
        # Print final statistics
        print("=" * 60)
        print("🎉 Intelligent Alt Text Generation Complete!")
        print(f"📊 Files processed: {self.stats['processed']}")
        print(f"📝 Files modified: {processed_files}")
        print(f"➕ Alt attributes added: {self.stats['added']}")
        print(f"🔧 Alt attributes improved: {self.stats['improved']}")
        print(f"⏭️  Images skipped (already good): {self.stats['skipped']}")
        print(f"🎯 Total images enhanced: {self.stats['added'] + self.stats['improved']}")

def main():
    """Main function to run the intelligent alt text generator."""
    generator = IntelligentAltGenerator()
    generator.process_all_files()

if __name__ == "__main__":
    main() 