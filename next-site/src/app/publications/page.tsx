import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema, webPageSchema } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import { SITE } from '@/lib/constants';
import PublicationsContent from './PublicationsContent';

export const metadata = buildMetadata({
  title: 'Publications',
  description:
    'Technical blog posts across AWS, Hugging Face, Medium, Arcee AI, and The AI Realist newsletter. 414+ articles on machine learning, NLP, computer vision, and AI deployment.',
  path: '/publications',
  keywords: [
    'technical writing',
    'AI blog posts',
    'machine learning articles',
    'AWS blog',
    'Hugging Face blog',
    'The AI Realist',
    'AI newsletter',
  ],
});

export default function PublicationsPage() {
  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: 'Home', url: SITE.url },
        { name: 'Publications', url: `${SITE.url}/publications` },
      ])} />
      <StructuredData data={webPageSchema(
        'Publications',
        '414+ technical blog posts across AWS, Hugging Face, Medium, and Arcee AI.',
        `${SITE.url}/publications`,
      )} />
      <PublicationsContent />
    </>
  );
}
