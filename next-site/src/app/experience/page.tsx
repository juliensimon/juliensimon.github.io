import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema, webPageSchema } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import { SITE } from '@/lib/constants';
import ExperienceContent from './ExperienceContent';

export const metadata = buildMetadata({
  title: 'Experience',
  description:
    '30+ years of professional experience in AI, cloud computing, and software engineering. From Apple to AWS, Hugging Face, and Fortino Capital.',
  path: '/experience',
  keywords: [
    'career',
    'AI leadership',
    'AWS',
    'Hugging Face',
    'Apple',
    'CTO',
    'VP Engineering',
  ],
});

export default function ExperiencePage() {
  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: 'Home', url: SITE.url },
        { name: 'Experience', url: `${SITE.url}/experience` },
      ])} />
      <StructuredData data={webPageSchema(
        'Experience',
        '30+ years of professional experience in AI, cloud computing, and software engineering.',
        'https://www.julien.org/experience',
      )} />
      <ExperienceContent />
    </>
  );
}
