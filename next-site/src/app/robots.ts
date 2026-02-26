import type { MetadataRoute } from 'next';
import { SITE } from '@/lib/constants';

export const dynamic = 'force-static';

export default function robots(): MetadataRoute.Robots {
  const disallowPaths = ['/.git/', '/.github/', '/node_modules/', '/scripts/'];

  return {
    rules: [
      // Default rule for all crawlers
      {
        userAgent: '*',
        allow: '/',
        disallow: disallowPaths,
      },
      // Explicitly welcome AI search and training crawlers
      // OpenAI
      { userAgent: 'GPTBot', allow: '/' },
      { userAgent: 'OAI-SearchBot', allow: '/' },
      { userAgent: 'ChatGPT-User', allow: '/' },
      // Anthropic
      { userAgent: 'ClaudeBot', allow: '/' },
      { userAgent: 'Claude-SearchBot', allow: '/' },
      { userAgent: 'Claude-User', allow: '/' },
      // Google AI
      { userAgent: 'Google-Extended', allow: '/' },
      // Perplexity
      { userAgent: 'PerplexityBot', allow: '/' },
      // Apple Intelligence
      { userAgent: 'Applebot-Extended', allow: '/' },
      // Meta AI
      { userAgent: 'meta-externalagent', allow: '/' },
    ],
    sitemap: `${SITE.url}/sitemap-index.xml`,
  };
}
