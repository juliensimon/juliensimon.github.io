import { SITE, SOCIAL_LINKS } from './constants';
import { TOTAL_ARTICLES } from '@/data/publications';
import { TOTAL_DATASETS } from '@/data/datasets';
import { YOUTUBE_STATS } from '@/data/youtube';
import { SPEAKING_STATS } from '@/data/speaking';

export function personSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'Person',
    '@id': `${SITE.url}/#person`,
    name: 'Julien Simon',
    jobTitle: 'AI Operating Partner',
    worksFor: {
      '@type': 'Organization',
      name: 'Fortino Capital',
      url: 'https://www.fortinocapital.com',
      description: 'Private Equity and Venture Capital firm',
    },
    description:
      'Open source AI advocate who champions transparent, open-weights models over black box LLMs. Research-fluent expert democratizing AI through accessible, controllable solutions enterprises can understand and deploy. Author of The AI Realist newsletter (airealist.ai).',
    url: SITE.url,
    mainEntityOfPage: { '@id': `${SITE.url}/#profilepage` },
    image: {
      '@type': 'ImageObject',
      url: SITE.image,
      width: 200,
      height: 200,
    },
    sameAs: [
      ...SOCIAL_LINKS.map((l) => l.href),
      // Authoritative entity databases for AI knowledge graph disambiguation
      'https://www.wikidata.org/wiki/Q138589324',
      'https://www.crunchbase.com/person/julien-simon-2',
      'https://www.amazon.com/stores/Julien-Simon/author/B089RFQTQG',
      'https://www.packtpub.com/authors/julien-simon',
      'https://sessionize.com/julien-simon/',
    ],
    knowsAbout: [
      // Core expertise
      'Small Language Models',
      'Enterprise AI',
      'Open Source AI Implementation',
      'AI Inference Optimization',
      'Hugging Face',
      'Amazon SageMaker',
      'Cloud Computing',
      'AWS',
      // Enterprise AI expertise
      'Enterprise AI Deployment',
      'AI Strategy',
      // Industry analysis topics (from The AI Realist newsletter)
      'EU AI Act',
      'AI Regulation',
      'European Digital Sovereignty',
      'CLOUD Act',
      'Model Context Protocol (MCP)',
      'Distributed Systems',
      'AI Infrastructure Economics',
      'CPU Inference',
      'llama.cpp',
      'GGUF Quantization',
      'AI Hardware Optimization',
      'Arm AI Inference',
      'Domain-Specific Small Language Models',
      'AI Market Maturation',
      'LLM Scaling Laws',
      'Open-Weights Models',
      'AI Geopolitics',
      'MLOps',
    ],
    alumniOf: [
      {
        '@type': 'Organization',
        name: 'Amazon Web Services',
        url: 'https://aws.amazon.com',
        description: 'Global Evangelist, Machine Learning and AI (2015–2021)',
      },
      {
        '@type': 'Organization',
        name: 'Hugging Face',
        url: 'https://huggingface.co',
        description: 'Chief Evangelist (2021–2024)',
      },
      {
        '@type': 'Organization',
        name: 'Arcee AI',
        url: 'https://www.arcee.ai',
        description: 'Vice President & Chief Evangelist (2024–2025)',
      },
      {
        '@type': 'EducationalOrganization',
        name: 'Sorbonne University',
        description: "Master's degree in Computer Systems (1995)",
      },
      {
        '@type': 'EducationalOrganization',
        name: 'ISEP Paris',
        description: 'Engineering degree (1993)',
      },
    ],
    hasOccupation: [
      {
        '@type': 'Occupation',
        name: 'AI Operating Partner',
        occupationLocation: { '@type': 'Country', name: 'Netherlands' },
        description: 'Helping portfolio companies build and deploy AI at Fortino Capital.',
      },
    ],
    publishesContentIn: {
      '@id': 'https://www.airealist.ai/#newsletter',
    },
    hasCredential: [
      {
        '@type': 'EducationalOccupationalCredential',
        name: 'Author of "Learn Amazon SageMaker"',
        credentialCategory: 'Published Author',
        description: 'First book ever published on Amazon SageMaker (Packt Publishing, 2020 & 2021)',
      },
      {
        '@type': 'EducationalOccupationalCredential',
        name: '#1 AI Evangelist — AI Magazine 2021',
        credentialCategory: 'Industry Award',
      },
      {
        '@type': 'EducationalOccupationalCredential',
        name: 'Featured in "The 100 Shaping AI in Europe" (2025)',
        credentialCategory: 'Industry Recognition',
        description: 'Recognized by L\'Opinion and Oliver Wyman in the "Builders" category',
      },
    ],
    award: ['AI Magazine #1 AI Evangelist 2021', 'Trophees CIO Prix de l\'Innovation 2013'],
    contactPoint: { '@type': 'ContactPoint', contactType: 'email', email: SITE.email },
    knowsLanguage: ['English', 'French'],
    nationality: 'French',
  };
}

