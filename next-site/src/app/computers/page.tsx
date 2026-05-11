import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema, webPageSchema } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import Breadcrumbs from '@/components/ui/Breadcrumbs';
import { SITE } from '@/lib/constants';
import ComputersContent from './ComputersContent';

export const metadata = buildMetadata({
  title: 'Vintage Computers, UNIX, and Me — Personal Collection',
  description:
    'Julien Simon\'s personal collection of vintage and retro computers spanning 40+ years — from Apple II and Amiga to SGI workstations, Sun SPARC, NeXT, and DEC systems. UNIX, BSD, and the machines that shaped computing.',
  path: '/computers',
  keywords: [
    'vintage computers',
    'retro computing',
    'Apple II',
    'Amiga',
    'SGI',
    'Sun SPARC',
    'computer collection',
  ],
});

export default function ComputersPage() {
  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: 'Home', url: SITE.url },
        { name: 'Vintage Computers', url: `${SITE.url}/computers` },
      ])} />
      <StructuredData data={webPageSchema(
        'Vintage Computers',
        'A personal collection of vintage and retro computers, from Apple II to Amiga, SGI workstations, and Sun SPARC systems.',
        `${SITE.url}/computers`,
      )} />
      <Breadcrumbs items={[
        { name: 'Home', href: '/' },
        { name: 'Vintage Computers', href: '/computers' },
      ]} />
      <ComputersContent />
    </>
  );
}
