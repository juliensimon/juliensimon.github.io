'use client';

import Image from 'next/image';
import Link from 'next/link';
import { motion } from 'framer-motion';
import MetricCard from '@/components/ui/MetricCard';
import SocialButton from '@/components/ui/SocialButton';
import TypingEffect from '@/components/ui/TypingEffect';
import { SOCIAL_LINKS, METRICS } from '@/lib/constants';

const LATEST_UPDATES = [
  {
    title: 'Advanced RAG Techniques with Arcee Trinity Mini Local',
    href: '/youtube/2026/20260109_Advanced_RAG_Techniques_with_Arcee_Trinity_Mini_Local.html',
    date: 'January 9, 2026',
    icon: 'video',
  },
  {
    title: 'Build a Reasoning AI Chatbot with Arcee AI Trinity Mini',
    href: '/youtube/2025/20251222_Build_a_Reasoning_AI_Chatbot_with_Arcee_AI_Trinity_Mini_Gradio_OpenRouter.html',
    date: 'December 22, 2025',
    icon: 'video',
  },
  {
    title: "The Sovereignty Mirage: Why European Clouds Won't Save Your Data",
    href: '/blog/industry-perspectives/2025-12-04_the-sovereignty-mirage-why-european-clouds-wont-save-your-data/index.html',
    date: 'December 4, 2025',
    icon: 'article',
  },
  {
    title: 'Build web apps in minutes with Replit Design Mode!',
    href: '/youtube/2025/20251204_Build_web_apps_in_minutes_with_Replit_Design_Mode.html',
    date: 'December 4, 2025',
    icon: 'video',
  },
  {
    title: 'Introducing the Arcee AI Trinity Models',
    href: '/youtube/2025/20251204_Introducing_the_Arcee_AI_Trinity_Models.html',
    date: 'December 4, 2025',
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
      '665+ speaking engagements worldwide, including major industry events, Fortune 500 companies, and institutions like UNESCO, World Bank, New York Federal Reserve, and sovereign funds.',
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

export default function HomePage() {
  return (
    <>
      {/* ── Hero Section ─────────────────────────────────── */}
      <section className="relative min-h-[85vh] flex items-center justify-center overflow-hidden pt-20">
        <div className="absolute inset-0 gradient-mesh" />
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-background" />

        <div className="relative z-10 max-w-4xl mx-auto px-4 text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <Image
              src="/assets/julien.webp"
              alt="Julien Simon"
              width={160}
              height={160}
              priority
              className="mx-auto rounded-full border-4 border-primary/30 shadow-xl shadow-primary/10 mb-6"
            />
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-5xl sm:text-6xl lg:text-7xl font-bold font-heading gradient-brand-text mb-3"
          >
            Julien Simon
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-xl sm:text-2xl font-semibold text-text mb-3"
          >
            AI Operating Partner @ Fortino Capital
          </motion.p>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="text-lg text-text-muted h-8 mb-8"
          >
            <TypingEffect texts={TYPING_PHRASES} />
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
            className="flex flex-wrap justify-center gap-2"
          >
            {SOCIAL_LINKS.map((link) => (
              <SocialButton key={link.name} name={link.name} href={link.href} />
            ))}
          </motion.div>
        </div>
      </section>

      {/* ── About + Latest Updates ────────────────────────── */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid lg:grid-cols-[2fr_1fr] gap-12">
          <div>
            <motion.h2
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="text-3xl font-bold font-heading gradient-brand-text mb-6"
            >
              About
            </motion.h2>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="space-y-4 text-text leading-relaxed"
            >
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
            </motion.div>
          </div>

          <div>
            <motion.h2
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="text-3xl font-bold font-heading gradient-brand-text mb-6"
            >
              Latest Updates
            </motion.h2>
            <div className="space-y-4">
              {LATEST_UPDATES.map((item, i) => (
                <motion.a
                  key={item.href}
                  href={item.href}
                  initial={{ opacity: 0, y: 12 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.08 }}
                  className="block glass-card rounded-xl p-4 hover:scale-[1.01] transition-all duration-300 group"
                >
                  <p className="text-xs text-text-muted mb-1">
                    {item.icon === 'video' ? '📺' : '📝'} {item.date}
                  </p>
                  <h4 className="text-sm font-semibold text-text group-hover:text-primary transition-colors">
                    {item.title}
                  </h4>
                </motion.a>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ── Industry Impact & Metrics ──────────────────────── */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-3xl font-bold font-heading gradient-brand-text mb-4 text-center"
        >
          Industry Impact &amp; Recognition
        </motion.h2>
        <motion.p
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.1 }}
          className="text-center text-text-muted max-w-3xl mx-auto mb-10"
        >
          Julien&apos;s approach to AI—combining theoretical depth with practical results—has
          earned recognition across the global tech community.
        </motion.p>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
          {METRICS.map((m, i) => (
            <MetricCard key={m.label} value={m.value} suffix={m.suffix} label={m.label} index={i} />
          ))}
        </div>

        {/* Philosophy cards */}
        <div className="grid sm:grid-cols-2 gap-4 mb-12">
          {PHILOSOPHY_CARDS.map((card, i) => (
            <motion.div
              key={card.title}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.08 }}
              className="glass-card rounded-xl p-5 border-l-4 border-primary"
            >
              <h3 className="text-base font-semibold text-text mb-2">
                {card.title}
              </h3>
              <p className="text-sm text-text-muted">
                {card.description}
              </p>
            </motion.div>
          ))}
        </div>

        {/* Recognition */}
        <div>
          <h3 className="text-xl font-bold font-heading text-text mb-4">
            Recognition &amp; Milestones
          </h3>
          <div className="space-y-3">
            {RECOGNITIONS.map((item, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -16 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.06 }}
                className="glass-card rounded-lg p-4 border-l-4 border-secondary"
              >
                <p className="text-sm text-text">{item}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Expertise Grid ─────────────────────────────────── */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-3xl font-bold font-heading gradient-brand-text mb-8 text-center"
        >
          Expertise &amp; Leadership Impact
        </motion.h2>

        <div className="grid sm:grid-cols-2 gap-5">
          {EXPERTISE_CARDS.map((card, i) => (
            <motion.div
              key={card.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.08 }}
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
            </motion.div>
          ))}
        </div>
      </section>

      {/* ── Contact ────────────────────────────────────────── */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-3xl font-bold font-heading gradient-brand-text mb-4"
        >
          Contact
        </motion.h2>
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.1 }}
          className="text-text-muted space-y-2"
        >
          <p>For portfolio company advisory, strategy consulting, speaking engagements, or AI partnerships:</p>
          <p>
            <a href="mailto:julien@julien.org" className="text-primary hover:text-primary-hover font-medium">
              julien@julien.org
            </a>
          </p>
        </motion.div>
      </section>
    </>
  );
}
