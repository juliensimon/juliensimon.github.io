import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import CodeContent from './CodeContent';

export const metadata = buildMetadata({
  title: 'Code & Projects',
  description:
    'Open source projects, GitHub repositories, and code examples for machine learning, AI, and cloud computing.',
  path: '/code',
  keywords: [
    'open source',
    'GitHub',
    'code examples',
    'machine learning code',
    'AI projects',
  ],
});

export default function CodePage() {
  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: 'Home', url: 'https://www.julien.org' },
        { name: 'Code & Projects', url: 'https://www.julien.org/code' },
      ])} />
      <CodeContent />
    </>
  );
}
