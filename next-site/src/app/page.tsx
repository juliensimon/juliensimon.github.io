import { buildMetadata } from '@/lib/metadata';
import { webSiteSchema, webPageSchema, profilePageSchema, faqSchema, HOMEPAGE_FAQS } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import { SITE } from '@/lib/constants';
import { TOTAL_ARTICLES } from '@/data/publications';
import { SPEAKING_STATS } from '@/data/speaking';
import { YOUTUBE_STATS } from '@/data/youtube';
import HomeContent from './HomeContent';

const HOME_DESCRIPTION = `Julien Simon — AI expert, Operating Partner at Fortino Capital. ${SPEAKING_STATS.totalEvents}+ talks, ${TOTAL_ARTICLES}+ articles, ${YOUTUBE_STATS.subscriberCount}K YouTube subscribers. Former AWS & Hugging Face. Author of The AI Realist.`;

export const metadata = buildMetadata({
  title: 'AI Operating Partner & Expert in Small Language Models',
  description: HOME_DESCRIPTION,
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
        HOME_DESCRIPTION,
        SITE.url,
      )} />
      <StructuredData data={faqSchema(HOMEPAGE_FAQS, SITE.url)} />
      <HomeContent />
    </>
  );
}
