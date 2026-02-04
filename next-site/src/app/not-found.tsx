'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';

export default function NotFound() {
  return (
    <section className="min-h-[80vh] flex items-center justify-center pt-20">
      <div className="text-center px-4">
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className="text-8xl font-bold font-heading gradient-brand-text mb-4">404</h1>
          <p className="text-xl text-text-muted mb-8">
            This page doesn&apos;t exist yet. Maybe it&apos;s still being migrated.
          </p>
          <Link
            href="/"
            className="inline-block px-8 py-3 rounded-xl gradient-brand text-white font-semibold hover:opacity-90 transition-opacity"
          >
            Back to Home
          </Link>
        </motion.div>
      </div>
    </section>
  );
}
