---
description: Sync new YouTube videos from @juliensimonfr to julien.org
---

Fetch the YouTube channel feed and detect new videos not yet on the website.

## Features

- **No API key required**: Uses the public YouTube Atom feed (~15 most recent videos)
- **Shorts excluded**: Automatically detects and skips YouTube Shorts (use `--include-shorts` to override)
- **Automatic transcripts**: Downloads audio via yt-dlp, transcribes with distil-whisper, and cleans up AI terminology
- **Dual-write**: Creates pages in both `youtube/YYYY/` and `next-site/public/youtube/YYYY/`
- **Auto-updates**: Updates year index files (sorted by date, newest first), `youtube.ts` counts, and LATEST_UPDATES on the homepage
- **Deduplication**: Checks existing HTML files for YouTube video IDs to avoid duplicates
- **Backfill**: Can add transcripts to existing videos that are missing them

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

6. Monitor the GitHub Actions deployment:
   ```bash
   gh run list --repo juliensimon/juliensimon.github.io --limit 1
   ```
   Then watch it until completion:
   ```bash
   gh run watch <run-id> --repo juliensimon/juliensimon.github.io --exit-status
   ```
   If the deployment fails, investigate the logs with:
   ```bash
   gh run view <run-id> --repo juliensimon/juliensimon.github.io --log-failed
   ```

## Options

| Flag | Description |
|------|-------------|
| `--dry-run` | Preview changes without modifying files |
| `--force` | Force re-sync of all videos from the feed |
| `--channel-id ID` | Use a specific channel ID (auto-resolved from @handle if omitted) |
| `--include-shorts` | Include YouTube Shorts (excluded by default) |
| `--no-transcript` | Skip transcript generation (create pages without transcripts) |
| `--backfill-transcripts` | Find existing videos without transcripts and add them |
| `--whisper-model MODEL` | Whisper model for transcription (default: `distil-whisper/distil-large-v3`) |

## Transcript Pipeline

New videos automatically get transcripts via this pipeline:

1. **Audio extraction**: `yt-dlp` downloads audio as 16kHz mono WAV
2. **Transcription**: `distil-whisper/distil-large-v3` (runs on MPS/Apple Silicon when available)
3. **Text cleanup**: Fixes common speech-to-text errors:
   - RC/Arsy → Arcee, Lama → Llama, hugging face → Hugging Face
   - Sagemaker → SageMaker, pytorch → PyTorch, open vino → OpenVINO
   - Deep Seek → DeepSeek, Tensor flow → TensorFlow, Open AI → OpenAI
4. **Paragraph formatting**: Breaks transcript into readable paragraphs (~5 sentences each)

### Backfilling Existing Videos

To add transcripts to existing videos that are missing them:
```bash
# Preview which videos need transcripts
python3 scripts/sync_youtube.py --backfill-transcripts --dry-run

# Run the backfill
python3 scripts/sync_youtube.py --backfill-transcripts
```

### Requirements

- `yt-dlp` (installed via Homebrew or pip)
- `ffmpeg` (installed via Homebrew)
- `torch` and `transformers` Python packages

## What Gets Updated

| File | Change |
|------|--------|
| `youtube/YYYY/*.html` | New video HTML page with transcript (repo root) |
| `next-site/public/youtube/YYYY/*.html` | New video HTML page with transcript (Next.js public) |
| `youtube/YYYY/index.html` | Year index updated with new entry |
| `next-site/public/youtube/YYYY/index.html` | Year index updated with new entry |
| `next-site/src/data/youtube.ts` | VIDEO_YEARS count and totalVideos incremented |
| `next-site/src/app/HomeContent.tsx` | LATEST_UPDATES prepended with new videos |
