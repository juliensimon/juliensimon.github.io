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
    <ScrollReveal direction="scale" delay={index * 0.06}>
      <Link
        href={href}
        className="block glass-card rounded-xl p-5 text-center hover:scale-[1.03] transition-all duration-300 group"
      >
        <div className="text-2xl font-bold font-heading gradient-brand-text mb-1">
          {year}
        </div>
        <div className="text-sm text-text-muted">
          {count} {label}
        </div>
      </Link>
    </ScrollReveal>
  );
}
