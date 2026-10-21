'use client';

import ExportedImage from 'next-image-export-optimizer';
import GradientHero from '@/components/ui/GradientHero';
import ScrollReveal from '@/components/ui/ScrollReveal';
import MetricCard from '@/components/ui/MetricCard';
import YearCard from '@/components/ui/YearCard';
import dynamic from 'next/dynamic';

const SpeakingMap = dynamic(() => import('@/components/ui/SpeakingMap'), {
  ssr: false,
  loading: () => <div className="w-full h-[400px] sm:h-[500px] glass-card rounded-xl animate-pulse" />,
});
import RelatedContent from '@/components/ui/RelatedContent';
import { SPEAKING_STATS, SPEAKING_YEARS } from '@/data/speaking';
import { SPEAKING_EVENTS } from '@/data/speaking-events';
import {
  SPEAKING_BIO_LONG,
  SPEAKING_BIO_SHORT,
  SPEAKING_FORMATS,
  SPEAKING_LANGUAGES,
  SPEAKING_PHOTOS,
  SPEAKING_REQUEST_FIELDS,
  SPEAKING_TOPICS,
} from '@/data/speaking-booking';
import { TOTAL_ARTICLES } from '@/data/publications';
import { YOUTUBE_STATS } from '@/data/youtube';
import { SITE } from '@/lib/constants';

const REQUEST_HREF = `mailto:${SITE.email}?subject=${encodeURIComponent('Speaking request')}&body=${encodeURIComponent(
  `${SPEAKING_REQUEST_FIELDS.map((f) => `${f}:`).join('\n')}\n`,
)}`;

const RECENT_EVENTS = (SPEAKING_EVENTS['2026'] ?? []).slice(0, 5);

