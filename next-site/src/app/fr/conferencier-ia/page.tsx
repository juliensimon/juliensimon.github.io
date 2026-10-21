import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema, webPageSchema, speakingServiceSchema, SPEAKING_FAQS_FR } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import FaqSection from '@/components/ui/FaqSection';
import Breadcrumbs from '@/components/ui/Breadcrumbs';
import { SITE } from '@/lib/constants';
import { SPEAKING_STATS } from '@/data/speaking';
import { SPEAKING_COPY } from '@/data/speaking-copy';
import SpeakingContent from '../../speaking/SpeakingContent';

const PATH = '/fr/conferencier-ia';
const t = SPEAKING_COPY.fr;

export const metadata = buildMetadata({
  title: `Conférencier IA : ${SPEAKING_STATS.totalEvents}+ interventions, ${SPEAKING_STATS.countries} pays`,
  description:
    `Réservez Julien Simon pour une keynote IA, un atelier de direction ou une table ronde. IA en entreprise en production, petits modèles de langage, modèles ouverts et matériel. En français et en anglais. ${SPEAKING_STATS.totalEvents}+ interventions dans ${SPEAKING_STATS.countries} pays.`,
  path: PATH,
  keywords: [
    'conférencier IA',
    'keynote IA',
    'conférencier intelligence artificielle',
    'atelier IA direction',
    'petits modèles de langage',
    'intervenant IA entreprise',
    'The AI Realist',
  ],
  ogImage: `${SITE.url}/assets/speaking/og-speaking.jpg`,
  ogImageAlt: 'Julien Simon donnant une keynote sur l\'IA en entreprise devant des dirigeants à Paris',
  locale: 'fr_FR',
  languages: {
    en: `${SITE.url}/speaking`,
    fr: `${SITE.url}${PATH}`,
    'x-default': `${SITE.url}/speaking`,
  },
});

export default function ConferencierIaPage() {
  const url = `${SITE.url}${PATH}`;
  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: t.breadcrumbHome, url: SITE.url },
        { name: t.breadcrumbPage, url },
      ])} />
      <StructuredData data={webPageSchema(
        'Julien Simon, conférencier IA',
        `Keynotes, ateliers de direction et tables rondes sur l'IA en entreprise, les petits modèles de langage et l'industrie de l'IA. ${SPEAKING_STATS.totalEvents}+ interventions dans ${SPEAKING_STATS.countries} pays.`,
        url,
        undefined,
        'fr',
      )} />
      <StructuredData data={speakingServiceSchema(t.formats, ['French', 'English'], {
        path: PATH,
        name: 'Keynotes IA et ateliers de direction',
        description:
          'Keynotes, ateliers de direction, tables rondes et approfondissements techniques sur l\'IA en entreprise en production, les petits modèles de langage et l\'industrie de l\'IA.',
        catalogName: 'Formats d\'intervention',
        inLanguage: 'fr',
      })} />
      <Breadcrumbs items={[
        { name: t.breadcrumbHome, href: '/' },
        { name: t.breadcrumbPage, href: PATH },
      ]} />
      <SpeakingContent lang="fr" />
      <div lang="fr">
        <FaqSection faqs={SPEAKING_FAQS_FR} pageUrl={url} heading={t.faqHeading} />
      </div>
    </>
  );
}
