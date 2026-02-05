'use client';

import Image from 'next/image';
import { motion } from 'framer-motion';

import { BOOKS } from '@/data/books';

export default function BooksContent() {
  return (
    <>
      <div className="pt-24 pb-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold font-heading text-text">
          Books
        </h1>
        <p className="mt-2 text-text-muted">
          Published works on machine learning and cloud computing
        </p>
      </div>

      <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        <div className="space-y-6">
          {BOOKS.map((book, i) => (
            <motion.div
              key={book.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="glass-card rounded-xl p-6 flex gap-6"
            >
              {book.coverImage && (
                <div className="shrink-0 hidden sm:block">
                  <Image
                    src={book.coverImage}
                    alt={book.title}
                    width={112}
                    height={168}
                    className="w-28 rounded-lg shadow-md"
                  />
                </div>
              )}
              <div className="flex-1">
                <div className="flex items-start justify-between mb-1">
                  <h2 className="text-xl font-bold font-heading text-text">
                    {book.title}
                  </h2>
                </div>
                <p className="text-xs text-highlight font-semibold mb-2">{book.role}</p>
                <p className="text-sm text-text mb-3">
                  {book.description}
                </p>
                {book.editions && (
                  <p className="text-xs text-text-muted mb-2">{book.editions}</p>
                )}
                <div className="flex items-center gap-4 text-xs text-text-muted">
                  {book.publisher && <span>{book.publisher}</span>}
                  {book.pages && <span>{book.pages} pages</span>}
                  {book.amazonUrl && (
                    <a href={book.amazonUrl} target="_blank" rel="noopener noreferrer" className="text-primary hover:text-primary-hover font-medium">
                      Amazon &rarr;
                    </a>
                  )}
                  {book.githubUrl && (
                    <a href={book.githubUrl} target="_blank" rel="noopener noreferrer" className="text-primary hover:text-primary-hover font-medium">
                      GitHub &rarr;
                    </a>
                  )}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </section>
    </>
  );
}
