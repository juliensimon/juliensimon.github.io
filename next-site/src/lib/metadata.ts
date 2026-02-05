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
  const displayTitle = `${title} | ${SITE.name}`;

  return {
    // Homepage: use absolute title to bypass the layout template.
    // Secondary pages: return just the page title; the layout template
    // ("%s | Julien Simon") appends the site name automatically.
    title: path === '/' ? { absolute: SITE.title } : title,
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
      title: displayTitle,
      description,
      siteName: `${SITE.name} - AI Operating Partner`,
      locale: SITE.locale,
      images: [{ url: SITE.ogImage, width: 1200, height: 630, alt: `${SITE.name} - AI Operating Partner at Fortino Capital` }],
    },
    twitter: {
      card: 'summary_large_image',
      title: displayTitle,
      description,
      images: [SITE.ogImage],
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
      'contact-email': SITE.email,
    },
  };
}
