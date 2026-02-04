import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import AWSMediumContent from './AWSMediumContent';

export const metadata = buildMetadata({
  title: 'AWS Medium Posts',
  description:
    'Cross-published AWS technical content on Medium covering AI/ML services, best practices, and tutorials.',
  path: '/blog-posts/aws-medium',
  keywords: [
    'AWS Medium',
    'cross-published',
    'AWS tutorials',
    'cloud AI',
    'ML services',
  ],
});

export default function AWSMediumBlogPage() {
  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: 'Home', url: 'https://www.julien.org' },
        { name: 'Publications', url: 'https://www.julien.org/publications' },
        { name: 'AWS Medium Posts', url: 'https://www.julien.org/blog-posts/aws-medium' },
      ])} />
      <AWSMediumContent />
    </>
  );
}
