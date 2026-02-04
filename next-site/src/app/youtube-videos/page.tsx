import { buildMetadata } from '@/lib/metadata';
import YouTubeContent from './YouTubeContent';

export const metadata = buildMetadata({
  title: 'YouTube Videos',
  description:
    '445K+ subscribers. Tutorials, demos, and deep-dives on AI, machine learning, Hugging Face, and AWS services.',
  path: '/youtube-videos',
  keywords: [
    'YouTube',
    'AI tutorials',
    'machine learning videos',
    'Hugging Face demos',
    'tech education',
  ],
});

export default function YouTubeVideosPage() {
  return <YouTubeContent />;
}
