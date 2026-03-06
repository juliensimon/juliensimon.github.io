export interface VideoYear {
  year: number;
  count: number;
  href: string;
}

export const YOUTUBE_STATS = {
  totalVideos: 450,
  subscribers: '494K+',
  subscriberCount: 494, // numeric value for MetricCard
  channelUrl: 'https://youtube.com/@juliensimonfr',
  yearsOfContent: 15,
} as const;

export const POPULAR_VIDEO_IDS = ['Zdu5UyA46io', '_hNRG3E4Ny4', 'cf8z3Q8PFQQ', 'hMs8VNRy5Ys'];

export const LATEST_VIDEOS = [
  { id: 'zP7s_IdrVRs', title: 'Deep Dive: Teaching Arcee Trinity Mini to Read Medical Research with RLVR and GRPO', date: 'March 3, 2026' },
  { id: 'LPYYrQsUuWQ', title: 'Open-source Coding with Cline and Arcee Trinity Large', date: 'February 14, 2026' },
  { id: 'lOi6mxY7QP4', title: 'Building a Kanban Task Management Web App from Scratch with Replit', date: 'February 8, 2026' },
];

export const VIDEO_YEARS: VideoYear[] = [
  { year: 2026, count: 8, href: '/youtube/2026/index.html' },
  { year: 2025, count: 44, href: '/youtube/2025/index.html' },
  { year: 2024, count: 54, href: '/youtube/2024/index.html' },
  { year: 2023, count: 27, href: '/youtube/2023/index.html' },
  { year: 2022, count: 33, href: '/youtube/2022/index.html' },
  { year: 2021, count: 45, href: '/youtube/2021/index.html' },
  { year: 2020, count: 64, href: '/youtube/2020/index.html' },
  { year: 2019, count: 35, href: '/youtube/2019/index.html' },
  { year: 2018, count: 32, href: '/youtube/2018/index.html' },
  { year: 2017, count: 72, href: '/youtube/2017/index.html' },
  { year: 2016, count: 23, href: '/youtube/2016/index.html' },
  { year: 2015, count: 2, href: '/youtube/2015/index.html' },
  { year: 2014, count: 2, href: '/youtube/2014/index.html' },
  { year: 2013, count: 7, href: '/youtube/2013/index.html' },
  { year: 2011, count: 2, href: '/youtube/2011/index.html' },
];
