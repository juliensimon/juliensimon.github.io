export interface Repository {
  name: string;
  description: string;
  url: string;
  language?: string;
  stars?: number;
  forks?: number;
  tags: string[];
}

export const PINNED_REPOSITORIES: Repository[] = [
  {
    name: 'starlink-viz',
    description: 'Real-time 3D Starlink satellite tracker with space/sky views, live telemetry, and ISL routing for ~10,000 satellites.',
    url: 'https://github.com/juliensimon/starlink-viz',
    language: 'TypeScript',
    stars: 8,
    forks: 1,
    tags: ['Three.js', 'Next.js', 'Satellite Tracking', '3D Visualization'],
  },
  {
    name: 'space-datasets',
    description: '160+ auto-updated space, astronomy & physics datasets on Hugging Face (NASA, NOAA, ESA, JPL, SpaceX, Wikidata).',
    url: 'https://github.com/juliensimon/space-datasets',
    language: 'Python',
    stars: 2,
    tags: ['Hugging Face', 'NASA', 'Astronomy', 'Open Data'],
  },
  {
    name: 'cache-commander',
    description: 'Terminal UI tool to explore, audit, and clean developer cache directories with CVE scanning.',
    url: 'https://github.com/juliensimon/cache-commander',
    language: 'Rust',
    stars: 11,
    forks: 1,
    tags: ['TUI', 'Cache Management', 'CVE Scanning', 'Developer Tools'],
  },
  {
    name: 'ocel-generator',
    description: 'Generate realistic multi-agent workflow traces with LLM-enriched content (pip installable).',
    url: 'https://github.com/juliensimon/ocel-generator',
    language: 'Python',
    stars: 4,
    forks: 1,
    tags: ['OCEL', 'Process Mining', 'Multi-Agent', 'Synthetic Data'],
  },
  {
    name: 'sagemaker-inference-container-cpu',
    description: 'Amazon SageMaker container for Hugging Face inference on Graviton and Intel CPUs.',
    url: 'https://github.com/juliensimon/sagemaker-inference-container-cpu',
    language: 'Python',
    stars: 11,
    forks: 1,
    tags: ['SageMaker', 'llama.cpp', 'ARM64', 'AMD64'],
  },
  {
    name: 'my-aws-talks-2015-2021',
    description: 'Collection of 300+ AWS presentations from tenure as Technical Evangelist at Amazon Web Services.',
    url: 'https://github.com/juliensimon/my-aws-talks-2015-2021',
    stars: 13,
    forks: 1,
    tags: ['AWS', 'Presentations', 'Technical Evangelism', 'Archive'],
  },
];

export const GITHUB_USERNAME = 'juliensimon';
export const GITHUB_PROFILE = 'https://github.com/juliensimon';
