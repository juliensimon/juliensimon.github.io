import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema, bookSchema, webPageSchema, faqSchema, BOOKS_FAQS } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import Breadcrumbs from '@/components/ui/Breadcrumbs';
import { SITE } from '@/lib/constants';
import { BOOKS } from '@/data/books';
import BooksContent from './BooksContent';

export const metadata = buildMetadata({
  title: 'Books on AI and Machine Learning by Julien Simon',
  description:
    'Books by Julien Simon on machine learning and cloud, including "Learn Amazon SageMaker" (Packt, 2 editions) — the first book ever published on Amazon SageMaker.',
  path: '/books',
  keywords: [
    'AI books',
    'machine learning books',
    'Amazon SageMaker',
    'Learn Amazon SageMaker',
    'Packt Publishing',
    'technical author',
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
        'Books by Julien Simon on machine learning and cloud, including "Learn Amazon SageMaker" (Packt Publishing, 2 editions) — the first book ever published on Amazon SageMaker.',
        `${SITE.url}/books`,
      )} />
      {BOOKS.map((book) => (
        <StructuredData key={book.title} data={bookSchema(book)} />
      ))}
      <StructuredData data={faqSchema(BOOKS_FAQS, `${SITE.url}/books`)} />
      <Breadcrumbs items={[
        { name: 'Home', href: '/' },
        { name: 'Books', href: '/books' },
      ]} />
      <BooksContent />
    </>
  );
}
