#!/usr/bin/env python3
"""
Sync YouTube videos to julien.org

Fetches the latest videos from the YouTube channel feed
and creates the appropriate HTML files on the website.

Usage:
    python sync_youtube.py --dry-run  # Preview changes
    python sync_youtube.py            # Apply changes
"""

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import NamedTuple

import requests
import xml.etree.ElementTree as ET

# YouTube channel
CHANNEL_HANDLE = "juliensimonfr"
CHANNEL_ID = "UCVonoXm3SI_Q0ZNHd5JPawA"

# Paths
REPO_ROOT = Path(__file__).parent.parent
BASE = REPO_ROOT / "next-site"
PUBLIC = BASE / "public"
SRC = BASE / "src"
REPO_YOUTUBE = REPO_ROOT / "youtube"

# Namespaces for YouTube Atom feed
NS = {
    'atom': 'http://www.w3.org/2005/Atom',
    'yt': 'http://www.youtube.com/xml/schemas/2015',
    'media': 'http://search.yahoo.com/mrss/',
}


class VideoItem(NamedTuple):
    """Parsed YouTube video entry."""
    video_id: str
    title: str
    published: datetime
    description: str


def resolve_channel_id(handle: str) -> str:
    """Resolve a YouTube @handle to a channel ID by fetching the channel page."""
    url = f"https://www.youtube.com/@{handle}"
    print(f"Resolving channel ID for @{handle}...")
    response = requests.get(url, timeout=15, headers={
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0'
        ),
        'Accept-Language': 'en-US,en;q=0.9',
    })
    response.raise_for_status()

    # Extract channel ID from page source (broad match)
    match = re.search(r'(UC[a-zA-Z0-9_-]{22})', response.text)
    if match:
        return match.group(1)

    raise ValueError(f"Could not resolve channel ID for @{handle}")


def fetch_feed(channel_id: str) -> list[VideoItem]:
    """Fetch and parse the YouTube Atom feed (returns ~15 most recent videos)."""
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    print(f"Fetching {url}...")
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    videos = []

    for entry in root.findall('atom:entry', NS):
        video_id = entry.findtext('yt:videoId', '', NS)
        title = entry.findtext('atom:title', '', NS).strip()
        pub_str = entry.findtext('atom:published', '', NS)

        # Get description from media:group/media:description
        media_group = entry.find('media:group', NS)
        description = ''
        if media_group is not None:
            description = media_group.findtext(
                'media:description', '', NS
            ).strip()

        # Parse ISO 8601 date
        try:
            published = datetime.fromisoformat(pub_str.replace('Z', '+00:00'))
            published = published.replace(tzinfo=None)
        except ValueError:
            published = datetime.now()

        if video_id and title:
            videos.append(VideoItem(
                video_id=video_id,
                title=title,
                published=published,
                description=description,
            ))

    return videos


def is_short(video_id: str) -> bool:
    """Check if a video is a YouTube Short by probing the /shorts/ URL.
    If /shorts/<id> stays on /shorts/, it's a Short. If it redirects to
    /watch, it's a regular video."""
    try:
        resp = requests.head(
            f"https://www.youtube.com/shorts/{video_id}",
            allow_redirects=True,
            timeout=10,
            headers={
                'User-Agent': (
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                    'AppleWebKit/537.36'
                ),
            },
        )
        return '/shorts/' in resp.url
    except requests.RequestException:
        return False


def filter_shorts(videos: list[VideoItem]) -> list[VideoItem]:
    """Remove YouTube Shorts from the video list."""
    filtered = []
    for video in videos:
        if is_short(video.video_id):
            print(f"  Skipping Short: {video.title}")
        else:
            filtered.append(video)
    return filtered


def title_to_filename(title: str) -> str:
    """Convert title to filename format (Title_Words_Here)."""
    clean = re.sub(r'[^\w\s-]', '', title)
    return re.sub(r'\s+', '_', clean.strip())


def is_video_existing(year: int, youtube_id: str) -> bool:
    """Check if a video with this YouTube ID already exists on the site."""
    # Check both locations
    for base_dir in [PUBLIC / "youtube", REPO_YOUTUBE]:
        year_dir = base_dir / str(year)
        if not year_dir.exists():
            continue
        for html_file in year_dir.glob("*.html"):
            if html_file.name == "index.html":
                continue
            try:
                content = html_file.read_text(encoding='utf-8')
                if youtube_id in content:
                    return True
            except Exception:
                continue
    return False


