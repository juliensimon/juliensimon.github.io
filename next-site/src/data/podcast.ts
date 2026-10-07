// The AI Realist podcast. The episode list is generated: scripts/sync_podcast.py writes
// podcast-episodes.json from the podcast's public feed. Do not edit that file by hand.
import episodes from './podcast-episodes.json';

export interface PodcastEpisode {
  title: string;
  date: string;      // the written piece's publication date, YYYY-MM-DD
  minutes: number;
  seconds: number;
  summary: string;
  audio: string;
  image: string;
  article: string;   // the written piece on airealist.ai
  page: string;      // its page on this site, with the player; '' until the article is archived here
}

export const PODCAST = {
  name: 'The AI Realist',
  tagline: 'AI without the hype: what it costs, who profits, and what the filings say.',
  description:
    'The audio edition of The AI Realist, Julien Simon\'s newsletter on the AI industry. Each episode is one written piece, narrated by an AI voice: GPU and cloud economics, inference costs, open-weight models, chips and export rules, AI regulation, and the business models of the AI labs.',
  feed: 'https://podcast.julien.org/feed.xml',
  apple: 'https://podcasts.apple.com/podcast/the-ai-realist/id6819758071',
  spotify: 'https://open.spotify.com/show/78U6RiqMDd0wnY3FmJFZGF',
  newsletter: 'https://www.airealist.ai/subscribe',
  cover: '/assets/ai-realist-podcast-cover.png',
  coverFull: 'https://podcast.julien.org/art/cover.jpg',
} as const;

export const PODCAST_EPISODES: PodcastEpisode[] = (episodes as PodcastEpisode[]).filter((e) => e.title);
