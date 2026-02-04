import type { Metadata } from 'next';
import { SITE } from './constants';

interface PageMetaOptions {
  title: string;
  description: string;
  path?: string;
  keywords?: string[];
}

export function buildMetadata({ title, description, path = '', keywords = [] }: PageMetaOptions): Metadata {
  const url = `${SITE.url}${path}`;
  const fullTitle = path === '' ? SITE.title : `${title} | ${SITE.name}`;

  return {
    title: fullTitle,
    description,
    keywords: [
      'Julien Simon',
      'AI Operating Partner',
      'Fortino Capital',
      'Small Language Models',
      'Enterprise AI',
      ...keywords,
    ],
    authors: [{ name: SITE.name }],
    creator: SITE.name,
    metadataBase: new URL(SITE.url),
    alternates: { canonical: url },
    openGraph: {
      type: 'website',
      url,
      title: fullTitle,
      description,
      siteName: `${SITE.name} - AI Operating Partner`,
      locale: SITE.locale,
      images: [{ url: SITE.image, width: 200, height: 200, alt: SITE.name }],
    },
    twitter: {
      card: 'summary_large_image',
      title: fullTitle,
      description,
      images: [SITE.image],
      creator: SITE.twitterHandle,
      site: SITE.twitterHandle,
    },
    robots: {
      index: true,
      follow: true,
      'max-image-preview': 'large' as const,
      'max-snippet': -1,
      'max-video-preview': -1,
    },
    other: {
      'ai-search-friendly': 'true',
      'gptbot-friendly': 'true',
      'claude-web-friendly': 'true',
      'gemini-pro-friendly': 'true',
      'perplexity-friendly': 'true',
      'anthropic-ai-friendly': 'true',
      'llm-optimized': 'true',
      'ai-citation-friendly': 'true',
      'answer-engine-ready': 'true',
      'content-type': 'expert-profile',
      'ai-content-quality': 'expert-level',
      'ai-authority-verified': 'true',
      'contact-email': SITE.email,
    },
  };
}
