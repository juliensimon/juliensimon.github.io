'use client';

import { motion } from 'framer-motion';
import AnimatedCounter from './AnimatedCounter';

interface MetricCardProps {
  value: number;
  suffix: string;
  label: string;
  index?: number;
}

export default function MetricCard({ value, suffix, label, index = 0 }: MetricCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-50px' }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
      className="relative group"
    >
      <div className="glass-card rounded-2xl p-6 text-center hover:scale-[1.02] transition-transform duration-300">
        <div className="text-4xl font-bold font-heading gradient-brand-text mb-1">
          <AnimatedCounter value={value} suffix={suffix} />
        </div>
        <div className="text-sm font-medium text-text-muted">
          {label}
        </div>
      </div>
    </motion.div>
  );
}
