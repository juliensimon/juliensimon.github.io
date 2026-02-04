'use client';

import { motion } from 'framer-motion';

interface ContentCardProps {
  title: string;
  href: string;
  date?: string;
  excerpt?: string;
  icon?: string;
  index?: number;
  external?: boolean;
}

export default function ContentCard({
  title,
  href,
  date,
  excerpt,
  icon,
  index = 0,
  external = false,
}: ContentCardProps) {
  const linkProps = external
    ? { target: '_blank' as const, rel: 'noopener noreferrer' }
    : {};

  return (
    <motion.a
      href={href}
      {...linkProps}
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-30px' }}
      transition={{ duration: 0.4, delay: index * 0.05 }}
      className="block group glass-card rounded-xl p-5 hover:scale-[1.01] transition-all duration-300"
    >
      {date && (
        <p className="text-xs text-text-muted mb-1">
          {icon && <span className="mr-1">{icon}</span>}
          {date}
        </p>
      )}
      <h3 className="text-base font-semibold text-text group-hover:text-primary transition-colors">
        {title}
      </h3>
      {excerpt && (
        <p className="mt-1.5 text-sm text-text-muted line-clamp-2">
          {excerpt}
        </p>
      )}
    </motion.a>
  );
}
