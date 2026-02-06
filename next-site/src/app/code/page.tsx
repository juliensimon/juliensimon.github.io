import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema, webPageSchema } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import { SITE } from '@/lib/constants';
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
        { name: 'Home', url: SITE.url },
        { name: 'Code & Projects', url: `${SITE.url}/code` },
      ])} />
      <StructuredData data={webPageSchema(
        'Code & Projects',
        'Open source projects and code examples for machine learning, AI, and cloud computing.',
        `${SITE.url}/code`,
      )} />
      <CodeContent />
    </>
  );
}
