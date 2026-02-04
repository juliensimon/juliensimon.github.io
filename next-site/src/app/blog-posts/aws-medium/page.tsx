'use client';

import BlogListingPage from '@/components/ui/BlogListingPage';
import { AWS_MEDIUM_POSTS } from '@/data/blog-listings/aws-medium';

export default function AWSMediumPostsPage() {
  return (
    <BlogListingPage
      title="AWS Medium Posts"
      subtitle="Cross-published AWS technical content on Medium"
      posts={AWS_MEDIUM_POSTS}
    />
  );
}