export function profilePageSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'ProfilePage',
    '@id': `${SITE.url}/#profilepage`,
    name: 'Julien Simon - AI Operating Partner at Fortino Capital',
    description: SITE.description,
    url: SITE.url,
    mainEntity: { '@id': `${SITE.url}/#person` },
    isPartOf: { '@id': `${SITE.url}/#website` },
    dateModified: new Date().toISOString().split('T')[0],
    inLanguage: 'en',
  };
}

export function webSiteSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    '@id': `${SITE.url}/#website`,
    name: SITE.name,
    url: SITE.url,
    description: SITE.description,
    inLanguage: 'en',
    author: { '@id': `${SITE.url}/#person` },
    publisher: { '@id': `${SITE.url}/#person` },
  };
}

export function breadcrumbSchema(items: { name: string; url: string }[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    '@id': `${items[items.length - 1]?.url || SITE.url}/#breadcrumb`,
    itemListElement: items.map((item, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: item.name,
      item: { '@type': 'WebPage', '@id': item.url, name: item.name },
    })),
  };
}

export function webPageSchema(name: string, description: string, url: string, dateModified?: string) {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    '@id': `${url}/#webpage`,
    name,
    description,
    url,
    isPartOf: { '@id': `${SITE.url}/#website` },
    about: { '@id': `${SITE.url}/#person` },
    inLanguage: 'en',
    ...(dateModified && { dateModified }),
  };
}

export function collectionPageSchema(name: string, description: string, url: string) {
  return {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    '@id': `${url}/#collectionpage`,
    name,
    description,
    url,
    isPartOf: { '@id': `${SITE.url}/#website` },
    author: { '@id': `${SITE.url}/#person` },
    inLanguage: 'en',
  };
}

export function faqSchema(faqs: { question: string; answer: string }[], pageUrl?: string) {
  const baseUrl = pageUrl || SITE.url;
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    '@id': `${baseUrl}/#faq`,
    mainEntity: faqs.map((faq) => ({
      '@type': 'Question',
      name: faq.question,
      acceptedAnswer: { '@type': 'Answer', text: faq.answer },
    })),
  };
}

export function bookSchema(book: {
  title: string;
  description: string;
  publisher?: string;
  pages?: number;
  coverImage?: string;
  amazonUrl?: string;
}) {
  // Amazon URLs contain ISBN-10 in the /dp/XXXXXXXXXX/ path segment
  const isbn = book.amazonUrl?.match(/\/dp\/([0-9X]{10})/)?.[1];
  return {
    '@context': 'https://schema.org',
    '@type': 'Book',
    name: book.title,
    description: book.description,
    author: { '@id': `${SITE.url}/#person` },
    ...(book.publisher && { publisher: { '@type': 'Organization', name: book.publisher } }),
    ...(book.pages && { numberOfPages: book.pages }),
    ...(book.coverImage && { image: book.coverImage }),
    ...(book.amazonUrl && { url: book.amazonUrl }),
    ...(isbn && { isbn }),
    inLanguage: 'en',
  };
}

export function youtubeChannelSchema(channel: {
  name: string;
  description: string;
  channelUrl: string;
  subscriberCount: number;
  videoCount: number;
}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    '@id': `${SITE.url}/youtube-videos/#collectionpage`,
    name: channel.name,
    description: channel.description,
    url: `${SITE.url}/youtube-videos`,
    author: { '@id': `${SITE.url}/#person` },
    about: {
      '@type': 'WebPage',
      name: `${channel.name} YouTube Channel`,
      url: channel.channelUrl,
      description: `${channel.videoCount}+ educational videos on AI, machine learning, and cloud computing`,
      interactionStatistic: [
        {
          '@type': 'InteractionCounter',
          interactionType: { '@type': 'SubscribeAction' },
          userInteractionCount: channel.subscriberCount,
        },
      ],
    },
    inLanguage: 'en',
  };
}

