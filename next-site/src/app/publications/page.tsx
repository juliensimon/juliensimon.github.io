import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
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
  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: 'Home', url: 'https://www.julien.org' },
        { name: 'Publications', url: 'https://www.julien.org/publications' },
      ])} />
      <PublicationsContent />
    </>
  );
}
