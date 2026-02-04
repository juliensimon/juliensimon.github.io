import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import MediumContent from './MediumContent';

export const metadata = buildMetadata({
  title: 'Medium Articles',
  description:
    '200+ technical deep-dives and industry analysis on AI, machine learning, and cloud computing published on Medium.',
  path: '/blog-posts/medium',
  keywords: [
    'Medium',
    'technical articles',
    'AI analysis',
    'machine learning deep-dives',
    'industry insights',
  ],
});

export default function MediumBlogPage() {
  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: 'Home', url: 'https://www.julien.org' },
        { name: 'Publications', url: 'https://www.julien.org/publications' },
        { name: 'Medium Articles', url: 'https://www.julien.org/blog-posts/medium' },
      ])} />
      <MediumContent />
    </>
  );
}
