import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema, webPageSchema, faqSchema, eventSchema, SPEAKING_FAQS } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import Breadcrumbs from '@/components/ui/Breadcrumbs';
import { SITE } from '@/lib/constants';
import { SPEAKING_EVENTS } from '@/data/speaking-events';
import SpeakingContent from './SpeakingContent';

export const metadata = buildMetadata({
  title: 'Speaking — 685+ Talks on AI & Machine Learning',
  description:
    '685+ talks and workshops at conferences worldwide on AI, machine learning, and cloud computing. Keynotes at AWS re:Invent, ODSC, and more.',
  path: '/speaking',
  keywords: [
    'conference speaker',
    'AI talks',
    'machine learning workshops',
    'keynote speaker',
    'tech conferences',
    'The AI Realist',
  ],
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
        '685+ talks and workshops at conferences worldwide on AI, machine learning, and cloud computing.',
        `${SITE.url}/speaking`,
      )} />
      <StructuredData data={faqSchema(SPEAKING_FAQS, `${SITE.url}/speaking`)} />
      <StructuredData data={eventListData} />
      <Breadcrumbs items={[
        { name: 'Home', href: '/' },
        { name: 'Speaking', href: '/speaking' },
      ]} />
      <SpeakingContent />
    </>
  );
}
