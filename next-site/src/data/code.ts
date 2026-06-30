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
    name: 'cache-commander',
    description: 'Cache Commander — a TUI and MCP server to explore, audit, and clean developer cache directories. Scan for CVEs, find outdated packages, reclaim disk space. Supports pip, npm, Cargo, HuggingFace, Homebrew, and more.',
    url: 'https://github.com/juliensimon/cache-commander',
    language: 'Rust',
    stars: 66,
    forks: 6,
    tags: ['TUI', 'Cache Management', 'CVE Scanning', 'Developer Tools'],
  },
  {
    name: 'canopy',
    description: 'Ship faster with parallel Claude Code sessions — one native macOS window, git worktrees, sandboxes, auto-resume, merge & finish, token dashboard.',
    url: 'https://github.com/juliensimon/canopy',
    language: 'Swift',
    stars: 101,
    forks: 3,
    tags: ['Claude Code', 'macOS', 'Git Worktrees', 'Developer Tools'],
  },
  {
    name: 'starlink-viz',
    description: 'Real-time 3D Starlink satellite tracker with Space view, Sky view, live dish telemetry, SGP4 propagation, and ISL routing. Track ~10,000 satellites, ground stations, handoffs, and network performance — built with Next.js and Three.js.',
    url: 'https://github.com/juliensimon/starlink-viz',
    language: 'TypeScript',
    stars: 23,
    forks: 7,
    tags: ['Three.js', 'Next.js', 'Satellite Tracking', '3D Visualization'],
  },
  {
    name: 'apollo11-ai-walkthrough',
    description: 'AI-generated technical walkthrough of the Apollo 11 Guidance Computer flight software (Luminary099)',
    url: 'https://github.com/juliensimon/apollo11-ai-walkthrough',
    language: 'Python',
    stars: 41,
    forks: 9,
    tags: ['Apollo 11', 'AI Analysis', 'Flight Software', 'Historical'],
  },
  {
    name: 'sagemaker-inference-container-cpu',
    description: 'An Amazon SageMaker Container for Hugging Face Inference on Graviton and Intel CPUs',
    url: 'https://github.com/juliensimon/sagemaker-inference-container-cpu',
    language: 'Python',
    stars: 11,
    forks: 1,
    tags: ['SageMaker', 'llama.cpp', 'ARM64', 'AMD64'],
  },
  {
    name: 'ocel-generator',
    description: 'Generate realistic multi-agent workflow traces with LLM-enriched content, semantic validation, and PM4Py compatibility. pip install open-agent-traces',
    url: 'https://github.com/juliensimon/ocel-generator',
    language: 'Python',
    stars: 16,
    forks: 3,
    tags: ['OCEL', 'Process Mining', 'Multi-Agent', 'Synthetic Data'],
  },
];

export const GITHUB_USERNAME = 'juliensimon';
export const GITHUB_PROFILE = 'https://github.com/juliensimon';
