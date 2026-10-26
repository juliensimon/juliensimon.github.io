import Link from 'next/link';
import { notFound } from 'next/navigation';
import type { Metadata } from 'next';
import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema, collectionPageSchema } from '@/lib/structured-data';
import { topicItems, absolute, type TopicItem } from '@/lib/topic-items';
import StructuredData from '@/components/seo/StructuredData';
import FaqSection from '@/components/ui/FaqSection';
import Breadcrumbs from '@/components/ui/Breadcrumbs';
import GradientHero from '@/components/ui/GradientHero';
import { SITE } from '@/lib/constants';
import { TOPICS, TOPIC_BY_SLUG } from '@/data/topics';
import { SPEAKING_STATS } from '@/data/speaking';
import { TOTAL_ARTICLES } from '@/data/publications';

interface Props {
  params: Promise<{ topic: string }>;
}

export const dynamicParams = false;

export function generateStaticParams() {
  return TOPICS.map((t) => ({ topic: t.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { topic: slug } = await params;
  const topic = TOPIC_BY_SLUG[slug];
  if (!topic) return { title: 'Not Found', robots: { index: false, follow: false } };
  return buildMetadata({
    title: topic.title,
    description: topic.description,
    path: `/topics/${topic.slug}`,
    keywords: topic.keywords,
  });
}

const dateLabel = (iso: string) =>
  new Date(`${iso}T00:00:00Z`).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' });

function ItemList({ heading, items }: { heading: string; items: TopicItem[] }) {
  if (items.length === 0) return null;
  return (
    <section className="mb-14">
      <h2 className="text-2xl font-bold font-heading gradient-brand-text mb-6">{heading}</h2>
      <ul className="space-y-3">
        {items.map((item) => (
          <li key={item.href} className="glass-card rounded-xl p-5">
            <p className="text-xs text-text-muted mb-1">{dateLabel(item.date)}</p>
            <Link href={item.href} className="font-semibold text-text hover:text-primary transition-colors">
              {item.title}
            </Link>
            {item.summary && <p className="text-sm text-text-muted mt-1">{item.summary}</p>}
          </li>
        ))}
      </ul>
    </section>
  );
}

export default async function TopicPage({ params }: Props) {
  const { topic: slug } = await params;
  const topic = TOPIC_BY_SLUG[slug];
  if (!topic) notFound();

  const { articles, videos } = topicItems(topic);
  const url = absolute(`/topics/${topic.slug}`);
  const newest = [...articles, ...videos].sort((a, b) => b.date.localeCompare(a.date))[0];
  const others = TOPICS.filter((t) => t.slug !== topic.slug);

  const counts = [
    articles.length > 0 && `${articles.length} articles`,
    videos.length > 0 && `${videos.length} videos`,
  ].filter(Boolean).join(' and ');
  const latest = articles.slice(0, 3).map((a) => `"${a.title}" (${dateLabel(a.date)})`).join('; ');

  const faqs = [
    {
      question: topic.question,
      answer: `Julien Simon covers ${topic.name.toLowerCase()} in ${counts} on julien.org. ${
        latest ? `The newest articles are ${latest}. ` : ''
      }${topic.intro}`,
    },
    {
      question: `Where are Julien Simon's pieces on ${topic.name.toLowerCase()} published?`,
      answer:
        'Articles appear first in The AI Realist newsletter (airealist.ai) and are archived on julien.org. Videos are on the YouTube channel @juliensimonfr, each with a full transcript on julien.org.',
    },
    ...(videos.length > 0
      ? [{
          question: `Which videos does Julien Simon have on ${topic.name.toLowerCase()}?`,
          answer: `${videos.length} videos on the YouTube channel @juliensimonfr, each with a transcript on julien.org. The newest are ${videos
            .slice(0, 3)
            .map((v) => `"${v.title}" (${dateLabel(v.date)})`)
            .join('; ')}.`,
        }]
      : []),
  ];

  const listData = {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    '@id': `${url}/#itemlist`,
    name: topic.title,
    numberOfItems: articles.length + videos.length,
    itemListElement: [...articles, ...videos].map((item, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      url: absolute(item.href),
      name: item.title,
    })),
  };

  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: 'Home', url: SITE.url },
        { name: 'Topics', url: absolute('/topics') },
        { name: topic.name, url },
      ])} />
      <StructuredData data={{
        ...collectionPageSchema(topic.title, topic.description, url),
        dateModified: newest?.date,
        about: topic.keywords.map((name) => ({ '@type': 'Thing', name })),
        publisher: { '@id': `${SITE.url}/#person` },
        mainEntity: { '@id': `${url}/#itemlist` },
      }} />
      <StructuredData data={listData} />
      <Breadcrumbs items={[
        { name: 'Home', href: '/' },
        { name: 'Topics', href: '/topics' },
        { name: topic.name, href: `/topics/${topic.slug}` },
      ]} />
      <GradientHero title={topic.name} subtitle={topic.intro} />
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        {newest && (
          <p className="text-sm text-text-muted mb-10">
            {counts}. Last updated {dateLabel(newest.date)}.
          </p>
        )}
        <ItemList heading={`${topic.name}: articles`} items={articles} />
        <ItemList heading={`${topic.name}: videos`} items={videos} />
        <section aria-labelledby="author-heading" className="glass-card rounded-xl p-6 mb-14">
          <h2 id="author-heading" className="text-xl font-bold font-heading text-text mb-3">About the author</h2>
          <p className="text-sm text-text-muted leading-relaxed">
            <Link href="/" className="font-semibold text-text hover:text-primary">Julien Simon</Link> is an AI Operating Partner at
            Fortino Capital. He was VP and Chief Evangelist at Arcee AI, Chief Evangelist at Hugging Face and Global Evangelist
            for AI and machine learning at AWS, and wrote &ldquo;Learn Amazon SageMaker&rdquo; (Packt). He has given{' '}
            {SPEAKING_STATS.totalEvents}+ talks in {SPEAKING_STATS.countries} countries and published {TOTAL_ARTICLES}+ technical articles.
            See his <Link href="/experience" className="underline hover:text-primary">experience</Link> and{' '}
            <a href="https://www.wikidata.org/wiki/Q138589324" className="underline hover:text-primary">Wikidata entry</a>.
          </p>
          <p className="text-sm text-text-muted leading-relaxed mt-3">
            Method: figures come from filings, court documents, vendor documentation and measurements I ran, and each piece dates its numbers.
          </p>
        </section>
        <section className="mb-14">
          <h2 className="text-xl font-bold font-heading text-text mb-3">Go further</h2>
          <ul className="space-y-1 text-sm text-text-muted">
            <li>
              <Link href="/speaking" className="underline hover:text-primary">Book a keynote or workshop on {topic.name.toLowerCase()}</Link>
            </li>
            <li>
              <Link href="/podcast" className="underline hover:text-primary">Listen to The AI Realist podcast</Link>
            </li>
            <li>
              <a href="https://www.airealist.ai/subscribe" className="underline hover:text-primary">Subscribe to The AI Realist newsletter</a>
            </li>
          </ul>
        </section>
        <section className="mb-14">
          <h2 className="text-xl font-bold font-heading text-text mb-3">More topics</h2>
          <ul className="flex flex-wrap gap-2">
            {others.map((t) => (
              <li key={t.slug}>
                <Link href={`/topics/${t.slug}`} className="glass-card rounded-full px-4 py-1 text-sm text-text hover:text-primary transition-colors">
                  {t.name}
                </Link>
              </li>
            ))}
          </ul>
        </section>
      </div>
      <FaqSection faqs={faqs} pageUrl={url} />
    </>
  );
}