def is_substack_content(video: VideoItem) -> bool:
    """Check if a video's description indicates it's a Substack blog post
    rather than a genuine YouTube video. Substack posts sometimes appear
    in YouTube feeds when they contain embedded videos."""
    desc_lower = video.description.lower()
    substack_signals = [
        'airealist.ai',
        'read full post on substack',
        'substack.com',
    ]
    return any(signal in desc_lower for signal in substack_signals)


# ---------------------------------------------------------------------------
# Transcript generation
# ---------------------------------------------------------------------------

# Text replacements applied to transcripts (case-insensitive matching,
# replaced with the exact casing given in the value).
TRANSCRIPT_REPLACEMENTS: list[tuple[str, str]] = [
    # Standalone pronoun "i"
    (r'\bi\b(?=\s[a-z]|\s[A-Z]|\')', 'I'),
    # Arcee AI — Whisper hears "RC", "Arsy", "rcai", "RC AI", etc.
    (r'\brcai\b', 'Arcee AI'),
    (r'\bRC AI\b', 'Arcee AI'),
    (r'\bRC\b', 'Arcee'),
    (r'\bArsy\b', 'Arcee'),
    (r'\bArcee\.ai\b', 'Arcee AI'),
    # LLaMA / Llama
    (r'\bLama\b', 'Llama'),
    (r'\bllama\b', 'Llama'),
    # Hugging Face
    (r'\bhugging face\b', 'Hugging Face'),
    (r'\bHuggingface\b', 'Hugging Face'),
    (r'\bhuggingface\b', 'Hugging Face'),
    # AWS services
    (r'\bSagemaker\b', 'SageMaker'),
    (r'\bsagemaker\b', 'SageMaker'),
    (r'\bBedrock\b', 'Bedrock'),
    # Common AI terms
    (r'\bGPT\b', 'GPT'),
    (r'\bOpen AI\b', 'OpenAI'),
    (r'\bopen AI\b', 'OpenAI'),
    (r'\bPytorch\b', 'PyTorch'),
    (r'\bpytorch\b', 'PyTorch'),
    (r'\bTensor flow\b', 'TensorFlow'),
    (r'\btensor flow\b', 'TensorFlow'),
    (r'\btensorflow\b', 'TensorFlow'),
    (r'\bOpen Vino\b', 'OpenVINO'),
    (r'\bopen vino\b', 'OpenVINO'),
    (r'\bopenvino\b', 'OpenVINO'),
    (r'\bDeep Seek\b', 'DeepSeek'),
    (r'\bdeep seek\b', 'DeepSeek'),
    (r'\bGGUF\b', 'GGUF'),
    (r'\bgguf\b', 'GGUF'),
    (r'\bMLX\b', 'MLX'),
    # Name
    (r'\bJulian\b', 'Julien'),
    # Versioning
    (r'\bapache 2 zero\b', 'Apache 2.0'),
    (r'\bApache 2 zero\b', 'Apache 2.0'),
    (r'\bapache 2\.0\b', 'Apache 2.0'),
]

# Whisper model for transcription
DEFAULT_WHISPER_MODEL = "distil-whisper/distil-large-v3"

# Lazy-loaded pipeline
_asr_pipeline = None


_whisper_model = None
_whisper_processor = None
_whisper_device = None
_whisper_dtype = None


def _load_whisper(model_id: str = DEFAULT_WHISPER_MODEL):
    """Lazy-load the Whisper model and processor."""
    global _whisper_model, _whisper_processor, _whisper_device, _whisper_dtype
    if _whisper_model is not None:
        return

    print(f"  Loading transcription model: {model_id}")
    import torch
    from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor

    _whisper_device = "mps" if torch.backends.mps.is_available() else "cpu"
    _whisper_dtype = torch.float16 if _whisper_device != "cpu" else torch.float32
    print(f"  Device: {_whisper_device}, dtype: {_whisper_dtype}")

    _whisper_model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, dtype=_whisper_dtype, low_cpu_mem_usage=True,
    )
    _whisper_model.to(_whisper_device)
    _whisper_processor = AutoProcessor.from_pretrained(model_id)

    # Suppress the specific MPS warning about cumsum with int64
    import warnings
    warnings.filterwarnings("ignore", message=".*cumsum_out_mps.*")


