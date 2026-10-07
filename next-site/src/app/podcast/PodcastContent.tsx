import GradientHero from '@/components/ui/GradientHero';
import RelatedContent from '@/components/ui/RelatedContent';
import { PODCAST, PODCAST_EPISODES } from '@/data/podcast';
import { TOTAL_ARTICLES } from '@/data/publications';
import { YOUTUBE_STATS } from '@/data/youtube';

function longDate(day: string) {
  return new Date(`${day}T12:00:00Z`).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' });
}

export default function PodcastContent() {
  return (
    <>
      <GradientHero title="The AI Realist Podcast" subtitle={PODCAST.tagline} />

      <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        <div className="glass-card rounded-xl p-6 sm:p-8 flex flex-col sm:flex-row gap-6 items-center sm:items-start">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={PODCAST.cover}
            alt="The AI Realist podcast cover"
            width={160}
            height={160}
            className="rounded-lg shrink-0 border border-text-muted/20"
          />
          <div>
            <p className="text-text-muted mb-5">{PODCAST.description}</p>
            {/* Apple's badge is its own artwork, unmodified (Apple Podcasts Identity Guidelines). Spotify
                publishes no badge file: its design guidelines allow the official icon on black with
                the wording "Listen on Spotify". Both read 2026-10-07. Keep them the same height. */}
            <div className="flex flex-wrap items-center gap-4">
              <a href={PODCAST.apple} target="_blank" rel="noopener noreferrer" className="hover:opacity-85 transition-opacity">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src="/assets/badges/listen-on-apple-podcasts.svg" alt="Listen on Apple Podcasts" width={126} height={40} />
              </a>
              <a
                href={PODCAST.spotify}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2.5 h-10 px-4 rounded-[7px] bg-black text-white text-sm font-semibold hover:opacity-85 transition-opacity"
              >
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src="/assets/badges/spotify-icon-green.svg" alt="" width={23} height={22} />
                Listen on Spotify
              </a>
              <a href={PODCAST.feed} target="_blank" rel="noopener noreferrer" className="text-sm text-primary font-semibold hover:underline">
                RSS feed
              </a>
              <a href={PODCAST.newsletter} target="_blank" rel="noopener noreferrer" className="text-sm text-primary font-semibold hover:underline">
                Read the newsletter
              </a>
            </div>
          </div>
        </div>
      </section>

      <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        <h2 className="text-2xl font-bold font-heading text-text mb-6">
          {PODCAST_EPISODES.length} episodes
        </h2>
        <ol className="space-y-5 list-none p-0">
          {PODCAST_EPISODES.map((episode) => {
            const read = episode.page || episode.article;
            return (
              <li key={episode.audio} className="glass-card rounded-xl p-6">
                <p className="text-xs text-text-muted mb-1">
                  <time dateTime={episode.date}>{longDate(episode.date)}</time> · {episode.minutes} min
                </p>
                <h3 className="text-lg font-semibold text-text mb-2">
                  <a href={read} className="hover:text-primary transition-colors">{episode.title}</a>
                </h3>
                <p className="text-sm text-text-muted mb-4">{episode.summary}</p>
                <audio controls preload="none" className="w-full mb-3" src={episode.audio} />
                <a href={read} className="text-sm text-primary font-medium hover:underline">
                  Read the written piece, with every source
                </a>
              </li>
            );
          })}
        </ol>
      </section>

      <RelatedContent items={[
        { href: '/blog/industry-perspectives/', title: 'AI Realist', subtitle: 'The written pieces behind every episode', metric: 'Newsletter archive' },
        { href: '/youtube-videos', title: 'Videos', subtitle: 'Tutorials, demos, and deep dives', metric: `${YOUTUBE_STATS.subscriberCount}K subscribers` },
        { href: '/publications', title: 'Publications', subtitle: 'Technical articles on AI and ML', metric: `${TOTAL_ARTICLES}+ articles` },
      ]} />
    </>
  );
}
