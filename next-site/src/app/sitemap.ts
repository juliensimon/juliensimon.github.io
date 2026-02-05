import type { MetadataRoute } from 'next';
import { SITE } from '@/lib/constants';
import { SPEAKING_YEARS } from '@/data/speaking';
import { BLOG_CATEGORY_SLUGS } from '@/data/blog-categories';

export const dynamic = 'force-static';

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date().toISOString();

  // Core static pages
  const staticPages: MetadataRoute.Sitemap = [
    {
      url: SITE.url,
      lastModified: now,
      changeFrequency: 'daily',
      priority: 1.0,
    },
    {
      url: `${SITE.url}/experience`,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 0.9,
    },
    {
      url: `${SITE.url}/speaking`,
      lastModified: now,
      changeFrequency: 'daily',
      priority: 0.9,
    },
    {
      url: `${SITE.url}/publications`,
      lastModified: now,
      changeFrequency: 'daily',
      priority: 0.8,
    },
    {
      url: `${SITE.url}/youtube-videos`,
      lastModified: now,
      changeFrequency: 'daily',
      priority: 0.7,
    },
    {
      url: `${SITE.url}/books`,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 0.7,
    },
    {
      url: `${SITE.url}/code`,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 0.7,
    },
    {
      url: `${SITE.url}/computers`,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 0.6,
    },
  ];

  // Dynamic speaking year pages
  const speakingPages: MetadataRoute.Sitemap = SPEAKING_YEARS.map((y) => ({
    url: `${SITE.url}/speaking/${y.year}`,
    lastModified: now,
    changeFrequency: 'weekly' as const,
    priority: y.year >= 2024 ? 0.7 : 0.6,
  }));

  // Dynamic blog category pages
  const blogPages: MetadataRoute.Sitemap = BLOG_CATEGORY_SLUGS.map((slug) => ({
    url: `${SITE.url}/blog-posts/${slug}`,
    lastModified: now,
    changeFrequency: 'weekly' as const,
    priority: 0.7,
  }));

  return [...staticPages, ...speakingPages, ...blogPages];
}
