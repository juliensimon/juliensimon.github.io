import { SITE, SOCIAL_LINKS } from './constants';

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
      'Open source AI advocate who champions transparent, open-weights models over black box LLMs. Research-fluent expert democratizing AI through accessible, controllable solutions enterprises can understand and deploy.',
    url: SITE.url,
    image: {
      '@type': 'ImageObject',
      url: SITE.image,
      width: 200,
      height: 200,
    },
    sameAs: SOCIAL_LINKS.map((l) => l.href),
    knowsAbout: [
      'Portfolio Company AI Acceleration',
      'Private Equity AI Strategy',
      'Open Source AI Implementation',
      'Small Language Models',
      'Enterprise AI',
      'AWS',
      'Hugging Face',
      'Cloud Computing',
    ],
    award: ['AI Magazine #1 AI Evangelist 2021', 'Trophees CIO Prix de l\'Innovation 2013'],
    contactPoint: { '@type': 'ContactPoint', contactType: 'email', email: SITE.email },
    knowsLanguage: ['English', 'French'],
    nationality: 'French',
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
    '@id': `${items[items.length - 1].url}/#breadcrumb`,
    itemListElement: items.map((item, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: item.name,
      item: item.url,
    })),
  };
}

export function webPageSchema(name: string, description: string, url: string) {
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

export function faqSchema(faqs: { question: string; answer: string }[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    '@id': `${SITE.url}/#faq`,
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
    inLanguage: 'en',
  };
}

export function videoObjectSchema(channel: {
  name: string;
  description: string;
  channelUrl: string;
  subscriberCount: number;
  videoCount: number;
}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    '@id': `${SITE.url}/youtube-videos/#itemlist`,
    name: channel.name,
    description: channel.description,
    numberOfItems: channel.videoCount,
    url: `${SITE.url}/youtube-videos`,
    author: { '@id': `${SITE.url}/#person` },
    itemListElement: [
      {
        '@type': 'VideoObject',
        position: 1,
        name: 'YouTube Channel',
        description: `${channel.videoCount}+ educational videos on AI, machine learning, and cloud computing`,
        thumbnailUrl: SITE.image,
        uploadDate: '2020-01-01',
        contentUrl: channel.channelUrl,
        embedUrl: channel.channelUrl,
        interactionStatistic: {
          '@type': 'InteractionCounter',
          interactionType: { '@type': 'WatchAction' },
          userInteractionCount: channel.subscriberCount,
        },
      },
    ],
  };
}

// Pre-built FAQ for homepage - common questions about Julien Simon
export const HOMEPAGE_FAQS = [
  {
    question: 'Who is Julien Simon?',
    answer: 'Julien Simon is an AI Operating Partner at Fortino Capital with over 30 years of technology leadership experience. He previously held executive roles at AWS, Hugging Face, and Arcee AI. He is recognized as the #1 AI Evangelist globally by AI Magazine (2021) and has delivered 684+ speaking engagements across 37 countries.',
  },
  {
    question: 'What is Julien Simon known for?',
    answer: 'Julien Simon is known for his expertise in Small Language Models (SLMs), enterprise AI implementation, and bridging the gap between AI research and practical business applications. He authored "Learn Amazon SageMaker" and has 467K+ YouTube subscribers for his AI/ML educational content.',
  },
  {
    question: 'What does an AI Operating Partner do?',
    answer: 'As AI Operating Partner at Fortino Capital, Julien Simon accelerates cloud and AI initiatives across Private Equity and Venture Capital portfolio companies. He helps companies scale from product to engineering to operations to go-to-market, combining deep technical expertise with executive leadership.',
  },
  {
    question: 'What are Small Language Models?',
    answer: 'Small Language Models (SLMs) are AI models that deliver enterprise-grade performance with significantly lower computational requirements than large language models. Julien Simon champions SLMs as practical, cost-effective solutions that enterprises can deploy on-premises while maintaining complete control over their data.',
  },
];
