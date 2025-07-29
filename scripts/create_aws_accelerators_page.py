#!/usr/bin/env python3
"""
NLP-First AWS Accelerators Thematic Page Generator
Uses advanced NLP techniques for content analysis and classification
"""

import os
import re
import json
from collections import defaultdict, Counter
from typing import Dict, List, Optional, Tuple
from datetime import datetime, date
from dataclasses import dataclass
import nltk
import spacy
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag

@dataclass
class ContentAnalysis:
    """Structured content analysis results"""
    file_path: str
    title: str
    description: str
    date: Optional[date]
    platform: str
    url: str
    relevance_score: float
    difficulty_level: str
    technical_entities: List[str]
    semantic_topics: List[str]
    content_structure: Dict
    nlp_confidence: float

class NLPFirstAWSAcceleratorsGenerator:
    """NLP-first generator for AWS AI accelerators content"""
    
    def __init__(self):
        # Initialize NLP pipeline
        self._initialize_nlp()
        
        # Define semantic domains for AWS accelerators - user specified keywords
        self.accelerator_domains = {
            'aws_accelerators': ['trainium', 'inferentia', 'trn', 'inf', 'neuron', 'neuron sdk'],
            'aws_services': ['sagemaker', 'ec2', 'aws'],
            'aws_deployment': ['deploy', 'inference', 'training'],
            'aws_development': ['sdk', 'compiler', 'runtime']
        }
        
        self.content_items = []
    
    def _initialize_nlp(self):
        """Initialize NLP components with proper error handling"""
        try:
            # Download required NLTK data
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            
            # Load spaCy model with word vectors
            self.nlp = spacy.load('en_core_web_md')
            self.stop_words = set(stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer()
            
            print("✅ NLP pipeline initialized successfully")
            
        except Exception as e:
            print(f"❌ NLP initialization failed: {e}")
            self.nlp = None
            self.stop_words = set()
            self.lemmatizer = None
    
    def analyze_content(self) -> None:
        """Analyze all content using NLP-first approach"""
        content_dirs = ['blog', 'youtube']
        
        for content_dir in content_dirs:
            if os.path.exists(content_dir):
                self._scan_directory_nlp(content_dir)
    
    def _scan_directory_nlp(self, directory: str) -> None:
        """Scan directory using NLP-based filtering"""
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    self._analyze_file_nlp(file_path)
    
    def _analyze_file_nlp(self, file_path: str) -> None:
        """Analyze file using NLP-first approach"""
        try:
            # Skip root-level index files
            if file_path.endswith('index.html') and file_path.count('/') <= 1:
                return
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract basic metadata
            title = self._extract_title_nlp(content)
            description = self._extract_description_nlp(content)
            date = self._extract_date_nlp(file_path)
            platform = self._extract_platform_nlp(file_path)
            url = self._extract_url_nlp(file_path)
            
            # Skip generic pages using NLP
            if self._is_generic_page_nlp(title, content):
                return
            
            # Perform comprehensive NLP analysis
            analysis = self._perform_nlp_analysis(content, title, file_path)
            
            if analysis and analysis.relevance_score >= 0.3:  # Lower threshold but stricter scoring
                self.content_items.append(analysis)
                
        except Exception as e:
            pass  # Silently skip problematic files
    
    def _perform_nlp_analysis(self, content: str, title: str, file_path: str) -> Optional[ContentAnalysis]:
        """Perform comprehensive NLP analysis of content"""
        if not self.nlp:
            return None
        
        try:
            # Clean and prepare text for NLP
            clean_content = self._preprocess_text(content)
            clean_title = self._preprocess_text(title)
            
            # Create spaCy documents
            content_doc = self.nlp(clean_content[:10000])  # Limit for performance
            title_doc = self.nlp(clean_title)
            
            # Analyze semantic relevance
            relevance_score = self._calculate_semantic_relevance(content_doc, title_doc)
            
            # Extract technical entities
            technical_entities = self._extract_technical_entities_nlp(content_doc)
            
            # Identify semantic topics
            semantic_topics = self._identify_semantic_topics(content_doc)
            
            # Analyze content structure
            content_structure = self._analyze_content_structure_nlp(content_doc)
            
            # Assess difficulty using NLP
            difficulty_level = self._assess_difficulty_nlp(content_doc, title_doc)
            
            # Calculate NLP confidence
            nlp_confidence = self._calculate_nlp_confidence(content_doc, title_doc)
            
            # Extract metadata
            description = self._extract_description_nlp(content)
            date = self._extract_date_nlp(file_path)
            platform = self._extract_platform_nlp(file_path)
            url = self._extract_url_nlp(file_path)
            
            return ContentAnalysis(
                file_path=file_path,
                title=title,
                description=description,
                date=date,
                platform=platform,
                url=url,
                relevance_score=relevance_score,
                difficulty_level=difficulty_level,
                technical_entities=technical_entities,
                semantic_topics=semantic_topics,
                content_structure=content_structure,
                nlp_confidence=nlp_confidence
            )
            
        except Exception as e:
            return None
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for NLP analysis"""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _calculate_semantic_relevance(self, content_doc, title_doc) -> float:
        """Calculate semantic relevance using NLP - AWS accelerators specific"""
        if not content_doc or not title_doc:
            return 0.0
        
        # AWS accelerator specific terms that must be present (user specified)
        aws_accelerator_terms = [
            'trainium', 'inferentia', 'neuron', 'neuron sdk'
        ]
        
        # Additional AWS accelerator patterns
        aws_accelerator_patterns = [
            'trn1', 'trn2', 'inf1', 'inf2', 'aws trainium', 'aws inferentia'
        ]
        
        # Check for AWS accelerator terms in content
        content_text = content_doc.text.lower()
        title_text = title_doc.text.lower()
        
        # Count AWS accelerator terms
        aws_term_count = 0
        for term in aws_accelerator_terms:
            if term in content_text:
                aws_term_count += content_text.count(term) * 3.0  # Higher weight for content
            if term in title_text:
                aws_term_count += title_text.count(term) * 5.0   # Even higher weight for title
        
        # Count additional AWS accelerator patterns
        for pattern in aws_accelerator_patterns:
            if pattern in content_text:
                aws_term_count += content_text.count(pattern) * 3.0
            if pattern in title_text:
                aws_term_count += title_text.count(pattern) * 5.0
        
        # Require at least one AWS accelerator term to be considered relevant
        if aws_term_count == 0:
            return 0.0
        
        # Additional scoring for related AWS services
        aws_service_terms = ['sagemaker', 'ec2', 'aws']
        service_term_count = 0
        for term in aws_service_terms:
            if term in content_text:
                service_term_count += content_text.count(term) * 1.0
            if term in title_text:
                service_term_count += title_text.count(term) * 2.0
        
        # Technical ML terms (lower weight)
        ml_terms = ['inference', 'training', 'deployment', 'sdk', 'compiler']
        ml_term_count = 0
        for term in ml_terms:
            if term in content_text:
                ml_term_count += content_text.count(term) * 0.5
            if term in title_text:
                ml_term_count += title_text.count(term) * 1.0
        
        # Calculate total score
        total_score = aws_term_count + service_term_count + ml_term_count
        
        # Normalize to 0-1 range, with higher threshold for relevance
        normalized_score = min(total_score / 50.0, 1.0)
        
        # Boost score if AWS accelerator terms are in title
        if (any(term in title_text for term in aws_accelerator_terms) or 
            any(pattern in title_text for pattern in aws_accelerator_patterns)):
            normalized_score = min(normalized_score * 1.5, 1.0)
        
        return normalized_score
    
    def _extract_technical_entities_nlp(self, doc) -> List[str]:
        """Extract technical entities using NLP"""
        entities = []
        
        # AWS accelerator specific terms
        accelerator_terms = [
            'inferentia', 'trainium', 'neuron', 'sagemaker', 'ec2', 'aws',
            'pytorch', 'tensorflow', 'huggingface', 'transformer', 'model',
            'inference', 'training', 'optimization', 'deployment', 'compiler',
            'sdk', 'framework', 'quantization', 'pruning', 'distillation'
        ]
        
        # Named entities (organizations, products, locations)
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'GPE']:
                entities.append(ent.text)
        
        # Technical noun phrases with technical terms
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.lower()
            if (len(chunk.text) > 3 and 
                any(term in chunk_text for term in accelerator_terms)):
                entities.append(chunk.text)
        
        # Technical terms from accelerator domains
        for domain_terms in self.accelerator_domains.values():
            for term in domain_terms:
                if term in doc.text.lower():
                    # Find the actual token that contains this term
                    for token in doc:
                        if term in token.text.lower() and len(token.text) > 2:
                            entities.append(token.text)
        
        # Filter and deduplicate
        filtered_entities = []
        for entity in entities:
            entity_lower = entity.lower()
            # Skip common non-technical words
            if (entity_lower not in ['this', 'that', 'these', 'those', 'here', 'there'] and
                len(entity) > 2 and
                not entity_lower in ['color', 'margin', 'decoration', 'description']):
                filtered_entities.append(entity)
        
        return list(set(filtered_entities))[:10]  # Limit to top 10
    
    def _identify_semantic_topics(self, doc) -> List[str]:
        """Identify semantic topics using NLP"""
        topics = []
        
        # AWS accelerator specific topics
        accelerator_topics = [
            'inferentia', 'trainium', 'neuron', 'sagemaker', 'ec2', 'aws',
            'pytorch', 'tensorflow', 'huggingface', 'transformer', 'model',
            'inference', 'training', 'optimization', 'deployment', 'compiler',
            'sdk', 'framework', 'quantization', 'pruning', 'distillation',
            'performance', 'latency', 'throughput', 'acceleration', 'hardware'
        ]
        
        # Extract key phrases that contain accelerator terms
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.lower()
            if (len(chunk.text) > 3 and 
                any(topic in chunk_text for topic in accelerator_topics)):
                topics.append(chunk.text)
        
        # Extract technical terms from accelerator domains
        for domain_terms in self.accelerator_domains.values():
            for term in domain_terms:
                if term in doc.text.lower():
                    # Find the actual token that contains this term
                    for token in doc:
                        if term in token.text.lower() and len(token.text) > 2:
                            topics.append(token.text)
        
        # Filter and deduplicate
        filtered_topics = []
        for topic in topics:
            topic_lower = topic.lower()
            # Skip common non-technical words
            if (topic_lower not in ['this', 'that', 'these', 'those', 'here', 'there'] and
                len(topic) > 2 and
                not topic_lower in ['color', 'margin', 'decoration', 'description']):
                filtered_topics.append(topic)
        
        # Count and return most frequent topics
        topic_counter = Counter(filtered_topics)
        return [topic for topic, count in topic_counter.most_common(5)]
    
    def _analyze_content_structure_nlp(self, doc) -> Dict:
        """Analyze content structure using NLP"""
        sentences = list(doc.sents)
        
        structure = {
            'sentence_count': len(sentences),
            'avg_sentence_length': sum(len(sent) for sent in sentences) / len(sentences) if sentences else 0,
            'complex_sentences': sum(1 for sent in sentences if len(sent) > 25),
            'technical_sentences': sum(1 for sent in sentences if any(term in sent.text.lower() for domain in self.accelerator_domains.values() for term in domain)),
            'pos_distribution': Counter(token.pos_ for token in doc),
            'entity_count': len(doc.ents),
            'noun_phrases': len(list(doc.noun_chunks))
        }
        
        return structure
    
    def _assess_difficulty_nlp(self, content_doc, title_doc) -> str:
        """Assess difficulty using comprehensive NLP analysis"""
        if not content_doc:
            return 'intermediate'
        
        # Technical complexity analysis
        tech_complexity = self._analyze_technical_complexity_nlp(content_doc)
        
        # Linguistic complexity analysis
        ling_complexity = self._analyze_linguistic_complexity_nlp(content_doc)
        
        # Content structure analysis
        structure_complexity = self._analyze_structure_complexity_nlp(content_doc)
        
        # Audience signal analysis
        audience_complexity = self._analyze_audience_signals_nlp(content_doc, title_doc)
        
        # Combine scores with weights
        total_score = (
            tech_complexity * 0.35 +
            ling_complexity * 0.25 +
            structure_complexity * 0.25 +
            audience_complexity * 0.15
        )
        
        # Determine difficulty level
        if total_score >= 0.7:
            return 'advanced'
        elif total_score >= 0.4:
            return 'intermediate'
        else:
            return 'beginner'
    
    def _analyze_technical_complexity_nlp(self, doc) -> float:
        """Analyze technical complexity using NLP"""
        complexity_score = 0.0
        
        # Count technical entities
        tech_entities = len([ent for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT', 'GPE']])
        complexity_score += min(tech_entities * 0.1, 0.3)
        
        # Count technical noun phrases
        tech_nouns = len([chunk for chunk in doc.noun_chunks if len(chunk.text) > 5])
        complexity_score += min(tech_nouns * 0.05, 0.2)
        
        # Count complex sentences with technical terms
        complex_sentences = 0
        for sent in doc.sents:
            if len(sent) > 20:
                tech_terms = sum(1 for token in sent if any(term in token.text.lower() for domain in self.accelerator_domains.values() for term in domain))
                if tech_terms > 0:
                    complex_sentences += 1
        
        complexity_score += min(complex_sentences * 0.15, 0.3)
        
        return min(complexity_score, 1.0)
    
    def _analyze_linguistic_complexity_nlp(self, doc) -> float:
        """Analyze linguistic complexity using NLP"""
        complexity_score = 0.0
        
        # POS-based complexity
        pos_counts = Counter(token.pos_ for token in doc)
        total_tokens = len(doc)
        
        if total_tokens > 0:
            # More nouns and adjectives indicate technical content
            noun_ratio = (pos_counts.get('NOUN', 0) + pos_counts.get('PROPN', 0)) / total_tokens
            adj_ratio = pos_counts.get('ADJ', 0) / total_tokens
            verb_ratio = pos_counts.get('VERB', 0) / total_tokens
            
            pos_complexity = (noun_ratio * 0.4) + (adj_ratio * 0.3) - (verb_ratio * 0.2)
            complexity_score += min(max(pos_complexity, 0.0), 0.4)
        
        # Sentence structure complexity
        sentences = list(doc.sents)
        if sentences:
            long_sentences = sum(1 for sent in sentences if len(sent) > 25)
            complexity_score += min(long_sentences / len(sentences), 0.3)
        
        # Vocabulary complexity
        complex_words = sum(1 for token in doc if len(token.text) > 6 and not token.is_stop)
        if total_tokens > 0:
            vocab_complexity = complex_words / total_tokens
            complexity_score += min(vocab_complexity, 0.3)
        
        return min(complexity_score, 1.0)
    
    def _analyze_structure_complexity_nlp(self, doc) -> float:
        """Analyze content structure complexity using NLP"""
        complexity_score = 0.0
        
        # Count different types of content
        code_blocks = len(re.findall(r'```[\s\S]*?```', doc.text))
        complexity_score += min(code_blocks * 0.1, 0.2)
        
        # Count technical sections
        technical_sections = len(re.findall(r'(architecture|performance|optimization|deployment|configuration)', doc.text.lower()))
        complexity_score += min(technical_sections * 0.05, 0.2)
        
        # Count complex patterns
        complex_patterns = len(re.findall(r'[A-Z]{2,}|[a-z]+\.[a-z]+|[a-z]+_[a-z]+', doc.text))
        complexity_score += min(complex_patterns * 0.01, 0.2)
        
        return min(complexity_score, 1.0)
    
    def _analyze_audience_signals_nlp(self, content_doc, title_doc) -> float:
        """Analyze audience signals using NLP"""
        complexity_score = 0.0
        
        # Expert/Advanced signals
        expert_signals = [
            'advanced', 'expert', 'professional', 'enterprise', 'production',
            'optimization', 'performance', 'scaling', 'architecture', 'distributed',
            'microservices', 'kubernetes', 'monitoring', 'observability'
        ]
        
        # Beginner signals
        beginner_signals = [
            'beginner', 'introduction', 'overview', 'getting started', 'tutorial',
            'simple', 'basic', 'first time', 'hello world', 'guide'
        ]
        
        # Count signals in content
        content_text = content_doc.text.lower()
        expert_count = sum(1 for signal in expert_signals if signal in content_text)
        beginner_count = sum(1 for signal in beginner_signals if signal in content_text)
        
        # Count signals in title
        title_text = title_doc.text.lower()
        expert_count += sum(1 for signal in expert_signals if signal in title_text) * 2
        beginner_count += sum(1 for signal in beginner_signals if signal in title_text) * 2
        
        if expert_count > 0 and beginner_count == 0:
            complexity_score = min(expert_count * 0.2, 1.0)
        elif beginner_count > 0 and expert_count == 0:
            complexity_score = max(0.1, 1.0 - (beginner_count * 0.2))
        else:
            complexity_score = 0.5
        
        return complexity_score
    
    def _calculate_nlp_confidence(self, content_doc, title_doc) -> float:
        """Calculate confidence in NLP analysis"""
        confidence = 0.5  # Base confidence
        
        # Higher confidence for longer content
        if len(content_doc) > 100:
            confidence += 0.2
        
        # Higher confidence for content with entities
        if len(content_doc.ents) > 5:
            confidence += 0.2
        
        # Higher confidence for content with technical terms
        tech_terms = sum(1 for token in content_doc if any(term in token.text.lower() for domain in self.accelerator_domains.values() for term in domain))
        if tech_terms > 10:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _is_generic_page_nlp(self, title: str, content: str) -> bool:
        """Check if page is generic using NLP"""
        generic_patterns = [
            'julien simon - youtube videos',
            'julien simon - blog',
            'julien simon machine learning',
            'youtube videos -',
            'blog posts -',
            'index of',
            'directory listing'
        ]
        
        title_lower = title.lower()
        return any(pattern in title_lower for pattern in generic_patterns)
    
    # Metadata extraction methods (simplified for NLP-first approach)
    def _extract_title_nlp(self, content: str) -> str:
        """Extract title using NLP"""
        # First try to find <title> tag
        match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        # If no title tag, look for <h1> tag
        match = re.search(r'<h1[^>]*>([^<]+)</h1>', content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        return "Untitled"
    
    def _extract_description_nlp(self, content: str) -> str:
        """Extract description using NLP"""
        match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
        return match.group(1).strip() if match else ""
    
    def _extract_date_nlp(self, file_path: str) -> Optional[date]:
        """Extract date using NLP patterns"""
        date_patterns = [
            r'(\d{4})-(\d{2})-(\d{2})',
            r'(\d{4})/(\d{2})/(\d{2})',
            r'(\d{4})-(\d{2})',
            r'(\d{4})/(\d{2})',
            r'(\d{4})(\d{2})(\d{2})_'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, file_path)
            if match:
                try:
                    if len(match.groups()) == 3:
                        return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
                    elif len(match.groups()) == 2:
                        return date(int(match.group(1)), int(match.group(2)), 1)
                except (ValueError, IndexError):
                    continue
        
        return None
    
    def _extract_platform_nlp(self, file_path: str) -> str:
        """Extract platform using NLP"""
        if 'youtube' in file_path.lower():
            return 'YouTube Video'
        elif 'huggingface' in file_path.lower():
            return 'Hugging Face Blog'
        elif 'aws' in file_path.lower():
            return 'AWS Blog'
        else:
            return 'Blog Post'
    
    def _extract_url_nlp(self, file_path: str) -> str:
        """Extract URL using NLP patterns"""
        # Convert file path to URL
        url_path = file_path.replace('\\', '/')
        return f"https://julien.org/{url_path}"
    
    def generate_aws_accelerators_page(self) -> None:
        """Generate the AWS accelerators page using NLP-first approach"""
        if not self.content_items:
            print("❌ No content items found")
            return
        
        # Sort by date (most recent first) and relevance
        def sort_key(item):
            date_val = item.date or date(1900, 1, 1)
            return (-date_val.toordinal(), -item.relevance_score)
        
        self.content_items.sort(key=sort_key)
        
        # Calculate statistics
        stats = self._calculate_stats_nlp()
        
        # Generate HTML
        html_content = self._generate_html_content_nlp(stats)
        
        # Write to file
        os.makedirs('thematic-pages', exist_ok=True)
        with open('thematic-pages/aws-accelerators.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Created AWS Accelerators thematic page:")
        print(f"   📄 Total content items: {len(self.content_items)}")
        print(f"   📊 Platforms: {', '.join(set(item.platform for item in self.content_items))}")
        print(f"   🎯 Average relevance: {stats['avg_relevance_score']:.1%}")
        print(f"   📅 Date range: {stats['date_range']['earliest']} to {stats['date_range']['latest']}")
        print(f"   🤖 NLP Confidence: {stats['avg_nlp_confidence']:.1%}")
        print(f"\n📁 Page created at: thematic-pages/aws-accelerators.html")
    
    def _calculate_stats_nlp(self) -> Dict:
        """Calculate statistics using NLP-first approach"""
        platforms = list(set(item.platform for item in self.content_items))
        relevance_scores = [item.relevance_score for item in self.content_items]
        nlp_confidences = [item.nlp_confidence for item in self.content_items]
        
        dates = [item.date for item in self.content_items if item.date]
        earliest = min(dates) if dates else None
        latest = max(dates) if dates else None
        
        return {
            'total_content': len(self.content_items),
            'platforms': platforms,
            'avg_relevance_score': sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0,
            'avg_nlp_confidence': sum(nlp_confidences) / len(nlp_confidences) if nlp_confidences else 0,
            'date_range': {
                'earliest': earliest,
                'latest': latest
            }
        }
    
    def _generate_html_content_nlp(self, stats: Dict) -> str:
        """Generate HTML content using NLP-first approach"""
        content_sections = self._generate_content_sections_nlp()
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AWS AI Accelerators (Trainium, Inferentia, Neuron SDK) - Julien Simon | AI Expert</title>
    <meta name="description" content="Comprehensive expert content on AWS AI accelerators including AWS Trainium, AWS Inferentia, and Neuron SDK. Technical deep-dives, tutorials, and optimization strategies by Julien Simon.">
    
    <!-- SEO Meta Tags -->
    <meta name="keywords" content="AWS Trainium, AWS Inferentia, Neuron SDK, AWS AI accelerators, hardware acceleration, ML optimization, custom chips, Inferentia2, Trainium2">
    <meta name="author" content="Julien Simon">
    <meta name="robots" content="index, follow">
    
    <!-- Open Graph -->
    <meta property="og:title" content="AWS AI Accelerators - Julien Simon">
    <meta property="og:description" content="Expert content on AWS Trainium, Inferentia, and Neuron SDK for AI acceleration">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://julien.org/thematic-pages/aws-accelerators.html">
    
    <!-- Structured Data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "AWS AI Accelerators",
        "description": "Comprehensive expert content on AWS AI accelerators including AWS Trainium, AWS Inferentia, and Neuron SDK",
        "url": "https://julien.org/thematic-pages/aws-accelerators.html",
        "hasPart": [
            {{
                "@type": "CreativeWorkSeries",
                "name": "Expert Content on AWS AI Accelerators",
                "numberOfItems": {stats['total_content']},
                "description": "Technical deep-dives, tutorials, and optimization strategies for AWS AI accelerators"
            }}
        ],
        "author": {{
            "@type": "Person",
            "name": "Julien Simon",
            "jobTitle": "AI Technical Evangelist",
            "expertise": "AWS AI Accelerators"
        }},
        "about": [
            {{
                "@type": "DefinedTerm",
                "name": "AWS Trainium",
                "description": "AWS custom chip for ML training acceleration"
            }},
            {{
                "@type": "DefinedTerm", 
                "name": "AWS Inferentia",
                "description": "AWS custom chip for ML inference acceleration"
            }},
            {{
                "@type": "DefinedTerm",
                "name": "Neuron SDK",
                "description": "AWS SDK for developing on Trainium and Inferentia chips"
            }}
        ]
    }}
    </script>
    
    <link rel="stylesheet" href="../css/styles.css">
    <style>
        .theme-header {{
            background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
            color: white;
            padding: 3rem 0;
            margin-bottom: 2rem;
        }}
        .content-item {{
            margin-bottom: 2rem;
            padding: 1.5rem;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            background: white;
            transition: transform 0.2s;
        }}
        .content-item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        .difficulty-badge {{
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 500;
        }}
        .difficulty-beginner {{ background: #d4edda; color: #155724; }}
        .difficulty-intermediate {{ background: #fff3cd; color: #856404; }}
        .difficulty-advanced {{ background: #f8d7da; color: #721c24; }}
        .nlp-confidence {{
            font-size: 0.8rem;
            color: #6c757d;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <header class="theme-header">
        <div class="container">
            <nav>
                <a href="../index.html" style="color: white; text-decoration: none;">← Back to Home</a>
            </nav>
            
            <h1 style="margin: 2rem 0 1rem 0; font-size: 2.5rem;">AWS AI Accelerators</h1>
            <p style="font-size: 1.1rem; opacity: 0.8; margin-bottom: 1rem;">
                Custom chips for ML training and inference acceleration
            </p>
            
            <p style="font-size: 1rem; opacity: 0.9; margin-bottom: 2rem; line-height: 1.6;">
                AWS Trainium and Inferentia are custom silicon chips designed to accelerate machine learning workloads. Trainium optimizes model training with high performance and cost efficiency, while Inferentia delivers fast, low-latency inference for production deployments. The Neuron SDK provides the development tools needed to compile and optimize models for these specialized accelerators, enabling developers to achieve significant performance improvements over traditional CPU and GPU solutions.
            </p>
        </div>
    </header>
    
    <main class="container">
        <article>
            <section>
                <h2>Content</h2>
                
                {content_sections}
            </section>
        </article>
    </main>
    
    <footer style="background: #f8f9fa; padding: 2rem 0; margin-top: 3rem; text-align: center;">
        <p>Expert content by <a href="../index.html" style="color: #FF6B35;">Julien Simon</a> - AI Technical Evangelist</p>
        <p style="color: #6c757d; font-size: 0.9rem; margin-top: 0.5rem;">
            Specializing in AWS AI services, hardware acceleration, and practical AI implementation
        </p>
    </footer>
</body>
</html>"""
        
        return html
    
    def _generate_content_sections_nlp(self) -> str:
        """Generate content sections using NLP-first approach"""
        sections = []
        
        for item in self.content_items:
            # Determine icon based on platform
            icon = "📺" if "YouTube" in item.platform else "📄"
            
            # Format date
            date_str = ""
            if item.date:
                try:
                    date_str = item.date.strftime("%B %d, %Y")
                except AttributeError:
                    date_str = ""
            
            # Difficulty badge
            difficulty_class = f"difficulty-{item.difficulty_level}"
            difficulty_text = item.difficulty_level.title()
            
            # NLP confidence indicator
            confidence_text = f"🤖 NLP Confidence: {item.nlp_confidence:.1%}"
            
            # Technical entities (top 3)
            entities_text = ", ".join(item.technical_entities[:3]) if item.technical_entities else ""
            
            # Semantic topics (top 2)
            topics_text = ", ".join(item.semantic_topics[:2]) if item.semantic_topics else ""
            
            section = f"""
            <div class="content-item">
                <div style="margin-bottom: 1rem;">
                    <h3 style="margin: 0 0 0.5rem 0; color: #2c3e50;">
                        {icon} <a href="{item.url}" style="color: #2c3e50; text-decoration: none;">{item.title}</a>
                    </h3>
                    <div style="font-size: 0.9rem; color: #6c757d; margin-bottom: 1rem;">
                        <span>{item.platform}</span>
                        <span>•</span>
                        <span>{date_str}</span>
                        <span>•</span>
                        <span class="difficulty-badge {difficulty_class}">{difficulty_text}</span>
                        <span>•</span>
                        <span>🎯 Relevance: {item.relevance_score:.1%}</span>
                    </div>
                </div>
                
                <p style="color: #6c757d; font-size: 0.9rem; margin-bottom: 1rem;">
                    {item.description[:150]}{'...' if len(item.description) > 150 else ''}
                </p>
                
                <div style="margin-bottom: 1rem;">
                    <p class="nlp-confidence">{confidence_text}</p>
                </div>
            </div>"""
            
            sections.append(section)
        
        return "\n".join(sections)

def main():
    """Main function for NLP-first AWS accelerators page generation"""
    print("🔍 Analyzing content for AWS AI accelerators using NLP...")
    
    generator = NLPFirstAWSAcceleratorsGenerator()
    generator.analyze_content()
    generator.generate_aws_accelerators_page()

if __name__ == "__main__":
    main() 