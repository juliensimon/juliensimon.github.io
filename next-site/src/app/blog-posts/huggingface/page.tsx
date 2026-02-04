import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
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
  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: 'Home', url: 'https://www.julien.org' },
        { name: 'Publications', url: 'https://www.julien.org/publications' },
        { name: 'Hugging Face Blog Posts', url: 'https://www.julien.org/blog-posts/huggingface' },
      ])} />
      <HuggingFaceContent />
    </>
  );
}