def _get_audio_duration(audio_path: str) -> float:
    """Get audio duration in seconds from a WAV file."""
    import wave
    try:
        with wave.open(audio_path) as w:
            return w.getnframes() / w.getframerate()
    except Exception:
        return 0.0


def download_audio(video_id: str, output_dir: str) -> str | None:
    """Download audio from a YouTube video using yt-dlp.
    Returns path to the downloaded WAV file, or None on failure."""
    output_path = os.path.join(output_dir, f"{video_id}.wav")
    cmd = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "wav",
        "--postprocessor-args", "ffmpeg:-ar 16000 -ac 1",
        "--output", os.path.join(output_dir, f"{video_id}.%(ext)s"),
        "--no-playlist",
        "--no-warnings",
        "--progress",
        "--newline",
        f"https://www.youtube.com/watch?v={video_id}",
    ]
    try:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        )
        for line in proc.stdout:
            line = line.strip()
            # Show download progress lines
            if '[download]' in line and '%' in line:
                print(f"\r  {line}", end='', flush=True)
            elif '[ExtractAudio]' in line:
                print(f"\n  {line}")
        proc.wait(timeout=300)
        print()  # newline after progress

        if proc.returncode != 0:
            print(f"  Warning: yt-dlp exited with code {proc.returncode}")
            return None

        if os.path.exists(output_path):
            dur = _get_audio_duration(output_path)
            size_mb = os.path.getsize(output_path) / 1024 / 1024
            print(f"  Audio: {dur/60:.1f} min, {size_mb:.0f} MB")
            return output_path
        # yt-dlp may use a different intermediate extension
        for f in Path(output_dir).glob(f"{video_id}.*"):
            if f.suffix == ".wav":
                return str(f)
        print(f"  Warning: audio file not found after download for {video_id}")
        return None
    except (subprocess.TimeoutExpired, OSError) as e:
        print(f"  Warning: failed to download audio for {video_id}: {e}")
        return None


def transcribe_audio(audio_path: str, model_id: str = DEFAULT_WHISPER_MODEL) -> str:
    """Transcribe audio by chunking into 30s segments and using model.generate().

    This avoids the pipeline's chunk_length_s issues with long audio while
    still providing reliable transcription for videos of any length."""
    import time
    import torch
    import librosa

    _load_whisper(model_id)
    duration = _get_audio_duration(audio_path)
    dur_str = f"{duration/60:.1f} min" if duration else "unknown length"

    # Load full audio
    print(f"  Loading audio ({dur_str})...")
    audio_array, sr = librosa.load(audio_path, sr=16000)

    # Chunk into 30-second segments (Whisper's native window)
    chunk_samples = 30 * 16000  # 30s at 16kHz
    chunks = []
    for start_sample in range(0, len(audio_array), chunk_samples):
        chunk = audio_array[start_sample:start_sample + chunk_samples]
        chunks.append(chunk)

    total_chunks = len(chunks)
    print(f"  Transcribing {total_chunks} chunks ({dur_str})...")
    start = time.time()

    transcripts = []
    for i, chunk in enumerate(chunks):
        input_features = _whisper_processor(
            chunk, sampling_rate=16000, return_tensors="pt",
        ).input_features.to(_whisper_device, dtype=_whisper_dtype)

        with torch.no_grad():
            predicted_ids = _whisper_model.generate(
                input_features,
                max_new_tokens=440,
                language="en",
            )
        text = _whisper_processor.batch_decode(
            predicted_ids, skip_special_tokens=True,
        )[0].strip()
        transcripts.append(text)

        elapsed = time.time() - start
        pct = (i + 1) / total_chunks * 100
        print(f"\r  [{i+1}/{total_chunks}] {pct:.0f}% — {elapsed:.0f}s elapsed", end='', flush=True)

    elapsed = time.time() - start
    speed = duration / elapsed if elapsed > 0 else 0
    print(f"\r  Transcribed {dur_str} in {elapsed:.0f}s ({speed:.1f}x realtime)" + " " * 30)

    return " ".join(transcripts)