export function videoObjectListSchema(
  videos: { id: string; title: string; date: string }[],
  channelName: string,
  channelUrl: string,
) {
  return {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    '@id': `${SITE.url}/youtube-videos/#videolist`,
    name: `${channelName} - Latest Videos`,
    url: `${SITE.url}/youtube-videos`,
    numberOfItems: videos.length,
    itemListElement: videos.map((video, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      item: {
        '@type': 'VideoObject',
        name: video.title,
        description: `${video.title} — video by Julien Simon on ${channelName}`,
        uploadDate: new Date(video.date).toISOString(),
        thumbnailUrl: `https://img.youtube.com/vi/${video.id}/maxresdefault.jpg`,
        embedUrl: `https://www.youtube-nocookie.com/embed/${video.id}`,
        contentUrl: `https://www.youtube.com/watch?v=${video.id}`,
        author: { '@id': `${SITE.url}/#person` },
        publisher: {
          '@type': 'Organization',
          name: channelName,
          url: channelUrl,
        },
      },
    })),
  };
}

export function blogPostingListSchema(
  posts: { title: string; href: string; date?: string; description?: string }[],
  categoryName: string,
  categoryUrl: string,
) {
  return {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    '@id': `${categoryUrl}/#itemlist`,
    name: categoryName,
    url: categoryUrl,
    numberOfItems: posts.length,
    itemListElement: posts.slice(0, 50).map((post, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      item: {
        '@type': 'BlogPosting',
        headline: post.title,
        url: post.href,
        author: { '@id': `${SITE.url}/#person` },
        ...(post.date && { datePublished: post.date }),
        ...(post.description && { description: post.description }),
      },
    })),
  };
}

export function articleSchema(article: {
  title: string;
  description: string;
  datePublished: string;
  url: string;
  canonicalUrl: string;
  readTime?: string;
  tags?: string[];
}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: article.title,
    description: article.description,
    datePublished: article.datePublished,
    dateModified: article.datePublished,
    author: { '@id': `${SITE.url}/#person` },
    publisher: {
      '@type': 'Organization',
      name: 'The AI Realist',
      url: 'https://www.airealist.ai/',
    },
    mainEntityOfPage: article.canonicalUrl,
    url: article.url,
    inLanguage: 'en',
    ...(article.tags && { keywords: article.tags.join(', ') }),
    isPartOf: {
      '@type': 'Blog',
      name: 'The AI Realist',
      url: 'https://www.airealist.ai/',
    },
  };
}

export function newsletterSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'Periodical',
    '@id': 'https://www.airealist.ai/#newsletter',
    name: 'The AI Realist',
    alternateName: 'AI Realist Newsletter',
    url: 'https://www.airealist.ai/',
    description:
      'Practical AI for builders, operators, and investors. Long-form structural analysis of AI ecosystems, infrastructure, digital sovereignty, and investment architecture. Grounded in SEC filings, government surveys, legislative text, and regulatory documents.',
    publisher: { '@id': `${SITE.url}/#person` },
    inLanguage: 'en',
    dateCreated: '2022-08',
    genre: ['Technology', 'Artificial Intelligence', 'Industry Analysis', 'AI Policy', 'AI Infrastructure'],
    keywords:
      'EU AI Act, European digital sovereignty, CLOUD Act, AI regulation, Small Language Models, CPU inference, MCP protocol, AI infrastructure economics, open-weights models, AI geopolitics, LLM scaling, enterprise AI deployment',
    about: [
      { '@type': 'Thing', name: 'AI Industry Analysis', description: 'Structural analysis of AI market trends, infrastructure economics, and competitive dynamics' },
      { '@type': 'Thing', name: 'AI Regulation & Policy', description: 'EU AI Act impact, US AI Action Plan, digital sovereignty, and geopolitical implications' },
      { '@type': 'Thing', name: 'AI Infrastructure', description: 'CPU inference revolution, hardware optimization, datacenter economics, and energy constraints' },
      { '@type': 'Thing', name: 'Small Language Models', description: 'Domain-specific models that match large model performance at a fraction of the cost and energy' },
    ],
    audience: {
      '@type': 'Audience',
      audienceType: 'AI practitioners, enterprise architects, CTOs, investors, policy makers',
    },
  };
}

