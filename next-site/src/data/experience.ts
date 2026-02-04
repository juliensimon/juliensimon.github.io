export interface Experience {
  title: string;
  company: string;
  companyUrl?: string;
  period: string;
  description: string;
  achievements?: string[];
  techEnvironment?: { category: string; items: string[] }[];
}

export const EXPERIENCES: Experience[] = [
  {
    title: 'AI Operating Partner',
    company: 'Fortino Capital',
    companyUrl: 'https://www.fortinocapital.com',
    period: 'November 2025 – Present',
    description:
      'Supporting both the Private Equity arm and the Venture Capital arm, working across current and future portfolio companies to accelerate and scale cloud and AI initiatives.',
    achievements: [
      'Accelerate cloud and AI initiatives across PE and VC portfolio companies',
      'Provide strategic guidance on product development, engineering architecture, and operations optimization',
      'Support GTM acceleration through technology-enabled growth strategies',
      'Help portfolio companies scale their technology infrastructure and AI capabilities',
    ],
    techEnvironment: [
      { category: 'Portfolio Operations', items: ['PE & VC portfolio acceleration', 'Product strategy & development', 'Engineering leadership'] },
      { category: 'Cloud & AI', items: ['Cloud infrastructure scaling', 'AI strategy & implementation', 'Cost optimization'] },
      { category: 'GTM & Operations', items: ['GTM acceleration', 'Operations optimization', 'Technology transformation'] },
    ],
  },
  {
    title: 'Vice President & Chief Evangelist',
    company: 'Arcee AI',
    companyUrl: 'https://www.arcee.ai',
    period: '2024 – November 2025',
    description:
      'Acted as the first customer and provided in-depth feedback to the R&D team. Created deep technical content including code demos, blog posts, and YouTube videos (400k subscribers). Recognized as an Arm Ambassador.',
    achievements: [
      'First customer, providing product feedback to enhance usability',
      'Created deep technical content (code demos, blog posts, YouTube videos)',
      'Spoke at World Bank, Bank of Italy, and international conferences',
      'Benchmarked and deployed models across hardware platforms (CPU, GPU, AI accelerators)',
      'Recognized as Arm Ambassador for inference optimization expertise',
    ],
  },
  {
    title: 'Chief Evangelist',
    company: 'Hugging Face',
    companyUrl: 'https://huggingface.co',
    period: '2021 – 2024',
    description:
      'Led technical evangelism and community building for the leading open-source AI platform, focusing on transformer models, optimization, and deployment strategies.',
    achievements: [
      'Field CTO working with Fortune 500 teams on private infrastructure deployment',
      'Tech lead on projects with JPMorgan, engaging top-level stakeholders',
      'Initiated strategic partnerships with AWS, Azure, Google, Intel, AMD',
      'Led 250+ AWS customer meetings, generating $35M+ commercial pipeline',
      'Spoke at UNESCO, NY Federal Reserve, and major industry events',
    ],
    techEnvironment: [
      { category: 'AI/ML', items: ['Transformer models', 'Open-source libraries', 'Training & inference hardware'] },
      { category: 'Cloud', items: ['AWS', 'Azure', 'GCP'] },
      { category: 'Hardware', items: ['CPU (Intel, Arm)', 'GPU (Nvidia, AMD)', 'AI accelerators (Graphcore, Gaudi, Trainium)'] },
    ],
  },
  {
    title: 'Global Evangelist, Machine Learning and AI',
    company: 'Amazon Web Services',
    companyUrl: 'https://aws.amazon.com',
    period: '2015 – 2021',
    description:
      'Helped AWS customers worldwide understand and adopt the AWS AI/ML service portfolio. Authored the first book on Amazon SageMaker.',
    achievements: [
      '650+ talks in nearly 40 countries',
      'Authored "Learn Amazon SageMaker" — first published book on AWS SageMaker',
      'Promoted to Amazon Level 8 (Director-equivalent for ICs) — extremely rare',
      'Named #1 AI Evangelist by AI Magazine in 2021',
      'Second most senior technical evangelist at AWS after Jeff Barr',
      'Wrote 70+ launch blog posts',
    ],
    techEnvironment: [
      { category: 'AWS', items: ['All things AWS (10 certifications)', 'DevOps', 'Big data'] },
      { category: 'AI/ML', items: ['ML, DL (PyTorch, TensorFlow)', 'CV, NLP, Transformers'] },
      { category: 'Hardware', items: ['GPU', 'Inferentia', 'Trainium'] },
    ],
  },
  {
    title: 'Chief Technology Officer',
    company: 'Viadeo',
    period: 'October 2014 – October 2015',
    description:
      'Led software, infrastructure, and big data (70 engineers in Paris and San Francisco) for viadeo.com, a professional social network with 10M members.',
    achievements: [
      'Initiated and completed all-in migration of 200-server physical platform to AWS',
      'Managed 70 engineers across Paris and San Francisco',
    ],
    techEnvironment: [
      { category: 'Stack', items: ['Node.js', 'Java', 'MySQL', 'HBase', 'Spark', 'Redshift', 'EMR'] },
    ],
  },
  {
    title: 'Chief Technology Officer, Software',
    company: 'Aldebaran Robotics',
    companyUrl: 'https://www.softbankrobotics.com',
    period: 'February 2014 – September 2014',
    description:
      'Managed 130 engineers responsible for software engineering (OS, apps & web) and infrastructure for all Aldebaran robots.',
    achievements: [
      'Launched the world-famous Pepper robot in Tokyo (CNN article)',
      'Reorganized team and deployed Agile methods',
    ],
    techEnvironment: [
      { category: 'Stack', items: ['C++', 'Python', 'Embedded Linux', 'Speech recognition', 'Computer vision'] },
    ],
  },
  {
    title: 'Vice President, Engineering',
    company: 'Criteo',
    companyUrl: 'https://www.criteo.com',
    period: 'October 2010 – February 2014',
    description:
      'In charge of an online advertising SaaS platform used by 3000+ e-commerce companies in 30+ countries. 30B+ daily HTTP requests.',
    achievements: [
      'Publisher Platforms: Real-Time Bidding with Facebook, Google, Yahoo — 30B+ daily requests',
      'Scalability: 6PB Hadoop cluster, real-time and analytics processing',
      'Infrastructure: 7 datacenters (6000 devices), 30M\u20AC budget, 60+ engineers',
    ],
    techEnvironment: [
      { category: 'Languages', items: ['C#', 'Java', 'C/C++'] },
      { category: 'Big Data', items: ['MongoDB', 'Cloudera Hadoop', 'Storm', 'Kafka'] },
      { category: 'Infra', items: ['Linux', 'Cisco Nexus', 'F5/A10 load balancers'] },
    ],
  },
  {
    title: 'Chief Technology Officer',
    company: 'Pixmania',
    period: 'May 2009 – September 2010',
    description:
      'In charge of an e-commerce platform generating 2B\u20AC GMV. 150 engineers, 600+ servers, 2PB NetApp storage.',
    achievements: [
      'Lowered OPEX by 20% through better supplier management',
      'Managed 600+ servers across 7 locations',
    ],
  },
  {
    title: 'Vice President, Engineering',
    company: 'Digiplug',
    period: 'March 2007 – April 2009',
    description:
      'SaaS platform for digital supply chain services used by music majors (Universal, Sony, Warner). Scaled team from 12 to 50.',
    achievements: [
      'Designed and deployed infrastructure on 2 hosting locations (150 servers, 2M\u20AC+ CAPEX)',
      'Implemented ISO 27001 security standards',
    ],
  },
  {
    title: 'Director, R&D Mobile Communications',
    company: 'Oberthur Technologies',
    companyUrl: 'https://www.idemia.com',
    period: 'February 2002 – September 2006',
    description:
      'Led software development of all Telecom products (45 people in France, 25 in China and Philippines). Major customer wins (Vodafone Group, Cingular).',
    achievements: [
      '70 engineers across France, China, Philippines',
      'Won Vodafone Group and Cingular contracts',
      'Sustained 60% yearly increase in smartcard delivery volumes',
      'Custom SIM apps for SFR, Orange, TIM, Telefonica, Vodafone UK',
    ],
  },
];

export const EDUCATION = [
  {
    degree: "Master's degree in Computer Systems",
    school: 'Sorbonne University, Paris',
    year: '1995',
  },
  {
    degree: 'Engineering degree',
    school: 'ISEP, Paris',
    year: '1993',
  },
];
