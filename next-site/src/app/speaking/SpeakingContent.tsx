'use client';

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

export default function SpeakingContent() {
  return (
    <>
      <GradientHero
        title="Speaking"
        subtitle="Conferences, workshops, and keynotes on AI, machine learning, and cloud computing"
      />

      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 mb-16">
          <MetricCard value={SPEAKING_STATS.totalEvents} suffix="" label="Speaking Engagements" index={0} />
          <MetricCard value={SPEAKING_STATS.countries} suffix="" label="Countries" index={1} />
          <MetricCard value={SPEAKING_STATS.cities} suffix="" label="Cities" index={2} />
        </div>

        {/* Map */}
        <ScrollReveal direction="up" className="mb-12">
          <h2 className="text-2xl font-bold font-heading gradient-brand-text mb-6 text-center">
            Speaking Locations Worldwide
          </h2>
          <SpeakingMap />
        </ScrollReveal>

        {/* Notable venues */}
        <ScrollReveal direction="up" className="glass-card rounded-xl p-6 mb-12">
          <h2 className="text-xl font-bold font-heading text-text mb-3">
            Notable Venues
          </h2>
          <p className="text-sm text-text-muted">
            AWS re:Invent, AWS Summits worldwide, ODSC, UNESCO, World Bank, Bank of Italy,
            NY Federal Reserve, Fortune 500 companies, sovereign funds, and major
            technology conferences across six continents.
          </p>
        </ScrollReveal>

        {/* Book Julien CTA */}
        <ScrollReveal direction="up" className="mb-12">
          <div className="glass-card rounded-2xl p-8 text-center">
            <h2 className="text-2xl font-heading font-bold text-text mb-3">Book Julien to Speak</h2>
            <p className="text-text-muted mb-6 max-w-2xl mx-auto">
              Available for keynotes, panels, and workshops on AI strategy, small language models, and enterprise AI adoption.
            </p>
            <a
              href="mailto:julien@julien.org?subject=Speaking%20Inquiry"
              className="inline-flex items-center px-6 py-3 text-sm font-medium text-white rounded-lg gradient-brand hover:opacity-90 transition-opacity"
            >
              Get in Touch
            </a>
          </div>
        </ScrollReveal>

        {/* Year grid */}
        <h2 className="text-2xl font-bold font-heading gradient-brand-text mb-6 text-center">
          Browse by Year
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
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
      </section>

      <RelatedContent items={[
        { href: '/publications', title: 'Publications', subtitle: 'Technical articles on AI and ML', metric: '440 articles' },
        { href: '/youtube-videos', title: 'Videos', subtitle: 'Tutorials, demos, and deep dives', metric: '494K subscribers' },
        { href: '/books', title: 'Books', subtitle: 'Published works on ML and cloud', metric: '4 books' },
      ]} />
    </>
  );
}
