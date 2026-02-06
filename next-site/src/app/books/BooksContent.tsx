'use client';

import Image from 'next/image';

import GradientHero from '@/components/ui/GradientHero';
import ScrollReveal from '@/components/ui/ScrollReveal';
import { BOOKS } from '@/data/books';

export default function BooksContent() {
  return (
    <>
      <GradientHero
        title="Books"
        subtitle="Published works on machine learning and cloud computing"
      />

      <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        <div className="space-y-6">
          {BOOKS.map((book, i) => (
            <ScrollReveal
              key={book.title}
              direction="up"
              delay={i * 0.08}
              className="glass-card rounded-xl p-6 flex gap-6"
            >
              {book.coverImage && (
                <div className="shrink-0 hidden sm:block">
                  <Image
                    src={book.coverImage}
                    alt={`Cover of ${book.title}`}
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
            </ScrollReveal>
          ))}
        </div>
      </section>
    </>
  );
}
