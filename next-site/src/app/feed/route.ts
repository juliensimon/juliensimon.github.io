import { SITE } from '@/lib/constants';
import { INDUSTRY_PERSPECTIVES_ARTICLES } from '@/data/blog-listings/industry-perspectives';
import { BLOG_CATEGORIES } from '@/data/blog-categories';
import fs from 'fs';
import path from 'path';

export const dynamic = 'force-static';

interface FeedItem {
  title: string;
  url: string;
  date: string;
  description?: string;
  category: 'article' | 'video';
}

function parseMonthDate(dateStr: string): string | null {
  // Parse "Month YYYY" format (e.g. "September 2025") to ISO date
  const d = new Date(`${dateStr} 1`);
  if (isNaN(d.getTime())) return null;
  return d.toISOString().slice(0, 10);
}

function getVideoItems(): FeedItem[] {
  const youtubeDir = path.join(process.cwd(), '..', 'youtube');
  const items: FeedItem[] = [];

  if (!fs.existsSync(youtubeDir)) return items;

  for (const yearDir of fs.readdirSync(youtubeDir)) {
    const yearPath = path.join(youtubeDir, yearDir);
    if (!fs.statSync(yearPath).isDirectory()) continue;

    for (const file of fs.readdirSync(yearPath)) {
      if (file === 'index.html' || !file.endsWith('.html')) continue;

      // Parse filename: YYYYMMDD_Title_With_Underscores.html
      const match = file.match(/^(\d{4})(\d{2})(\d{2})_(.+)\.html$/);
      if (!match) continue;

      const [, y, m, d, rawTitle] = match;
      const date = `${y}-${m}-${d}`;
      const title = rawTitle.replace(/_/g, ' ').replace(/\+/g, ' ');
      const url = `${SITE.url}/youtube/${yearDir}/${file}`;

      items.push({ title, url, date, category: 'video' });
    }
  }

  return items;
}

function getBlogItems(): FeedItem[] {
  const items: FeedItem[] = [];
  for (const cat of Object.values(BLOG_CATEGORIES)) {
    for (const post of cat.posts) {
      // Use localHref if available, otherwise external href
      const url = post.localHref
        ? `${SITE.url}${post.localHref}`
        : post.href.startsWith('/')
          ? `${SITE.url}${post.href}`
          : post.href;
      if (!post.date) continue;
      const date = parseMonthDate(post.date);
      if (!date) continue;
      items.push({
        title: post.title,
        url,
        date,
        description: post.description || undefined,
        category: 'article',
      });
    }
  }
  return items;
}

export function GET() {
  const articleItems: FeedItem[] = INDUSTRY_PERSPECTIVES_ARTICLES.map((a) => ({
    title: a.title,
    url: `${SITE.url}/blog/industry-perspectives/${a.slug}/`,
    date: a.date,
    description: a.description || undefined,
    category: 'article',
  }));

  const blogItems = getBlogItems();
  const videoItems = getVideoItems();

  const allItems = [...articleItems, ...blogItems, ...videoItems].sort(
    (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime(),
  );

  const lastBuildDate = new Date().toUTCString();

  const items = allItems.map((item) => {
    const pubDate = new Date(item.date).toUTCString();
    const categoryTag = `\n      <category>${item.category === 'video' ? 'Video' : 'Article'}</category>`;
    const descTag = item.description ? `\n      <description><![CDATA[${item.description}]]></description>` : '';
    return `    <item>
      <title><![CDATA[${item.title}]]></title>
      <link>${item.url}</link>
      <guid isPermaLink="true">${item.url}</guid>
      <pubDate>${pubDate}</pubDate>
      <author>${SITE.email} (${SITE.name})</author>${categoryTag}${descTag}
    </item>`;
  });

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${SITE.name} - Articles &amp; Videos</title>
    <link>${SITE.url}</link>
    <description>AI industry analysis, technical deep dives, and video content by ${SITE.name}, AI Operating Partner at Fortino Capital.</description>
    <language>en</language>
    <lastBuildDate>${lastBuildDate}</lastBuildDate>
    <atom:link href="${SITE.url}/feed" rel="self" type="application/rss+xml" />
    <image>
      <url>${SITE.image}</url>
      <title>${SITE.name}</title>
      <link>${SITE.url}</link>
    </image>
${items.join('\n')}
  </channel>
</rss>`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/rss+xml; charset=utf-8',
    },
  });
}
