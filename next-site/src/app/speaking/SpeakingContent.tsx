'use client';

import GradientHero from '@/components/ui/GradientHero';
import ScrollReveal from '@/components/ui/ScrollReveal';
import MetricCard from '@/components/ui/MetricCard';
import YearCard from '@/components/ui/YearCard';
import SpeakingMap from '@/components/ui/SpeakingMap';
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
          <MetricCard value={SPEAKING_STATS.totalEvents} suffix="+" label="Speaking Engagements" index={0} />
          <MetricCard value={SPEAKING_STATS.countries} suffix="" label="Countries" index={1} />
          <MetricCard value={SPEAKING_STATS.cities} suffix="+" label="Cities" index={2} />
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

        {/* Podcasts & Media */}
        <ScrollReveal direction="up" className="grid sm:grid-cols-2 gap-4 mb-12">
          <a
            href="/podcasts.html"
            className="glass-card rounded-xl p-6 hover:shadow-lg transition-shadow group"
          >
            <h2 className="text-xl font-bold font-heading text-text mb-2 group-hover:text-primary transition-colors">
              Podcasts
            </h2>
            <p className="text-sm text-text-muted">
              Guest appearances on technology and AI podcasts.
            </p>
          </a>
          <a
            href="/media-analysts.html"
            className="glass-card rounded-xl p-6 hover:shadow-lg transition-shadow group"
          >
            <h2 className="text-xl font-bold font-heading text-text mb-2 group-hover:text-primary transition-colors">
              Media &amp; Analysts
            </h2>
            <p className="text-sm text-text-muted">
              Press coverage, TV interviews, and industry analyst briefings.
            </p>
          </a>
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
    </>
  );
}
