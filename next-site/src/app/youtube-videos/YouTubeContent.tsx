'use client';

import { motion } from 'framer-motion';

import MetricCard from '@/components/ui/MetricCard';
import YearCard from '@/components/ui/YearCard';
import { YOUTUBE_STATS, VIDEO_YEARS } from '@/data/youtube';

export default function YouTubeContent() {
  return (
    <>
      <div className="pt-24 pb-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold font-heading text-text">
          Videos
        </h1>
        <p className="mt-2 text-text-muted">
          {`${YOUTUBE_STATS.totalVideos}+ videos | ${YOUTUBE_STATS.subscribers} subscribers`}
        </p>
      </div>

      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 mb-12">
          <MetricCard value={YOUTUBE_STATS.totalVideos} suffix="+" label="Videos" index={0} />
          <MetricCard value={parseInt(YOUTUBE_STATS.subscribers)} suffix="K+" label="Subscribers" index={1} />
          <MetricCard value={YOUTUBE_STATS.yearsOfContent} suffix="" label="Years of Content" index={2} />
        </div>

        {/* Channel link */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <a
            href="https://youtube.com/juliensimonfr"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block px-8 py-3 rounded-xl gradient-brand text-white font-semibold hover:opacity-90 transition-opacity"
          >
            Visit YouTube Channel
          </a>
        </motion.div>

        {/* Year grid */}
        <h2 className="text-2xl font-bold font-heading gradient-brand-text mb-6 text-center">
          Browse by Year
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {VIDEO_YEARS.map((y, i) => (
            <YearCard
              key={y.year}
              year={y.year}
              count={y.count}
              label="videos"
              href={y.href}
              index={i}
            />
          ))}
        </div>
      </section>
    </>
  );
}