def clean_transcript(text: str) -> str:
    """Apply text replacements and clean up transcript."""
    # Fix Whisper hallucination artifacts at chunk boundaries
    text = re.sub(r'!{2,}', '', text)            # !!!! -> remove
    text = re.sub(r'\.{3,}', '...', text)        # normalize ellipses
    text = re.sub(r'!\s*\.', '.', text)           # !. -> .
    text = re.sub(r'\.\s*!', '.', text)           # .! -> .
    text = re.sub(r'to\.\.\.m!?\s*', '', text)    # "to...m!" artifact
    # Remove sequences of short exclamatory fragments (Whisper chunk-boundary noise)
    text = re.sub(r'(?:\w{1,4}!\s*){2,}', '', text)  # "it! Is! and!" patterns
    text = re.sub(r'(?<![a-zA-Z])!\s*', '', text) # isolated ! not after words

    for pattern, replacement in TRANSCRIPT_REPLACEMENTS:
        text = re.sub(pattern, replacement, text)

    # Clean up whitespace
    text = re.sub(r'  +', ' ', text)
    text = text.strip()

    # Capitalize first letter of text
    if text and text[0].islower():
        text = text[0].upper() + text[1:]

    # Capitalize after sentence-ending punctuation
    text = re.sub(r'([.!?]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), text)

    # Break into paragraphs roughly every 5 sentences for readability
    sentences = re.split(r'(?<=[.!?])\s+', text)
    paragraphs = []
    current = []
    for sentence in sentences:
        current.append(sentence)
        if len(current) >= 5:
            paragraphs.append(' '.join(current))
            current = []
    if current:
        paragraphs.append(' '.join(current))

    return '\n\n'.join(paragraphs)


def generate_transcript(
    video_id: str,
    model_id: str = DEFAULT_WHISPER_MODEL,
) -> str | None:
    """Full pipeline: download audio, transcribe, clean up.
    Returns cleaned transcript text or None on failure."""
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"  Downloading audio for {video_id}...")
        audio_path = download_audio(video_id, tmpdir)
        if not audio_path:
            return None

        print(f"  Transcribing...")
        raw_text = transcribe_audio(audio_path, model_id)
        if not raw_text:
            print(f"  Warning: empty transcript for {video_id}")
            return None

        transcript = clean_transcript(raw_text)
        word_count = len(transcript.split())
        print(f"  Transcript: {word_count} words")
        return transcript


def get_new_videos(
    videos: list[VideoItem], force: bool = False,
) -> list[VideoItem]:
    """Filter to only new videos not yet on the site."""
    if force:
        return videos

    new_videos = []
    for video in videos:
        if is_substack_content(video):
            print(f"  Skipping Substack content: {video.title}")
            continue
        year = video.published.year
        if not is_video_existing(year, video.video_id):
            new_videos.append(video)

    return new_videos


