# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal website for Julien Simon (julien.org), an AI Operating Partner at Fortino Capital. This is a static site hosted on GitHub Pages with no build system - HTML files are served directly.

## Development Commands

```bash
# Start local development server
python -m http.server 8000
# OR
npx serve .

# View site at http://localhost:8000
```

No build, lint, or test commands - this is a static HTML site.

## Architecture

### Content Structure
- **Root HTML pages**: Main site pages (`index.html`, `experience.html`, `speaking.html`, `publications.html`, `youtube.html`, `books.html`, `computers.html`, `code.html`)
- **Speaking archives**: Year-specific pages (`speaking-2016.html` through `speaking-2024.html`)
- **Blog platform archives**: Platform-specific listing pages (`aws-blog-posts.html`, `huggingface-blog-posts.html`, `arcee-blog-posts.html`, `medium-blog-posts.html`, `aws-medium-posts.html`)

### Blog Content (`/blog/`)
Contains migrated blog posts organized by platform:
- `legacy-posts-and-images/` - Old personal blog posts (2008-2016) organized by year
- `aws-posts-and-images/` - AWS blog posts
- `huggingface-posts-and-images/` - Hugging Face blog posts
- `arcee-posts/` - Arcee AI posts
- `aws-medium-posts-and-images/` - AWS Medium posts

Each blog post is a self-contained HTML file with embedded CSS - no external dependencies.

### Python Scripts (`/scripts/`)
56 utility scripts for content processing, primarily:
- **Blog extraction**: `extract_blog_posts.py` - Parse Atom feeds to HTML
- **Image processing**: `download_images.py` - Download and convert to WebP
- **Organization**: `organize_by_year.py` - Structure posts by year
- **SEO**: Various `add_seo_*.py` and `comprehensive_seo_update.py` scripts
- **Styling**: `apply_minimal_styling.py`, `apply_modern_styling.py`

Scripts require Python 3.6+ with dependencies from `requirements.txt` (ML libraries for analysis) or `simple_requirements.txt` (core libraries only).

### Frontend Assets
- `/css/` - Stylesheets (`styles.css`, `critical.css`, `minimal-blog-styles.css`)
- `/js/` - JavaScript (`main.js`, `performance-monitor.js`, `enhanced-knowledge-graph.js`)
- `/assets/` - Images and media
- `sw.js` - Service worker for PWA/offline support
- `manifest.json` - PWA manifest

### SEO/Discovery Files
- `sitemap.xml`, `sitemap-index.xml` - Main sitemaps
- `sitemap-blog.xml`, `sitemap-speaking.xml`, `sitemap-videos.xml` - Content-specific sitemaps
- `robots.txt` - Crawler instructions
- `llms.txt` - AI/LLM content discovery file
- `feed.xml` - RSS feed

## Key Patterns

### Adding/Updating Content
1. Edit the relevant HTML file directly
2. Update `sitemap.xml` with new/changed pages
3. If adding a new page, include standard meta tags and link in navigation

### Blog Post Processing Workflow
When processing legacy blog content:
```bash
cd scripts
python extract_blog_posts.py    # Extract from Atom feed
python download_images.py       # Download/convert images to WebP
python organize_by_year.py      # Organize into year folders
python fix_image_references.py  # Clean up image references
```

### Image Naming Convention
Blog images: `YYYY-MM-DD-post-title-image-01.webp`

### YouTube Video Content (`/youtube/`)
Videos are organized by year in folders (`youtube/2025/`, `youtube/2026/`, etc.):
- Each year folder contains individual video HTML files with embedded transcripts
- Each year folder has an `index.html` listing all videos for that year
- Video files follow naming: `YYYYMMDD_Video_Title_With_Underscores.html`

### Adding New Video Transcripts
When adding new video transcript pages:
1. Move the HTML file to the correct year folder (`youtube/YYYY/`)
2. Create year folder and `index.html` if it's a new year (use existing year index as template)
3. Update the year's `index.html`:
   - Add video entry at the top (most recent first)
   - Update the video count in the subtitle
4. Update `youtube.html`:
   - Update total video count in stats section (`▶️ <span>X+ videos</span>`)
   - Update total count in the paragraph (`<strong>Total: X videos</strong>`)
   - Update years count if new year added (`across X years of content`)
   - Add year card if new year (at top of years-grid)
   - Update existing year card video count if needed
5. Update `index.html` "Latest Updates" section:
   - Add new videos at the top (most recent first)
   - Keep exactly 5 items total (remove oldest entries)

### Video Counters to Update (Checklist)
When adding videos, these counters must stay synchronized:
- [ ] `youtube.html`: Stats section video count
- [ ] `youtube.html`: Paragraph total video count
- [ ] `youtube.html`: Years of content count (if new year)
- [ ] `youtube.html`: Year card video count
- [ ] `youtube/YYYY/index.html`: Subtitle video count
- [ ] `index.html`: Latest Updates section (5 items max)
