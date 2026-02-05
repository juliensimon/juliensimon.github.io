# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal website for Julien Simon (julien.org), an AI Operating Partner at Fortino Capital. The site is built with Next.js 15 and deployed to GitHub Pages via GitHub Actions.

## Development Commands

```bash
# Next.js development (primary workflow)
cd next-site
npm install        # Install dependencies
npm run dev        # Start dev server at http://localhost:3000
npm run build      # Build for production (outputs to next-site/out/)
npm run lint       # Run ESLint

# Legacy static content (for blog processing scripts)
cd scripts
python extract_blog_posts.py    # Extract posts from Atom feed
python download_images.py       # Download/convert images to WebP
python organize_by_year.py      # Organize into year folders
```

## Architecture

### Next.js Application (`/next-site/`)
The main site is a Next.js 15 app with static export (`output: 'export'`).

**Tech Stack:**
- Next.js 15 with App Router
- React 19
- TypeScript
- Tailwind CSS 4
- Framer Motion (animations)
- Leaflet (speaking map)

**Key Directories:**
- `src/app/` - App Router pages (each page has `page.tsx` + `*Content.tsx` client component)
- `src/components/` - Reusable UI and layout components
- `src/data/` - TypeScript data files for content (speaking, publications, youtube, etc.)
- `src/lib/` - Utilities (constants, metadata, structured-data)
- `public/` - Static assets (images, fonts)

**Data Files (`src/data/`):**
- `speaking.ts` - Speaking engagements by year
- `publications.ts` - Publication statistics
- `youtube.ts` - Video counts and data
- `experience.ts` - Career timeline
- `books.ts`, `code.ts`, `computers.ts` - Collection data
- `blog-listings/*.ts` - Blog post listings by platform (aws, huggingface, arcee, medium)

**Component Patterns:**
- Pages use server components (`page.tsx`) wrapping client components (`*Content.tsx`)
- UI components in `src/components/ui/` (ContentCard, MetricCard, YearCard, etc.)
- Layout components in `src/components/layout/` (Navigation, Footer)
- SEO via `src/components/seo/StructuredData.tsx` and `src/lib/metadata.ts`

### Legacy Content (`/blog/`, `/youtube/`)
Archived blog posts and video transcripts as self-contained HTML files:
- `blog/legacy-posts-and-images/` - Personal blog (2008-2016) organized by year
- `blog/aws-posts-and-images/`, `blog/huggingface-posts-and-images/` - Platform posts
- `youtube/YYYY/` - Video transcripts by year

### Python Scripts (`/scripts/`)
Content processing utilities for legacy blog posts:
- `extract_blog_posts.py` - Parse Atom feeds to HTML
- `download_images.py` - Download and convert to WebP
- `organize_by_year.py` - Structure posts by year
- `fix_image_references.py` - Clean up image references

## Deployment

GitHub Actions (`.github/workflows/deploy.yml`) automatically builds and deploys on push to master:
1. Runs `npm ci` and `npm run build` in `next-site/`
2. Uploads `next-site/out/` as artifact
3. Deploys to GitHub Pages

## Key Patterns

### Adding/Updating Content
1. Edit the relevant TypeScript data file in `next-site/src/data/`
2. For new pages, create `page.tsx` + `*Content.tsx` in `src/app/`
3. Update navigation in `src/lib/constants.ts` if needed
4. Run `npm run build` to verify static export works

### Updating Counts/Metrics
Global metrics in `next-site/src/lib/constants.ts`:
```typescript
export const METRICS = [
  { value: 350, suffix: '+', label: 'Technical Posts' },
  { value: 665, suffix: '+', label: 'Speaking Engagements' },
  // ...
];
```

### Adding Speaking Events
Edit `next-site/src/data/speaking.ts` - events are organized by year with location coordinates for the map.

### Adding YouTube Videos
1. Update counts in `next-site/src/data/youtube.ts`
2. For full transcripts, add HTML file to `youtube/YYYY/` folder (legacy format)