export function dataCatalogSchema(datasets: Array<{
  name: string;
  prettyName: string;
  description: string;
  hfUrl: string;
  source: string;
  updateFrequency?: string;
  records?: number;
}>) {
  return {
    '@context': 'https://schema.org',
    '@type': 'DataCatalog',
    name: 'Space Datasets by Julien Simon',
    description: `${TOTAL_DATASETS} open datasets for orbital mechanics, space weather, astronomy, and physics on Hugging Face`,
    url: `${SITE.url}/datasets`,
    publisher: { '@id': `${SITE.url}/#person` },
    dataset: datasets.map(d => ({
      '@type': 'Dataset',
      name: d.prettyName,
      description: d.description,
      url: d.hfUrl,
      license: 'https://creativecommons.org/licenses/by/4.0/',
      isAccessibleForFree: true,
      creator: { '@id': `${SITE.url}/#person` },
      distribution: {
        '@type': 'DataDownload',
        encodingFormat: 'application/x-parquet',
        contentUrl: d.hfUrl,
      },
      ...(d.source && { isBasedOn: d.source }),
      ...(d.records && { size: `${d.records.toLocaleString()} records` }),
    })),
  };
}

const MONTHS: Record<string, string> = {
  january: '01', february: '02', march: '03', april: '04',
  may: '05', june: '06', july: '07', august: '08',
  september: '09', october: '10', november: '11', december: '12',
};

/**
 * Parse a human-readable date string into ISO 8601 format (YYYY-MM-DD).
 * Handles: "March 18, 2026", "October 28–30, 2025", "2025" (year only).
 * Uses string parsing to avoid timezone-related off-by-one errors from Date.
 */
function parseToISODate(dateStr: string): string | null {
  // Already ISO 8601
  if (/^\d{4}-\d{2}-\d{2}/.test(dateStr)) return dateStr;
  // Year only
  if (/^\d{4}$/.test(dateStr.trim())) return dateStr.trim();
  // Strip date ranges: "October 28–30, 2025" → "October 28, 2025"
  const cleaned = dateStr.replace(/[–-]\d{1,2},/, ',');
  // Match "Month DD, YYYY"
  const match = cleaned.match(/(\w+)\s+(\d{1,2}),?\s+(\d{4})/);
  if (match) {
    const month = MONTHS[match[1].toLowerCase()];
    if (month) {
      return `${match[3]}-${month}-${match[2].padStart(2, '0')}`;
    }
  }
  return null;
}

/**
 * Determine if an event is online based on location/venue.
 */
function isOnlineEvent(event: { location?: string; venue?: string }): boolean {
  const text = `${event.location ?? ''} ${event.venue ?? ''}`.toLowerCase();
  return text.includes('online') || text.includes('twitch') || text.includes('webinar');
}

export function eventSchema(event: {
  title: string;
  venue?: string;
  date?: string;
  location?: string;
  description?: string;
  links?: { url: string; label: string }[];
}) {
  const parsed = event.date ? parseToISODate(event.date) : null;
  // Only use dates with at least YYYY-MM-DD precision; year-only values fail Google validation
  const isoDate = parsed && /^\d{4}-\d{2}-\d{2}/.test(parsed) ? parsed : null;
  const online = isOnlineEvent(event);
  // Use location if available, fall back to venue (which often contains city info)
  const placeName = event.location || event.venue;
  const eventLink = event.links?.find(l => l.label === 'Event')?.url || event.links?.[0]?.url;

  return {
    '@type': 'Event',
    name: event.title,
    ...(isoDate && { startDate: isoDate }),
    ...(event.description && { description: event.description }),
    eventStatus: 'https://schema.org/EventScheduled',
    eventAttendanceMode: online
      ? 'https://schema.org/OnlineEventAttendanceMode'
      : 'https://schema.org/OfflineEventAttendanceMode',
    ...(placeName && !online && {
      location: {
        '@type': 'Place',
        name: event.venue || placeName,
        address: event.location || event.venue,
      },
    }),
    ...(online && {
      location: {
        '@type': 'VirtualLocation',
        url: eventLink || SITE.url,
      },
    }),
    ...(event.venue && {
      organizer: {
        '@type': 'Organization',
        name: event.venue,
        ...(eventLink && { url: eventLink }),
      },
    }),
    performer: { '@id': `${SITE.url}/#person` },
    ...(eventLink && { url: eventLink }),
  };
}

