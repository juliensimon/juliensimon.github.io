'use client';

import { motion } from 'framer-motion';

import { REPOSITORIES, GITHUB_PROFILE } from '@/data/code';

export default function CodeContent() {
  return (
    <>
      <div className="pt-24 pb-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold font-heading text-text">
          Code
        </h1>
        <p className="mt-2 text-text-muted">
          Open-source projects, demos, and technical examples
        </p>
      </div>

      <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        <h2 className="sr-only">Open Source Repositories</h2>
        <div className="grid sm:grid-cols-2 gap-5">
          {REPOSITORIES.map((repo, i) => (
            <motion.a
              key={repo.name}
              href={repo.url}
              target="_blank"
              rel="noopener noreferrer"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.08 }}
              className={`block glass-card rounded-xl p-6 hover:scale-[1.02] transition-all duration-300 group ${
                repo.featured ? 'border border-primary/30' : ''
              }`}
            >
              <div className="flex items-center gap-2 mb-2">
                <svg className="w-5 h-5 text-text-muted" viewBox="0 0 16 16" fill="currentColor">
                  <path d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z" />
                </svg>
                <h3 className="text-base font-semibold text-text group-hover:text-primary transition-colors">
                  {repo.name}
                </h3>
                {repo.featured && (
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-primary/15 text-primary font-semibold">Featured</span>
                )}
              </div>
              <p className="text-sm text-text-muted mb-3">
                {repo.description}
              </p>
              <div className="flex flex-wrap gap-1.5">
                {repo.language && (
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-highlight/10 text-highlight font-medium">
                    {repo.language}
                  </span>
                )}
                {repo.tags.map((tag) => (
                  <span key={tag} className="text-[10px] px-2 py-0.5 rounded-full bg-primary/10 text-primary font-medium">
                    {tag}
                  </span>
                ))}
              </div>
            </motion.a>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mt-10"
        >
          <a
            href={GITHUB_PROFILE}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block px-8 py-3 rounded-xl gradient-brand text-white font-semibold hover:opacity-90 transition-opacity"
          >
            View All Repositories on GitHub
          </a>
        </motion.div>
      </section>
    </>
  );
}
