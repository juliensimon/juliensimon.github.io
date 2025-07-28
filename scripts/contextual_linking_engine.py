#!/usr/bin/env python3
"""
Contextual Internal Linking Engine
Automatically generates contextual internal links based on semantic analysis
"""

import os
import re
import json
from collections import defaultdict
from typing import Dict, List, Tuple
import hashlib

class ContextualLinkingEngine:
    """Generates smart internal links based on content analysis"""
    
    def __init__(self):
        self.content_graph = defaultdict(dict)
        self.entity_index = defaultdict(list)
        self.link_opportunities = defaultdict(list)
        
        # Define high-value linking patterns
        self.high_value_patterns = {
            'tutorial_to_advanced': {
                'source_indicators': ['introduction', 'getting started', 'basic', 'tutorial'],
                'target_indicators': ['advanced', 'deep dive', 'optimization', 'production'],
                'link_text_templates': [
                    'For advanced techniques, see {}',
                    'Take it further with {}',
                    'Deep dive: {}'
                ]
            },
            'concept_to_implementation': {
                'source_indicators': ['what is', 'overview', 'introduction to'],
                'target_indicators': ['how to', 'implementation', 'step by step', 'code'],
                'link_text_templates': [
                    'See practical implementation: {}',
                    'Learn how to implement: {}',
                    'Code example: {}'
                ]
            },
            'problem_to_solution': {
                'source_indicators': ['challenge', 'problem', 'issue', 'error'],
                'target_indicators': ['solution', 'fix', 'resolve', 'optimization'],
                'link_text_templates': [
                    'Solution: {}',
                    'How to fix: {}',
                    'Resolved in: {}'
                ]
            }
        }
    
    def analyze_content_for_linking(self, content_dir: str):
        """Analyze all content to identify linking opportunities"""
        content_files = self._get_content_files(content_dir)
        
        for file_path in content_files:
            content_data = self._extract_content_data(file_path)
            self.content_graph[file_path] = content_data
            
            # Build entity index
            for entity in content_data['entities']:
                self.entity_index[entity].append(file_path)
    
    def generate_contextual_links(self) -> Dict[str, List[Dict]]:
        """Generate contextual links for each piece of content"""
        for source_file, source_data in self.content_graph.items():
            links = []
            
            # Entity-based linking
            entity_links = self._generate_entity_links(source_file, source_data)
            links.extend(entity_links)
            
            # Pattern-based linking
            pattern_links = self._generate_pattern_links(source_file, source_data)
            links.extend(pattern_links)
            
            # Topic cluster linking
            cluster_links = self._generate_cluster_links(source_file, source_data)
            links.extend(cluster_links)
            
            # Temporal linking (older/newer content)
            temporal_links = self._generate_temporal_links(source_file, source_data)
            links.extend(temporal_links)
            
            self.link_opportunities[source_file] = links
        
        return dict(self.link_opportunities)
    
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
                'headers': self._extract_headers(content)
            }
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return {}
    
    def _extract_technical_entities(self, content: str) -> List[str]:
        """Extract technical entities from content"""
        entities = []
        
        technical_terms = [
            'SageMaker', 'Inferentia', 'EC2', 'S3', 'Lambda',
            'PyTorch', 'TensorFlow', 'Hugging Face', 'Transformers',
            'Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision',
            'SuperNova', 'Arcee', 'Small Language Models', 'LLM', 'SLM',
            'Quantization', 'Fine-tuning', 'Model Optimization'
        ]
        
        content_lower = content.lower()
        for term in technical_terms:
            if term.lower() in content_lower:
                entities.append(term)
        
        return entities
    
    def _generate_entity_links(self, source_file: str, source_data: Dict) -> List[Dict]:
        """Generate links based on shared entities"""
        links = []
        
        for entity in source_data['entities']:
            related_files = [f for f in self.entity_index[entity] if f != source_file]
            
            # Prioritize by relevance and authority
            for target_file in related_files[:3]:  # Max 3 entity-based links
                target_data = self.content_graph.get(target_file, {})
                
                link_score = self._calculate_link_relevance(source_data, target_data)
                if link_score > 0.7:  # High relevance threshold
                    links.append({
                        'target_file': target_file,
                        'target_title': target_data.get('title', ''),
                        'link_type': 'entity_based',
                        'entity': entity,
                        'relevance_score': link_score,
                        'context': f"Related content on {entity}"
                    })
        
        return links
    
    def _generate_pattern_links(self, source_file: str, source_data: Dict) -> List[Dict]:
        """Generate links based on content patterns"""
        links = []
        
        for pattern_name, pattern_config in self.high_value_patterns.items():
            source_matches = any(indicator in source_data.get('title', '').lower() + 
                               source_data.get('description', '').lower() 
                               for indicator in pattern_config['source_indicators'])
            
            if source_matches:
                # Find target content matching target indicators
                for target_file, target_data in self.content_graph.items():
                    if target_file == source_file:
                        continue
                    
                    target_text = target_data.get('title', '').lower() + target_data.get('description', '').lower()
                    target_matches = any(indicator in target_text 
                                       for indicator in pattern_config['target_indicators'])
                    
                    if target_matches:
                        # Check for shared entities to ensure relevance
                        shared_entities = set(source_data.get('entities', [])) & set(target_data.get('entities', []))
                        if shared_entities:
                            links.append({
                                'target_file': target_file,
                                'target_title': target_data.get('title', ''),
                                'link_type': 'pattern_based',
                                'pattern': pattern_name,
                                'shared_entities': list(shared_entities),
                                'relevance_score': 0.8
                            })
        
        return links
    
    def _generate_cluster_links(self, source_file: str, source_data: Dict) -> List[Dict]:
        """Generate links within topic clusters"""
        links = []
        
        # Define topic clusters
        clusters = {
            'aws_ai': ['sagemaker', 'inferentia', 'ec2', 'aws'],
            'small_language_models': ['slm', 'small language', 'arcee', 'efficient'],
            'model_optimization': ['quantization', 'optimization', 'performance', 'efficiency'],
            'practical_ai': ['practical', 'implementation', 'deployment', 'enterprise']
        }
        
        # Find which clusters this content belongs to
        source_clusters = []
        source_text = (source_data.get('title', '') + ' ' + source_data.get('description', '')).lower()
        
        for cluster_name, keywords in clusters.items():
            if any(keyword in source_text for keyword in keywords):
                source_clusters.append(cluster_name)
        
        # Find other content in same clusters
        for cluster in source_clusters:
            cluster_keywords = clusters[cluster]
            
            for target_file, target_data in self.content_graph.items():
                if target_file == source_file:
                    continue
                
                target_text = (target_data.get('title', '') + ' ' + target_data.get('description', '')).lower()
                if any(keyword in target_text for keyword in cluster_keywords):
                    links.append({
                        'target_file': target_file,
                        'target_title': target_data.get('title', ''),
                        'link_type': 'cluster_based',
                        'cluster': cluster,
                        'relevance_score': 0.75
                    })
        
        return links[:5]  # Limit cluster links
    
    def _generate_temporal_links(self, source_file: str, source_data: Dict) -> List[Dict]:
        """Generate links to chronologically related content"""
        links = []
        
        source_date = source_data.get('date')
        if not source_date:
            return links
        
        # Find content from similar time periods with related topics
        for target_file, target_data in self.content_graph.items():
            if target_file == source_file:
                continue
            
            target_date = target_data.get('date')
            if not target_date:
                continue
            
            # Check if dates are close (within 6 months)
            if abs((source_date - target_date).days) < 180:
                shared_entities = set(source_data.get('entities', [])) & set(target_data.get('entities', []))
                if shared_entities:
                    links.append({
                        'target_file': target_file,
                        'target_title': target_data.get('title', ''),
                        'link_type': 'temporal',
                        'shared_entities': list(shared_entities),
                        'relevance_score': 0.6
                    })
        
        return links[:2]  # Limit temporal links
    
    def _calculate_link_relevance(self, source_data: Dict, target_data: Dict) -> float:
        """Calculate relevance score between two pieces of content"""
        score = 0.0
        
        # Entity overlap
        source_entities = set(source_data.get('entities', []))
        target_entities = set(target_data.get('entities', []))
        entity_overlap = len(source_entities & target_entities) / len(source_entities | target_entities) if source_entities | target_entities else 0
        score += entity_overlap * 0.4
        
        # Topic similarity (simplified)
        source_topics = set(source_data.get('topics', []))
        target_topics = set(target_data.get('topics', []))
        topic_overlap = len(source_topics & target_topics) / len(source_topics | target_topics) if source_topics | target_topics else 0
        score += topic_overlap * 0.3
        
        # Complementary difficulty levels
        source_level = source_data.get('difficulty_level', 'intermediate')
        target_level = target_data.get('difficulty_level', 'intermediate')
        if (source_level == 'beginner' and target_level in ['intermediate', 'advanced']) or \
           (source_level == 'intermediate' and target_level == 'advanced'):
            score += 0.2
        
        # Content type compatibility
        source_type = source_data.get('content_type', 'article')
        target_type = target_data.get('content_type', 'article')
        if source_type != target_type:  # Different types can be complementary
            score += 0.1
        
        return min(score, 1.0)
    
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
        # Simplified difficulty assessment
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
        # Extract date from file path pattern
        import datetime
        date_match = re.search(r'(\d{4})[/-](\d{2})[/-](\d{2})', file_path)
        if date_match:
            return datetime.date(int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3)))
        return None
    
    def _extract_headers(self, content: str) -> List[str]:
        """Extract headers from content"""
        headers = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', content, re.IGNORECASE)
        return [re.sub(r'<[^>]+>', '', header) for header in headers]
    
    def inject_contextual_links(self, link_opportunities: Dict[str, List[Dict]]):
        """Inject contextual links into content files"""
        for source_file, links in link_opportunities.items():
            if not links:
                continue
            
            try:
                with open(source_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Add related content section
                if '</main>' in content or '</article>' in content:
                    related_section = self._generate_related_content_section(links)
                    content = content.replace('</main>', f'{related_section}</main>')
                    content = content.replace('</article>', f'{related_section}</article>')
                
                with open(source_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except Exception as e:
                print(f"Error injecting links into {source_file}: {e}")
    
    def _generate_related_content_section(self, links: List[Dict]) -> str:
        """Generate HTML for related content section"""
        if not links:
            return ""
        
        # Sort by relevance
        sorted_links = sorted(links, key=lambda x: x.get('relevance_score', 0), reverse=True)[:5]
        
        html = '''
        <section class="related-content" aria-labelledby="related-content-title">
            <h3 id="related-content-title">Related Technical Content</h3>
            <div class="related-links">
        '''
        
        for link in sorted_links:
            # Generate relative URL
            rel_url = link['target_file'].replace('blog/', '/blog/').replace('youtube/', '/youtube/')
            
            html += f'''
                <a href="{rel_url}" class="related-link" data-link-type="{link.get('link_type', 'contextual')}">
                    <span class="related-title">{link.get('target_title', 'Related Content')}</span>
                    <span class="related-context">{link.get('context', 'Related technical content')}</span>
                </a>
            '''
        
        html += '''
            </div>
        </section>
        '''
        
        return html

def main():
    """Main execution function"""
    engine = ContextualLinkingEngine()
    
    # Analyze content
    print("Analyzing content for linking opportunities...")
    engine.analyze_content_for_linking('blog/')
    engine.analyze_content_for_linking('youtube/')
    
    # Generate contextual links
    print("Generating contextual links...")
    link_opportunities = engine.generate_contextual_links()
    
    # Save analysis results
    with open('contextual_links_analysis.json', 'w') as f:
        json.dump(link_opportunities, f, indent=2, default=str)
    
    print(f"Generated contextual links for {len(link_opportunities)} content pieces")
    print(f"Total link opportunities: {sum(len(links) for links in link_opportunities.values())}")
    
    # Inject links (uncomment to apply)
    # engine.inject_contextual_links(link_opportunities)

if __name__ == "__main__":
    main() 