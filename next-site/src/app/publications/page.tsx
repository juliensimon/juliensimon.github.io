import { buildMetadata } from '@/lib/metadata';
import PublicationsContent from './PublicationsContent';

export const metadata = buildMetadata({
  title: 'Publications',
  description:
    'Technical blog posts across AWS, Hugging Face, Medium, and Arcee AI. 300+ articles on machine learning, NLP, computer vision, and AI deployment.',
  path: '/publications',
  keywords: [
    'technical writing',
    'AI blog posts',
    'machine learning articles',
    'AWS blog',
    'Hugging Face blog',
  ],
});

export default function PublicationsPage() {
  return <PublicationsContent />;
}
