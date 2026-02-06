'use client';

import Image from 'next/image';
import Link from 'next/link';
import MetricCard from '@/components/ui/MetricCard';
import ScrollReveal from '@/components/ui/ScrollReveal';
import SocialButton from '@/components/ui/SocialButton';
import TypingEffect from '@/components/ui/TypingEffect';
import { SOCIAL_LINKS, METRICS } from '@/lib/constants';

const LATEST_UPDATES = [
  {
    title: 'The EU Cloud and AI Development Act (CADA): A Last Shot at Cloud Sovereignty, or Another Expensive Debacle?',
    href: '/blog/industry-perspectives/2026-02-03_the-eu-cloud-and-ai-development-act-cada-a-last-shot-at-cloud-sovereignty-or-another-expensive-debacle/index.html',
    date: 'February 3, 2026',
    icon: 'article',
  },
  {
    title: 'Arcee AI Trinity Large: An Open 400B MoE Model',
    href: '/youtube/2026/20260201_Arcee_AI_Trinity_Large_An_Open_400B_MoE_Model.html',
    date: 'February 1, 2026',
    icon: 'video',
  },
  {
    title: 'Build Mobile Apps with Replit in Minutes!',
    href: '/youtube/2026/20260125_Build_Mobile_Apps_with_Replit_in_Minutes.html',
    date: 'January 25, 2026',
    icon: 'video',
  },
  {
    title: 'AI Sovereignty in Europe: A Decision Framework',
    href: '/blog/industry-perspectives/2026-01-19_ai-sovereignty-in-europe-a-decision-framework/index.html',
    date: 'January 19, 2026',
    icon: 'article',
  },
  {
    title: 'Verdent : AI Coding with Parallel Agents — Full Demo!',
    href: '/youtube/2026/20260119_Verdent_AI_Coding_with_Parallel_Agents_Full_Demo.html',
    date: 'January 19, 2026',
    icon: 'video',
  },
];

const EXPERTISE_CARDS = [
  {
    title: 'Portfolio AI Acceleration',
    description:
      'Accelerating cloud and AI initiatives across Private Equity and Venture Capital portfolios at Fortino Capital. Supporting portfolio companies from product to engineering to operations to GTM.',
    link: '/experience',
    linkText: 'View Executive Experience',
  },
  {
    title: 'AI & Machine Learning Leadership',
    description:
      '30+ years of technology leadership including roles at AWS, Hugging Face, and Arcee AI. Proven track record scaling AI/ML teams and helping Fortune 500 companies implement cost-effective AI solutions.',
    link: '/experience',
    linkText: 'View Executive Experience',
  },
  {
    title: 'Cloud & Enterprise Strategy',
    description:
      'Deep expertise in cloud-native AI deployment, enterprise architecture, and infrastructure scaling. Helping portfolio companies optimize cloud costs, accelerate product development, and scale operations.',
    link: '/code',
    linkText: 'View Technical Examples',
  },
  {
    title: 'Global Thought Leadership',
    description:
      '684+ speaking engagements worldwide, including major industry events, Fortune 500 companies, and institutions like UNESCO, World Bank, New York Federal Reserve, and sovereign funds.',
    link: '/speaking',
    linkText: 'View Speaking History',
  },
];

const PHILOSOPHY_CARDS = [
  { title: 'Small Models, Big Results', description: 'Champion Small Language Models that deliver enterprise-grade performance with significantly lower computational requirements.' },
  { title: 'Privacy-First Architecture', description: 'Design AI solutions for on-premises and private cloud deployment, ensuring enterprises maintain complete control.' },
  { title: 'Enterprise-Scale Implementation', description: 'Build AI strategies that grow with business needs—from proof-of-concept to company-wide deployment.' },
  { title: 'Transparency Over Black Boxes', description: 'Champion open-weights models that enterprises can inspect, understand, and control.' },
];

const RECOGNITIONS = [
  'First Published Book on Amazon SageMaker (2019) - "Learn Amazon SageMaker" became the industry standard reference',
  'AI Magazine #1 AI Evangelist (2021) - Ranked as the leading AI evangelist alongside luminaries like Andrew Ng',
  'AWS Level 8 Promotion (2021) - Extremely rare achievement equivalent to Director level for individual contributors',
  'Arm Ambassador (2025) - Recognized for expertise in AI inference optimization on Arm platforms',
  'Featured in "The 100 Shaping AI in Europe" (2025) - Recognized by L\'Opinion and Oliver Wyman in the "Builders" category',
];

