import { buildMetadata } from '@/lib/metadata';
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
  return <CodeContent />;
}
