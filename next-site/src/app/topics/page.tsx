import Link from 'next/link';
import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema, collectionPageSchema } from '@/lib/structured-data';
import { topicItems, absolute } from '@/lib/topic-items';
import StructuredData from '@/components/seo/StructuredData';
import Breadcrumbs from '@/components/ui/Breadcrumbs';
import GradientHero from '@/components/ui/GradientHero';
import { SITE } from '@/lib/constants';
import { TOPICS } from '@/data/topics';

const DESCRIPTION =
  'Julien Simon on AI chips, AI infrastructure economics, European AI sovereignty, and small and open-weight models: articles and videos by topic.';

export const metadata = buildMetadata({
  title: 'AI Topics: Chips, Sovereignty, Small Models',
  description: DESCRIPTION,
  path: '/topics',
  keywords: TOPICS.map((t) => t.name),
});

export default function TopicsPage() {
  const url = absolute('/topics');
  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: 'Home', url: SITE.url },
        { name: 'Topics', url },
      ])} />
      <StructuredData data={collectionPageSchema('AI Topics', DESCRIPTION, url)} />
      <Breadcrumbs items={[
        { name: 'Home', href: '/' },
        { name: 'Topics', href: '/topics' },
      ]} />
      <GradientHero
        title="AI Topics"
        subtitle="The articles and videos on each subject I cover, newest first."
      />
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-20 grid gap-4">
        {TOPICS.map((topic) => {
          const { articles, videos } = topicItems(topic);
          return (
            <Link key={topic.slug} href={`/topics/${topic.slug}`} className="glass-card rounded-xl p-6 block hover:opacity-90 transition-opacity">
              <h2 className="text-xl font-semibold text-text mb-2">{topic.name}</h2>
              <p className="text-sm text-text-muted mb-3">{topic.intro}</p>
              <p className="text-xs uppercase tracking-wide text-text-muted">
                {[articles.length > 0 && `${articles.length} articles`, videos.length > 0 && `${videos.length} videos`].filter(Boolean).join(' · ')}
              </p>
            </Link>
          );
        })}
      </div>
    </>
  );
}
