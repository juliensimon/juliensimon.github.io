import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema, youtubeChannelSchema, videoObjectListSchema, webPageSchema, faqSchema, YOUTUBE_FAQS } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import Breadcrumbs from '@/components/ui/Breadcrumbs';
import { SITE } from '@/lib/constants';
import { YOUTUBE_STATS, LATEST_VIDEOS } from '@/data/youtube';
import YouTubeContent from './YouTubeContent';

export const metadata = buildMetadata({
  title: 'YouTube Videos',
  description:
    '494K subscribers. Hands-on tutorials on running AI models locally, fine-tuning LLMs, deploying on AWS, and using Hugging Face — by Julien Simon.',
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
        '494K subscribers. Hands-on tutorials on running AI models locally, fine-tuning LLMs, deploying on AWS, and using Hugging Face.',
        `${SITE.url}/youtube-videos`,
      )} />
      <StructuredData data={youtubeChannelSchema({
        name: 'Julien Simon - AI & Machine Learning',
        description: 'Tutorials, demos, and deep-dives on AI, machine learning, Hugging Face, and AWS services.',
        channelUrl: YOUTUBE_STATS.channelUrl,
        subscriberCount: YOUTUBE_STATS.subscriberCount * 1000,
        videoCount: YOUTUBE_STATS.totalVideos,
      })} />
      <StructuredData data={videoObjectListSchema(
        LATEST_VIDEOS,
        'Julien Simon - AI & Machine Learning',
        YOUTUBE_STATS.channelUrl,
      )} />
      <StructuredData data={faqSchema(YOUTUBE_FAQS, `${SITE.url}/youtube-videos`)} />
      <Breadcrumbs items={[
        { name: 'Home', href: '/' },
        { name: 'Videos', href: '/youtube-videos' },
      ]} />
      <YouTubeContent />
    </>
  );
}
