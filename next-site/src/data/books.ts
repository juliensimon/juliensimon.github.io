export interface Book {
  title: string;
  role: string;
  publisher?: string;
  editions?: string;
  pages?: number;
  description: string;
  coverImage?: string;
  amazonUrl?: string;
  githubUrl?: string;
}

export const BOOKS: Book[] = [
  {
    title: 'Learn Amazon SageMaker',
    role: 'Author (Single author)',
    publisher: 'Packt Publishing',
    editions: 'First edition (August 2020), Second edition (September 2021)',
    pages: 490,
    description:
      'The first book ever published on Amazon SageMaker, AWS\' flagship machine learning service. Covers the full ML lifecycle from data preparation to model deployment at scale.',
    coverImage: 'https://m.media-amazon.com/images/I/61nbUcX6nCL._SY385_.jpg',
    amazonUrl: 'https://www.amazon.com/Learn-Amazon-SageMaker-developers-scientists/dp/180020891X',
    githubUrl: 'https://github.com/PacktPublishing/Learn-Amazon-SageMaker',
  },
  {
    title: 'Natural Language Processing with AWS AI Services',
    role: 'Contributor (Foreword)',
    description:
      'A comprehensive guide to implementing NLP solutions using AWS AI services (Amazon Comprehend, Translate, Polly, etc.).',
  },
];