export default function SpeakingContent() {
  return (
    <>
      <GradientHero
        title="Keynote Speaker on Enterprise AI"
        subtitle={`Keynotes, executive workshops and panels on AI in production, small language models and the AI industry. In ${SPEAKING_LANGUAGES.join(' and ')}.`}
      >
        <div className="mt-8 flex flex-wrap items-center justify-center gap-3 animate-page-fade-up" style={{ animationDelay: '0.3s' }}>
          <a
            href="#request"
            className="gradient-brand text-white font-semibold px-6 py-3 rounded-lg hover:opacity-90 transition-opacity"
          >
            Request a talk
          </a>
          <a
            href="#bio"
            className="glass-card text-text font-semibold px-6 py-3 rounded-lg hover:opacity-80 transition-opacity"
          >
            Bio
          </a>
        </div>
      </GradientHero>

      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        {/* Proof */}
        {SPEAKING_PHOTOS.map((photo) => (
          <ScrollReveal key={photo.src} direction="up" className="mb-12">
            <figure className="glass-card rounded-xl overflow-hidden max-w-4xl mx-auto">
              <ExportedImage
                src={photo.src}
                alt={photo.alt}
                width={photo.width}
                height={photo.height}
                className="w-full h-auto"
                sizes="(max-width: 1024px) 100vw, 896px"
                priority
              />
              <figcaption className="px-5 py-3 text-xs text-text-muted flex flex-wrap justify-between gap-2">
                <span>{photo.caption}</span>
                <span>Photo: {photo.credit}</span>
              </figcaption>
            </figure>
          </ScrollReveal>
        ))}

        <div className="grid grid-cols-3 gap-4 mb-16">
          <MetricCard value={SPEAKING_STATS.totalEvents} suffix="+" label="Speaking Engagements" index={0} />
          <MetricCard value={SPEAKING_STATS.countries} suffix="" label="Countries" index={1} />
          <MetricCard value={SPEAKING_STATS.cities} suffix="" label="Cities" index={2} />
        </div>

        {/* Topics */}
        <h2 className="text-2xl font-bold font-heading gradient-brand-text mb-2 text-center">Sample talks</h2>
        <p className="text-text-muted text-center max-w-2xl mx-auto mb-8">
          Three examples from a wider range. Julien covers AI strategy, engineering, open models, hardware, cloud and the
          AI industry, and builds each talk around your audience, your sector and the question you need answered.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
          {SPEAKING_TOPICS.map((topic, i) => (
            <ScrollReveal key={topic.title} direction="up" delay={i * 0.08} className="glass-card rounded-xl p-6">
              <h3 className="text-lg font-semibold text-text mb-3">{topic.title}</h3>
              <p className="text-sm text-text-muted mb-3">{topic.takeaway}</p>
              <p className="text-xs uppercase tracking-wide text-text-muted">For {topic.audience}</p>
            </ScrollReveal>
          ))}
        </div>

        {/* Formats */}
        <h2 className="text-2xl font-bold font-heading gradient-brand-text mb-8 text-center">Formats</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-16">
          {SPEAKING_FORMATS.map((format, i) => (
            <ScrollReveal key={format.name} direction="up" delay={i * 0.06} className="glass-card rounded-xl p-6">
              <div className="flex items-baseline justify-between gap-3 mb-2">
                <h3 className="text-lg font-semibold text-text">{format.name}</h3>
                <span className="text-xs text-text-muted whitespace-nowrap">{format.length}</span>
              </div>
              <p className="text-sm text-text-muted mb-3">{format.description}</p>
              <p className="text-xs uppercase tracking-wide text-text-muted">{format.audience}</p>
            </ScrollReveal>
          ))}
        </div>

        {/* Recent */}
        <h2 className="text-2xl font-bold font-heading gradient-brand-text mb-8 text-center">Recent talks</h2>
        <ul className="max-w-3xl mx-auto space-y-3 mb-16">
          {RECENT_EVENTS.map((event) => (
            <li key={`${event.title}-${event.date}`} className="glass-card rounded-xl p-5">
              <p className="text-xs text-text-muted mb-1">
                {[event.date, event.location].filter(Boolean).join(' · ')}
              </p>
              <p className="font-semibold text-text">{event.title}</p>
              {event.venue && <p className="text-sm text-text-muted">{event.venue}</p>}
            </li>
          ))}
        </ul>

        {/* Map */}
        <ScrollReveal direction="up" className="mb-12">
          <h2 className="text-2xl font-bold font-heading gradient-brand-text mb-6 text-center">
            Speaking Locations Worldwide
          </h2>
          <SpeakingMap />
        </ScrollReveal>

        {/* Year grid */}
        <h2 className="text-2xl font-bold font-heading gradient-brand-text mb-6 text-center">
          Browse by Year
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 mb-16">
          {SPEAKING_YEARS.map((y, i) => (
            <YearCard
              key={y.year}
              year={y.year}
              count={y.count}
              label="events"
              href={`/speaking/${y.year}`}
              index={i}
            />
          ))}
        </div>

        {/* Bio */}
        <section id="bio" aria-labelledby="bio-heading" className="max-w-3xl mx-auto mb-16 scroll-mt-24">
          <h2 id="bio-heading" className="text-2xl font-bold font-heading gradient-brand-text mb-6 text-center">
            Bio
          </h2>
          <div className="glass-card rounded-xl p-6 mb-4">
            <h3 className="text-sm font-semibold uppercase tracking-wide text-text-muted mb-2">Short bio</h3>
            <p className="text-sm text-text leading-relaxed">{SPEAKING_BIO_SHORT}</p>
          </div>
          <div className="glass-card rounded-xl p-6 mb-4">
            <h3 className="text-sm font-semibold uppercase tracking-wide text-text-muted mb-2">Long bio</h3>
            <p className="text-sm text-text leading-relaxed">{SPEAKING_BIO_LONG}</p>
          </div>
        </section>

        {/* Request */}
        <section
          id="request"
          aria-labelledby="request-heading"
          className="glass-card rounded-xl p-8 max-w-3xl mx-auto scroll-mt-24"
        >
          <h2 id="request-heading" className="text-2xl font-bold font-heading gradient-brand-text mb-3 text-center">
            Request a talk
          </h2>
          <p className="text-text-muted text-center mb-6">
            Keynotes and workshops for companies are paid engagements, quoted on the format, the travel and the rights
            you need. Send the brief below and Julien replies within two business days.
          </p>
          <ul className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-2 text-sm text-text mb-8">
            {SPEAKING_REQUEST_FIELDS.map((f) => (
              <li key={f} className="flex gap-2">
                <span aria-hidden="true" className="text-highlight">+</span>
                {f}
              </li>
            ))}
          </ul>
          <div className="text-center">
            <a
              href={REQUEST_HREF}
              className="inline-block gradient-brand text-white font-semibold px-8 py-3 rounded-lg hover:opacity-90 transition-opacity"
            >
              Email the brief to {SITE.email}
            </a>
            <p className="text-xs text-text-muted mt-3">
              Or message Julien on{' '}
              <a href="https://www.linkedin.com/in/juliensimon" className="underline">
                LinkedIn
              </a>
              .
            </p>
          </div>
        </section>
      </section>

      <RelatedContent items={[
        { href: '/publications', title: 'Publications', subtitle: 'Technical articles on AI and ML', metric: `${TOTAL_ARTICLES}+ articles` },
        { href: '/youtube-videos', title: 'Videos', subtitle: 'Tutorials, demos, and deep dives', metric: `${YOUTUBE_STATS.subscriberCount}K subscribers` },
        { href: '/books', title: 'Books', subtitle: 'Published works on ML and cloud', metric: '4 books' },
      ]} />
    </>
  );
}
