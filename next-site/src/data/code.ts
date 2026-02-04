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
    name: 'gradio-mcp-server-builder',
    description: 'CLI tool to create MCP servers with Gradio web interfaces from existing Python functions.',
    url: 'https://github.com/juliensimon/gradio-mcp-server-builder',
    language: 'Python',
    tags: ['MCP Protocol', 'Gradio UI', 'AI/ML Tools', 'Code Generation'],
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
    name: 'aws-samples',
    description: 'Developer resources for Arcee models on AWS.',
    url: 'https://github.com/juliensimon/aws-samples',
    language: 'Jupyter Notebook',
    tags: ['AWS', 'SageMaker', 'CloudFormation', 'JumpStart'],
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
