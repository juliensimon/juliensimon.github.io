import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
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
        { name: 'Home', url: 'https://www.julien.org' },
        { name: 'Experience', url: 'https://www.julien.org/experience' },
      ])} />
      <ExperienceContent />
    </>
  );
}
