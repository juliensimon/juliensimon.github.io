import { SITE } from '@/lib/constants';
import { INDUSTRY_PERSPECTIVES_ARTICLES } from '@/data/blog-listings/industry-perspectives';

export const dynamic = 'force-static';

export function GET() {
  const articles = [...INDUSTRY_PERSPECTIVES_ARTICLES].sort(
    (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime(),
  );

  const lastBuildDate = new Date().toUTCString();

  const items = articles.map((a) => {
    const url = `${SITE.url}/blog/industry-perspectives/${a.slug}/index.html`;
    const pubDate = new Date(a.date).toUTCString();
    return `    <item>
      <title><![CDATA[${a.title}]]></title>
      <link>${url}</link>
      <guid isPermaLink="true">${url}</guid>
      <pubDate>${pubDate}</pubDate>
      <author>${SITE.email} (${SITE.name})</author>${a.description ? `\n      <description><![CDATA[${a.description}]]></description>` : ''}
    </item>`;
  });

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${SITE.name} - Industry Perspectives</title>
    <link>${SITE.url}/industry-perspectives</link>
    <description>AI industry analysis and perspectives by ${SITE.name}, AI Operating Partner at Fortino Capital.</description>
    <language>en</language>
    <lastBuildDate>${lastBuildDate}</lastBuildDate>
    <atom:link href="${SITE.url}/feed" rel="self" type="application/rss+xml" />
    <image>
      <url>${SITE.image}</url>
      <title>${SITE.name} - Industry Perspectives</title>
      <link>${SITE.url}</link>
    </image>
${items.join('\n')}
  </channel>
</rss>`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/rss+xml; charset=utf-8',
    },
  });
}
