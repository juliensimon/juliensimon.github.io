'use client';

import BlogListingPage from '@/components/ui/BlogListingPage';
import { HUGGINGFACE_POSTS } from '@/data/blog-listings/huggingface';

export default function HuggingFaceBlogPostsPage() {
  return (
    <BlogListingPage
      title="Hugging Face Blog Posts"
      subtitle="25+ articles on transformer models and the HF ecosystem"
      posts={HUGGINGFACE_POSTS}
    />
  );
}
