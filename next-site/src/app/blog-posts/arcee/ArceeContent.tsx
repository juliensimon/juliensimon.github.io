'use client';

import BlogListingPage from '@/components/ui/BlogListingPage';
import { ARCEE_POSTS } from '@/data/blog-listings/arcee';

export default function ArceeContent() {
  return (
    <BlogListingPage
      title="Arcee AI Blog Posts"
      subtitle="Articles on Small Language Models and practical AI deployment"
      posts={ARCEE_POSTS}
    />
  );
}
