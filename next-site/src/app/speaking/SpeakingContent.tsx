'use client';

import Link from 'next/link';
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
  SPEAKING_COPY,
  formatEventDate,
  formatEventLocation,
  type SpeakingLang,
} from '@/data/speaking-copy';
import { TOTAL_ARTICLES } from '@/data/publications';
import { YOUTUBE_STATS } from '@/data/youtube';
import { SITE } from '@/lib/constants';

const RECENT_EVENTS = (SPEAKING_EVENTS['2026'] ?? []).slice(0, 5);

export default function SpeakingContent({ lang = 'en' }: { lang?: SpeakingLang }) {
  const t = SPEAKING_COPY[lang];
  const requestHref = `mailto:${SITE.email}?subject=${encodeURIComponent(t.requestSubject)}&body=${encodeURIComponent(
    `${t.requestFields.map((f) => `${f}:`).join('\n')}\n`,
  )}`;

  return (
    <div lang={lang}>
      <GradientHero
        title={t.heroTitle}
        subtitle={t.heroSubtitle}
      >
        <div className="mt-8 flex flex-wrap items-center justify-center gap-3 animate-page-fade-up" style={{ animationDelay: '0.3s' }}>
          <a
            href="#request"
            className="gradient-brand text-white font-semibold px-6 py-3 rounded-lg hover:opacity-90 transition-opacity"
          >
            {t.ctaRequest}
          </a>
          <a
            href="#bio"
            className="glass-card text-text font-semibold px-6 py-3 rounded-lg hover:opacity-80 transition-opacity"
          >
            {t.ctaBio}
          </a>
        </div>
        <p className="mt-4 text-sm text-text-muted animate-page-fade-up" style={{ animationDelay: '0.4s' }}>
          <Link href={t.switchHref} lang={t.switchLang} hrefLang={t.switchLang} className="underline hover:opacity-80">
            {t.switchLabel}
          </Link>
        </p>
      </GradientHero>

      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        {/* Proof */}
        {t.photos.map((photo) => (
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
                <span>{t.photoCredit} {photo.credit}</span>
              </figcaption>
            </figure>
          </ScrollReveal>
        ))}

        <div className="grid grid-cols-3 gap-4 mb-16">
          <MetricCard value={SPEAKING_STATS.totalEvents} suffix="+" label={t.metrics.events} index={0} />
          <MetricCard value={SPEAKING_STATS.countries} suffix="" label={t.metrics.countries} index={1} />
          <MetricCard value={SPEAKING_STATS.cities} suffix="" label={t.metrics.cities} index={2} />
        </div>

        {/* Topics */}
        <h2 className="text-2xl font-bold font-heading gradient-brand-text mb-2 text-center">{t.talksHeading}</h2>
        <p className="text-text-muted text-center max-w-2xl mx-auto mb-8">{t.talksIntro}</p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
          {t.topics.map((topic, i) => (
            <ScrollReveal key={topic.title} direction="up" delay={i * 0.08} className="glass-card rounded-xl p-6">
              <h3 className="text-lg font-semibold text-text mb-3">{topic.title}</h3>
              <p className="text-sm text-text-muted mb-3">{topic.takeaway}</p>
              <p className="text-xs uppercase tracking-wide text-text-muted">{t.audienceLabel} {topic.audience}</p>
            </ScrollReveal>
          ))}
        </div>

        {/* Formats */}
        <h2 className="text-2xl font-bold font-heading gradient-brand-text mb-8 text-center">{t.formatsHeading}</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-16">
          {t.formats.map((format, i) => (
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
        <h2 className="text-2xl font-bold font-heading gradient-brand-text mb-8 text-center">{t.recentHeading}</h2>
        <ul className="max-w-3xl mx-auto space-y-3 mb-16">
          {RECENT_EVENTS.map((event) => (
            <li key={`${event.title}-${event.date}`} className="glass-card rounded-xl p-5">
              <p className="text-xs text-text-muted mb-1">
                {[formatEventDate(lang, event.date), formatEventLocation(lang, event.location)].filter(Boolean).join(' · ')}
              </p>
              <p className="font-semibold text-text">{event.title}</p>
              {event.venue && <p className="text-sm text-text-muted">{event.venue}</p>}
            </li>
          ))}
        </ul>

        {/* Map */}
        <ScrollReveal direction="up" className="mb-12">
          <h2 className="text-2xl font-bold font-heading gradient-brand-text mb-6 text-center">
            {t.mapHeading}
          </h2>
          <SpeakingMap />
        </ScrollReveal>

        {/* Year grid */}
        {t.yearsHeading && (
          <>
        <h2 className="text-2xl font-bold font-heading gradient-brand-text mb-6 text-center">
          {t.yearsHeading}
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
          </>
        )}

        {/* Bio */}
        <section id="bio" aria-labelledby="bio-heading" className="max-w-3xl mx-auto mb-16 scroll-mt-24">
          <h2 id="bio-heading" className="text-2xl font-bold font-heading gradient-brand-text mb-6 text-center">
            {t.bioHeading}
          </h2>
          <div className="glass-card rounded-xl p-6 mb-4">
            <h3 className="text-sm font-semibold uppercase tracking-wide text-text-muted mb-2">{t.bioShortLabel}</h3>
            <p className="text-sm text-text leading-relaxed">{t.bioShort}</p>
          </div>
          <div className="glass-card rounded-xl p-6 mb-4">
            <h3 className="text-sm font-semibold uppercase tracking-wide text-text-muted mb-2">{t.bioLongLabel}</h3>
            <p className="text-sm text-text leading-relaxed">{t.bioLong}</p>
          </div>
        </section>

        {/* Request */}
        <section
          id="request"
          aria-labelledby="request-heading"
          className="glass-card rounded-xl p-8 max-w-3xl mx-auto scroll-mt-24"
        >
          <h2 id="request-heading" className="text-2xl font-bold font-heading gradient-brand-text mb-3 text-center">
            {t.requestHeading}
          </h2>
          <p className="text-text-muted text-center mb-6">{t.requestIntro}</p>
          <ul className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-2 text-sm text-text mb-8">
            {t.requestFields.map((f) => (
              <li key={f} className="flex gap-2">
                <span aria-hidden="true" className="text-highlight">+</span>
                {f}
              </li>
            ))}
          </ul>
          <div className="text-center">
            <a
              href={requestHref}
              className="inline-block gradient-brand text-white font-semibold px-8 py-3 rounded-lg hover:opacity-90 transition-opacity"
            >
              {t.requestButton(SITE.email)}
            </a>
            <p className="text-xs text-text-muted mt-3">
              {t.linkedinLead}{' '}
              <a href="https://www.linkedin.com/in/juliensimon" className="underline">
                LinkedIn
              </a>
              {t.linkedinTrail}
            </p>
            <p className="text-xs text-text-muted mt-1">
              {t.sessionizeLead}{' '}
              <a href="https://sessionize.com/julien-simon-ai" className="underline">
                Sessionize
              </a>
              {t.linkedinTrail}
            </p>
          </div>
        </section>
      </section>

      {lang === 'en' && (
        <RelatedContent items={[
        { href: '/publications', title: 'Publications', subtitle: 'Technical articles on AI and ML', metric: `${TOTAL_ARTICLES}+ articles` },
        { href: '/youtube-videos', title: 'Videos', subtitle: 'Tutorials, demos, and deep dives', metric: `${YOUTUBE_STATS.subscriberCount}K subscribers` },
        { href: '/books', title: 'Books', subtitle: 'Published works on ML and cloud', metric: '4 books' },
      ]} />
      )}
    </div>
  );
}
