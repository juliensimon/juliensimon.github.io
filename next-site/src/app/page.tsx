import { buildMetadata } from '@/lib/metadata';
import { webSiteSchema, faqSchema, HOMEPAGE_FAQS } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import HomeContent from './HomeContent';

export const metadata = buildMetadata({
  title: 'AI Operating Partner & Expert in Small Language Models',
  description:
    'AI Operating Partner at Fortino Capital. 30+ years accelerating cloud and AI across PE/VC portfolios. Expert in Small Language Models and enterprise AI.',
  path: '/',
  keywords: [
    'AI expert',
    'machine learning',
    'PE AI strategy',
    'cloud computing',
    'Hugging Face',
    'AWS',
  ],
});

export default function HomePage() {
  return (
    <>
      <StructuredData data={webSiteSchema()} />
      <StructuredData data={faqSchema(HOMEPAGE_FAQS)} />
      <HomeContent />
    </>
  );
}
