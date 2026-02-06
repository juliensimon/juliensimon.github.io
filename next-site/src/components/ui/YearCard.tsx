'use client';

import Link from 'next/link';
import ScrollReveal from './ScrollReveal';

interface YearCardProps {
  year: number;
  count: number;
  label: string;
  href: string;
  index?: number;
}

export default function YearCard({ year, count, label, href, index = 0 }: YearCardProps) {
  return (
    <ScrollReveal direction="scale" delay={index * 0.08}>
      <Link
        href={href}
        className="block glass-card rounded-xl p-5 text-center hover:scale-[1.02] transition-all duration-300 group relative overflow-hidden"
      >
        <div className="text-2xl font-bold font-heading gradient-brand-text mb-1">
          {year}
        </div>
        <div className="text-sm text-text-muted">
          {count} {label}
        </div>
        <div className="absolute inset-x-0 bottom-3 text-xs text-primary font-medium opacity-0 group-hover:opacity-100 transition-opacity duration-300">
          View {label} →
        </div>
      </Link>
    </ScrollReveal>
  );
}
