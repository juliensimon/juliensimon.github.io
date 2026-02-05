import type { BlogPost } from '@/components/ui/BlogListingPage';
import { AWS_POSTS } from './blog-listings/aws';
import { AWS_MEDIUM_POSTS } from './blog-listings/aws-medium';
import { ARCEE_POSTS } from './blog-listings/arcee';
import { HUGGINGFACE_POSTS } from './blog-listings/huggingface';
import { MEDIUM_POSTS } from './blog-listings/medium';

export interface BlogCategory {
  slug: string;
  title: string;
  subtitle: string;
  description: string;
  keywords: string[];
  posts: BlogPost[];
}

export const BLOG_CATEGORIES: Record<string, BlogCategory> = {
  aws: {
    slug: 'aws',
    title: 'AWS Blog Posts',
    subtitle: `${AWS_POSTS.length} technical articles on AWS AI/ML services`,
    description: `${AWS_POSTS.length}+ technical articles on AWS AI/ML services including SageMaker, Rekognition, Comprehend, and more.`,
    keywords: ['AWS blog', 'Amazon SageMaker', 'AWS AI', 'AWS machine learning', 'cloud AI services'],
    posts: AWS_POSTS,
  },
  'aws-medium': {
    slug: 'aws-medium',
    title: 'AWS Medium Posts',
    subtitle: `${AWS_MEDIUM_POSTS.length} cross-published AWS technical articles on Medium`,
    description: `${AWS_MEDIUM_POSTS.length} technical articles on AWS AI/ML services cross-published on Medium.`,
    keywords: ['AWS Medium', 'AWS tutorials', 'Amazon SageMaker tutorials', 'AWS AI guides'],
    posts: AWS_MEDIUM_POSTS,
  },
  arcee: {
    slug: 'arcee',
    title: 'Arcee AI Blog Posts',
    subtitle: `${ARCEE_POSTS.length} articles on Small Language Models and practical AI deployment`,
    description: `${ARCEE_POSTS.length} articles on Small Language Models, model merging, and practical enterprise AI deployment from Arcee AI.`,
    keywords: ['Arcee AI', 'Small Language Models', 'SLM', 'model merging', 'enterprise AI'],
    posts: ARCEE_POSTS,
  },
  huggingface: {
    slug: 'huggingface',
    title: 'Hugging Face Blog Posts',
    subtitle: `${HUGGINGFACE_POSTS.length} articles on transformer models and the HF ecosystem`,
    description: `${HUGGINGFACE_POSTS.length} articles on transformers, Hugging Face Hub, Inference Endpoints, and the ML ecosystem.`,
    keywords: ['Hugging Face', 'transformers', 'NLP', 'machine learning', 'HF Hub'],
    posts: HUGGINGFACE_POSTS,
  },
  medium: {
    slug: 'medium',
    title: 'Medium Articles',
    subtitle: `${MEDIUM_POSTS.length} technical deep-dives and industry analysis`,
    description: `${MEDIUM_POSTS.length} technical deep-dives on machine learning, AI, and cloud computing on Medium.`,
    keywords: ['Medium blog', 'AI articles', 'machine learning tutorials', 'tech blog'],
    posts: MEDIUM_POSTS,
  },
};

export const BLOG_CATEGORY_SLUGS = Object.keys(BLOG_CATEGORIES);
