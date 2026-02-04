import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import ArceeContent from './ArceeContent';

export const metadata = buildMetadata({
  title: 'Arcee AI Blog Posts',
  description:
    'Articles on Small Language Models, model merging, practical AI deployment, and enterprise AI strategies with Arcee AI.',
  path: '/blog-posts/arcee',
  keywords: [
    'Arcee AI',
    'model merging',
    'AI deployment',
    'enterprise AI',
  ],
});

export default function ArceeBlogPage() {
  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: 'Home', url: 'https://www.julien.org' },
        { name: 'Publications', url: 'https://www.julien.org/publications' },
        { name: 'Arcee AI Blog Posts', url: 'https://www.julien.org/blog-posts/arcee' },
      ])} />
      <ArceeContent />
    </>
  );
}
