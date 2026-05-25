import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema, webPageSchema } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import Breadcrumbs from '@/components/ui/Breadcrumbs';
import { SITE } from '@/lib/constants';
import { MEDIA_STATS } from '@/data/media';
import MediaContent from './MediaContent';

export const metadata = buildMetadata({
  title: `Media, Analysts & Podcasts — ${MEDIA_STATS.total} Appearances`,
  description: `${MEDIA_STATS.total} press interviews, analyst briefings, and podcast appearances by Julien Simon, ${MEDIA_STATS.yearSpan}. Covering AI, machine learning, small language models, and cloud computing.`,
  path: '/media',
  keywords: [
    'press',
    'interviews',
    'podcasts',
    'analyst relations',
    'media appearances',
    'AI commentary',
  ],
});

export default function MediaPage() {
  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: 'Home', url: SITE.url },
        { name: 'Media', url: `${SITE.url}/media` },
      ])} />
      <StructuredData data={webPageSchema(
        'Media, Analysts & Podcasts',
        `${MEDIA_STATS.total} press interviews, analyst briefings, and podcast appearances by Julien Simon, ${MEDIA_STATS.yearSpan}.`,
        `${SITE.url}/media`,
      )} />
      <Breadcrumbs items={[
        { name: 'Home', href: '/' },
        { name: 'Media', href: '/media' },
      ]} />
      <MediaContent />
    </>
  );
}
