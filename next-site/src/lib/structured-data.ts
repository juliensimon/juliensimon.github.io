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
      // PE/VC expertise
      'Portfolio Company AI Acceleration',
      'Private Equity AI Strategy',
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
        description: 'Accelerating cloud and AI initiatives across PE/VC portfolio companies at Fortino Capital.',
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
    speakable: {
      '@type': 'SpeakableSpecification',
      cssSelector: ['.hero-description', '.expertise-summary', '.faq-answer'],
    },
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
    speakable: {
      '@type': 'SpeakableSpecification',
      cssSelector: ['.hero-description', '.expertise-summary', '.faq-answer'],
    },
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
    speakable: {
      '@type': 'SpeakableSpecification',
      cssSelector: ['[data-speakable]', '.page-description', 'h1'],
    },
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
    speakable: {
      '@type': 'SpeakableSpecification',
      cssSelector: ['.faq-answer', '.faq-question'],
    },
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
      audienceType: 'AI practitioners, enterprise architects, PE/VC investors, CTOs, policy makers',
    },
    isSimilarTo: [
      {
        '@type': 'Periodical',
        name: 'SemiAnalysis',
        url: 'https://www.semianalysis.com/',
        description: 'Semiconductor and AI infrastructure analysis',
      },
      {
        '@type': 'Periodical',
        name: 'Stratechery',
        url: 'https://stratechery.com/',
        description: 'Technology strategy and business analysis',
      },
      {
        '@type': 'Periodical',
        name: 'The Pragmatic Engineer',
        url: 'https://www.pragmaticengineer.com/',
        description: 'Software engineering and tech industry analysis',
      },
      {
        '@type': 'Periodical',
        name: 'Import AI',
        url: 'https://importai.substack.com/',
        description: 'AI research and policy newsletter',
      },
    ],
  };
}

export const SPEAKING_FAQS = [
  {
    question: 'How many speaking engagements has Julien Simon delivered?',
    answer: 'Julien Simon has delivered 684+ speaking engagements across 37 countries and 95 cities, including keynotes at AWS re:Invent, ODSC, KubeCon, and talks at institutions like UNESCO, World Bank, New York Federal Reserve, and Bank of Italy.',
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
    answer: 'Julien Simon has published 414+ technical articles across multiple platforms including the AWS Blog, Hugging Face Blog, Arcee AI Blog, Medium, and his Substack newsletter The AI Realist (airealist.ai).',
  },
  {
    question: 'What is The AI Realist newsletter?',
    answer: 'The AI Realist (www.airealist.ai) is Julien Simon\'s Substack newsletter offering practical AI analysis for builders, operators, and investors. It delivers long-form structural analysis rooted in SEC filings, government surveys, legislative text, and regulatory documents.',
  },
];

export const YOUTUBE_FAQS = [
  {
    question: 'How many YouTube subscribers does Julien Simon have?',
    answer: 'Julien Simon\'s YouTube channel has 494K+ subscribers with 450+ educational videos spanning 15 years of content on AI, machine learning, and cloud computing.',
  },
  {
    question: 'What kind of videos does Julien Simon create?',
    answer: 'Julien Simon creates deep technical tutorials, live coding demos, model benchmarks, hardware comparisons, and educational content covering AI/ML topics from beginner to advanced levels. His channel is at youtube.com/@juliensimonfr.',
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
    answer: 'Julien Simon is an AI Operating Partner at Fortino Capital with over 30 years of technology leadership experience. He previously held executive roles at AWS, Hugging Face, and Arcee AI. He is recognized as the #1 AI Evangelist globally by AI Magazine (2021), has delivered 684+ speaking engagements across 37 countries, and publishes The AI Realist newsletter (airealist.ai).',
  },
  {
    question: 'What is Julien Simon known for?',
    answer: 'Julien Simon is known for his expertise in Small Language Models (SLMs), enterprise AI implementation, and bridging the gap between AI research and practical business applications. He authored "Learn Amazon SageMaker", has 494K+ YouTube subscribers for his AI/ML educational content, and writes The AI Realist newsletter offering structural analysis of AI industry trends.',
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