export function eventListSchema(
  events: {
    title: string;
    venue?: string;
    date?: string;
    location?: string;
    description?: string;
    links?: { url: string; label: string }[];
  }[],
  pageUrl: string,
  listName: string,
  maxItems?: number,
) {
  const items = maxItems ? events.slice(0, maxItems) : events;
  return {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    '@id': `${pageUrl}/#eventlist`,
    name: listName,
    url: pageUrl,
    numberOfItems: items.length,
    itemListElement: items.map((event, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      item: eventSchema(event),
    })),
  };
}

export const SPEAKING_FAQS = [
  {
    question: 'How many speaking engagements has Julien Simon delivered?',
    answer: `Julien Simon has delivered ${SPEAKING_STATS.totalEvents}+ speaking engagements across ${SPEAKING_STATS.countries} countries and ${SPEAKING_STATS.cities} cities, including keynotes at AWS re:Invent, ODSC, KubeCon, and talks at institutions like UNESCO, World Bank, New York Federal Reserve, and Bank of Italy.`,
  },
  {
    question: 'What topics does Julien Simon speak about?',
    answer: 'Julien Simon speaks about Small Language Models, enterprise AI implementation, open-source AI, cloud computing, AI hardware optimization, and practical strategies for deploying AI in production. His talks range from deep technical demos to strategic keynotes for executive audiences.',
  },
  {
    question: 'Can I book Julien Simon for a speaking engagement?',
    answer: 'Yes, Julien Simon is available for keynotes, workshops, and technical talks. Contact him at julien@julien.org or via LinkedIn at linkedin.com/in/juliensimon.',
  },
];

export const PUBLICATIONS_FAQS = [
  {
    question: 'How many articles has Julien Simon published?',
    answer: `Julien Simon has published ${TOTAL_ARTICLES}+ technical articles across multiple platforms including the AWS Blog, Hugging Face Blog, Arcee AI Blog, Medium, and his Substack newsletter The AI Realist (airealist.ai).`,
  },
  {
    question: 'What is The AI Realist newsletter?',
    answer: 'The AI Realist (www.airealist.ai) is Julien Simon\'s Substack newsletter offering practical AI analysis for builders, operators, and investors. It delivers long-form structural analysis rooted in SEC filings, government surveys, legislative text, and regulatory documents.',
  },
];

export const YOUTUBE_FAQS = [
  {
    question: 'How many YouTube subscribers does Julien Simon have?',
    answer: `Julien Simon's YouTube channel has ${YOUTUBE_STATS.subscriberCount}K+ subscribers with ${YOUTUBE_STATS.totalVideos}+ educational videos spanning ${YOUTUBE_STATS.yearsOfContent} years of content on AI, machine learning, and cloud computing.`,
  },
  {
    question: 'What kind of videos does Julien Simon create?',
    answer: 'Julien Simon creates deep technical tutorials, live coding demos, model benchmarks, hardware comparisons, and educational content covering AI/ML topics from beginner to advanced levels. His channel is at youtube.com/@juliensimonfr.',
  },
];

export const BOOKS_FAQS = [
  {
    question: 'What books has Julien Simon written?',
    answer: 'Julien Simon authored "Learn Amazon SageMaker" (Packt Publishing, 2 editions in 2020 and 2021) — the first book ever published on Amazon SageMaker. He also co-authored "Natural Language Processing with AWS AI Services" and has contributed to additional technical works on machine learning and cloud computing.',
  },
  {
    question: 'What is "Learn Amazon SageMaker" about?',
    answer: '"Learn Amazon SageMaker" is a hands-on guide to building, training, and deploying machine learning models on AWS SageMaker. It covers data preparation, model training, hyperparameter tuning, deployment, monitoring, and MLOps best practices — used by data scientists and ML engineers worldwide as a definitive SageMaker reference.',
  },
  {
    question: 'Where can I buy Julien Simon\'s books?',
    answer: 'Julien Simon\'s books are available on Amazon (https://www.amazon.com/stores/Julien-Simon/author/B089RFQTQG), Packt Publishing (https://www.packtpub.com/authors/julien-simon), and most major online bookstores. Code samples and supplementary materials are typically open-sourced on GitHub.',
  },
];

