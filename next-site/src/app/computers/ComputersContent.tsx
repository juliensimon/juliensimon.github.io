'use client';

import Image from 'next/image';
import { motion } from 'framer-motion';

import { COMPUTERS, UNIX_JOURNEY, UNIX_BOOKS, VINTAGE_CDS, UNIX_PHILOSOPHY } from '@/data/computers';

export default function ComputersContent() {
  return (
    <>
      <div className="pt-24 pb-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold font-heading text-text">
          Computers, UNIX, and Me
        </h1>
        <p className="mt-2 text-text-muted">
          A journey through computing history — the machines that shaped a career
        </p>
      </div>

      <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        {/* Computers grid */}
        <div className="grid sm:grid-cols-2 gap-5">
          {COMPUTERS.map((computer, i) => (
            <motion.div
              key={computer.name}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.06 }}
              className="glass-card rounded-xl overflow-hidden"
            >
              {computer.image && (
                <div className="aspect-video relative bg-surface">
                  <Image
                    src={computer.image}
                    alt={computer.name}
                    fill
                    className="object-contain p-4"
                    sizes="(max-width: 640px) 100vw, 50vw"
                  />
                </div>
              )}
              <div className="p-5">
                <div className="flex items-baseline justify-between mb-1">
                  <h2 className="text-lg font-semibold text-text">
                    {computer.wikiUrl ? (
                      <a href={computer.wikiUrl} target="_blank" rel="noopener noreferrer" className="hover:text-primary transition-colors">
                        {computer.name}
                      </a>
                    ) : computer.name}
                  </h2>
                  <span className="text-sm text-highlight font-bold">{computer.year}</span>
                </div>
                <p className="text-sm text-text-muted mb-2">
                  {computer.cpu} &middot; {computer.ram}
                </p>
                {computer.software && (
                  <p className="text-sm text-text-muted">
                    {computer.software}
                  </p>
                )}
              </div>
            </motion.div>
          ))}
        </div>

        {/* UNIX Journey */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-20"
        >
          <h2 className="text-3xl font-bold font-heading gradient-brand-text mb-6 text-center">
            My UNIX Journey (1992&ndash;)
          </h2>
          <div className="glass-card rounded-xl p-6 space-y-4">
            {UNIX_JOURNEY.map((paragraph, i) => (
              <p key={i} className="text-base text-text leading-relaxed">
                {paragraph}
              </p>
            ))}
          </div>
        </motion.div>

        {/* UNIX Books */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-16"
        >
          <h2 className="text-3xl font-bold font-heading gradient-brand-text mb-6 text-center">
            UNIX Book Collection
          </h2>
          <div className="grid sm:grid-cols-2 gap-5">
            {UNIX_BOOKS.map((book, i) => (
              <motion.div
                key={book.title}
                initial={{ opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.05 }}
                className="glass-card rounded-xl p-5 flex gap-4"
              >
                {book.image && (
                  <div className="shrink-0 hidden sm:block">
                    <Image
                      src={book.image}
                      alt={`Cover of ${book.title}`}
                      width={80}
                      height={120}
                      className="w-20 rounded-lg shadow-md"
                    />
                  </div>
                )}
                <div className="flex-1 min-w-0">
                  <h3 className="text-base font-bold text-text mb-0.5">
                    {book.title}
                  </h3>
                  <p className="text-sm text-primary font-medium mb-1">
                    {book.author} &middot; {book.year}
                  </p>
                  <p className="text-sm text-text-muted leading-relaxed">
                    {book.description}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Vintage CDs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-16"
        >
          <h2 className="text-2xl font-bold font-heading gradient-brand-text mb-6 text-center">
            Vintage UNIX &amp; BSD CD Collection
          </h2>
          <div className="glass-card rounded-xl overflow-hidden">
            <div className="relative aspect-[3/1] bg-surface">
              <Image
                src="/assets/computers/vintage-cds-collection.webp"
                alt="Vintage UNIX and BSD CD collection"
                fill
                className="object-contain p-4"
                sizes="100vw"
              />
            </div>
            <div className="p-6 grid sm:grid-cols-2 gap-4">
              {VINTAGE_CDS.map((cd) => (
                <div key={cd.title}>
                  <h3 className="text-base font-semibold text-text">
                    {cd.title}
                    <span className="text-sm text-highlight font-normal ml-2">{cd.year}</span>
                  </h3>
                  <p className="text-sm text-text-muted mt-0.5">
                    {cd.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* UNIX Philosophy */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-16"
        >
          <h2 className="text-2xl font-bold font-heading gradient-brand-text mb-6 text-center">
            UNIX Philosophy
          </h2>
          <div className="glass-card rounded-xl overflow-hidden">
            <div className="relative aspect-[3/1] bg-surface">
              <Image
                src="/assets/computers/unix-license-plate.webp"
                alt="Live Free or Die - UNIX license plate"
                fill
                className="object-contain p-4"
                sizes="100vw"
              />
            </div>
            <div className="p-6">
              <p className="text-sm text-text leading-relaxed">
                {UNIX_PHILOSOPHY}
              </p>
            </div>
          </div>
        </motion.div>
      </section>
    </>
  );
}
