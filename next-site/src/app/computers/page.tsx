import { buildMetadata } from '@/lib/metadata';
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
  return <ComputersContent />;
}
