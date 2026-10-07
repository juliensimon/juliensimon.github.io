import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema, podcastSeriesSchema, podcastEpisodeListSchema } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import Breadcrumbs from '@/components/ui/Breadcrumbs';
import { SITE } from '@/lib/constants';
import { PODCAST_EPISODES } from '@/data/podcast';
import PodcastContent from './PodcastContent';

export const metadata = buildMetadata({
  title: 'The AI Realist Podcast: AI Without the Hype',
  description:
    'The AI Realist podcast by Julien Simon: each piece of the newsletter on the AI industry, narrated. GPU and cloud economics, inference costs, open models, chips, regulation. On Apple Podcasts and Spotify.',
  path: '/podcast',
  keywords: ['AI podcast', 'The AI Realist', 'AI industry analysis', 'AI economics', 'open-weight models'],
});

export default function PodcastPage() {
  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: 'Home', url: SITE.url },
        { name: 'Podcast', url: `${SITE.url}/podcast` },
      ])} />
      <StructuredData data={podcastSeriesSchema()} />
      <StructuredData data={podcastEpisodeListSchema(PODCAST_EPISODES)} />
      <Breadcrumbs items={[
        { name: 'Home', href: '/' },
        { name: 'Podcast', href: '/podcast' },
      ]} />
      <PodcastContent />
    </>
  );
}
