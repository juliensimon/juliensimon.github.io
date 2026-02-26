export const SITE = {
  name: 'Julien Simon',
  title: 'Julien Simon - AI Operating Partner at Fortino Capital',
  description:
    'AI Operating Partner at Fortino Capital. 30+ years accelerating cloud and AI across PE/VC portfolios. Expert in Small Language Models and enterprise AI.',
  url: 'https://www.julien.org',
  image: 'https://www.julien.org/assets/julien.webp',
  ogImage: 'https://www.julien.org/assets/og-image-1200x630.png',
  locale: 'en_US',
  email: 'julien@julien.org',
  twitterHandle: '@julsimon',
  umamiId: '27550dad-d418-4f5d-ad1b-dab573da1020',
} as const;

export const SOCIAL_LINKS = [
  { name: 'GitHub', href: 'https://github.com/juliensimon', icon: 'github' },
  { name: 'Hugging Face', href: 'https://huggingface.co/juliensimon', icon: 'huggingface' },
  { name: 'LinkedIn', href: 'https://linkedin.com/in/juliensimon', icon: 'linkedin' },
  { name: 'Medium', href: 'https://julsimon.medium.com/', icon: 'medium' },
  { name: 'Substack', href: 'https://julsimon.substack.com/', icon: 'substack' },
  { name: 'Twitter (X)', href: 'https://x.com/julsimon', icon: 'twitter' },
  { name: 'YouTube', href: 'https://youtube.com/@juliensimonfr', icon: 'youtube' },
  { name: 'Slideshare', href: 'https://fr.slideshare.net/JulienSIMON5/presentations', icon: 'slideshare' },
] as const;

export const NAV_ITEMS = [
  { label: 'Home', href: '/' },
  { label: 'Experience', href: '/experience' },
  { label: 'Speaking', href: '/speaking' },
  { label: 'Publications', href: '/publications' },
  { label: 'Code', href: '/code' },
  { label: 'Videos', href: '/youtube-videos' },
  { label: 'Books', href: '/books' },
  { label: 'Computers, UNIX, and Me', href: '/computers' },
] as const;

// Note: These values should stay in sync with:
// - TOTAL_ARTICLES in publications.ts (Technical Posts)
// - SPEAKING_STATS.totalEvents in speaking.ts (Speaking Engagements)
// - YOUTUBE_STATS.subscribers in youtube.ts (YouTube Subscribers)
// Run `npm run validate` to check for mismatches
export const METRICS = [
  { value: 409, suffix: '+', label: 'Technical Posts' },
  { value: 684, suffix: '+', label: 'Speaking Engagements' },
  { value: 467, suffix: 'K+', label: 'YouTube Subscribers' },
  { value: 30, suffix: '+', label: 'Years Experience' },
] as const;
