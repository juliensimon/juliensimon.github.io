'use client';

import BlogListingPage from '@/components/ui/BlogListingPage';
import { MEDIUM_POSTS } from '@/data/blog-listings/medium';

export default function MediumBlogPostsPage() {
  return (
    <BlogListingPage
      title="Medium Articles"
      subtitle="200+ technical deep-dives and industry analysis"
      posts={MEDIUM_POSTS}
    />
  );
}
