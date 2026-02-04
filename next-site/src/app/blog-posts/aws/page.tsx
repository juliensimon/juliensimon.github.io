'use client';

import BlogListingPage from '@/components/ui/BlogListingPage';
import { AWS_POSTS } from '@/data/blog-listings/aws';

export default function AWSBlogPostsPage() {
  return (
    <BlogListingPage
      title="AWS Blog Posts"
      subtitle="68+ technical articles on AWS AI/ML services"
      posts={AWS_POSTS}
    />
  );
}
