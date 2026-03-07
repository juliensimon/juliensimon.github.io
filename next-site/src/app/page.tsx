import { buildMetadata } from '@/lib/metadata';
import { webSiteSchema, webPageSchema, profilePageSchema, faqSchema, HOMEPAGE_FAQS } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import { SITE } from '@/lib/constants';
import HomeContent from './HomeContent';

export const metadata = buildMetadata({
  title: 'AI Operating Partner & Expert in Small Language Models',
  description:
    'AI Operating Partner at Fortino Capital. 30+ years accelerating cloud and AI across PE/VC portfolios. Expert in Small Language Models and enterprise AI. Author of The AI Realist newsletter.',
  path: '/',
  keywords: [
    'AI expert',
    'machine learning',
    'PE AI strategy',
    'cloud computing',
    'Hugging Face',
    'AWS',
    'The AI Realist',
    'AI newsletter',
  ],
});

export default function HomePage() {
  return (
    <>
      <StructuredData data={webSiteSchema()} />
      <StructuredData data={profilePageSchema()} />
      <StructuredData data={webPageSchema(
        'Julien Simon - AI Operating Partner at Fortino Capital',
        'AI Operating Partner at Fortino Capital. 30+ years accelerating cloud and AI across PE/VC portfolios. Expert in Small Language Models and enterprise AI. Author of The AI Realist newsletter.',
        SITE.url,
      )} />
      <StructuredData data={faqSchema(HOMEPAGE_FAQS, SITE.url)} />
      <HomeContent />
    </>
  );
}
