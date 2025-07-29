#!/usr/bin/env python3
"""
Advanced Difficulty Assessment System
Intelligently classifies technical content difficulty using multiple signals
"""

import re
import json
from typing import Dict, List, Tuple
from collections import defaultdict

class AdvancedDifficultyAssessor:
    """Advanced difficulty assessment using multiple signals"""
    
    def __init__(self):
        # Difficulty indicators by category
        self.difficulty_indicators = {
            'beginner': {
                'keywords': [
                    'introduction', 'getting started', 'basic', 'tutorial', 'first steps',
                    'overview', 'what is', 'explained', 'guide', 'beginner', 'new to',
                    'simple', 'easy', 'start here', 'fundamentals', 'basics'
                ],
                'code_patterns': [
                    r'print\(', r'hello world', r'basic example', r'simple demo',
                    r'first time', r'getting started', r'installation'
                ],
                'content_patterns': [
                    r'if you are new to', r'for beginners', r'no prior knowledge',
                    r'assumes no background', r'step by step', r'walkthrough'
                ]
            },
            'intermediate': {
                'keywords': [
                    'implementation', 'how to', 'step by step', 'example', 'demo',
                    'practical', 'hands-on', 'working with', 'using', 'deploy',
                    'configure', 'setup', 'integration', 'middle', 'moderate'
                ],
                'code_patterns': [
                    r'def ', r'class ', r'import ', r'from ', r'pip install',
                    r'configuration', r'parameters', r'options', r'api'
                ],
                'content_patterns': [
                    r'assumes basic knowledge', r'familiar with', r'experience with',
                    r'working knowledge', r'practical implementation', r'real-world'
                ]
            },
            'advanced': {
                'keywords': [
                    'advanced', 'optimization', 'production', 'enterprise', 'scaling',
                    'performance', 'architecture', 'deep dive', 'expert', 'master',
                    'complex', 'sophisticated', 'cutting edge', 'state of the art',
                    'optimization', 'fine-tuning', 'custom', 'advanced techniques'
                ],
                'code_patterns': [
                    r'@decorator', r'async def', r'class Meta:', r'__init__',
                    r'lambda ', r'comprehension', r'generator', r'context manager',
                    r'custom', r'optimization', r'performance', r'benchmark'
                ],
                'content_patterns': [
                    r'for advanced users', r'expert level', r'deep technical',
                    r'production ready', r'enterprise grade', r'optimization',
                    r'performance tuning', r'advanced techniques', r'custom implementation'
                ]
            }
        }
        
        # Technical complexity signals
        self.technical_complexity = {
            'high_complexity_terms': [
                'distributed', 'microservices', 'kubernetes', 'docker', 'orchestration',
                'scalability', 'high availability', 'fault tolerance', 'load balancing',
                'monitoring', 'observability', 'telemetry', 'metrics', 'logging',
                'security', 'authentication', 'authorization', 'encryption', 'ssl',
                'performance tuning', 'optimization', 'benchmarking', 'profiling',
                'custom implementation', 'advanced algorithms', 'machine learning',
                'deep learning', 'neural networks', 'transformers', 'attention mechanisms',
                'quantization', 'pruning', 'distillation', 'fine-tuning'
            ],
            'medium_complexity_terms': [
                'api', 'rest', 'json', 'xml', 'database', 'sql', 'nosql',
                'caching', 'session', 'authentication', 'authorization',
                'testing', 'unit tests', 'integration tests', 'deployment',
                'ci/cd', 'pipeline', 'workflow', 'automation', 'scripting'
            ],
            'low_complexity_terms': [
                'basic', 'simple', 'hello world', 'tutorial', 'example',
                'demo', 'overview', 'introduction', 'getting started'
            ]
        }
        
        # Content structure signals
        self.structure_signals = {
            'beginner': {
                'sections': ['introduction', 'prerequisites', 'step by step', 'summary'],
                'code_ratio': 0.2,  # Low code to text ratio
                'header_depth': 2,   # Shallow header structure
                'word_count_range': (500, 2000)
            },
            'intermediate': {
                'sections': ['overview', 'implementation', 'example', 'testing', 'deployment'],
                'code_ratio': 0.4,  # Medium code to text ratio
                'header_depth': 3,   # Medium header structure
                'word_count_range': (1500, 5000)
            },
            'advanced': {
                'sections': ['architecture', 'optimization', 'performance', 'scaling', 'production'],
                'code_ratio': 0.6,  # High code to text ratio
                'header_depth': 4,   # Deep header structure
                'word_count_range': (3000, 15000)
            }
        }
    
    def assess_difficulty(self, content: str, title: str = "", description: str = "") -> Dict:
        """Comprehensive difficulty assessment using multiple signals"""
        
        # Combine all text for analysis
        full_text = f"{title} {description} {content}".lower()
        
        # 1. Keyword-based assessment
        keyword_scores = self._assess_keywords(full_text)
        
        # 2. Code complexity assessment
        code_scores = self._assess_code_complexity(content)
        
        # 3. Technical term complexity
        technical_scores = self._assess_technical_complexity(full_text)
        
        # 4. Content structure assessment
        structure_scores = self._assess_content_structure(content)
        
        # 5. Content length and depth
        length_scores = self._assess_content_length(content)
        
        # 6. Audience signals
        audience_scores = self._assess_audience_signals(full_text)
        
        # Combine all scores with weights
        final_scores = self._combine_scores({
            'keyword': keyword_scores,
            'code': code_scores,
            'technical': technical_scores,
            'structure': structure_scores,
            'length': length_scores,
            'audience': audience_scores
        })
        
        # Determine primary difficulty level
        primary_difficulty = max(final_scores.items(), key=lambda x: x[1])[0]
        
        # Calculate confidence score
        confidence = self._calculate_confidence(final_scores)
        
        return {
            'primary_difficulty': primary_difficulty,
            'confidence': confidence,
            'detailed_scores': final_scores,
            'signals': {
                'keyword_matches': self._get_keyword_matches(full_text),
                'technical_terms': self._get_technical_terms(full_text),
                'code_indicators': self._get_code_indicators(content),
                'structure_indicators': self._get_structure_indicators(content)
            }
        }
    
    def _assess_keywords(self, text: str) -> Dict[str, float]:
        """Assess difficulty based on keyword presence"""
        scores = {'beginner': 0.0, 'intermediate': 0.0, 'advanced': 0.0}
        
        for level, indicators in self.difficulty_indicators.items():
            score = 0.0
            for keyword in indicators['keywords']:
                if keyword.lower() in text:
                    score += 0.1
            
            # Normalize score
            scores[level] = min(score, 1.0)
        
        return scores
    
    def _assess_code_complexity(self, content: str) -> Dict[str, float]:
        """Assess difficulty based on code complexity"""
        scores = {'beginner': 0.0, 'intermediate': 0.0, 'advanced': 0.0}
        
        # Count code blocks
        code_blocks = re.findall(r'<pre><code.*?>(.*?)</code></pre>', content, re.DOTALL)
        code_ratio = len(''.join(code_blocks)) / len(content) if content else 0
        
        # Analyze code patterns
        for level, indicators in self.difficulty_indicators.items():
            score = 0.0
            
            # Pattern matching
            for pattern in indicators['code_patterns']:
                matches = re.findall(pattern, content, re.IGNORECASE)
                score += len(matches) * 0.05
            
            # Code ratio consideration
            if level == 'beginner' and code_ratio < 0.3:
                score += 0.3
            elif level == 'intermediate' and 0.2 < code_ratio < 0.6:
                score += 0.3
            elif level == 'advanced' and code_ratio > 0.4:
                score += 0.3
            
            scores[level] = min(score, 1.0)
        
        return scores
    
    def _assess_technical_complexity(self, text: str) -> Dict[str, float]:
        """Assess difficulty based on technical term complexity"""
        scores = {'beginner': 0.0, 'intermediate': 0.0, 'advanced': 0.0}
        
        # Count technical terms by complexity
        high_complexity_count = sum(1 for term in self.technical_complexity['high_complexity_terms'] 
                                   if term.lower() in text)
        medium_complexity_count = sum(1 for term in self.technical_complexity['medium_complexity_terms'] 
                                    if term.lower() in text)
        low_complexity_count = sum(1 for term in self.technical_complexity['low_complexity_terms'] 
                                 if term.lower() in text)
        
        # Score based on complexity distribution
        total_terms = high_complexity_count + medium_complexity_count + low_complexity_count
        
        if total_terms > 0:
            scores['beginner'] = min(low_complexity_count / total_terms, 1.0)
            scores['intermediate'] = min(medium_complexity_count / total_terms, 1.0)
            scores['advanced'] = min(high_complexity_count / total_terms, 1.0)
        
        return scores
    
    def _assess_content_structure(self, content: str) -> Dict[str, float]:
        """Assess difficulty based on content structure"""
        scores = {'beginner': 0.0, 'intermediate': 0.0, 'advanced': 0.0}
        
        # Count headers by depth
        headers = re.findall(r'<h([1-6])[^>]*>(.*?)</h[1-6]>', content, re.IGNORECASE)
        header_depths = [int(h[0]) for h in headers]
        max_depth = max(header_depths) if header_depths else 1
        
        # Analyze section patterns
        section_text = ' '.join([h[1].lower() for h in headers])
        
        for level, structure in self.structure_signals.items():
            score = 0.0
            
            # Header depth matching
            if level == 'beginner' and max_depth <= 2:
                score += 0.3
            elif level == 'intermediate' and 2 <= max_depth <= 4:
                score += 0.3
            elif level == 'advanced' and max_depth >= 3:
                score += 0.3
            
            # Section pattern matching
            for section in structure['sections']:
                if section.lower() in section_text:
                    score += 0.1
            
            scores[level] = min(score, 1.0)
        
        return scores
    
    def _assess_content_length(self, content: str) -> Dict[str, float]:
        """Assess difficulty based on content length and depth"""
        scores = {'beginner': 0.0, 'intermediate': 0.0, 'advanced': 0.0}
        
        word_count = len(content.split())
        
        # Length-based scoring
        if word_count < 1000:
            scores['beginner'] += 0.4
        elif 1000 <= word_count < 3000:
            scores['intermediate'] += 0.4
        elif word_count >= 3000:
            scores['advanced'] += 0.4
        
        # Depth indicators
        if 'advanced' in content.lower() or 'expert' in content.lower():
            scores['advanced'] += 0.3
        if 'basic' in content.lower() or 'simple' in content.lower():
            scores['beginner'] += 0.3
        
        return scores
    
    def _assess_audience_signals(self, text: str) -> Dict[str, float]:
        """Assess difficulty based on audience signals"""
        scores = {'beginner': 0.0, 'intermediate': 0.0, 'advanced': 0.0}
        
        # Audience-specific phrases
        audience_indicators = {
            'beginner': [
                'no prior knowledge', 'assumes no background', 'for beginners',
                'getting started', 'first time', 'new to', 'introduction'
            ],
            'intermediate': [
                'assumes basic knowledge', 'familiar with', 'working knowledge',
                'experience with', 'practical', 'hands-on'
            ],
            'advanced': [
                'for advanced users', 'expert level', 'deep technical',
                'production ready', 'enterprise grade', 'optimization'
            ]
        }
        
        for level, indicators in audience_indicators.items():
            score = 0.0
            for indicator in indicators:
                if indicator.lower() in text:
                    score += 0.2
            scores[level] = min(score, 1.0)
        
        return scores
    
    def _combine_scores(self, all_scores: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """Combine all assessment scores with weights"""
        weights = {
            'keyword': 0.25,
            'code': 0.20,
            'technical': 0.20,
            'structure': 0.15,
            'length': 0.10,
            'audience': 0.10
        }
        
        final_scores = {'beginner': 0.0, 'intermediate': 0.0, 'advanced': 0.0}
        
        for category, category_scores in all_scores.items():
            weight = weights.get(category, 0.1)
            for level, score in category_scores.items():
                final_scores[level] += score * weight
        
        return final_scores
    
    def _calculate_confidence(self, scores: Dict[str, float]) -> float:
        """Calculate confidence in the assessment"""
        max_score = max(scores.values())
        second_max = sorted(scores.values(), reverse=True)[1]
        
        # Higher confidence if there's a clear winner
        confidence = (max_score - second_max) / max_score if max_score > 0 else 0
        return min(confidence, 1.0)
    
    def _get_keyword_matches(self, text: str) -> Dict[str, List[str]]:
        """Get keyword matches for each difficulty level"""
        matches = {'beginner': [], 'intermediate': [], 'advanced': []}
        
        for level, indicators in self.difficulty_indicators.items():
            for keyword in indicators['keywords']:
                if keyword.lower() in text.lower():
                    matches[level].append(keyword)
        
        return matches
    
    def _get_technical_terms(self, text: str) -> Dict[str, List[str]]:
        """Get technical terms found in content"""
        found_terms = {
            'high_complexity': [],
            'medium_complexity': [],
            'low_complexity': []
        }
        
        for term in self.technical_complexity['high_complexity_terms']:
            if term.lower() in text.lower():
                found_terms['high_complexity'].append(term)
        
        for term in self.technical_complexity['medium_complexity_terms']:
            if term.lower() in text.lower():
                found_terms['medium_complexity'].append(term)
        
        for term in self.technical_complexity['low_complexity_terms']:
            if term.lower() in text.lower():
                found_terms['low_complexity'].append(term)
        
        return found_terms
    
    def _get_code_indicators(self, content: str) -> Dict[str, List[str]]:
        """Get code complexity indicators"""
        indicators = {'beginner': [], 'intermediate': [], 'advanced': []}
        
        for level, indicators_config in self.difficulty_indicators.items():
            for pattern in indicators_config['code_patterns']:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    indicators[level].extend(matches[:3])  # Limit to 3 examples
        
        return indicators
    
    def _get_structure_indicators(self, content: str) -> Dict[str, any]:
        """Get content structure indicators"""
        headers = re.findall(r'<h([1-6])[^>]*>(.*?)</h[1-6]>', content, re.IGNORECASE)
        
        return {
            'header_count': len(headers),
            'max_depth': max([int(h[0]) for h in headers]) if headers else 0,
            'sections': [h[1] for h in headers[:5]],  # First 5 headers
            'code_blocks': len(re.findall(r'<pre><code', content))
        }

def main():
    """Demo the advanced difficulty assessment"""
    assessor = AdvancedDifficultyAssessor()
    
    # Example content for testing
    test_content = """
    <h1>Advanced Model Optimization with AWS Inferentia2</h1>
    <p>This advanced tutorial assumes you have experience with machine learning and AWS services.</p>
    
    <h2>Architecture Overview</h2>
    <p>We'll implement a sophisticated distributed inference pipeline using custom optimizations.</p>
    
    <h3>Performance Optimization</h3>
    <pre><code>
    @optimize_for_inference
    def custom_model_compiler(model, target_hardware):
        # Advanced quantization and pruning
        quantized_model = apply_quantization(model, precision='int8')
        pruned_model = apply_pruning(quantized_model, sparsity=0.7)
        return compile_for_inferentia2(pruned_model)
    </code></pre>
    
    <h3>Production Deployment</h3>
    <p>Enterprise-grade deployment with monitoring and auto-scaling.</p>
    """
    
    result = assessor.assess_difficulty(test_content, 
                                       title="Advanced Model Optimization", 
                                       description="Enterprise-grade ML optimization")
    
    print("🎯 Advanced Difficulty Assessment Results:")
    print(f"Primary Difficulty: {result['primary_difficulty'].title()}")
    print(f"Confidence: {result['confidence']:.1%}")
    print(f"\nDetailed Scores:")
    for level, score in result['detailed_scores'].items():
        print(f"  {level.title()}: {score:.1%}")
    
    print(f"\n🔍 Technical Terms Found:")
    for complexity, terms in result['signals']['technical_terms'].items():
        if terms:
            print(f"  {complexity.replace('_', ' ').title()}: {', '.join(terms[:3])}")
    
    print(f"\n📊 Structure Analysis:")
    structure = result['signals']['structure_indicators']
    print(f"  Headers: {structure['header_count']}")
    print(f"  Max Depth: {structure['max_depth']}")
    print(f"  Code Blocks: {structure['code_blocks']}")

if __name__ == "__main__":
    main() 