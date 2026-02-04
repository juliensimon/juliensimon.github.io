import { buildMetadata } from '@/lib/metadata';
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
  return <AWSMediumContent />;
}
