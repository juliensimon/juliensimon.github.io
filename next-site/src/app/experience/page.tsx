import { buildMetadata } from '@/lib/metadata';
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
  return <ExperienceContent />;
}
