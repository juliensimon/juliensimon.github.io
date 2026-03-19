import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema, webPageSchema, faqSchema, eventListSchema, SPEAKING_FAQS } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import Breadcrumbs from '@/components/ui/Breadcrumbs';
import { SITE } from '@/lib/constants';
import { SPEAKING_EVENTS } from '@/data/speaking-events';
import SpeakingContent from './SpeakingContent';

export const metadata = buildMetadata({
  title: 'Speaking — 684+ Talks on AI & Machine Learning',
  description:
    '684+ talks and workshops at conferences worldwide on AI, machine learning, and cloud computing. Keynotes at AWS re:Invent, ODSC, and more.',
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
  // Flatten all events across years for the ItemList (latest 50)
  const allEvents = Object.entries(SPEAKING_EVENTS)
    .sort(([a], [b]) => Number(b) - Number(a))
    .flatMap(([, events]) => events);

  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: 'Home', url: SITE.url },
        { name: 'Speaking', url: `${SITE.url}/speaking` },
      ])} />
      <StructuredData data={webPageSchema(
        'Speaking Engagements',
        '684+ talks and workshops at conferences worldwide on AI, machine learning, and cloud computing.',
        `${SITE.url}/speaking`,
      )} />
      <StructuredData data={faqSchema(SPEAKING_FAQS, `${SITE.url}/speaking`)} />
      <StructuredData data={eventListSchema(
        allEvents,
        `${SITE.url}/speaking`,
        'Julien Simon — Speaking Engagements',
        50,
      )} />
      <Breadcrumbs items={[
        { name: 'Home', href: '/' },
        { name: 'Speaking', href: '/speaking' },
      ]} />
      <SpeakingContent />
    </>
  );
}
