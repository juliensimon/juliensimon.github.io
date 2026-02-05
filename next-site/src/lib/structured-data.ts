import { SITE, SOCIAL_LINKS } from './constants';

export function personSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'Person',
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
    hasCredential: [
      {
        '@type': 'EducationalOccupationalCredential',
        credentialCategory: 'Professional Certification',
        recognizedBy: { '@type': 'Organization', name: 'AI Magazine' },
        name: '#1 AI Evangelist 2021',
      },
    ],
    memberOf: [
      { '@type': 'Organization', name: 'Arcee AI', url: 'https://arcee.ai' },
      { '@type': 'Organization', name: 'Amazon Web Services', url: 'https://aws.amazon.com' },
      { '@type': 'Organization', name: 'Hugging Face', url: 'https://huggingface.co' },
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
    name: SITE.name,
    url: SITE.url,
    description: SITE.description,
    author: { '@type': 'Person', name: SITE.name },
  };
}

export function breadcrumbSchema(items: { name: string; url: string }[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
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
    name,
    description,
    url,
    mainEntity: {
      '@type': 'Person',
      name: 'Julien Simon',
    },
  };
}

export function faqSchema(faqs: { question: string; answer: string }[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqs.map((faq) => ({
      '@type': 'Question',
      name: faq.question,
      acceptedAnswer: { '@type': 'Answer', text: faq.answer },
    })),
  };
}

export function speakableSchema(cssSelectors: string[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    speakable: {
      '@type': 'SpeakableSpecification',
      cssSelector: cssSelectors,
    },
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
