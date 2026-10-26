import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema, webPageSchema, eventSchema, speakingServiceSchema, SPEAKING_FAQS } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import FaqSection from '@/components/ui/FaqSection';
import Breadcrumbs from '@/components/ui/Breadcrumbs';
import { SITE } from '@/lib/constants';
import { SPEAKING_EVENTS } from '@/data/speaking-events';
import { SPEAKING_STATS } from '@/data/speaking';
import { SPEAKING_FORMATS, SPEAKING_LANGUAGES } from '@/data/speaking-booking';
import SpeakingContent from './SpeakingContent';

export const metadata = buildMetadata({
  title: `AI Keynote Speaker: ${SPEAKING_STATS.totalEvents}+ Talks, ${SPEAKING_STATS.countries} Countries`,
  description:
    `Book Julien Simon for an AI keynote, executive workshop or panel on enterprise AI and small language models. English and French. ${SPEAKING_STATS.totalEvents}+ talks in ${SPEAKING_STATS.countries} countries.`,
  path: '/speaking',
  keywords: [
    'AI keynote speaker',
    'book a keynote speaker',
    'enterprise AI speaker',
    'AI executive workshop',
    'small language models talk',
    'conférencier IA',
    'The AI Realist',
  ],
  ogImage: `${SITE.url}/assets/speaking/og-speaking.jpg`,
  ogImageAlt: 'Julien Simon giving a keynote on enterprise AI to executives in Paris',
  languages: {
    en: `${SITE.url}/speaking`,
    fr: `${SITE.url}/fr/conferencier-ia`,
    'x-default': `${SITE.url}/speaking`,
  },
});

export default function SpeakingPage() {
  // Flatten all events across years for the ItemList (latest 50), preserving year context
  const allEventsWithYear = Object.entries(SPEAKING_EVENTS)
    .sort(([a], [b]) => Number(b) - Number(a))
    .flatMap(([year, events]) => events.map(e => ({ ...e, _year: year })));

  // Build event list with per-event year fallback
  const top50 = allEventsWithYear.slice(0, 50);
  const eventListData = {
    '@context': 'https://schema.org' as const,
    '@type': 'ItemList' as const,
    '@id': `${SITE.url}/speaking/#eventlist`,
    name: 'Julien Simon — Speaking Engagements',
    url: `${SITE.url}/speaking`,
    numberOfItems: top50.length,
    itemListElement: top50.map((event, i) => {
      // _year is an internal field not part of the schema
      const { _year, ...eventData } = event;
      void _year;
      return {
        '@type': 'ListItem' as const,
        position: i + 1,
        item: eventSchema(eventData),
      };
    }),
  };

  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: 'Home', url: SITE.url },
        { name: 'Speaking', url: `${SITE.url}/speaking` },
      ])} />
      <StructuredData data={webPageSchema(
        'Speaking Engagements',
        `Keynotes, executive workshops and panels on enterprise AI, small language models and the AI industry. ${SPEAKING_STATS.totalEvents}+ talks in ${SPEAKING_STATS.countries} countries.`,
        `${SITE.url}/speaking`,
      )} />
      <StructuredData data={speakingServiceSchema(SPEAKING_FORMATS, SPEAKING_LANGUAGES)} />
      <StructuredData data={eventListData} />
      <Breadcrumbs items={[
        { name: 'Home', href: '/' },
        { name: 'Speaking', href: '/speaking' },
      ]} />
      <SpeakingContent />
      <FaqSection faqs={SPEAKING_FAQS} pageUrl={`${SITE.url}/speaking`} />
    </>
  );
}
