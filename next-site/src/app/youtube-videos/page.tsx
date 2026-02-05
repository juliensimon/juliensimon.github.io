import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import YouTubeContent from './YouTubeContent';

export const metadata = buildMetadata({
  title: 'YouTube Videos',
  description:
    '467K+ subscribers. Tutorials, demos, and deep-dives on AI, machine learning, Hugging Face, and AWS services.',
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
  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: 'Home', url: 'https://www.julien.org' },
        { name: 'YouTube Videos', url: 'https://www.julien.org/youtube-videos' },
      ])} />
      <YouTubeContent />
    </>
  );
}
