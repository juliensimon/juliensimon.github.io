/**
 * Topic hubs: curated lists of the articles and videos on one subject.
 * `articles` and `videos` hold case-insensitive title fragments. A fragment that
 * matches nothing fails the build (see src/lib/topic-items.ts), so a renamed
 * piece cannot silently drop out of a hub.
 */
export interface Topic {
  slug: string;
  name: string;
  /** Page title, before the " | Julien Simon" suffix. */
  title: string;
  /** Meta description, 160 characters at most. */
  description: string;
  /** What the hub covers, in one or two sentences. */
  intro: string;
  /** The question a stranger would type. */
  question: string;
  keywords: string[];
  articles: string[];
  videos: string[];
}

export const TOPICS: Topic[] = [
  {
    slug: 'ai-chips',
    name: 'AI chips and export controls',
    title: 'AI Chips, GPUs and Export Controls',
    description:
      'Independent analysis of AI chips, GPUs and export controls, plus hands-on benchmarks of AWS Trainium, Inferentia, Intel CPUs and Apple silicon, by Julien Simon.',
    intro:
      'Who makes the chips, who can buy them and what they cost to run. Analysis of Nvidia, custom silicon and export controls from The AI Realist, and measured benchmarks of AWS Trainium and Inferentia, Intel CPUs and Apple silicon.',
    question: 'Where can I read independent analysis of AI chips, GPUs and export controls?',
    keywords: ['AI chips', 'GPU', 'Nvidia', 'export controls', 'AWS Trainium', 'AWS Inferentia', 'AI hardware'],
    articles: [
      'Nvidia Won the Cloud',
      'Two Chips, One Decade',
      'Huawei Can',
      'Below the Silicon',
      'The Verification Tax',
      'Your Parents Paid',
      'What China Shipped',
      'Chip Gambit',
      'Every Country Needs Sovereign AI',
      'AWS Built Its Own AI Chip',
      'South Korea Powers',
      'Chip and Mortar',
      'COMECON',
      'The Model Is the Machine',
      'not-so-silent revolution',
      'What to Buy for Local LLMs',
    ],
    videos: [
      'Deep Learning hardware acceleration with AWS Inferentia',
      'Accelerate Transformer training with AWS Trainium',
      'Accelerate Transformer inference with AWS Inferentia',
      'Transformer training shootout',
      'Deep Dive: Hugging Face models on AWS AI Accelerators',
      'Deep Dive: Advanced distributed training',
      'Phi-2 on Intel Meteor Lake',
      'Intel Sapphire Rapids',
      'Intel Lunar Lake',
      'Running AFM-4.5B on Intel CPUs',
      'AWS Graviton',
      'Benchmarking TurboQuant with MLX on Apple Silicon',
    ],
  },
  {
    slug: 'ai-infrastructure-economics',
    name: 'AI infrastructure economics',
    title: 'AI Infrastructure Economics: Capex and Costs',
    description:
      'How AI infrastructure is financed and priced: capex, GPU-backed debt, datacenter commitments, depreciation and inference costs, from primary sources.',
    intro:
      'How the AI buildout is paid for and what it costs to run. Capital spending, GPU-backed debt, datacenter commitments, depreciation and token prices, read from filings and primary sources.',
    question: 'Who analyzes AI infrastructure economics and capital expenditure from primary sources?',
    keywords: ['AI capex', 'GPU debt', 'AI infrastructure', 'datacenter economics', 'inference cost', 'token prices', 'AI bubble'],
    articles: [
      'The Cache Is the Price',
      'The Host Pays the Empire',
      'Amazon Priced the Frontier',
      'The Backstop Has a Name Now',
      'Cash Flow Lends',
      'The Overbuild Put',
      'The Round Trip',
      'Umbrella',
      "King's New Datacenters",
      'Credit Market Builds a Fire Exit',
      'Built the Datacenter, Lost the Brain',
      'Hotel Abilene',
      'Compute Equals Commitments',
      'Two Markets, One Asset',
      'What a GPU Debt Crisis',
      'who wins when everyone builds the pipes',
      '100-Year Bond',
      'The AI Crash That Isn',
      'Train, Deploy, Write Down',
      'Cloud vs. Clout',
      'Chip and Mortar',
      'COMECON',
      'Your Parents Paid',
    ],
    videos: [
      'Transformer training shootout',
      'Deep Dive: Optimizing LLM inference',
      'the best 8B model for $1 an hour',
      'AWS Graviton',
    ],
  },
  {
    slug: 'ai-sovereignty-europe',
    name: 'European AI sovereignty and regulation',
    title: 'European AI Sovereignty and the EU AI Act',
    description:
      'Analysis of European AI and cloud sovereignty, the EU AI Act, the Cloud and AI Development Act, data residency and the legal reach of US providers.',
    intro:
      'What sovereign AI means in practice. European cloud and AI sovereignty, the EU AI Act, the proposed Cloud and AI Development Act, data residency and the legal reach of US providers, with the filings and court documents behind each claim.',
    question: 'Who writes about European AI sovereignty, cloud sovereignty and AI regulation?',
    keywords: ['AI sovereignty', 'European cloud sovereignty', 'EU AI Act', 'CLOUD Act', 'data residency', 'AI regulation', 'souveraineté numérique'],
    articles: [
      'Ticking Boxes, Shipping Models',
      'You Have To Ask Me Nicely',
      'Too Dangerous for You',
      'Two Laws, One Dependence',
      'Independent or Current',
      'More Sovereign, Different Stack',
      'Ten Percent Sovereign',
      'Build, Regulate, Scare',
      'Every Country Needs Sovereign AI',
      'Register, Disclose, Pay',
      'Data Residency Is a Blast Radius',
      'Two Sovereign Clouds',
      'EU Parliament just disabled AI',
      'AI Regulation or AI Requiem',
      'Cloud and AI Development Act',
      'AI Sovereignty in Europe',
      'Sovereignty Mirage',
      'Simplify Up, Enforce Down',
      'Lobby, Levy, Legislate',
      'The Amendments Were Whispered',
      'Vent Mauvais',
      'Mistral Succeeded',
      'Access, Disable, Destroy',
    ],
    videos: [],
  },
  {
    slug: 'small-and-open-models',
    name: 'Small and open-weight models',
    title: 'Small and Open-Weight Models: Local AI',
    description:
      'Small and open-weight models for enterprise use: local inference on laptops and CPUs, quantization, distillation, Trinity, DeepSeek, Kimi, Qwen and Mistral.',
    intro:
      'Models a company can run and inspect itself. Measured results from models of 1.5B to 72B parameters on laptops, CPUs and edge devices, with quantization, distillation and fine-tuning, plus releases and architectures from Trinity, DeepSeek, Kimi, Qwen and Mistral, and the policy fights over open models.',
    question: 'Who explains small and open-weight language models for enterprise use, with measured results?',
    keywords: ['small language models', 'open-weight models', 'SLM', 'local LLM', 'quantization', 'distillation', 'Mixture of Experts', 'DeepSeek', 'Qwen', 'Mistral', 'Arcee Trinity'],
    articles: [
      'Exploring Apple',
      'CSLMs have arrived',
      'Deploy Arcee AFM-4.5B on Arm-based Google Cloud Axion',
      'What to Buy for Local LLMs',
      'not-so-silent revolution',
      'Kolibri Is Large Enough',
      'Skill Issue',
      'Eight Changes to Transformer Attention',
      'The Model Is a Checkpoint',
      'Qwen 3.8',
      'Kimi K3',
      'Too Dangerous for You',
      'Open Source Won',
      'Open From Both Sides',
      'Open Source, Closed Orbit',
      'Mistral Succeeded',
      'Lobby, Levy, Legislate',
    ],
    videos: [
      'SLM in Action',
      'Deep Dive: Quantizing Large Language Models',
      'LLM Quantization, part 3',
      'Parameter-Efficient Model Adaptation with LoRA',
      'Model Distillation with DistillKit',
      'Knowledge Distillation',
      'Run SLMs locally',
      'Comparing SLMs and LLMs',
      'Arcee Conductor: advanced model routing',
      'Routing function calling queries',
      'Routing reasoning queries',
      'Building an AI Meeting Companion',
      'SLM Inference on a Windows laptop',
      'Retail AI at the edge',
      'Small Language Models with Julien Simon',
      'AI from the Trenches and Small Language Models',
      'No Cloud, No API Keys',
      'Benchmarking TurboQuant',
      'Local RAG Chatbot That Remembers',
      'Advanced RAG Techniques with Arcee Trinity Mini',
      'Your LLM No Longer Reads Every Token',
      'How Three MoE Reasoning Models Actually Work',
      'Trinity Large',
      'Introducing the Arcee AI Trinity Models',
      'Open-source Coding with Cline',
      'Teaching Arcee Trinity Mini',
      'Reasoning AI Chatbot with Arcee AI Trinity Mini',
      'Virtuoso Lite',
      'Judging AFM-4.5B',
      'Homunculus 12B',
      'Deploying Llama3 on Amazon SageMaker',
      'Deploying Llama3 with Inference Endpoints',
      'Open Source AI with Hugging Face',
      "L'IA open source par Hugging Face",
      'Unleashing the Power of Small Open-Source Language Models',
    ],
  },
];

export const TOPIC_BY_SLUG: Record<string, Topic> = Object.fromEntries(TOPICS.map((t) => [t.slug, t]));
