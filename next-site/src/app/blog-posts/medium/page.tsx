import { buildMetadata } from '@/lib/metadata';
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
  return <MediumContent />;
}
