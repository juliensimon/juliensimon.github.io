import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import AWSContent from './AWSContent';

export const metadata = buildMetadata({
  title: 'AWS Blog Posts',
  description:
    '68+ technical articles on AWS AI/ML services including SageMaker, Rekognition, Comprehend, and more.',
  path: '/blog-posts/aws',
  keywords: [
    'AWS blog',
    'Amazon SageMaker',
    'AWS AI',
    'AWS machine learning',
    'cloud AI services',
  ],
});

export default function AWSBlogPage() {
  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: 'Home', url: 'https://www.julien.org' },
        { name: 'Publications', url: 'https://www.julien.org/publications' },
        { name: 'AWS Blog Posts', url: 'https://www.julien.org/blog-posts/aws' },
      ])} />
      <AWSContent />
    </>
  );
}
