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
npm run validate   # Data-consistency checks — also runs automatically as `prebuild`

# Python scripts - one-time setup
python3 -m venv venv && venv/bin/pip install -r scripts/requirements.txt

# Content sync (run from repo root)
venv/bin/python scripts/sync_substack.py --dry-run
venv/bin/python scripts/sync_youtube.py --dry-run

# Legacy static content (for blog processing scripts)
cd scripts
../venv/bin/python extract_blog_posts.py    # Extract posts from Atom feed
../venv/bin/python download_images.py       # Download/convert images to WebP
../venv/bin/python organize_by_year.py      # Organize into year folders
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

### The archive (`next-site/public/blog/`, `next-site/public/youtube/`)
The back catalogue: ~647 archived blog posts and ~477 video transcripts, as self-contained HTML
served straight from `public/`. This is the copy that ships.

- `next-site/public/blog/YYYY-MM-DD-slug/` - posts, one folder each
- `next-site/public/blog/industry-perspectives/` - the Substack pieces; the sibling `research/`
  workspace reads this exact directory as its `PUBLISHED_ARCHIVE`, so do not move or rename it
- `next-site/public/youtube/YYYY/` - transcripts by year

**`youtube/` at the repo root is a second, older copy** left from the pre-Next.js layout. Nothing
builds from it. Read either, hand-edit neither.

Listing metadata lives separately, in `next-site/src/data/blog-listings/*.ts` (one file per
platform: aws, aws-medium, huggingface, arcee, medium, legacy, industry-perspectives).

### Python Scripts (`/scripts/`)
**83 scripts, with their own `scripts/README.md` — read that rather than guessing.** Most are
one-shot migrations that have already run; re-running one is rarely what you want. The two in
routine use are the content syncs:

```bash
venv/bin/python scripts/sync_substack.py --dry-run
venv/bin/python scripts/sync_youtube.py --dry-run
```

A third, `scripts/sync_podcast.py` (stdlib only, any `python3`), adds a "Listen" audio player to
the Industry Perspectives articles that have an episode of The AI Realist podcast. The podcast is
produced by a separate pipeline in `../research/podcast/`; this script shares no code with it and
reads only its public feed, `https://podcast.julien.org/feed.xml`. The player sits between
`<!-- podcast:start -->` and `<!-- podcast:end -->`, before `<div class="article-content">` and never
inside it, because `research/` reads everything inside that div as the text of the piece.
`sync_youtube.py` skips podcast episodes (`is_podcast_episode`): they show up in the channel's
video list, and each is the audio of an article that already has its page.

Since 2026-10-07 the same run puts the podcast on the site in three more places, all from the feed
and none edited by hand:
- a schema.org `PodcastEpisode` block inside each player, so a search engine knows the article has
  an audio version;
- `next-site/src/data/podcast-episodes.json`, the episode list behind the `/podcast` page
  (`src/app/podcast/`, show constants in `src/data/podcast.ts`, `PodcastSeries` schema in
  `src/lib/structured-data.ts`). The page is the show's home on the web: `podcast.julien.org/`
  itself serves only the feed and the files;
- the "## Podcast: The AI Realist" section of `llms.txt` (five latest episodes) and `llms-full.txt`
  (all), replaced in place on each run.

The `/podcast` page carries the two platform badges, in `next-site/public/assets/badges/`. Apple's
is its own artwork from `toolbox.marketingtools.apple.com`, unmodified: at least 30 pixels high,
clear space of a tenth of its height, below or beside the copy, never next to the Apple Podcasts
icon (Apple Podcasts Identity Guidelines, read 2026-10-07). Spotify publishes no badge file: the
button is its official green icon on black with "Listen on Spotify", which its design guidelines
allow (developer.spotify.com/documentation/design, read 2026-10-07). Do not redraw either. The
homepage row has a "Podcast" button to `/podcast`; it is not in `SOCIAL_LINKS`, because that list is
also the person's `sameAs` in the structured data and a show is not a profile.

Only an https address on `podcast.julien.org` is ever written (`.mp3` for audio, `.jpg` for an
image), and feed text goes into the structured data with `<` escaped. `--selftest` covers all of it.

`next-site/cleanup.py` is **not** one of these. It rewrites every HTML file under `public/blog/`
and `public/youtube/` in place, with no dry-run and no confirmation, and its `BASE_DIR` currently
points at a directory that no longer exists — so today it is inert. Repointing it arms a bulk
mutation over ~1,124 live files. Do not fix that path casually.

## Deployment

GitHub Actions (`.github/workflows/deploy.yml`) automatically builds and deploys on push to master:
1. Runs `npm ci` and `npm run build` in `next-site/`
2. Uploads `next-site/out/` as artifact
3. Deploys to GitHub Pages

`npm run build` is wrapped by two hooks in `next-site/package.json`, and both can fail a deploy:

- **`prebuild`** runs `scripts/validate-counts.mjs`, which checks the claimed counts against the
  filesystem — YouTube videos, blog-post array lengths, speaking-year totals against `totalEvents`.
  **A metric edited in `src/lib/constants.ts` without the matching content fails the build here.**
  That is the repository's one real gate; run `npm run validate` before pushing.
- **`postbuild`** runs image optimization, `scripts/generate-redirects.mjs`, then
  `python3 ../scripts/generate_legacy_sitemap.py`. That last step couples the Node build to a
  working Python 3 at the repo root, so a broken venv breaks the deploy in a step that looks like
  a JavaScript failure.

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
