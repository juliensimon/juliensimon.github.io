'use client';

import Link from 'next/link';
import ScrollReveal from './ScrollReveal';

interface RelatedItem {
  href: string;
  title: string;
  subtitle: string;
  metric?: string;
}

interface RelatedContentProps {
  items: RelatedItem[];
}

export default function RelatedContent({ items }: RelatedContentProps) {
  return (
    <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
      <ScrollReveal direction="up">
        <h2 className="text-2xl font-bold font-heading gradient-brand-text mb-6 text-center">
          Explore More
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {items.map((item, i) => (
            <ScrollReveal
              key={item.href}
              direction="up"
              delay={i * 0.1}
            >
              <Link
                href={item.href}
                className="block glass-card rounded-xl p-6 hover:scale-[1.02] transition-all duration-300 group h-full"
              >
                <h3 className="text-lg font-semibold text-text group-hover:text-primary transition-colors mb-1">
                  {item.title}
                </h3>
                <p className="text-sm text-text-muted mb-3">
                  {item.subtitle}
                </p>
                {item.metric && (
                  <p className="text-sm font-bold text-highlight">
                    {item.metric}
                  </p>
                )}
              </Link>
            </ScrollReveal>
          ))}
        </div>
      </ScrollReveal>
    </section>
  );
}
