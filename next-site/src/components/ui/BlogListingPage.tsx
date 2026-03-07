'use client';

import { useState } from 'react';
import Link from 'next/link';

import GradientHero from './GradientHero';
import ScrollReveal from './ScrollReveal';

export interface BlogPost {
  title: string;
  href: string;
  date?: string;
  description?: string;
  localHref?: string;
}

interface Props {
  title: string;
  subtitle: string;
  posts: BlogPost[];
  backLabel?: string;
}

export default function BlogListingPage({ title, subtitle, posts, backLabel = 'Publications' }: Props) {
  const [search, setSearch] = useState('');

  const filtered = search
    ? posts.filter((p) =>
        p.title.toLowerCase().includes(search.toLowerCase()) ||
        p.description?.toLowerCase().includes(search.toLowerCase())
      )
    : posts;

  return (
    <>
      <GradientHero title={title} subtitle={subtitle} />

      <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        {/* Search */}
        <div className="mb-8">
          <input
            type="text"
            placeholder="Filter posts..."
            aria-label="Filter posts"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full max-w-md mx-auto block px-4 py-2 rounded-lg border border-border bg-surface text-text placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-primary/50"
          />
        </div>

        {/* Posts list */}
        <div className="space-y-3">
          {filtered.map((post, i) => {
            const isExternal = post.href.startsWith('https://');
            const linkProps = isExternal
              ? { target: '_blank' as const, rel: 'noopener noreferrer' }
              : {};
            return (
              <ScrollReveal
                key={post.href}
                as="a"
                href={post.href}
                {...linkProps}
                direction="up"
                delay={Math.min(i * 0.03, 0.5)}
                margin="-20px"
                className="block glass-card rounded-lg p-4 hover:scale-[1.005] transition-all duration-300 group"
              >
                {post.date && (
                  <p className="text-xs text-text-muted mb-0.5">
                    {post.date}
                  </p>
                )}
                <h2 className="text-sm font-medium text-text group-hover:text-primary transition-colors">
                  {post.title}
                  {isExternal && <span className="sr-only"> (opens in new tab)</span>}
                </h2>
                {post.description && (
                  <p className="text-xs text-text-muted mt-1 line-clamp-2">
                    {post.description}
                  </p>
                )}
                {post.localHref && (
                  <p className="mt-1">
                    <a
                      href={post.localHref}
                      onClick={(e) => e.stopPropagation()}
                      className="text-[10px] text-primary/60 hover:text-primary transition-colors"
                    >
                      local copy
                    </a>
                  </p>
                )}
              </ScrollReveal>
            );
          })}
        </div>

        {filtered.length === 0 && (
          <p className="text-center text-text-muted py-8">
            No posts match your search.
          </p>
        )}

        <div className="mt-8 text-center">
          <Link href="/publications" className="text-primary hover:text-primary-hover font-medium">
            &larr; Back to {backLabel}
          </Link>
        </div>
      </section>
    </>
  );
}
