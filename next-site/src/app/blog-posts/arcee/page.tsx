import { buildMetadata } from '@/lib/metadata';
import ArceeContent from './ArceeContent';

export const metadata = buildMetadata({
  title: 'Arcee AI Blog Posts',
  description:
    'Articles on Small Language Models, model merging, practical AI deployment, and enterprise AI strategies with Arcee AI.',
  path: '/blog-posts/arcee',
  keywords: [
    'Arcee AI',
    'Small Language Models',
    'model merging',
    'AI deployment',
    'enterprise AI',
  ],
});

export default function ArceeBlogPage() {
  return <ArceeContent />;
}
