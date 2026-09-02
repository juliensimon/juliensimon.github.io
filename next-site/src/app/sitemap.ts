import type { MetadataRoute } from 'next';
import { SITE } from '@/lib/constants';
import { SPEAKING_YEARS } from '@/data/speaking';
import { BLOG_CATEGORY_SLUGS } from '@/data/blog-categories';
import { INDUSTRY_PERSPECTIVES_ARTICLES } from '@/data/blog-listings/industry-perspectives';

export const dynamic = 'force-static';

export default function sitemap(): MetadataRoute.Sitemap {
  // ponytail: lastModified is omitted where no real content date exists;
  // a build timestamp on every deploy is noise, not a freshness signal.
  const staticPages: MetadataRoute.Sitemap = [
    {
      url: SITE.url,
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
      changeFrequency: 'weekly',
      priority: 0.9,
    },
    {
      url: `${SITE.url}/publications`,
      changeFrequency: 'weekly',
      priority: 0.8,
    },
    {
      url: `${SITE.url}/youtube-videos`,
      changeFrequency: 'weekly',
      priority: 0.7,
    },
    {
      url: `${SITE.url}/media`,
      changeFrequency: 'monthly',
      priority: 0.7,
    },
    {
      url: `${SITE.url}/datasets`,
      changeFrequency: 'monthly',
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
    ...(y.year < currentYear && { lastModified: `${y.year}-12-31` }),
    changeFrequency: y.year >= currentYear ? 'weekly' as const : 'yearly' as const,
    priority: y.year >= currentYear ? 0.7 : 0.5,
  }));

  // Dynamic blog category pages
  const blogPages: MetadataRoute.Sitemap = BLOG_CATEGORY_SLUGS.map((slug) => ({
    url: `${SITE.url}/blog-posts/${slug}`,
    changeFrequency: 'weekly' as const,
    priority: 0.7,
  }));

  // Industry Perspectives index + individual articles (static HTML, outside Next.js).
  // The Python sitemap script no longer emits these; this file owns them.
  const industryIndex: MetadataRoute.Sitemap = [{
    url: `${SITE.url}/blog/industry-perspectives/`,
    changeFrequency: 'weekly',
    priority: 0.7,
  }];
  const articlePages: MetadataRoute.Sitemap = INDUSTRY_PERSPECTIVES_ARTICLES.map((a) => ({
    url: `${SITE.url}/blog/industry-perspectives/${encodeURIComponent(a.slug)}/`,
    lastModified: a.date,
    changeFrequency: 'yearly' as const,
    priority: 0.6,
  }));

  return [...staticPages, ...speakingPages, ...blogPages, ...industryIndex, ...articlePages];
}
