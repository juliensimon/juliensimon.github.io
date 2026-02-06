import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema, videoObjectSchema, webPageSchema } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import { SITE } from '@/lib/constants';
import { YOUTUBE_STATS } from '@/data/youtube';
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
        { name: 'Home', url: SITE.url },
        { name: 'YouTube Videos', url: `${SITE.url}/youtube-videos` },
      ])} />
      <StructuredData data={webPageSchema(
        'YouTube Videos',
        '467K+ subscribers. Tutorials, demos, and deep-dives on AI, machine learning, Hugging Face, and AWS services.',
        `${SITE.url}/youtube-videos`,
      )} />
      <StructuredData data={videoObjectSchema({
        name: 'Julien Simon - AI & Machine Learning',
        description: 'Tutorials, demos, and deep-dives on AI, machine learning, Hugging Face, and AWS services.',
        channelUrl: YOUTUBE_STATS.channelUrl,
        subscriberCount: YOUTUBE_STATS.subscriberCount * 1000,
        videoCount: YOUTUBE_STATS.totalVideos,
      })} />
      <YouTubeContent />
    </>
  );
}
