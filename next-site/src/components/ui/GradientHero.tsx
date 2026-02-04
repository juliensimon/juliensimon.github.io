'use client';

import { motion } from 'framer-motion';

interface GradientHeroProps {
  title: string;
  subtitle?: string;
  children?: React.ReactNode;
}

export default function GradientHero({ title, subtitle, children }: GradientHeroProps) {
  return (
    <section className="relative min-h-[40vh] flex items-center justify-center overflow-hidden pt-24 pb-16">
      {/* Gradient mesh background */}
      <div className="absolute inset-0 gradient-mesh" />
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-background" />

      <div className="relative z-10 max-w-4xl mx-auto px-4 text-center">
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-4xl sm:text-5xl lg:text-6xl font-bold font-heading gradient-brand-text mb-4"
        >
          {title}
        </motion.h1>
        {subtitle && (
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.15 }}
            className="text-lg text-text-muted max-w-2xl mx-auto"
          >
            {subtitle}
          </motion.p>
        )}
        {children}
      </div>
    </section>
  );
}
