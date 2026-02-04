'use client';

import Link from 'next/link';

interface Props {
  year: string;
  count?: number;
}

export default function SpeakingYearContent({ year, count }: Props) {
  return (
    <>
      <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-20">
        <iframe
          src={`/speaking-${year}.html`}
          title={`Speaking events ${year}`}
          className="w-full min-h-[80vh] rounded-xl border border-border bg-white"
          style={{ border: 'none' }}
        />

        <div className="mt-8 text-center">
          <Link href="/speaking" className="text-primary hover:text-primary-hover font-medium">
            &larr; Back to Speaking Overview
          </Link>
        </div>
      </section>
    </>
  );
}
