'use client';

import Link from 'next/link';
import GradientHero from '@/components/ui/GradientHero';
import ScrollReveal from '@/components/ui/ScrollReveal';
import type { SpeakingEvent } from '@/data/speaking-events';

interface Props {
  year: string;
  events: SpeakingEvent[];
  totalCount: number;
}

export default function SpeakingYearContent({ year, events, totalCount }: Props) {

  return (
    <>
      <GradientHero
        title={`Speaking ${year}`}
        subtitle={`${totalCount} event${totalCount !== 1 ? 's' : ''} — conferences, workshops, and meetups on AI, machine learning, and cloud computing`}
      />

      <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        {events.length > 0 ? (
          <div className="space-y-4">
            {events.map((event, i) => (
              <ScrollReveal
                key={`${event.title}-${i}`}
                direction="up"
                delay={Math.min(i * 0.04, 0.5)}
                margin="-20px"
                className="glass-card rounded-xl p-5"
              >
                <div className="flex items-start justify-between gap-4">
                  <h2 className="text-base font-semibold text-text">
                    {event.title}
                  </h2>
                  {event.date && (
                    <span className="text-xs text-highlight font-medium whitespace-nowrap shrink-0">
                      {event.date}
                    </span>
                  )}
                </div>

                {(event.venue || event.location) && (
                  <p className="text-sm text-primary mt-1">
                    {event.venue}
                    {event.venue && event.location ? ' — ' : ''}
                    {event.location}
                  </p>
                )}

                {event.description && (
                  <p className="text-sm text-text-muted mt-2 leading-relaxed">
                    {event.description}
                  </p>
                )}

                <div className="flex flex-wrap items-center gap-2 mt-3">
                  {event.tags?.map((tag) => (
                    <span
                      key={tag}
                      className="text-[10px] px-2 py-0.5 rounded-full bg-primary/10 text-primary font-medium"
                    >
                      {tag}
                    </span>
                  ))}

                  {event.links?.map((link) => (
                    <a
                      key={link.url}
                      href={link.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-[10px] px-2 py-0.5 rounded-full bg-highlight/10 text-highlight font-medium hover:bg-highlight/20 transition-colors"
                    >
                      {link.label} &rarr;
                    </a>
                  ))}
                </div>
              </ScrollReveal>
            ))}
          </div>
        ) : (
          <div className="glass-card rounded-xl p-8 text-center">
            <p className="text-text-muted">
              {totalCount} events recorded for {year}. Detailed listings are being migrated.
            </p>
          </div>
        )}

        <div className="mt-8 text-center">
          <Link href="/speaking" className="text-primary hover:text-primary-hover font-medium">
            &larr; Back to Speaking Overview
          </Link>
        </div>
      </section>
    </>
  );
}
