'use client';

import { useState } from 'react';
import GradientHero from '@/components/ui/GradientHero';
import ScrollReveal from '@/components/ui/ScrollReveal';
import RelatedContent from '@/components/ui/RelatedContent';
import { FEATURED_DATASETS, DOMAINS, HF_PROFILE, TOTAL_DATASETS } from '@/data/datasets';
import { TOTAL_ARTICLES } from '@/data/publications';
import { YOUTUBE_STATS } from '@/data/youtube';

function formatRecords(n?: number): string {
  if (!n) return '';
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1).replace(/\.0$/, '')}M rows`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}K rows`;
  return `${n.toLocaleString()} rows`;
}

export default function DatasetsContent() {
  const [activeDomain, setActiveDomain] = useState<string>('all');
  const filtered = activeDomain === 'all'
    ? FEATURED_DATASETS
    : FEATURED_DATASETS.filter(d => d.domain === activeDomain);

  return (
    <>
      <GradientHero
        title="Space Datasets"
        subtitle={`${TOTAL_DATASETS} open datasets for orbital mechanics, space weather, astronomy & physics`}
      />

      <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        <h2 className="sr-only">Featured Datasets</h2>

        {/* Domain filter tabs */}
        <div className="flex flex-wrap justify-center gap-2 mb-8">
          {DOMAINS.map((domain) => (
            <button
              key={domain.key}
              onClick={() => setActiveDomain(domain.key)}
              className={`text-sm px-4 py-1.5 rounded-full font-medium transition-all duration-200 ${
                activeDomain === domain.key
                  ? 'gradient-brand text-white'
                  : 'bg-highlight/10 text-text-muted hover:text-text hover:bg-highlight/20'
              }`}
            >
              {domain.label}
            </button>
          ))}
        </div>

        <div className="grid sm:grid-cols-2 gap-5">
          {filtered.map((dataset, i) => (
            <ScrollReveal
              key={dataset.name}
              as="a"
              href={dataset.hfUrl}
              target="_blank"
              rel="noopener noreferrer"
              direction="up"
              delay={i * 0.08}
              className="block glass-card rounded-xl p-6 hover:scale-[1.02] transition-all duration-300 group"
            >
              <div className="flex items-center gap-2 mb-2">
                <svg className="w-5 h-5 text-text-muted" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fillRule="evenodd" d="M.99 5.24A2.25 2.25 0 0 1 3.25 3h13.5A2.25 2.25 0 0 1 19 5.25l.01 9.5A2.25 2.25 0 0 1 16.76 17H3.26A2.25 2.25 0 0 1 1 14.75l-.01-9.5Zm1.5.01v9.5c0 .414.336.75.75.75h13.5a.75.75 0 0 0 .75-.75l-.01-9.5a.75.75 0 0 0-.75-.75H3.25a.75.75 0 0 0-.75.75ZM5 7.5a.75.75 0 0 1 .75-.75h8.5a.75.75 0 0 1 0 1.5h-8.5A.75.75 0 0 1 5 7.5Zm.75 2.25a.75.75 0 0 0 0 1.5h5.5a.75.75 0 0 0 0-1.5h-5.5Z" clipRule="evenodd" />
                </svg>
                <h2 className="text-base font-semibold text-text group-hover:text-primary transition-colors">
                  {dataset.prettyName}
                </h2>
              </div>
              <p className="text-sm text-text-muted mb-3">
                {dataset.description}
              </p>
              <div className="flex items-center justify-between">
                <div className="flex flex-wrap gap-1.5">
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-highlight/10 text-highlight font-medium">
                    {dataset.source}
                  </span>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-primary/10 text-primary font-medium">
                    {dataset.updateFrequency}
                  </span>
                </div>
                <div className="flex items-center gap-3 text-text-muted text-xs shrink-0">
                  {dataset.records && (
                    <span>{formatRecords(dataset.records)}</span>
                  )}
                </div>
              </div>
            </ScrollReveal>
          ))}
        </div>

        <ScrollReveal direction="up" className="text-center mt-10">
          <a
            href={HF_PROFILE}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block px-8 py-3 rounded-xl gradient-brand text-white font-semibold hover:opacity-90 transition-opacity"
          >
            Explore All {TOTAL_DATASETS} Datasets on Hugging Face
          </a>
        </ScrollReveal>
      </section>

      <RelatedContent items={[
        { href: '/code', title: 'Code', subtitle: 'Open-source projects and demos', metric: '6 repositories' },
        { href: '/youtube-videos', title: 'Videos', subtitle: 'Tutorials, demos, and deep dives', metric: `${YOUTUBE_STATS.subscriberCount}K subscribers` },
        { href: '/publications', title: 'Publications', subtitle: 'Technical articles on AI and ML', metric: `${TOTAL_ARTICLES}+ articles` },
      ]} />
    </>
  );
}