const TYPING_PHRASES = [
  'Accelerating AI across PE/VC portfolios',
  'Championing Small Language Models',
  'Bridging AI research and enterprise reality',
  'Making AI practical, not magical',
];

export default function HomeContent() {
  return (
    <>
      {/* ── Hero Section ─────────────────────────────────── */}
      <section className="relative min-h-[70vh] md:min-h-[85vh] flex items-center justify-center overflow-hidden pt-20">
        <div className="absolute inset-0 gradient-mesh" />
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-background" />

        <div className="relative z-10 max-w-4xl mx-auto px-4 text-center">
          <div className="animate-page-fade-scale">
            <Image
              src="/assets/julien.webp"
              alt="Julien Simon - AI Operating Partner at Fortino Capital"
              width={160}
              height={160}
              priority
              className="mx-auto rounded-full border-4 border-primary/30 shadow-xl shadow-primary/10 mb-6"
            />
          </div>

          <h1 className="mb-3 animate-page-fade-up" style={{ animationDelay: '0.1s' }}>
            <span className="block text-5xl sm:text-6xl lg:text-7xl font-bold font-heading gradient-brand-text">
              Julien Simon
            </span>
            <span className="block text-xl sm:text-2xl font-semibold text-text mt-3">
              AI Operating Partner @ Fortino Capital
            </span>
          </h1>

          <div
            className="text-lg text-text-muted h-8 mb-8 animate-page-fade-in"
            style={{ animationDelay: '0.4s' }}
          >
            <TypingEffect texts={TYPING_PHRASES} />
          </div>

          <div
            className="flex flex-wrap justify-center gap-2 animate-page-fade-up"
            style={{ animationDelay: '0.5s' }}
          >
            {SOCIAL_LINKS.map((link) => (
              <SocialButton key={link.name} name={link.name} href={link.href} />
            ))}
          </div>
        </div>
      </section>

      {/* ── About + Latest Updates ────────────────────────── */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid lg:grid-cols-[2fr_1fr] gap-12">
          <div>
            <ScrollReveal direction="left">
              <h2 className="text-3xl font-bold font-heading gradient-brand-text mb-6">
                About
              </h2>
            </ScrollReveal>
            <ScrollReveal direction="up" delay={0.1} className="space-y-4 text-text leading-relaxed">
              <p>
                <strong>Julien Simon bridges the gap between AI research and enterprise reality.</strong>{' '}
                While many experts choose either academic research or practical implementation,
                Julien deliberately combines both. He reads research papers, decrypts the mathematical
                foundations behind breakthrough methods, and obsesses over translating them into
                shareable knowledge and solutions that actually work at scale.
              </p>
              <p>
                As AI Operating Partner at Fortino Capital, Julien accelerates cloud and AI
                initiatives across both the Private Equity and Venture Capital portfolios. With
                over 30 years of technology experience at AWS, Hugging Face, Arcee AI, Criteo, and
                other major companies, he brings deep technical expertise combined with executive
                leadership to help portfolio companies scale from product to engineering to
                operations to GTM.
              </p>
              <p>
                Julien&apos;s career reflects continuous learning across computing&apos;s evolution,
                always grounded in first principles. He&apos;s adapted from MySQL web platforms to
                Generative AI, from programming Motorola 68k processors to optimizing modern AI
                accelerators, from real-time operating systems to cloud-native architectures.
              </p>
              <p>
                Julien&apos;s mission? <strong>To demystify buzzwords and cut through industry hype to
                focus on what actually works in production.</strong>
              </p>
            </ScrollReveal>
          </div>

          <div>
            <ScrollReveal direction="right">
              <h2 className="text-3xl font-bold font-heading gradient-brand-text mb-6">
                Latest Updates
              </h2>
            </ScrollReveal>
            <div className="space-y-4">
              {LATEST_UPDATES.map((item, i) => (
                <ScrollReveal
                  key={item.href}
                  as="a"
                  href={item.href}
                  direction="up"
                  delay={i * 0.08}
                  className="block glass-card rounded-xl p-4 hover:scale-[1.01] transition-all duration-300 group"
                >
                  <p className="text-xs text-text-muted mb-1">
                    {item.icon === 'video' ? (
                      <>
                        <span aria-hidden="true">📺</span>
                        <span className="sr-only">Video: </span>
                      </>
                    ) : (
                      <>
                        <span aria-hidden="true">📝</span>
                        <span className="sr-only">Article: </span>
                      </>
                    )}{' '}
                    {item.date}
                  </p>
                  <h3 className="text-sm font-semibold text-text group-hover:text-primary transition-colors">
                    {item.title}
                  </h3>
                </ScrollReveal>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ── Industry Impact & Metrics ──────────────────────── */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <ScrollReveal direction="up">
          <h2 className="text-3xl font-bold font-heading gradient-brand-text mb-4 text-center">
            Industry Impact &amp; Recognition
          </h2>
        </ScrollReveal>
        <ScrollReveal direction="up" delay={0.1} className="text-center text-text-muted max-w-3xl mx-auto mb-10">
          <p>
            Julien&apos;s approach to AI—combining theoretical depth with practical results—has
            earned recognition across the global tech community.
          </p>
        </ScrollReveal>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
          {METRICS.map((m, i) => (
            <MetricCard key={m.label} value={m.value} suffix={m.suffix} label={m.label} index={i} />
          ))}
        </div>

        {/* Philosophy cards */}
        <div className="grid sm:grid-cols-2 gap-4 mb-12">
          {PHILOSOPHY_CARDS.map((card, i) => (
            <ScrollReveal
              key={card.title}
              direction="up"
              delay={i * 0.08}
              className="glass-card rounded-xl p-5 border-l-4 border-primary"
            >
              <h3 className="text-base font-semibold text-text mb-2">
                {card.title}
              </h3>
              <p className="text-sm text-text-muted">
                {card.description}
              </p>
            </ScrollReveal>
          ))}
        </div>

        {/* Recognition */}
        <div>
          <h3 className="text-xl font-bold font-heading text-text mb-4">
            Recognition &amp; Milestones
          </h3>
          <div className="space-y-3">
            {RECOGNITIONS.map((item, i) => (
              <ScrollReveal
                key={i}
                direction="left"
                delay={i * 0.08}
                className="glass-card rounded-lg p-4 border-l-4 border-secondary"
              >
                <p className="text-sm text-text">{item}</p>
              </ScrollReveal>
            ))}
          </div>
        </div>
      </section>

      {/* ── Expertise Grid ─────────────────────────────────── */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <ScrollReveal direction="up">
          <h2 className="text-3xl font-bold font-heading gradient-brand-text mb-8 text-center">
            Expertise &amp; Leadership Impact
          </h2>
        </ScrollReveal>

        <div className="grid sm:grid-cols-2 gap-5">
          {EXPERTISE_CARDS.map((card, i) => (
            <ScrollReveal
              key={card.title}
              direction="up"
              delay={i * 0.08}
              className="glass-card rounded-xl p-6 border-l-4 border-primary flex flex-col justify-between"
            >
              <div>
                <h3 className="text-lg font-semibold text-text mb-2">
                  {card.title}
                </h3>
                <p className="text-sm text-text-muted mb-4">
                  {card.description}
                </p>
              </div>
              <Link
                href={card.link}
                className="text-sm font-medium text-primary hover:text-primary-hover transition-colors"
              >
                {card.linkText} &rarr;
              </Link>
            </ScrollReveal>
          ))}
        </div>
      </section>

      {/* ── Contact ────────────────────────────────────────── */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
        <ScrollReveal direction="up">
          <h2 className="text-3xl font-bold font-heading gradient-brand-text mb-4">
            Contact
          </h2>
        </ScrollReveal>
        <ScrollReveal direction="up" delay={0.1} className="text-text-muted space-y-2">
          <p>For portfolio company advisory, strategy consulting, speaking engagements, or AI partnerships:</p>
          <p>
            <a href="mailto:julien@julien.org" className="text-primary hover:text-primary-hover font-medium">
              julien@julien.org
            </a>
          </p>
        </ScrollReveal>
      </section>
    </>
  );
}
