import { buildMetadata } from '@/lib/metadata';
import { webSiteSchema, webPageSchema, profilePageSchema, faqSchema, HOMEPAGE_FAQS } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import { SITE } from '@/lib/constants';
import HomeContent from './HomeContent';

export const metadata = buildMetadata({
  title: 'AI Operating Partner & Expert in Small Language Models',
  description:
    'Julien Simon — AI expert, Operating Partner at Fortino Capital. 684 talks, 417 articles, 494K YouTube subscribers. Former AWS & Hugging Face. Author of The AI Realist.',
  path: '/',
  keywords: [
    'AI expert',
    'machine learning',
    'enterprise AI strategy',
    'cloud computing',
    'Hugging Face',
    'AWS',
    'The AI Realist',
    'AI newsletter',
    'Fortino Capital',
    'julien ai',
  ],
});

export default function HomePage() {
  return (
    <>
      <StructuredData data={webSiteSchema()} />
      <StructuredData data={profilePageSchema()} />
      <StructuredData data={webPageSchema(
        'Julien Simon - AI Operating Partner at Fortino Capital',
        'Julien Simon — AI expert, Operating Partner at Fortino Capital. 684 talks, 417 articles, 494K YouTube subscribers. Former AWS & Hugging Face. Author of The AI Realist.',
        SITE.url,
      )} />
      <StructuredData data={faqSchema(HOMEPAGE_FAQS, SITE.url)} />
      <HomeContent />
    </>
  );
}
