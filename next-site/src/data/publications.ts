export interface PublicationCategory {
  name: string;
  count: number;
  description: string;
  href: string;
  dateRange: string;
}

export const PUBLICATION_CATEGORIES: PublicationCategory[] = [
  {
    name: 'Industry Perspectives',
    count: 18,
    description: 'Company-agnostic thoughts and lessons learned.',
    href: '/blog/industry-perspectives/index.html',
    dateRange: '2021 - Present',
  },
  {
    name: 'Arcee AI',
    count: 16,
    description: 'Technical articles as VP & Chief Evangelist at Arcee AI.',
    href: '/blog-posts/arcee',
    dateRange: '2024 - November 2025',
  },
  {
    name: 'Hugging Face',
    count: 25,
    description: 'Articles on the HF blog as Chief Evangelist.',
    href: '/blog-posts/huggingface',
    dateRange: '2021 - 2024',
  },
  {
    name: 'AWS Blog Posts',
    count: 68,
    description: 'Technical articles on AWS blogs.',
    href: '/blog-posts/aws',
    dateRange: '2015 - 2021',
  },
  {
    name: 'AWS Medium Posts',
    count: 182,
    description: 'Technical articles on Medium during AWS tenure.',
    href: '/blog-posts/aws-medium',
    dateRange: '2015 - 2021',
  },
  {
    name: 'Legacy Blog Posts',
    count: 90,
    description: 'Pre-AWS technical articles archive.',
    href: '/blog/legacy-posts-and-images/index.html',
    dateRange: '2008 - 2016',
  },
];

export const TOTAL_ARTICLES = 392;
