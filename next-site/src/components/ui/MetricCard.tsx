'use client';

import ScrollReveal from './ScrollReveal';
import AnimatedCounter from './AnimatedCounter';

interface MetricCardProps {
  value: number;
  suffix: string;
  label: string;
  index?: number;
}

export default function MetricCard({ value, suffix, label, index = 0 }: MetricCardProps) {
  return (
    <ScrollReveal direction="up" delay={index * 0.1} margin="-50px" className="relative group">
      <div className="glass-card rounded-2xl p-6 text-center hover:scale-[1.02] transition-transform duration-300">
        <div className="text-4xl font-bold font-heading gradient-brand-text mb-1">
          <AnimatedCounter value={value} suffix={suffix} />
        </div>
        <div className="text-sm font-medium text-text-muted">
          {label}
        </div>
      </div>
    </ScrollReveal>
  );
}
