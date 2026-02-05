import { notFound } from 'next/navigation';
import { Metadata } from 'next';
import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import { SITE } from '@/lib/constants';
import BlogListingPage from '@/components/ui/BlogListingPage';
import { BLOG_CATEGORIES, BLOG_CATEGORY_SLUGS } from '@/data/blog-categories';

interface Props {
  params: Promise<{ category: string }>;
}

export async function generateStaticParams() {
  return BLOG_CATEGORY_SLUGS.map((category) => ({ category }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { category } = await params;
  const config = BLOG_CATEGORIES[category];
  if (!config) return {};

  return buildMetadata({
    title: config.title,
    description: config.description,
    path: `/blog-posts/${category}`,
    keywords: config.keywords,
  });
}

export default async function BlogCategoryPage({ params }: Props) {
  const { category } = await params;
  const config = BLOG_CATEGORIES[category];

  if (!config) {
    notFound();
  }

  return (
    <>
      <StructuredData
        data={breadcrumbSchema([
          { name: 'Home', url: SITE.url },
          { name: 'Publications', url: `${SITE.url}/publications` },
          { name: config.title, url: `${SITE.url}/blog-posts/${category}` },
        ])}
      />
      <BlogListingPage
        title={config.title}
        subtitle={config.subtitle}
        posts={config.posts}
      />
    </>
  );
}
