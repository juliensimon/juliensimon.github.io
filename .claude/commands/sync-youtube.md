---
description: Sync new YouTube videos from @juliensimonfr to julien.org
---

Fetch the YouTube channel feed and detect new videos not yet on the website.

## Features

- **No API key required**: Uses the public YouTube Atom feed (~15 most recent videos)
- **Shorts excluded**: Automatically detects and skips YouTube Shorts (use `--include-shorts` to override)
- **Dual-write**: Creates pages in both `youtube/YYYY/` and `next-site/public/youtube/YYYY/`
- **Auto-updates**: Updates year index files (sorted by date, newest first), `youtube.ts` counts, and LATEST_UPDATES on the homepage
- **Deduplication**: Checks existing HTML files for YouTube video IDs to avoid duplicates

## Steps

1. Run the sync script in dry-run mode first:
   ```bash
   python3 scripts/sync_youtube.py --dry-run
   ```

2. Review the detected new videos and confirm they look correct

3. Run the actual sync:
   ```bash
   python3 scripts/sync_youtube.py
   ```

4. Build and verify:
   ```bash
   cd next-site && npm run build
   ```

5. Commit and push changes

## Options

| Flag | Description |
|------|-------------|
| `--dry-run` | Preview changes without modifying files |
| `--force` | Force re-sync of all videos from the feed |
| `--channel-id ID` | Use a specific channel ID (auto-resolved from @handle if omitted) |
| `--include-shorts` | Include YouTube Shorts (excluded by default) |

## What Gets Updated

| File | Change |
|------|--------|
| `youtube/YYYY/*.html` | New video HTML page (repo root) |
| `next-site/public/youtube/YYYY/*.html` | New video HTML page (Next.js public) |
| `youtube/YYYY/index.html` | Year index updated with new entry |
| `next-site/public/youtube/YYYY/index.html` | Year index updated with new entry |
| `next-site/src/data/youtube.ts` | VIDEO_YEARS count and totalVideos incremented |
| `next-site/src/app/HomeContent.tsx` | LATEST_UPDATES prepended with new videos |