def create_video_page(
    video: VideoItem,
    dry_run: bool,
    transcript: str | None = None,
) -> Path:
    """Create a video HTML page, optionally with a transcript."""
    year = video.published.year
    date_str = video.published.strftime('%Y%m%d')
    filename = f"{date_str}_{title_to_filename(video.title)}"
    display_date = video.published.strftime('%B %d, %Y').replace(' 0', ' ')

    # Truncate description for display if very long
    description = video.description
    if len(description) > 2000:
        description = description[:2000] + '...'

    # Build transcript HTML section
    transcript_html = ''
    if transcript:
        # Convert paragraphs to HTML
        paragraphs = transcript.split('\n\n')
        transcript_body = '\n'.join(
            f'            {html.escape(p)}' if i == 0
            else f'\n{html.escape(p)}'
            for i, p in enumerate(paragraphs)
        )
        transcript_html = f'''
        <div class="transcript">
<h2>Transcript</h2>
{transcript_body}</div>'''

    html_content = f'''<!DOCTYPE html><html lang="en"><head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(video.title)}</title>
    <meta name="description" content="{html.escape(video.title)} - YouTube video by Julien Simon">
    <meta property="og:title" content="{html.escape(video.title)}">
    <meta property="og:type" content="video.other">
    <meta property="og:url" content="https://www.julien.org/youtube/{year}/{date_str}_{title_to_filename(video.title)}.html">
    <link rel="canonical" href="https://www.julien.org/youtube/{year}/{date_str}_{title_to_filename(video.title)}.html">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
    <link rel="icon" type="image/x-icon" href="/assets/favicon.ico">
    <link rel="stylesheet" href="../style.css">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{html.escape(video.title)}">
    <meta name="twitter:creator" content="@julsimon">
    <script defer src="https://cloud.umami.is/script.js" data-website-id="27550dad-d418-4f5d-ad1b-dab573da1020"></script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": "{html.escape(video.title).replace(chr(34), '&quot;')}",
        "description": "{html.escape(video.title)} - YouTube video by Julien Simon",
        "uploadDate": "{video.published.strftime('%Y-%m-%d')}",
        "embedUrl": "https://www.youtube.com/embed/{video.video_id}",
        "thumbnailUrl": "https://img.youtube.com/vi/{video.video_id}/maxresdefault.jpg",
        "author": {{ "@id": "https://www.julien.org/#person" }}
    }}
    </script>
</head>
<body>
    <div class="container">
        <h1>{html.escape(video.title)}</h1>
        <div class="date">{display_date}</div>

        <div class="video-container">
            <iframe src="https://www.youtube.com/embed/{video.video_id}" allowfullscreen="" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture">
            </iframe>
        </div>

        <div class="description">{html.escape(description)}</div>
{transcript_html}
        <div class="tags">
            <h2>Tags</h2>
            <span class="tag">AI</span><span class="tag">Machine Learning</span><span class="tag">Technology</span>
        </div>

        <div class="links">
            <a href="index.html">&larr; Back to {year} Videos</a>
            <a href="/youtube-videos">&larr; Back to YouTube Overview</a>
        </div>
    </div>


</body></html>'''

    # Write to both locations
    for base_dir in [PUBLIC / "youtube", REPO_YOUTUBE]:
        year_dir = base_dir / str(year)
        filepath = year_dir / f"{filename}.html"
        if not dry_run:
            year_dir.mkdir(parents=True, exist_ok=True)
            filepath.write_text(html_content, encoding='utf-8')

    return PUBLIC / "youtube" / str(year) / f"{filename}.html"


def _sort_video_entries(content: str) -> str:
    """Sort video-item entries in an index page by date (newest first).

    Splits the video-list div into individual video-item blocks,
    sorts them by the YYYYMMDD prefix in their href filename,
    and reassembles the HTML.
    """
    marker = '<div class="video-list">'
    end_marker = '<div class="links">'

    start = content.find(marker)
    end = content.find(end_marker)
    if start == -1 or end == -1:
        return content

    before = content[:start + len(marker)]
    after = content[end:]
    list_html = content[start + len(marker):end]

    # Split into individual items at each <div class="video-item"> boundary
    parts = re.split(r'(?=<div class="video-item">)', list_html.strip())
    items = [p.strip() for p in parts if p.strip()]

    if len(items) < 2:
        return content

    # Sort by date extracted from href filename (YYYYMMDD prefix)
    def sort_key(item_html: str) -> str:
        m = re.search(r'href="(\d{8})_', item_html)
        return m.group(1) if m else '00000000'

    items.sort(key=sort_key, reverse=True)

    return before + '\n' + '\n'.join(items) + '\n' + after


