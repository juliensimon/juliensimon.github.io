'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';

interface YearCardProps {
  year: number;
  count: number;
  label: string;
  href: string;
  index?: number;
}

export default function YearCard({ year, count, label, href, index = 0 }: YearCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.4, delay: index * 0.06 }}
    >
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
    </motion.div>
  );
}
