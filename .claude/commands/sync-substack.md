---
description: Sync new posts from julsimon.substack.com to julien.org
---

Fetch the Substack RSS feed and detect new posts not yet on the website.

## Features

- **Full content extraction**: Downloads complete article content (not just excerpts)
- **Image downloading**: Downloads images and converts to WebP format
- **HTML cleaning**: Removes Substack-specific markup, tracking, and subscription elements
- **Read time calculation**: Calculates actual read time from word count

## Steps

1. Run the sync script in dry-run mode first:
   ```bash
   python3 scripts/sync_substack.py --dry-run
   ```

2. Review the detected new posts and confirm they look correct

3. Run the actual sync:
   ```bash
   python3 scripts/sync_substack.py
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
| `--force` | Force re-sync of all posts, ignoring existing files |
| `--update-existing` | Re-process existing articles to update content and download images |

## Output Structure

Articles are saved to:
```
next-site/public/blog/industry-perspectives/
  YYYY-MM-DD_post-slug/
    index.html      # Full article with cleaned HTML
    metadata.json   # Post metadata including image count
    image-01.webp   # Downloaded images (WebP format)
    image-02.webp
    ...
```

## Re-processing Existing Posts

To update old posts with full content and images:
```bash
python3 scripts/sync_substack.py --update-existing
```

This will re-process all posts, downloading images and cleaning HTML for posts that previously only had excerpts.
