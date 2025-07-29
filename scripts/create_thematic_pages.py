#!/usr/bin/env python3
"""
Thematic Content Aggregation System
Creates dedicated pages that group related posts and videos by theme
"""

import os
import re
import json
from collections import defaultdict
from typing import Dict, List, Tuple
from datetime import datetime
import hashlib

class ThematicContentAggregator:
    """Creates thematic pages by grouping related content"""
    
    def __init__(self):
        self.content_index = {}
        self.thematic_clusters = defaultdict(list)
        self.theme_definitions = {
            'small-language-models': {
                'name': 'Small Language Models (SLMs)',
                'description': 'Cost-effective alternatives to large language models for enterprise AI',
                'keywords': ['SLM', 'Small Language Models', 'Arcee', 'SuperNova', 'cost-effective AI', 'enterprise AI'],
                'priority': 1
            },
            'aws-ai-services': {
                'name': 'AWS AI Services & SageMaker',
                'description': 'Cloud-native AI deployment and optimization on AWS',
                'keywords': ['SageMaker', 'AWS Inferentia', 'AWS Trainium', 'EC2', 'Lambda', 'S3', 'AWS AI'],
                'priority': 1
            },
            'hugging-face-ecosystem': {
                'name': 'Hugging Face Ecosystem',
                'description': 'Open-source AI tools, transformers, and model optimization',
                'keywords': ['Hugging Face', 'Transformers', 'Model Hub', 'Optimum', 'Diffusers'],
                'priority': 1
            },
            'hardware-acceleration': {
                'name': 'AI Hardware Acceleration',
                'description': 'Specialized hardware for training and inference optimization',
                'keywords': ['Inferentia', 'Trainium', 'GPU', 'Neuron', 'hardware acceleration', 'optimization'],
                'priority': 2
            },
            'enterprise-ai-strategy': {
                'name': 'Enterprise AI Strategy',
                'description': 'Strategic AI adoption and governance for Fortune 500 companies',
                'keywords': ['enterprise', 'strategy', 'governance', 'Fortune 500', 'business value'],
                'priority': 2
            },
            'model-optimization': {
                'name': 'Model Optimization & Deployment',
                'description': 'Techniques for optimizing ML models for production',
                'keywords': ['quantization', 'fine-tuning', 'deployment', 'optimization', 'production'],
                'priority': 2
            },
            'nlp-applications': {
                'name': 'Natural Language Processing',
                'description': 'NLP applications and transformer-based solutions',
                'keywords': ['NLP', 'BERT', 'RoBERTa', 'text classification', 'sentiment analysis'],
                'priority': 3
            },
            'computer-vision': {
                'name': 'Computer Vision & Image Generation',
                'description': 'CV applications and generative AI for images',
                'keywords': ['computer vision', 'ViT', 'Stable Diffusion', 'image generation', 'CV'],
                'priority': 3
            },
            'mlops-and-deployment': {
                'name': 'MLOps & Model Deployment',
                'description': 'Production ML workflows and deployment strategies',
                'keywords': ['MLOps', 'deployment', 'pipeline', 'monitoring', 'production'],
                'priority': 3
            },
            'ai-cost-optimization': {
                'name': 'AI Cost Optimization',
                'description': 'Strategies for reducing AI infrastructure costs',
                'keywords': ['cost optimization', 'budget', 'efficiency', 'ROI', 'cost-effective'],
                'priority': 2
            }
        }
    
    def analyze_content_for_themes(self, content_dir: str):
        """Analyze all content and assign to thematic clusters"""
        content_files = self._get_content_files(content_dir)
        
        for file_path in content_files:
            content_data = self._extract_content_data(file_path)
            if content_data:
                self.content_index[file_path] = content_data
                self._assign_to_themes(file_path, content_data)
    
    def _get_content_files(self, content_dir: str) -> List[str]:
        """Get all HTML content files"""
        files = []
        for root, dirs, filenames in os.walk(content_dir):
            for filename in filenames:
                if filename.endswith('.html'):
                    files.append(os.path.join(root, filename))
        return files
    
    def _extract_content_data(self, file_path: str) -> Dict:
        """Extract relevant data from content file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                'title': self._extract_title(content),
                'description': self._extract_description(content),
                'entities': self._extract_technical_entities(content),
                'topics': self._extract_topics(content),
                'difficulty_level': self._assess_difficulty(content),
                'content_type': self._classify_content_type(content),
                'date': self._extract_date(file_path),
                'word_count': len(content.split()),
                'headers': self._extract_headers(content),
                'url': self._extract_url(file_path),
                'platform': self._extract_platform(file_path)
            }
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return {}
    
    def _assign_to_themes(self, file_path: str, content_data: Dict):
        """Assign content to thematic clusters based on semantic analysis"""
        content_text = f"{content_data.get('title', '')} {content_data.get('description', '')}".lower()
        entities = [e.lower() for e in content_data.get('entities', [])]
        
        theme_scores = {}
        
        for theme_id, theme_info in self.theme_definitions.items():
            score = 0.0
            
            # Keyword matching
            for keyword in theme_info['keywords']:
                if keyword.lower() in content_text:
                    score += 0.3
                if keyword.lower() in entities:
                    score += 0.5
            
            # Entity overlap
            theme_entities = set(theme_info['keywords'])
            content_entities = set(entities)
            entity_overlap = len(theme_entities & content_entities) / len(theme_entities | content_entities) if theme_entities | content_entities else 0
            score += entity_overlap * 0.4
            
            if score > 0.2:  # Minimum threshold for theme assignment
                theme_scores[theme_id] = score
        
        # Assign to top 2-3 themes
        sorted_themes = sorted(theme_scores.items(), key=lambda x: x[1], reverse=True)
        for theme_id, score in sorted_themes[:3]:
            self.thematic_clusters[theme_id].append({
                'file_path': file_path,
                'content_data': content_data,
                'theme_score': score
            })
    
    def _extract_technical_entities(self, content: str) -> List[str]:
        """Extract technical entities from content"""
        entities = []
        
        technical_terms = [
            'SageMaker', 'Inferentia', 'EC2', 'S3', 'Lambda',
            'PyTorch', 'TensorFlow', 'Hugging Face', 'Transformers',
            'Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision',
            'SuperNova', 'Arcee', 'Small Language Models', 'LLM', 'SLM',
            'Quantization', 'Fine-tuning', 'Model Optimization', 'Trainium',
            'BERT', 'RoBERTa', 'DistilBERT', 'ALBERT', 'ViT',
            'Stable Diffusion', 'Optimum', 'Neuron', 'AWS AI'
        ]
        
        content_lower = content.lower()
        for term in technical_terms:
            if term.lower() in content_lower:
                entities.append(term)
        
        return entities
    
    def _extract_title(self, content: str) -> str:
        """Extract title from HTML content"""
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        return title_match.group(1) if title_match else ""
    
    def _extract_description(self, content: str) -> str:
        """Extract description from HTML content"""
        desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', content, re.IGNORECASE)
        return desc_match.group(1) if desc_match else ""
    
    def _extract_topics(self, content: str) -> List[str]:
        """Extract topics from content"""
        # Simplified topic extraction
        return []
    
    def _assess_difficulty(self, content: str) -> str:
        """Assess content difficulty level"""
        if any(word in content.lower() for word in ['introduction', 'basic', 'getting started']):
            return 'beginner'
        elif any(word in content.lower() for word in ['advanced', 'optimization', 'production']):
            return 'advanced'
        return 'intermediate'
    
    def _classify_content_type(self, content: str) -> str:
        """Classify content type"""
        if 'code' in content.lower() or '<pre>' in content:
            return 'tutorial'
        elif any(word in content.lower() for word in ['overview', 'introduction']):
            return 'overview'
        return 'article'
    
    def _extract_date(self, file_path: str) -> object:
        """Extract date from file path"""
        import datetime
        date_match = re.search(r'(\d{4})[/-](\d{2})[/-](\d{2})', file_path)
        if date_match:
            return datetime.date(int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3)))
        return None
    
    def _extract_headers(self, content: str) -> List[str]:
        """Extract headers from content"""
        headers = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', content, re.IGNORECASE)
        return [re.sub(r'<[^>]+>', '', header) for header in headers]
    
    def _extract_url(self, file_path: str) -> str:
        """Extract URL from file path"""
        # Convert file path to URL
        url = file_path.replace('blog/', '/blog/').replace('youtube/', '/youtube/')
        if url.startswith('/'):
            url = url[1:]
        return f"https://julien.org/{url}"
    
    def _extract_platform(self, file_path: str) -> str:
        """Extract platform from file path"""
        if 'blog/' in file_path:
            if 'huggingface' in file_path:
                return 'Hugging Face Blog'
            elif 'aws' in file_path:
                return 'AWS Blog'
            elif 'arcee' in file_path:
                return 'Arcee AI Blog'
            else:
                return 'Technical Blog'
        elif 'youtube/' in file_path:
            return 'YouTube Video'
        return 'Other'
    
    def generate_thematic_pages(self) -> Dict[str, Dict]:
        """Generate thematic page content for each cluster"""
        thematic_pages = {}
        
        for theme_id, theme_info in self.theme_definitions.items():
            if theme_id in self.thematic_clusters:
                cluster_content = self.thematic_clusters[theme_id]
                
                # Sort by relevance score and date
                cluster_content.sort(key=lambda x: (x['theme_score'], x['content_data'].get('date', datetime.min)), reverse=True)
                
                thematic_pages[theme_id] = {
                    'theme_info': theme_info,
                    'content': cluster_content,
                    'stats': self._calculate_cluster_stats(cluster_content),
                    'subthemes': self._identify_subthemes(cluster_content)
                }
        
        return thematic_pages
    
    def _calculate_cluster_stats(self, cluster_content: List[Dict]) -> Dict:
        """Calculate statistics for a thematic cluster"""
        total_content = len(cluster_content)
        platforms = defaultdict(int)
        difficulty_levels = defaultdict(int)
        content_types = defaultdict(int)
        date_range = []
        
        for item in cluster_content:
            content_data = item['content_data']
            platforms[content_data.get('platform', 'Unknown')] += 1
            difficulty_levels[content_data.get('difficulty_level', 'intermediate')] += 1
            content_types[content_data.get('content_type', 'article')] += 1
            
            if content_data.get('date'):
                date_range.append(content_data['date'])
        
        return {
            'total_content': total_content,
            'platforms': dict(platforms),
            'difficulty_levels': dict(difficulty_levels),
            'content_types': dict(content_types),
            'date_range': {
                'earliest': min(date_range) if date_range else None,
                'latest': max(date_range) if date_range else None
            },
            'avg_theme_score': sum(item['theme_score'] for item in cluster_content) / len(cluster_content) if cluster_content else 0
        }
    
    def _identify_subthemes(self, cluster_content: List[Dict]) -> List[Dict]:
        """Identify subthemes within a cluster"""
        subthemes = defaultdict(list)
        
        for item in cluster_content:
            content_data = item['content_data']
            entities = content_data.get('entities', [])
            
            # Group by primary entity
            if entities:
                primary_entity = entities[0]
                subthemes[primary_entity].append(item)
        
        return [
            {
                'name': subtheme_name,
                'content': subtheme_content,
                'count': len(subtheme_content)
            }
            for subtheme_name, subtheme_content in subthemes.items()
        ]
    
    def create_thematic_html_pages(self, thematic_pages: Dict[str, Dict]):
        """Create HTML pages for each thematic cluster"""
        for theme_id, theme_data in thematic_pages.items():
            html_content = self._generate_thematic_page_html(theme_id, theme_data)
            
            # Create directory if it doesn't exist
            os.makedirs('thematic-pages', exist_ok=True)
            
            # Write HTML file
            with open(f'thematic-pages/{theme_id}.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
    
    def _generate_thematic_page_html(self, theme_id: str, theme_data: Dict) -> str:
        """Generate HTML content for a thematic page"""
        theme_info = theme_data['theme_info']
        content = theme_data['content']
        stats = theme_data['stats']
        subthemes = theme_data['subthemes']
        
        # Generate content sections
        content_sections = self._generate_content_sections(content)
        subtheme_sections = self._generate_subtheme_sections(subthemes)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{theme_info['name']} - Julien Simon | AI Expert</title>
    <meta name="description" content="{theme_info['description']} - Expert content by Julien Simon covering {stats['total_content']} articles and videos on {theme_info['name'].lower()}.">
    
    <!-- SEO Meta Tags -->
    <meta name="keywords" content="{', '.join(theme_info['keywords'])}">
    <meta name="author" content="Julien Simon">
    <meta name="robots" content="index, follow">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{theme_info['name']} - Julien Simon">
    <meta property="og:description" content="{theme_info['description']}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://julien.org/thematic-pages/{theme_id}.html">
    
    <!-- Structured Data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "{theme_info['name']}",
        "description": "{theme_info['description']}",
        "url": "https://julien.org/thematic-pages/{theme_id}.html",
        "hasPart": [
            {{
                "@type": "CreativeWorkSeries",
                "name": "Expert Content on {theme_info['name']}",
                "numberOfItems": {stats['total_content']},
                "description": "Comprehensive technical content on {theme_info['name'].lower()}"
            }}
        ],
        "author": {{
            "@type": "Person",
            "name": "Julien Simon",
            "jobTitle": "AI Technical Evangelist",
            "expertise": "{theme_info['name']}"
        }}
    }}
    </script>
    
    <link rel="stylesheet" href="../css/styles.css">
</head>
<body>
    <header>
        <nav>
            <a href="../index.html">← Back to Home</a>
        </nav>
    </header>
    
    <main>
        <article>
            <header>
                <h1>{theme_info['name']}</h1>
                <p class="theme-description">{theme_info['description']}</p>
                
                <div class="theme-stats">
                    <div class="stat">
                        <span class="stat-number">{stats['total_content']}</span>
                        <span class="stat-label">Articles & Videos</span>
                    </div>
                    <div class="stat">
                        <span class="stat-number">{len(stats['platforms'])}</span>
                        <span class="stat-label">Platforms</span>
                    </div>
                    <div class="stat">
                        <span class="stat-number">{stats['date_range']['earliest'].year if stats['date_range']['earliest'] else 'N/A'}</span>
                        <span class="stat-label">Since</span>
                    </div>
                </div>
            </header>
            
            {subtheme_sections}
            
            {content_sections}
        </article>
    </main>
    
    <footer>
        <p>Expert content by <a href="../index.html">Julien Simon</a> - AI Technical Evangelist</p>
    </footer>
</body>
</html>"""
        
        return html
    
    def _generate_content_sections(self, content: List[Dict]) -> str:
        """Generate HTML sections for content items"""
        sections = []
        
        for item in content:
            content_data = item['content_data']
            theme_score = item['theme_score']
            
            # Determine icon based on platform
            icon = "📺" if "YouTube" in content_data.get('platform', '') else "📄"
            
            # Format date
            date_str = ""
            if content_data.get('date'):
                date_str = content_data['date'].strftime("%B %Y")
            
            # Difficulty indicator
            difficulty_icon = {
                'beginner': '🟢',
                'intermediate': '🟡', 
                'advanced': '🔴'
            }.get(content_data.get('difficulty_level', 'intermediate'), '🟡')
            
            section = f"""
            <section class="content-item" style="margin-bottom: 2rem; padding: 1.5rem; border: 1px solid #e9ecef; border-radius: 8px; background: white;">
                <div class="content-header">
                    <h3 style="margin: 0 0 0.5rem 0; color: #2c3e50;">
                        {icon} {content_data.get('title', 'Untitled')}
                    </h3>
                    <div class="content-meta" style="font-size: 0.9rem; color: #6c757d; margin-bottom: 1rem;">
                        <span>{content_data.get('platform', 'Unknown')}</span>
                        <span>•</span>
                        <span>{date_str}</span>
                        <span>•</span>
                        <span>{difficulty_icon} {content_data.get('difficulty_level', 'intermediate').title()}</span>
                        <span>•</span>
                        <span>🎯 Relevance: {theme_score:.1%}</span>
                    </div>
                </div>
                
                <p style="color: #495057; margin-bottom: 1rem;">
                    {content_data.get('description', 'No description available.')}
                </p>
                
                <div class="content-entities" style="margin-bottom: 1rem;">
                    <strong>Key Topics:</strong>
                    {', '.join(content_data.get('entities', [])[:5])}
                </div>
                
                <a href="{content_data.get('url', '#')}" 
                   style="display: inline-block; padding: 0.5rem 1rem; background: #FF6B35; color: white; text-decoration: none; border-radius: 4px; font-weight: 500;">
                    Read Full Content →
                </a>
            </section>"""
            
            sections.append(section)
        
        return '\n'.join(sections)
    
    def _generate_subtheme_sections(self, subthemes: List[Dict]) -> str:
        """Generate HTML sections for subthemes"""
        if not subthemes:
            return ""
        
        sections = []
        sections.append('<section class="subthemes" style="margin-bottom: 3rem;">')
        sections.append('<h2>Subtopics</h2>')
        sections.append('<div class="subtheme-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">')
        
        for subtheme in subthemes:
            section = f"""
            <div class="subtheme-card" style="padding: 1rem; border: 1px solid #dee2e6; border-radius: 6px; background: #f8f9fa;">
                <h3 style="margin: 0 0 0.5rem 0; color: #495057; font-size: 1.1rem;">{subtheme['name']}</h3>
                <p style="margin: 0; color: #6c757d; font-size: 0.9rem;">{subtheme['count']} articles/videos</p>
            </div>"""
            sections.append(section)
        
        sections.append('</div>')
        sections.append('</section>')
        
        return '\n'.join(sections)
    
    def generate_sitemap_updates(self, thematic_pages: Dict[str, Dict]) -> str:
        """Generate sitemap entries for thematic pages"""
        entries = []
        
        for theme_id, theme_data in thematic_pages.items():
            theme_info = theme_data['theme_info']
            entries.append(f"""
    <url>
        <loc>https://julien.org/thematic-pages/{theme_id}.html</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>""")
        
        return '\n'.join(entries)

