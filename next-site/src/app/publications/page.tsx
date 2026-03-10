import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema, webPageSchema, faqSchema, PUBLICATIONS_FAQS } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import Breadcrumbs from '@/components/ui/Breadcrumbs';
import { SITE } from '@/lib/constants';
import PublicationsContent from './PublicationsContent';

export const metadata = buildMetadata({
  title: 'Publications',
  description:
    '417 articles on AI, machine learning, and cloud computing. Published on AWS Blog, Hugging Face, Medium, and The AI Realist newsletter by Julien Simon.',
  path: '/publications',
  keywords: [
    'technical writing',
    'AI blog posts',
    'machine learning articles',
    'AWS blog',
    'Hugging Face blog',
    'The AI Realist',
    'AI newsletter',
  ],
});

export default function PublicationsPage() {
  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: 'Home', url: SITE.url },
        { name: 'Publications', url: `${SITE.url}/publications` },
      ])} />
      <StructuredData data={webPageSchema(
        'Publications',
        '417 articles on AI, machine learning, and cloud computing by Julien Simon.',
        `${SITE.url}/publications`,
      )} />
      <StructuredData data={faqSchema(PUBLICATIONS_FAQS, `${SITE.url}/publications`)} />
      <Breadcrumbs items={[
        { name: 'Home', href: '/' },
        { name: 'Publications', href: '/publications' },
      ]} />
      <PublicationsContent />
    </>
  );
}
