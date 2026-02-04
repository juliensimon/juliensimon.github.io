import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
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
  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: 'Home', url: 'https://www.julien.org' },
        { name: 'Books', url: 'https://www.julien.org/books' },
      ])} />
      <BooksContent />
    </>
  );
}
