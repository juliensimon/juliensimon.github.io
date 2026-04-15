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
    description: 'Real-time 3D Starlink satellite tracker with Space view, Sky view, live dish telemetry, SGP4 propagation, and ISL routing. Track ~10,000 satellites, ground stations, handoffs, and network performance — built with Next.js and Three.js.',
    url: 'https://github.com/juliensimon/starlink-viz',
    language: 'TypeScript',
    stars: 9,
    forks: 1,
    tags: ['Three.js', 'Next.js', 'Satellite Tracking', '3D Visualization'],
  },
  {
    name: 'space-datasets',
    description: '160+ auto-updated space, astronomy & physics datasets on Hugging Face (NASA, NOAA, ESA, JPL, SpaceX, Wikidata). Satellites, asteroids, space probes (Voyager, Cassini, Mars), space weather, exoplanets, pulsars, radio/X-ray surveys, cosmic rays, particle physics, and more. Parquet format, no API keys.',
    url: 'https://github.com/juliensimon/space-datasets',
    language: 'Python',
    stars: 3,
    tags: ['Hugging Face', 'NASA', 'Astronomy', 'Open Data'],
  },
  {
    name: 'cache-commander',
    description: 'Cache Commander — a TUI and MCP server to explore, audit, and clean developer cache directories. Scan for CVEs, find outdated packages, reclaim disk space. Supports pip, npm, Cargo, HuggingFace, Homebrew, and more.',
    url: 'https://github.com/juliensimon/cache-commander',
    language: 'Rust',
    stars: 43,
    forks: 2,
    tags: ['TUI', 'Cache Management', 'CVE Scanning', 'Developer Tools'],
  },
  {
    name: 'ocel-generator',
    description: 'Generate realistic multi-agent workflow traces with LLM-enriched content, semantic validation, and PM4Py compatibility. pip install open-agent-traces',
    url: 'https://github.com/juliensimon/ocel-generator',
    language: 'Python',
    stars: 15,
    forks: 2,
    tags: ['OCEL', 'Process Mining', 'Multi-Agent', 'Synthetic Data'],
  },
  {
    name: 'sagemaker-inference-container-cpu',
    description: 'An Amazon SageMaker Container for Hugging Face Inference on Graviton and Intel CPUs.',
    url: 'https://github.com/juliensimon/sagemaker-inference-container-cpu',
    language: 'Python',
    stars: 11,
    forks: 1,
    tags: ['SageMaker', 'llama.cpp', 'ARM64', 'AMD64'],
  },
  {
    name: 'my-aws-talks-2015-2021',
    description: 'My collection of 300+ AWS presentations and talks from my time as a Technical Evangelist at Amazon Web Services (2015-2021).',
    url: 'https://github.com/juliensimon/my-aws-talks-2015-2021',
    stars: 13,
    forks: 1,
    tags: ['AWS', 'Presentations', 'Technical Evangelism', 'Archive'],
  },
];

export const GITHUB_USERNAME = 'juliensimon';
export const GITHUB_PROFILE = 'https://github.com/juliensimon';
