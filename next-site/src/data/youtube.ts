export interface VideoYear {
  year: number;
  count: number;
  href: string;
}

export interface LatestVideo {
  id: string;
  title: string;
  date: string;
  /** One-line teaser written from the video transcript. */
  summary?: string;
}

export const YOUTUBE_STATS = {
  totalVideos: 461,
  subscriberCount: 573, // numeric value in thousands for MetricCard
  channelUrl: 'https://youtube.com/@juliensimonfr',
  yearsOfContent: 15,
} as const;

export const POPULAR_VIDEO_IDS = ['Zdu5UyA46io', '_hNRG3E4Ny4', 'cf8z3Q8PFQQ', 'hMs8VNRy5Ys'];

export const LATEST_VIDEOS: LatestVideo[] = [
  { id: 'Hd3ZreKZefE', title: 'Reviewing AI-Written Code with CodeRabbit', date: 'October 19, 2026', summary: 'A coding agent\'s 998-line pull request, reviewed with CodeRabbit: a global lock that makes users wait on each other, and a user ID that is not access control.' },
  { id: 'IbBecjA93ks', title: 'Your LLM No Longer Reads Every Token: 8 Attention Designs Explained', date: 'October 11, 2026' },
  { id: '9d2xYP1WlRo', title: 'Fine-Tuning Qwen3.5-9B on Crusoe Intelligence Foundry: from 70% to 91% for $0.12', date: 'October 7, 2026' },
];

export const VIDEO_YEARS: VideoYear[] = [
  { year: 2026, count: 22, href: '/youtube/2026/' },
  { year: 2025, count: 41, href: '/youtube/2025/' },
  { year: 2024, count: 54, href: '/youtube/2024/' },
  { year: 2023, count: 27, href: '/youtube/2023/' },
  { year: 2022, count: 33, href: '/youtube/2022/' },
  { year: 2021, count: 45, href: '/youtube/2021/' },
  { year: 2020, count: 64, href: '/youtube/2020/' },
  { year: 2019, count: 35, href: '/youtube/2019/' },
  { year: 2018, count: 32, href: '/youtube/2018/' },
  { year: 2017, count: 72, href: '/youtube/2017/' },
  { year: 2016, count: 23, href: '/youtube/2016/' },
  { year: 2015, count: 2, href: '/youtube/2015/' },
  { year: 2014, count: 2, href: '/youtube/2014/' },
  { year: 2013, count: 7, href: '/youtube/2013/' },
  { year: 2011, count: 2, href: '/youtube/2011/' },
];