def update_year_index(year: int, video: VideoItem, dry_run: bool) -> bool:
    """Update the youtube/YYYY/index.html with a new video entry.
    Returns True if the entry was added."""
    date_str = video.published.strftime('%Y%m%d')
    filename = f"{date_str}_{title_to_filename(video.title)}"
    display_date = video.published.strftime('%B %-d, %Y')

    added = False
    for base_dir in [PUBLIC / "youtube", REPO_YOUTUBE]:
        index_path = base_dir / str(year) / "index.html"
        if not index_path.exists():
            continue

        content = index_path.read_text(encoding='utf-8')

        # Skip if already present
        if video.video_id in content or f'href="{filename}.html"' in content:
            continue

        # Update video count in subtitle
        count_match = re.search(r'(\d+) videos? from', content)
        current_count = int(count_match.group(1)) if count_match else 0
        new_count = current_count + 1
        new_subtitle = (
            f'{new_count} video{"s" if new_count != 1 else ""} from {year}'
        )
        content = re.sub(
            r'<div class="subtitle">[^<]+</div>',
            f'<div class="subtitle">{new_subtitle}</div>',
            content,
        )

        # Create new video entry
        new_entry = (
            f'<div class="video-item">\n'
            f'<a class="video-title" href="{filename}.html">'
            f'{html.escape(video.title)}</a>\n'
            f'<div class="video-date">{display_date}</div>'
            f'<div class="video-tags">'
            f'<span class="video-tag">AI</span>'
            f'<span class="video-tag">Tutorial</span>'
            f'</div>\n'
            f'</div>\n'
        )

        # Insert after video-list opening tag
        content = re.sub(
            r'(<div class="video-list">)\n',
            f'\\1\n{new_entry}',
            content,
        )

        # Re-sort all entries by date (newest first)
        content = _sort_video_entries(content)

        if not dry_run:
            index_path.write_text(content, encoding='utf-8')

        added = True

    if added:
        print(f"  Updated year index for {year}")

    return added


def update_youtube_ts(year: int, videos_to_add: int, dry_run: bool):
    """Update src/data/youtube.ts with new counts."""
    ts_path = SRC / "data" / "youtube.ts"
    if not ts_path.exists():
        print(f"  Warning: youtube.ts not found: {ts_path}")
        return

    content = ts_path.read_text(encoding='utf-8')

    # Update VIDEO_YEARS count for this year
    year_pattern = rf'(\{{\s*year:\s*{year},\s*count:\s*)(\d+)'
    year_match = re.search(year_pattern, content)

    if year_match:
        old_count = int(year_match.group(2))
        new_count = old_count + videos_to_add
        content = re.sub(year_pattern, f'\\g<1>{new_count}', content)
        print(f"  Updated VIDEO_YEARS[{year}]: {old_count} -> {new_count}")
    else:
        # Year not in list yet — add it at the top of VIDEO_YEARS
        new_entry = (
            f"  {{ year: {year}, count: {videos_to_add}, "
            f"href: '/youtube/{year}/index.html' }},\n"
        )
        content = content.replace(
            'export const VIDEO_YEARS: VideoYear[] = [\n',
            f'export const VIDEO_YEARS: VideoYear[] = [\n{new_entry}',
        )
        print(f"  Added new year {year} with {videos_to_add} videos")

    # Update totalVideos
    total_pattern = r'(totalVideos:\s*)(\d+)'
    total_match = re.search(total_pattern, content)
    if total_match:
        old_total = int(total_match.group(2))
        new_total = old_total + videos_to_add
        content = re.sub(total_pattern, f'\\g<1>{new_total}', content)
        print(f"  Updated totalVideos: {old_total} -> {new_total}")

    if not dry_run:
        ts_path.write_text(content, encoding='utf-8')


