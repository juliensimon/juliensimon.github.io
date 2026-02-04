import { buildMetadata } from '@/lib/metadata';
import SpeakingContent from './SpeakingContent';

export const metadata = buildMetadata({
  title: 'Speaking',
  description:
    '600+ talks and workshops at conferences worldwide on AI, machine learning, and cloud computing. Keynotes at AWS re:Invent, KubeCon, and more.',
  path: '/speaking',
  keywords: [
    'conference speaker',
    'AI talks',
    'machine learning workshops',
    'keynote speaker',
    'tech conferences',
  ],
});

export default function SpeakingPage() {
  return <SpeakingContent />;
}
