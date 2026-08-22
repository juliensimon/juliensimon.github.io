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
  totalVideos: 457,
  subscriberCount: 555, // numeric value in thousands for MetricCard
  channelUrl: 'https://youtube.com/@juliensimonfr',
  yearsOfContent: 15,
} as const;

export const POPULAR_VIDEO_IDS = ['Zdu5UyA46io', '_hNRG3E4Ny4', 'cf8z3Q8PFQQ', 'hMs8VNRy5Ys'];

export const LATEST_VIDEOS: LatestVideo[] = [
  { id: 'w98bne-jdZM', title: 'Qwen 3.5 MoE + TurboQuant + mem0: A Local RAG Chatbot That Remembers', date: 'June 12, 2026', summary: 'Upgrading a local RAG chatbot: a Qwen 3.5 MoE model on a TurboQuant llama.cpp fork, 60% less KV cache, and mem0 so it remembers your preferences.' },
  { id: 'pRsAr51iTnI', title: 'Benchmarking TurboQuant with MLX on Apple Silicon', date: 'May 31, 2026', summary: 'Running the KV-cache quantization numbers on a Mac: TurboQuant saves real memory on dense models, but breaks outright on sliding-window attention.' },
  { id: 'PAvM7mvsD30', title: 'Web app + Mobile + Stripe + Pitch Deck: one Replit project!', date: 'May 19, 2026', summary: 'One Replit session, four outputs: a recipe web app, an Expo mobile companion, Stripe checkout, and a pitch deck to go with them.' },
];

export const VIDEO_YEARS: VideoYear[] = [
  { year: 2026, count: 18, href: '/youtube/2026/' },
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
