import { buildMetadata } from '@/lib/metadata';
import BooksContent from './BooksContent';

export const metadata = buildMetadata({
  title: 'Books',
  description:
    'Published books on AI and machine learning, including "Learn Amazon SageMaker" and other technical resources.',
  path: '/books',
  keywords: [
    'AI books',
    'machine learning books',
    'Amazon SageMaker',
    'technical author',
    'O\'Reilly',
  ],
});

export default function BooksPage() {
  return <BooksContent />;
}
