import type { MetadataRoute } from 'next';
import { SITE } from '@/lib/constants';
import { SPEAKING_YEARS } from '@/data/speaking';
import { SPEAKING_EVENTS } from '@/data/speaking-events';
import { LATEST_VIDEOS } from '@/data/youtube';
import { INDUSTRY_PERSPECTIVES_ARTICLES } from '@/data/blog-listings/industry-perspectives';
import { TOPICS } from '@/data/topics';
import { topicItems } from '@/lib/topic-items';
import { BLOG_CATEGORY_SLUGS } from '@/data/blog-categories';

export const dynamic = 'force-static';

const isoDay = (d: Date) => d.toISOString().slice(0, 10);

// Newest content date among past items; future-dated talks are not yet content.
// Dates read as UTC so the ISO day matches the day written in the data.
function newest(dates: (string | undefined)[]): string | undefined {
  const now = Date.now();
  const times = dates
    .map((d) => (d ? Date.parse(`${d} UTC`) : NaN))
    .filter((t) => !Number.isNaN(t) && t <= now);
  return times.length ? isoDay(new Date(Math.max(...times))) : undefined;
}

export default function sitemap(): MetadataRoute.Sitemap {
  // ponytail: lastModified is omitted where no real content date exists;
  // a build timestamp on every deploy is noise, not a freshness signal.
  // The dates below come from the newest item on the page, never from the build.
  const speakingDate = newest(Object.values(SPEAKING_EVENTS).flat().map((e) => e.date));
  const videoDate = newest(LATEST_VIDEOS.map((v) => v.date));
  const articleDate = newest(INDUSTRY_PERSPECTIVES_ARTICLES.map((a) => a.date));
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
      lastModified: speakingDate,
      changeFrequency: 'weekly',
      priority: 0.9,
      alternates: {
        languages: {
          en: `${SITE.url}/speaking`,
          fr: `${SITE.url}/fr/conferencier-ia`,
        },
      },
    },
    {
      url: `${SITE.url}/fr/conferencier-ia`,
      lastModified: speakingDate,
      changeFrequency: 'weekly',
      priority: 0.8,
      alternates: {
        languages: {
          en: `${SITE.url}/speaking`,
          fr: `${SITE.url}/fr/conferencier-ia`,
        },
      },
    },
    {
      url: `${SITE.url}/publications`,
      lastModified: articleDate,
      changeFrequency: 'weekly',
      priority: 0.8,
    },
    {
      url: `${SITE.url}/youtube-videos`,
      lastModified: videoDate,
      changeFrequency: 'weekly',
      priority: 0.7,
    },
    {
      url: `${SITE.url}/podcast`,
      lastModified: articleDate,
      changeFrequency: 'weekly',
      priority: 0.8,
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

  // Industry Perspectives index only. The articles canonicalize to their original
  // publication (airealist.ai, Hugging Face, Medium), so listing them here would
  // contradict that canonical.
  const industryIndex: MetadataRoute.Sitemap = [{
    url: `${SITE.url}/blog/industry-perspectives/`,
    lastModified: articleDate,
    changeFrequency: 'weekly',
    priority: 0.7,
  }];
  // Topic hubs: lastmod is the newest piece listed on the hub.
  const topicPages: MetadataRoute.Sitemap = TOPICS.map((t) => {
    const { articles, videos } = topicItems(t);
    return {
      url: `${SITE.url}/topics/${t.slug}`,
      lastModified: newest([...articles, ...videos].map((i) => i.date)),
      changeFrequency: 'weekly' as const,
      priority: 0.8,
    };
  });
  const topicsIndex: MetadataRoute.Sitemap = [{ url: `${SITE.url}/topics`, lastModified: articleDate, changeFrequency: 'weekly', priority: 0.8 }];

  return [...staticPages, ...topicsIndex, ...topicPages, ...speakingPages, ...blogPages, ...industryIndex];
}
