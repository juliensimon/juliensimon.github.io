export interface Repository {
  name: string;
  description: string;
  url: string;
  language?: string;
  tags: string[];
  featured?: boolean;
}

export const REPOSITORIES: Repository[] = [
  {
    name: 'starlink-viz',
    description: 'Real-time 3D Starlink satellite tracker with live dish telemetry. Track ~10,000 satellites, ground stations, handoffs, and network performance.',
    url: 'https://github.com/juliensimon/starlink-viz',
    language: 'TypeScript',
    tags: ['Three.js', 'Next.js', 'Satellite Tracking', '3D Visualization'],
    featured: true,
  },
  {
    name: 'gradio-mcp-server-builder',
    description: 'CLI tool to create MCP servers with Gradio web interfaces from existing Python functions.',
    url: 'https://github.com/juliensimon/gradio-mcp-server-builder',
    language: 'Python',
    tags: ['MCP Protocol', 'Gradio UI', 'AI/ML Tools', 'Code Generation'],
    featured: true,
  },
  {
    name: 'ai-inference-tco-calculator',
    description: 'AI Inference TCO Calculator — compare API vs self-hosted GPU vs local/edge inference costs.',
    url: 'https://github.com/juliensimon/ai-inference-tco-calculator',
    language: 'Python',
    tags: ['TCO Analysis', 'AI Inference', 'GPU Costs', 'Cost Optimization'],
    featured: true,
  },
  {
    name: 'arcee-demos',
    description: 'Demos, examples, and tools for Arcee AI models and services.',
    url: 'https://github.com/juliensimon/arcee-demos',
    language: 'Jupyter Notebook',
    tags: ['Arcee AI', 'SuperNova', 'Model Engine', 'Conductor'],
  },
  {
    name: 'huggingface-demos',
    description: 'Practical demos and tutorials for Hugging Face technologies, optimization, and deployment.',
    url: 'https://github.com/juliensimon/huggingface-demos',
    language: 'Jupyter Notebook',
    tags: ['Hugging Face', 'Optimum', 'Neuron', 'Trainium', 'Inferentia2'],
  },
  {
    name: 'radar-evaluator',
    description: 'Framework for evaluating and comparing LLMs across industry domains using radar charts and automated scoring.',
    url: 'https://github.com/juliensimon/radar-evaluator',
    tags: ['LLM Evaluation', 'Radar Charts', 'Automated Scoring', 'Benchmarking'],
  },
  {
    name: 'sagemaker-inference-container-cpu',
    description: 'Docker Container for HF Inference on CPU. Cost-efficient AI inference with SLMs.',
    url: 'https://github.com/juliensimon/sagemaker-inference-container-cpu',
    language: 'Python',
    tags: ['SageMaker', 'llama.cpp', 'ARM64', 'AMD64'],
  },
];

export const GITHUB_PROFILE = 'https://github.com/juliensimon?tab=repositories';
