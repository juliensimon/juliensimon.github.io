import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import ComputersContent from './ComputersContent';

export const metadata = buildMetadata({
  title: 'Vintage Computers',
  description:
    'A personal collection of vintage and retro computers. From Apple II to Amiga, SGI workstations, and Sun SPARC systems.',
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
        { name: 'Home', url: 'https://www.julien.org' },
        { name: 'Vintage Computers', url: 'https://www.julien.org/computers' },
      ])} />
      <ComputersContent />
    </>
  );
}
