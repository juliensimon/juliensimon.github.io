import { buildMetadata } from '@/lib/metadata';
import HuggingFaceContent from './HuggingFaceContent';

export const metadata = buildMetadata({
  title: 'Hugging Face Blog Posts',
  description:
    '25+ articles on transformer models, the Hugging Face ecosystem, model optimization, and NLP best practices.',
  path: '/blog-posts/huggingface',
  keywords: [
    'Hugging Face',
    'transformers',
    'NLP',
    'model optimization',
    'inference endpoints',
  ],
});

export default function HuggingFaceBlogPage() {
  return <HuggingFaceContent />;
}
