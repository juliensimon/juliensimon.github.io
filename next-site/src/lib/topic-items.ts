import fs from 'node:fs';
import path from 'node:path';
import { INDUSTRY_PERSPECTIVES_ARTICLES } from '@/data/blog-listings/industry-perspectives';
import { SITE } from './constants';
import type { Topic } from '@/data/topics';

export interface TopicItem {
  kind: 'article' | 'video';
  title: string;
  href: string;
  /** ISO day. */
  date: string;
  summary: string;
}

const YOUTUBE_DIR = path.join(process.cwd(), 'public', 'youtube');
const decode = (s: string) =>
  s.replace(/&quot;/g, '"').replace(/&#x27;|&#39;/g, "'").replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const clip = (s: string, n: number) => (s.length <= n ? s : s.slice(0, n).replace(/\s+\S*$/, '').replace(/[,.;:]$/, ''));

let videoCache: TopicItem[] | null = null;

/** Every transcript page that is a real video (not a redirect stub), read from the shipped archive. */
function allVideos(): TopicItem[] {
  if (videoCache) return videoCache;
  const items: TopicItem[] = [];
  for (const year of fs.readdirSync(YOUTUBE_DIR)) {
    if (!/^\d{4}$/.test(year)) continue;
    for (const file of fs.readdirSync(path.join(YOUTUBE_DIR, year))) {
      const m = file.match(/^(\d{4})(\d{2})(\d{2})_.*\.html$/);
      if (!m) continue;
      const html = fs.readFileSync(path.join(YOUTUBE_DIR, year, file), 'utf8');
      const title = html.match(/<title>([\s\S]*?)<\/title>/)?.[1];
      if (!title || title.startsWith('Redirecting')) continue;
      const desc = html.match(/name="description" content="([\s\S]*?)"/)?.[1] ?? '';
      items.push({
        kind: 'video',
        title: decode(title).replace(/\s+-\s+Julien Simon$/, '').trim(),
        href: `/youtube/${year}/${file}`,
        date: `${m[1]}-${m[2]}-${m[3]}`,
        summary: clip(decode(desc), 200),
      });
    }
  }
  videoCache = items;
  return items;
}

function allArticles(): TopicItem[] {
  return INDUSTRY_PERSPECTIVES_ARTICLES.map((a) => ({
    kind: 'article' as const,
    title: a.title,
    href: `/blog/industry-perspectives/${a.slug}/`,
    date: a.date,
    summary: a.description,
  }));
}

function pick(pool: TopicItem[], fragments: string[], topic: string): TopicItem[] {
  const found = new Map<string, TopicItem>();
  for (const f of fragments) {
    const needle = f.toLowerCase();
    const hits = pool.filter((i) => i.title.toLowerCase().includes(needle));
    if (hits.length === 0) throw new Error(`Topic "${topic}": no piece matches "${f}"`);
    hits.forEach((h) => found.set(h.href, h));
  }
  return [...found.values()].sort((a, b) => b.date.localeCompare(a.date));
}

export function topicItems(topic: Topic): { articles: TopicItem[]; videos: TopicItem[] } {
  return {
    articles: pick(allArticles(), topic.articles, topic.slug),
    videos: pick(allVideos(), topic.videos, topic.slug),
  };
}

export const absolute = (href: string) => `${SITE.url}${href}`;
