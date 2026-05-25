import GradientHero from '@/components/ui/GradientHero';
import ScrollReveal from '@/components/ui/ScrollReveal';
import MetricCard from '@/components/ui/MetricCard';
import RelatedContent from '@/components/ui/RelatedContent';
import { MEDIA_ITEMS, MEDIA_STATS, type MediaItem } from '@/data/media';
import { TOTAL_ARTICLES } from '@/data/publications';
import { SPEAKING_STATS } from '@/data/speaking';
import { YOUTUBE_STATS } from '@/data/youtube';

function groupByYear(items: readonly MediaItem[]): Array<{ year: number; items: MediaItem[] }> {
  const buckets = new Map<number, MediaItem[]>();
  for (const item of items) {
    const key = item.year || 0;
    const bucket = buckets.get(key) ?? [];
    bucket.push(item);
    buckets.set(key, bucket);
  }
  return [...buckets.entries()]
    .sort(([a], [b]) => b - a)
    .map(([year, items]) => ({ year, items }));
}

function MediaCard({ item, index }: { item: MediaItem; index: number }) {
  return (
    <ScrollReveal
      direction="up"
      delay={Math.min(index, 5) * 0.05}
      className="glass-card rounded-xl p-5"
    >
      <h3 className="text-base font-semibold text-text mb-1.5">
        {item.url ? (
          <a
            href={item.url}
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-primary transition-colors"
          >
            {item.title}
            <svg className="inline-block w-3 h-3 ml-1 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
          </a>
        ) : (
          item.title
        )}
      </h3>
      <p className="text-xs text-primary/80 mb-2">
        <span className="font-medium">{item.outlet}</span>
        {item.type && <span className="text-text-muted"> • {item.type}</span>}
        {item.date && <span className="text-text-muted"> • {item.date}</span>}
      </p>
      {item.description && (
        <p className="text-sm text-text-muted leading-relaxed">
          {item.description}
        </p>
      )}
      {item.tags.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1.5">
          {item.tags.map((tag) => (
            <span
              key={tag}
              className="text-[10px] uppercase tracking-wide px-2 py-0.5 rounded-full bg-primary/10 text-primary/80"
            >
              {tag}
            </span>
          ))}
        </div>
      )}
    </ScrollReveal>
  );
}

export default function MediaContent() {
  const groups = groupByYear(MEDIA_ITEMS);

  return (
    <>
      <GradientHero
        title="Media, Analysts & Podcasts"
        subtitle="Press interviews, analyst briefings, and podcast appearances on AI, machine learning, and cloud computing"
      />

      <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        <div className="grid grid-cols-3 gap-4 mb-12">
          <MetricCard value={MEDIA_STATS.total} suffix="" label="Appearances" index={0} />
          <MetricCard value={MEDIA_STATS.byType.Press ?? 0} suffix="" label="Press & Analyst" index={1} />
          <MetricCard value={MEDIA_STATS.byType.Podcast ?? 0} suffix="" label="Podcasts" index={2} />
        </div>

        <div className="space-y-12">
          {groups.map(({ year, items }) => (
            <div key={year}>
              <h2 className="text-2xl font-bold font-heading gradient-brand-text mb-4">
                {year || 'Undated'}
                <span className="ml-2 text-sm font-normal text-text-muted">
                  ({items.length})
                </span>
              </h2>
              <div className="grid sm:grid-cols-2 gap-4">
                {items.map((item, i) => (
                  <MediaCard
                    key={`${item.title}-${item.outlet}-${item.date}-${i}`}
                    item={item}
                    index={i}
                  />
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      <RelatedContent items={[
        { href: '/publications', title: 'Publications', subtitle: 'Technical articles on AI and ML', metric: `${TOTAL_ARTICLES}+ articles` },
        { href: '/speaking', title: 'Speaking', subtitle: 'Conferences, workshops, and keynotes', metric: `${SPEAKING_STATS.totalEvents}+ engagements` },
        { href: '/youtube-videos', title: 'Videos', subtitle: 'Tutorials, demos, and deep dives', metric: `${YOUTUBE_STATS.subscriberCount}K subscribers` },
      ]} />
    </>
  );
}
