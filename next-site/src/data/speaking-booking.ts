export interface SpeakingFormat {
  name: string;
  length: string;
  audience: string;
  description: string;
}

export interface SpeakingTopic {
  title: string;
  audience: string;
  takeaway: string;
}

export interface SpeakingPhoto {
  src: string;
  alt: string;
  caption: string;
  credit: string;
  width: number;
  height: number;
}

export const SPEAKING_FORMATS: SpeakingFormat[] = [
  {
    name: 'Keynote',
    length: '30 to 45 minutes',
    audience: 'Conferences, customer events, leadership offsites',
    description:
      'One argument, told with real deployments, ending on what the audience changes on Monday.',
  },
  {
    name: 'Executive workshop',
    length: 'Half day',
    audience: 'CEOs, executive committees, boards',
    description:
      'A working session on your own AI portfolio: which projects to stop, which to fund, and how to measure a result.',
  },
  {
    name: 'Fireside chat or panel',
    length: '30 to 60 minutes',
    audience: 'Investor days, founder and portfolio events',
    description: 'Moderated conversation with direct answers and named examples. No slides required.',
  },
  {
    name: 'Technical deep dive',
    length: '60 to 90 minutes',
    audience: 'CTOs and engineering teams',
    description:
      'Live demos on small language models, local inference and agent evaluation, with code the team keeps.',
  },
];

export const SPEAKING_TOPICS: SpeakingTopic[] = [
  {
    title: 'Why enterprise AI pilots stall, and what production teams do differently',
    audience: 'CEOs, executive committees, portfolio leaders',
    takeaway:
      'Five mistakes that keep AI agents out of production, and the changes that move a pilot onto the P&L.',
  },
  {
    title: 'Small language models: free, private, local',
    audience: 'CTOs, engineering leaders, product teams',
    takeaway:
      'When a small model on your own hardware beats a hosted API on cost, privacy and control, and how to prove it on your data.',
  },
  {
    title: 'Open models, sovereignty and hardware: choosing what to run where',
    audience: 'CTOs, boards, public-sector technology leaders',
    takeaway:
      'Open-weight, self-hosted and sovereign are three different properties. How to choose models and infrastructure on license, cost and legal scope.',
  },
];

export const SPEAKING_PHOTOS: SpeakingPhoto[] = [
  {
    src: '/assets/speaking/ofelia-keynote-paris-2026.webp',
    alt: 'Julien Simon speaking to executives at La Galerie Bourbon in Paris, with a slide on five mistakes that block enterprise AI',
    caption: 'Sommet de la Transformation Agentique, La Galerie Bourbon, Paris, September 22, 2026',
    credit: 'Ofelia',
    width: 1600,
    height: 1067,
  },
];

export const SPEAKING_LANGUAGES = ['English', 'French'] as const;

export const SPEAKING_BIO_SHORT =
  'Julien Simon is Operating Partner and Head of the AI Studio at Fortino Capital, where he helps portfolio companies move AI from pilot to production. He previously led evangelism at Arcee AI, Hugging Face and AWS, and writes The AI Realist, a newsletter built on primary sources.';

export const SPEAKING_BIO_LONG =
  'Julien Simon is Operating Partner and Head of the AI Studio at Fortino Capital, a private equity and venture capital firm. He works with portfolio companies on the step most AI programs miss: getting an agent or a small language model into daily use, and measuring what it returns. Before Fortino Capital he was VP and Chief Evangelist at Arcee AI, Chief Evangelist at Hugging Face, and Global Evangelist for AI and machine learning at AWS. He wrote Learn Amazon SageMaker, runs a YouTube channel on AI engineering, and publishes The AI Realist, a newsletter that reads filings, model cards and legislation instead of press releases. He speaks in English and French.';

export const SPEAKING_REQUEST_FIELDS = [
  'Event name and organizer',
  'Date and city, or online',
  'Audience: who they are and how many',
  'Format and length',
  'Language',
  'Budget or fee range',
  'Recording and distribution plans',
] as const;