def main():
    """Main execution function"""
    aggregator = ThematicContentAggregator()
    
    print("🔍 Analyzing content for thematic clustering...")
    aggregator.analyze_content_for_themes('blog')
    aggregator.analyze_content_for_themes('youtube')
    
    print("📊 Generating thematic pages...")
    thematic_pages = aggregator.generate_thematic_pages()
    
    print("📝 Creating HTML pages...")
    aggregator.create_thematic_html_pages(thematic_pages)
    
    # Generate analysis report
    analysis_report = {
        'total_themes': len(thematic_pages),
        'theme_breakdown': {
            theme_id: {
                'name': data['theme_info']['name'],
                'content_count': len(data['content']),
                'avg_score': data['stats']['avg_theme_score'],
                'platforms': data['stats']['platforms']
            }
            for theme_id, data in thematic_pages.items()
        },
        'sitemap_entries': aggregator.generate_sitemap_updates(thematic_pages)
    }
    
    with open('thematic_analysis_report.json', 'w', encoding='utf-8') as f:
        json.dump(analysis_report, f, indent=2, default=str)
    
    print(f"✅ Created {len(thematic_pages)} thematic pages:")
    for theme_id, data in thematic_pages.items():
        print(f"   📄 {data['theme_info']['name']}: {len(data['content'])} items")
    
    print("\n📊 Analysis report saved to: thematic_analysis_report.json")

if __name__ == "__main__":
    main() 