def update_latest_updates(videos: list[VideoItem], dry_run: bool):
    """Update LATEST_UPDATES in HomeContent.tsx."""
    home_path = SRC / "app" / "HomeContent.tsx"
    if not home_path.exists():
        print(f"  Warning: HomeContent.tsx not found: {home_path}")
        return

    content = home_path.read_text(encoding='utf-8')

    updates_match = re.search(
        r'const LATEST_UPDATES = \[(.*?)\];',
        content,
        re.DOTALL,
    )
    if not updates_match:
        print("  Warning: Could not find LATEST_UPDATES array")
        return

    # Parse existing entries
    existing_entries = []
    entry_pattern = (
        r"\{\s*title:\s*['\"](.+?)['\"],\s*href:\s*['\"](.+?)['\"],"
        r"\s*date:\s*['\"](.+?)['\"],\s*icon:\s*['\"](.+?)['\"],?\s*\}"
    )
    for match in re.finditer(entry_pattern, updates_match.group(1)):
        existing_entries.append({
            'title': match.group(1),
            'href': match.group(2),
            'date': match.group(3),
            'icon': match.group(4),
        })

    # Build new entries (newest first)
    new_entries = []
    for video in sorted(videos, key=lambda v: v.published, reverse=True):
        date_str = video.published.strftime('%Y%m%d')
        filename = f"{date_str}_{title_to_filename(video.title)}"
        href = f"/youtube/{video.published.year}/{filename}.html"
        display_date = video.published.strftime('%B %-d, %Y')

        new_entries.append({
            'title': video.title.replace("'", "\\'"),
            'href': href,
            'date': display_date,
            'icon': 'video',
        })

    # Merge: new first, then existing (no duplicates), keep top 5
    seen_hrefs = {e['href'] for e in new_entries}
    unique_existing = [e for e in existing_entries if e['href'] not in seen_hrefs]
    all_entries = (new_entries + unique_existing)[:5]

    entries_str = ',\n  '.join([
        f"{{\n    title: '{e['title']}',\n    href: '{e['href']}',"
        f"\n    date: '{e['date']}',\n    icon: '{e['icon']}',\n  }}"
        for e in all_entries
    ])
    new_array = f"const LATEST_UPDATES = [\n  {entries_str},\n];"

    content = re.sub(
        r'const LATEST_UPDATES = \[[\s\S]*?\];(?=\s*\nconst )',
        new_array,
        content,
    )

    if not dry_run:
        home_path.write_text(content, encoding='utf-8')

    print(f"  Updated LATEST_UPDATES with {len(new_entries)} new videos")


def backfill_transcripts(
    dry_run: bool,
    model_id: str = DEFAULT_WHISPER_MODEL,
):
    """Find existing video pages without transcripts and add them."""
    print("\nScanning for videos without transcripts...")
    missing = []

    base = PUBLIC / "youtube"
    for html_file in sorted(base.rglob("*.html")):
        if html_file.name == "index.html":
            continue
        content = html_file.read_text(encoding='utf-8', errors='replace')
        if '<div class="transcript">' in content:
            continue
        # Extract video ID from embed URL
        m = re.search(r'youtube\.com/embed/([a-zA-Z0-9_-]+)', content)
        if not m:
            continue
        video_id = m.group(1)
        missing.append((html_file, video_id))

    if not missing:
        print("All video pages already have transcripts!")
        return

    print(f"Found {len(missing)} videos without transcripts:\n")
    for filepath, vid in missing:
        rel = filepath.relative_to(PUBLIC / "youtube")
        print(f"  {rel}  (ID: {vid})")

    if dry_run:
        print("\nDRY RUN - No files were modified")
        return

    success = 0
    for filepath, video_id in missing:
        rel = filepath.relative_to(PUBLIC / "youtube")
        print(f"\nProcessing {rel}...")
        transcript = generate_transcript(video_id, model_id)
        if not transcript:
            print(f"  Skipped (transcription failed)")
            continue

        # Build transcript HTML
        paragraphs = transcript.split('\n\n')
        transcript_body = '\n'.join(
            f'            {html.escape(p)}' if i == 0
            else f'\n{html.escape(p)}'
            for i, p in enumerate(paragraphs)
        )
        transcript_div = (
            f'<div class="transcript">\n'
            f'<h2>Transcript</h2>\n'
            f'{transcript_body}</div>'
        )

        # Insert transcript before the tags div in both copies
        for base_dir in [PUBLIC / "youtube", REPO_YOUTUBE]:
            target = base_dir / filepath.relative_to(PUBLIC / "youtube")
            if not target.exists():
                continue
            page_content = target.read_text(encoding='utf-8')
            # Insert before the tags/links section
            insertion_point = page_content.find('<div class="tags">')
            if insertion_point == -1:
                insertion_point = page_content.find('<div class="links">')
            if insertion_point == -1:
                insertion_point = page_content.find('<div class="video-links">')
            if insertion_point == -1:
                print(f"  Warning: could not find insertion point in {target}")
                continue
            new_content = (
                page_content[:insertion_point]
                + '\n        ' + transcript_div + '\n'
                + page_content[insertion_point:]
            )
            target.write_text(new_content, encoding='utf-8')

        success += 1
        print(f"  Added transcript ({len(transcript.split())} words)")

    print(f"\nBackfill complete: {success}/{len(missing)} transcripts added.")


