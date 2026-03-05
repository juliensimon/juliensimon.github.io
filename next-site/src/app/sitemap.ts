import type { MetadataRoute } from 'next';
import { SITE } from '@/lib/constants';
import { SPEAKING_YEARS } from '@/data/speaking';
import { BLOG_CATEGORY_SLUGS } from '@/data/blog-categories';
import { INDUSTRY_PERSPECTIVES_ARTICLES } from '@/data/blog-listings/industry-perspectives';

export const dynamic = 'force-static';

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date().toISOString();

  // Frequently updated pages get the build timestamp.
  // Rarely-changed pages get a fixed date so search engines
  // can distinguish fresh content from stable content.
  const staticPages: MetadataRoute.Sitemap = [
    {
      url: SITE.url,
      lastModified: now,
      changeFrequency: 'daily',
      priority: 1.0,
    },
    {
      url: `${SITE.url}/experience`,
      lastModified: '2025-10-01',
      changeFrequency: 'monthly',
      priority: 0.9,
    },
    {
      url: `${SITE.url}/speaking`,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 0.9,
    },
    {
      url: `${SITE.url}/publications`,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 0.8,
    },
    {
      url: `${SITE.url}/youtube-videos`,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 0.7,
    },
    {
      url: `${SITE.url}/books`,
      lastModified: '2025-06-01',
      changeFrequency: 'monthly',
      priority: 0.7,
    },
    {
      url: `${SITE.url}/code`,
      lastModified: '2025-06-01',
      changeFrequency: 'monthly',
      priority: 0.7,
    },
    {
      url: `${SITE.url}/computers`,
      lastModified: '2025-06-01',
      changeFrequency: 'monthly',
      priority: 0.6,
    },
  ];

  // Dynamic speaking year pages — current year uses build time, past years are stable
  const currentYear = new Date().getFullYear();
  const speakingPages: MetadataRoute.Sitemap = SPEAKING_YEARS.map((y) => ({
    url: `${SITE.url}/speaking/${y.year}`,
    lastModified: y.year >= currentYear ? now : `${y.year}-12-31`,
    changeFrequency: y.year >= currentYear ? 'weekly' as const : 'yearly' as const,
    priority: y.year >= currentYear ? 0.7 : 0.5,
  }));

  // Dynamic blog category pages
  const blogPages: MetadataRoute.Sitemap = BLOG_CATEGORY_SLUGS.map((slug) => ({
    url: `${SITE.url}/blog-posts/${slug}`,
    lastModified: now,
    changeFrequency: 'weekly' as const,
    priority: 0.7,
  }));

  // Individual industry-perspectives articles (static HTML, outside Next.js)
  const articlePages: MetadataRoute.Sitemap = INDUSTRY_PERSPECTIVES_ARTICLES.map((a) => ({
    url: `${SITE.url}/blog/industry-perspectives/${encodeURIComponent(a.slug)}/index.html`,
    lastModified: a.date,
    changeFrequency: 'yearly' as const,
    priority: 0.6,
  }));

  return [...staticPages, ...speakingPages, ...blogPages, ...articlePages];
}
