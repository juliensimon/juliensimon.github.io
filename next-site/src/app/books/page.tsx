import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema, bookSchema, webPageSchema } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import { SITE } from '@/lib/constants';
import { BOOKS } from '@/data/books';
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
        { name: 'Home', url: SITE.url },
        { name: 'Books', url: `${SITE.url}/books` },
      ])} />
      <StructuredData data={webPageSchema(
        'Books',
        'Published books on AI and machine learning, including "Learn Amazon SageMaker" and other technical resources.',
        `${SITE.url}/books`,
      )} />
      {BOOKS.map((book) => (
        <StructuredData key={book.title} data={bookSchema(book)} />
      ))}
      <BooksContent />
    </>
  );
}