def print_summary(new_videos: list[VideoItem]):
    """Print summary of detected new videos."""
    print(f"\nNEW VIDEOS DETECTED ({len(new_videos)}):\n")

    for video in new_videos:
        date_str = video.published.strftime('%Y%m%d')
        filename = f"{date_str}_{title_to_filename(video.title)}"
        print(f"  {video.title}")
        print(f"    YouTube ID: {video.video_id}")
        print(f"    Date: {video.published.strftime('%B %-d, %Y')}")
        print(f"    -> /youtube/{video.published.year}/{filename}.html")
        print()


def run(
    dry_run: bool = False,
    force: bool = False,
    channel_id: str | None = None,
    include_shorts: bool = False,
    no_transcript: bool = False,
    backfill: bool = False,
    whisper_model: str = DEFAULT_WHISPER_MODEL,
):
    """Main execution."""
    # Handle backfill mode
    if backfill:
        backfill_transcripts(dry_run=dry_run, model_id=whisper_model)
        return

    # Use hardcoded channel ID, resolve from handle, or use provided value
    if not channel_id:
        channel_id = CHANNEL_ID
    print(f"Channel ID: {channel_id}")

    # Fetch feed
    videos = fetch_feed(channel_id)
    print(f"Found {len(videos)} videos in feed")

    # Filter out Shorts (unless --include-shorts)
    if not include_shorts:
        print("Checking for Shorts...")
        videos = filter_shorts(videos)
        print(f"{len(videos)} regular videos after filtering Shorts")

    # Find new videos
    new_videos = get_new_videos(videos, force=force)

    if not new_videos:
        print("\nNo new videos detected. Site is up to date!")
        return

    print_summary(new_videos)

    if dry_run:
        print("DRY RUN - No files were modified")
        print("\nRun without --dry-run to apply changes")
        return

    # Create video pages (with transcripts unless --no-transcript)
    for video in new_videos:
        transcript = None
        if not no_transcript:
            print(f"\nGenerating transcript for: {video.title}")
            transcript = generate_transcript(video.video_id, whisper_model)
            if not transcript:
                print(f"  Warning: proceeding without transcript")

        filepath = create_video_page(video, dry_run, transcript=transcript)
        print(f"Created: {filepath}")

    # Update year indexes and collect counts
    year_video_counts: dict[int, int] = {}
    for video in new_videos:
        year = video.published.year
        if update_year_index(year, video, dry_run):
            year_video_counts[year] = year_video_counts.get(year, 0) + 1

    # Update youtube.ts counts
    for year, count in year_video_counts.items():
        update_youtube_ts(year, count, dry_run)

    # Update LATEST_UPDATES
    update_latest_updates(new_videos, dry_run)

    print(f"\nSync complete! {len(new_videos)} videos added.")
    print("\nNext steps:")
    print("  1. cd next-site && npm run build")
    print("  2. Verify the build succeeds")
    print("  3. Commit and push changes")


def main():
    parser = argparse.ArgumentParser(
        description='Sync YouTube videos to julien.org',
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying files',
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-sync of all videos from the feed',
    )
    parser.add_argument(
        '--channel-id',
        type=str,
        default=None,
        help='YouTube channel ID (auto-resolved from handle if omitted)',
    )
    parser.add_argument(
        '--include-shorts',
        action='store_true',
        help='Include YouTube Shorts (excluded by default)',
    )
    parser.add_argument(
        '--no-transcript',
        action='store_true',
        help='Skip transcript generation (create pages without transcripts)',
    )
    parser.add_argument(
        '--backfill-transcripts',
        action='store_true',
        help='Find existing videos without transcripts and add them',
    )
    parser.add_argument(
        '--whisper-model',
        type=str,
        default=DEFAULT_WHISPER_MODEL,
        help=f'Whisper model for transcription (default: {DEFAULT_WHISPER_MODEL})',
    )
    args = parser.parse_args()

    try:
        run(
            dry_run=args.dry_run,
            force=args.force,
            channel_id=args.channel_id,
            include_shorts=args.include_shorts,
            no_transcript=args.no_transcript,
            backfill=args.backfill_transcripts,
            whisper_model=args.whisper_model,
        )
    except requests.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