export const DATASETS_FAQS = [
  {
    question: 'What datasets has Julien Simon published?',
    answer: `Julien Simon publishes ${TOTAL_DATASETS}+ open datasets on Hugging Face covering orbital mechanics, space weather, astronomy, and physics. Sources include NASA, ESA, NOAA, and other public scientific repositories, packaged in efficient Parquet format with CC-BY-4.0 licensing.`,
  },
  {
    question: 'Are Julien Simon\'s datasets free to use?',
    answer: 'Yes, all datasets are released under CC-BY-4.0 (free for any use, including commercial, with attribution). They are distributed in Apache Parquet format on Hugging Face at https://huggingface.co/juliensimon, optimized for efficient analytics and ML workflows.',
  },
  {
    question: 'What can I do with these datasets?',
    answer: 'The datasets support a wide range of use cases: training ML models on satellite-tracking data, analyzing solar activity and space weather, exploring asteroid and exoplanet catalogs, benchmarking time-series models, and powering educational content. They are used by researchers, students, and AI practitioners worldwide.',
  },
];

export const CODE_FAQS = [
  {
    question: 'What open-source projects has Julien Simon built?',
    answer: 'Julien Simon maintains open-source projects including Canopy (a macOS app for parallel AI coding sessions), space-datasets (pipelines for building open scientific datasets), cache-explorer (a CLI tool for analyzing AI provider cache behavior), and additional repositories spanning AI tooling, ML demos, and developer utilities. See github.com/juliensimon for the full list.',
  },
  {
    question: 'Where can I find Julien Simon\'s code?',
    answer: 'All open-source code is on GitHub at https://github.com/juliensimon. Repositories include macOS applications, CLI tools, data pipelines, and ML demos. Most projects are MIT-licensed and accept community contributions.',
  },
];

export const EXPERIENCE_FAQS = [
  {
    question: 'Where has Julien Simon worked?',
    answer: 'Julien Simon has held leadership roles at Fortino Capital (AI Operating Partner), Arcee AI (VP & Chief Evangelist), Hugging Face (Chief Evangelist), AWS (Global Evangelist for AI/ML), and executive positions at Viadeo, Aldebaran Robotics, Criteo, Pixmania, and more across 30+ years.',
  },
  {
    question: 'What is Julien Simon\'s current role?',
    answer: 'Julien Simon is currently AI Operating Partner at Fortino Capital, where he accelerates cloud and AI initiatives across both the Private Equity and Venture Capital portfolios, helping portfolio companies scale technology infrastructure and AI capabilities.',
  },
];

// Pre-built FAQ for homepage - common questions about Julien Simon
export const HOMEPAGE_FAQS = [
  {
    question: 'Who is Julien Simon?',
    answer: `Julien Simon is an AI Operating Partner at Fortino Capital with over 30 years of technology leadership experience. He previously held executive roles at AWS, Hugging Face, and Arcee AI. He is recognized as the #1 AI Evangelist globally by AI Magazine (2021), has delivered ${SPEAKING_STATS.totalEvents}+ speaking engagements across ${SPEAKING_STATS.countries} countries, and publishes The AI Realist newsletter (airealist.ai).`,
  },
  {
    question: 'What is Julien Simon known for?',
    answer: `Julien Simon is known for his expertise in Small Language Models (SLMs), enterprise AI implementation, and bridging the gap between AI research and practical business applications. He authored "Learn Amazon SageMaker", has ${YOUTUBE_STATS.subscriberCount}K+ YouTube subscribers for his AI/ML educational content, and writes The AI Realist newsletter offering structural analysis of AI industry trends. He has published ${TOTAL_ARTICLES}+ technical articles and delivered ${SPEAKING_STATS.totalEvents}+ speaking engagements worldwide.`,
  },
  {
    question: 'What does an AI Operating Partner do?',
    answer: 'As AI Operating Partner at Fortino Capital, Julien Simon accelerates cloud and AI initiatives across Private Equity and Venture Capital portfolio companies. He helps companies scale from product to engineering to operations to go-to-market, combining deep technical expertise with executive leadership.',
  },
  {
    question: 'What are Small Language Models?',
    answer: 'Small Language Models (SLMs) are AI models that deliver enterprise-grade performance with significantly lower computational requirements than large language models. Julien Simon champions SLMs as practical, cost-effective solutions that enterprises can deploy on-premises while maintaining complete control over their data.',
  },
  {
    question: 'What is The AI Realist newsletter?',
    answer: 'The AI Realist (www.airealist.ai) is Julien Simon\'s Substack newsletter offering practical AI analysis for builders, operators, and investors. It delivers long-form structural analysis rooted in SEC filings, government surveys, legislative text, and regulatory documents, covering AI ecosystems, infrastructure, digital sovereignty, and investment architecture.',
  },
];
