'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';


export interface BlogPost {
  title: string;
  href: string;
  date?: string;
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
    ? posts.filter((p) => p.title.toLowerCase().includes(search.toLowerCase()))
    : posts;

  return (
    <>
      <div className="pt-24 pb-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold font-heading text-text">
          {title}
        </h1>
        {subtitle && (
          <p className="mt-2 text-text-muted">
            {subtitle}
          </p>
        )}
      </div>

      <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        {/* Search */}
        <div className="mb-8">
          <input
            type="text"
            placeholder="Filter posts..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full max-w-md mx-auto block px-4 py-2 rounded-lg border border-border bg-surface text-text placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-primary/50"
          />
        </div>

        {/* Posts list */}
        <div className="space-y-3">
          {filtered.map((post, i) => (
            <motion.a
              key={post.href}
              href={post.href}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-20px' }}
              transition={{ delay: Math.min(i * 0.03, 0.5) }}
              className="block glass-card rounded-lg p-4 hover:scale-[1.005] transition-all duration-300 group"
            >
              {post.date && (
                <p className="text-xs text-text-muted mb-0.5">
                  {post.date}
                </p>
              )}
              <h3 className="text-sm font-medium text-text group-hover:text-primary transition-colors">
                {post.title}
              </h3>
            </motion.a>
          ))}
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
