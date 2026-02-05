import type { Metadata } from 'next';
import { Inter, Space_Grotesk } from 'next/font/google';
import './globals.css';
import Navigation from '@/components/layout/Navigation';
import Footer from '@/components/layout/Footer';
import StructuredData from '@/components/seo/StructuredData';
import { personSchema } from '@/lib/structured-data';
import { SITE } from '@/lib/constants';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-sans',
});

const spaceGrotesk = Space_Grotesk({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-heading',
});

export const metadata: Metadata = {
  title: {
    default: SITE.title,
    template: `%s | ${SITE.name}`,
  },
  description: SITE.description,
  metadataBase: new URL(SITE.url),
  icons: { icon: '/assets/favicon.ico' },
  manifest: '/manifest.json',
  alternates: {
    types: { 'application/rss+xml': '/feed.xml' },
  },
  openGraph: {
    type: 'website',
    locale: SITE.locale,
    siteName: SITE.name,
    images: [{ url: SITE.image, width: 200, height: 200, alt: SITE.name }],
  },
  twitter: {
    card: 'summary',
    site: SITE.twitterHandle,
    creator: SITE.twitterHandle,
  },
  robots: {
    index: true,
    follow: true,
    'max-image-preview': 'large' as const,
    'max-snippet': -1,
    'max-video-preview': -1,
  },
  authors: [{ name: SITE.name }],
  creator: SITE.name,
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="en"
      dir="ltr"
      className={`${inter.variable} ${spaceGrotesk.variable}`}
    >
      <head>
        <meta name="theme-color" content="#1e40af" />
        <link rel="preconnect" href="https://cloud.umami.is" />
        <link rel="dns-prefetch" href="https://cloud.umami.is" />
        {/* Leaflet map resources (used on /speaking) */}
        <link rel="preconnect" href="https://unpkg.com" crossOrigin="anonymous" />
        <link rel="dns-prefetch" href="https://unpkg.com" />
        <link rel="preconnect" href="https://basemaps.cartocdn.com" crossOrigin="anonymous" />
        <link rel="dns-prefetch" href="https://basemaps.cartocdn.com" />
        {/* Umami Analytics */}
        <script defer src="https://cloud.umami.is/script.js" data-website-id={SITE.umamiId} />
        <StructuredData data={personSchema()} />
      </head>
      <body className="font-sans antialiased min-h-screen">
        <Navigation />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
