'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';

import { PUBLICATION_CATEGORIES, TOTAL_ARTICLES } from '@/data/publications';

export default function PublicationsContent() {
  return (
    <>
      <div className="pt-24 pb-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold font-heading text-text">
          Publications
        </h1>
        <p className="mt-2 text-text-muted">
          {`${TOTAL_ARTICLES}+ technical articles across multiple platforms`}
        </p>
      </div>

      <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        <div className="grid sm:grid-cols-2 gap-5">
          {PUBLICATION_CATEGORIES.map((cat, i) => {
            const isExternal = cat.href.startsWith('/blog/');
            const Wrapper = isExternal ? 'a' : Link;
            const linkProps = isExternal
              ? { href: cat.href }
              : { href: cat.href };

            return (
              <motion.div
                key={cat.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.08 }}
              >
                <Wrapper
                  {...linkProps}
                  className="block glass-card rounded-xl p-6 hover:scale-[1.02] transition-all duration-300 group h-full"
                >
                  <div className="flex items-baseline justify-between mb-1">
                    <h3 className="text-lg font-semibold text-text group-hover:text-primary transition-colors">
                      {cat.name}
                    </h3>
                    <span className="text-sm font-bold text-highlight">{cat.count}</span>
                  </div>
                  <p className="text-xs text-primary/70 mb-2">{cat.dateRange}</p>
                  <p className="text-sm text-text-muted">
                    {cat.description}
                  </p>
                </Wrapper>
              </motion.div>
            );
          })}
        </div>
      </section>
    </>
  );
}
