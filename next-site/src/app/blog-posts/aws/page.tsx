import { buildMetadata } from '@/lib/metadata';
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
  return <AWSContent />;
}
