'use client';

import GradientHero from '@/components/ui/GradientHero';
import ScrollReveal from '@/components/ui/ScrollReveal';
import RelatedContent from '@/components/ui/RelatedContent';
import { PINNED_REPOSITORIES, GITHUB_PROFILE } from '@/data/code';

export default function CodeContent() {
  return (
    <>
      <GradientHero
        title="Code"
        subtitle="Open-source projects, demos, and technical examples"
      />

      <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        <h2 className="sr-only">Open Source Repositories</h2>
        <div className="grid sm:grid-cols-2 gap-5">
          {PINNED_REPOSITORIES.map((repo, i) => (
            <ScrollReveal
              key={repo.name}
              as="a"
              href={repo.url}
              target="_blank"
              rel="noopener noreferrer"
              direction="up"
              delay={i * 0.08}
              className="block glass-card rounded-xl p-6 hover:scale-[1.02] transition-all duration-300 group"
            >
              <div className="flex items-center gap-2 mb-2">
                <svg className="w-5 h-5 text-text-muted" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
                  <path d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z" />
                </svg>
                <h2 className="text-base font-semibold text-text group-hover:text-primary transition-colors">
                  {repo.name}
                </h2>
              </div>
              <p className="text-sm text-text-muted mb-3">
                {repo.description}
              </p>
              <div className="flex items-center justify-between">
                <div className="flex flex-wrap gap-1.5">
                  {repo.language && (
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-highlight/10 text-highlight font-medium">
                      {repo.language}
                    </span>
                  )}
                  {repo.tags.slice(0, 2).map((tag) => (
                    <span key={tag} className="text-[10px] px-2 py-0.5 rounded-full bg-primary/10 text-primary font-medium">
                      {tag}
                    </span>
                  ))}
                </div>
                <div className="flex items-center gap-3 text-text-muted text-xs shrink-0">
                  {repo.stars != null && (
                    <span className="flex items-center gap-1">
                      <svg className="w-3.5 h-3.5" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
                        <path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z" />
                      </svg>
                      {repo.stars}
                    </span>
                  )}
                  {repo.forks != null && (
                    <span className="flex items-center gap-1">
                      <svg className="w-3.5 h-3.5" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
                        <path d="M5 5.372v.878c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-.878a2.25 2.25 0 1 1 1.5 0v.878a2.25 2.25 0 0 1-2.25 2.25h-1.5v2.128a2.251 2.251 0 1 1-1.5 0V8.5h-1.5A2.25 2.25 0 0 1 3.5 6.25v-.878a2.25 2.25 0 1 1 1.5 0ZM5 3.25a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Zm6.75.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm-3 8.75a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Z" />
                      </svg>
                      {repo.forks}
                    </span>
                  )}
                </div>
              </div>
            </ScrollReveal>
          ))}
        </div>

        <ScrollReveal direction="up" className="text-center mt-10">
          <a
            href={GITHUB_PROFILE}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block px-8 py-3 rounded-xl gradient-brand text-white font-semibold hover:opacity-90 transition-opacity"
          >
            View All Repositories on GitHub
          </a>
        </ScrollReveal>
      </section>

      <RelatedContent items={[
        { href: '/youtube-videos', title: 'Videos', subtitle: 'Tutorials, demos, and deep dives', metric: '494K subscribers' },
        { href: '/publications', title: 'Publications', subtitle: 'Technical articles on AI and ML', metric: '454+ articles' },
        { href: '/experience', title: 'Experience', subtitle: '30+ years of technology leadership' },
      ]} />
    </>
  );
}
