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

import json
import requests
import xml.etree.ElementTree as ET

from refresh_llms_txt import refresh_llms_files

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


# Target window for SEO meta descriptions. Bing and Google start truncating
# around 155-160; below ~70 they often flag the description as too short.
META_DESC_MAX = 155
META_DESC_MIN = 70


def build_meta_description(
    title: str,
    description: str,
    fallback_suffix: str = 'a video by Julien Simon on AI, ML, and small language models.',
) -> str:
    """Derive a unique, SEO-friendly meta description from a page's data.

    Why this exists: previously every YouTube page used a templated
    "<title> - YouTube video by Julien Simon" string, which Bing Webmaster
    flagged as both too short and duplicate across pages.

    `fallback_suffix` lets callers tailor the synthesized description when the
    body is empty or too short (e.g. blog posts shouldn't say "a video").
    """
    # Collapse whitespace, drop URL-only lines, and pick prose lines.
    prose_lines: list[str] = []
    for raw in (description or '').splitlines():
        line = raw.strip()
        if not line:
            continue
        # Skip lines that are essentially just a URL or a hashtag-only call-out.
        if re.fullmatch(r'(https?://\S+\s*)+', line):
            continue
        if line.startswith('#') and ' ' not in line:
            continue
        prose_lines.append(line)

    text = ' '.join(prose_lines)
    text = re.sub(r'\s+', ' ', text).strip()

    if len(text) >= META_DESC_MIN:
        if len(text) <= META_DESC_MAX:
            return text
        # Truncate at the last sentence/word boundary before the limit.
        cut = text[: META_DESC_MAX - 1]
        boundary = max(cut.rfind('. '), cut.rfind('! '), cut.rfind('? '))
        if boundary >= META_DESC_MIN:
            return cut[: boundary + 1]
        space = cut.rfind(' ')
        if space >= META_DESC_MIN:
            return cut[:space].rstrip(' ,;:-') + '…'
        return cut.rstrip() + '…'

    # Fallback: synthesize from the title so each page still has a distinct,
    # non-trivial description.
    title = title.strip().rstrip('.!?')
    return f"{title} — {fallback_suffix}"


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


def _parse_subscriber_text_to_thousands(text: str) -> int | None:
    """Convert YouTube subscriber-count text to integer thousands.

    Examples: '508K' -> 508, '1.2M' -> 1200, '508,000' -> 508, '5K' -> 5.
    YouTube rounds the displayed count down (e.g. 508K means 508,000-508,999),
    so the rounded thousands value matches what the site displays anyway.
    """
    text = text.strip().replace('\xa0', ' ')
    if ',' in text and not re.search(r'[KMB]', text):
        # Full digit string like "508,000"
        digits = text.replace(',', '')
        if digits.isdigit():
            return int(digits) // 1000
        return None
    match = re.match(r'([\d.]+)\s*([KMB])?', text)
    if not match:
        return None
    n = float(match.group(1))
    suffix = match.group(2)
    if suffix == 'M':
        n *= 1000
    elif suffix == 'B':
        n *= 1_000_000
    # 'K' or no suffix: already in thousands (raw count <1000 rounds to 0)
    return int(n)


def fetch_subscriber_count(channel_id: str) -> int | None:
    """Fetch the live subscriber count from the YouTube channel page.

    Returns the count in thousands (matching YOUTUBE_STATS.subscriberCount
    in next-site/src/data/youtube.ts), or None if extraction fails.

    YouTube serves a heavily-stripped page (without subscriber data) when the
    GDPR consent cookie is absent. Setting CONSENT=YES bypasses the consent
    interstitial and returns the full server-rendered page.
    """
    url = f"https://www.youtube.com/channel/{channel_id}"
    print(f"Fetching subscriber count from {url}...")
    try:
        response = requests.get(url, timeout=15, headers={
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            ),
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': (
                'text/html,application/xhtml+xml,application/xml;q=0.9,'
                'image/webp,*/*;q=0.8'
            ),
            'Cookie': 'CONSENT=YES+cb.20210328-17-p0.en+FX+222; SOCS=CAI',
        })
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"  Warning: failed to fetch channel page: {e}")
        return None

    # YouTube renders the subscriber count inside ytInitialData JSON. The exact
    # key has churned between releases (subscriberCountText, metadataParts,
    # contentMetadataViewModel...), so match the displayed text directly
    # — both the JSON form ("content":"521K subscribers") and the raw form.
    match = re.search(r'([\d.,]+\s*[KMB]?)\s*subscribers', response.text)
    if not match:
        print("  Warning: could not extract subscriber count from channel page")
        return None
    count_k = _parse_subscriber_text_to_thousands(match.group(1))
    if count_k is None:
        print(f"  Warning: could not parse subscriber text: {match.group(1)!r}")
    return count_k


def update_subscriber_count(new_count_k: int, dry_run: bool) -> None:
    """Sync YOUTUBE_STATS.subscriberCount and propagate to text surfaces.

    The numeric value in youtube.ts feeds JSON-LD FAQs and TSX components via
    template literals (auto-updated). Free-form prose in llms.txt, llms-full.txt,
    constants.ts (SITE.description), and experience.ts (Arcee narrative) still
    embeds the literal "<N>K" string, so we replace those occurrences here.
    """
    ts_path = SRC / "data" / "youtube.ts"
    if not ts_path.exists():
        print(f"  Warning: youtube.ts not found: {ts_path}")
        return

    content = ts_path.read_text(encoding='utf-8')
    pattern = r'(subscriberCount:\s*)(\d+)'
    match = re.search(pattern, content)
    if not match:
        print("  Warning: could not find subscriberCount in youtube.ts")
        return

    old = int(match.group(2))
    if old == new_count_k:
        print(f"  Subscriber count unchanged at {old}K")
        return

    # Update the source-of-truth data file first.
    new_content = re.sub(pattern, f'\\g<1>{new_count_k}', content)
    print(f"  Updated subscriberCount: {old}K -> {new_count_k}K")
    if not dry_run:
        ts_path.write_text(new_content, encoding='utf-8')

    # Propagate "<old>K" -> "<new>K" in surfaces that embed the literal value.
    # Word boundaries prevent matching numbers that happen to end in <old>K (e.g.
    # "1508K"); the K after the digits is anchored by a non-digit/non-letter.
    old_literal = f"{old}K"
    new_literal = f"{new_count_k}K"
    replace_pattern = re.compile(rf'\b{old}K(?![\dKMB])')
    targets = [
        BASE / "public" / "llms.txt",
        BASE / "public" / "llms-full.txt",
        SRC / "lib" / "constants.ts",
        SRC / "data" / "experience.ts",
    ]
    for target in targets:
        if not target.exists():
            continue
        text = target.read_text(encoding='utf-8')
        if old_literal not in text:
            continue
        updated = replace_pattern.sub(new_literal, text)
        if updated == text:
            continue
        rel = target.relative_to(REPO_ROOT)
        hits = len(replace_pattern.findall(text))
        print(f"  Propagated {old_literal} -> {new_literal} in {rel} ({hits} occurrences)")
        if not dry_run:
            target.write_text(updated, encoding='utf-8')

    # Update the METRICS array entry in constants.ts; validate-counts.mjs
    # regex-parses the literal value and fails CI if it drifts from
    # YOUTUBE_STATS.subscriberCount.
    constants_path = SRC / "lib" / "constants.ts"
    if constants_path.exists():
        text = constants_path.read_text(encoding='utf-8')
        metrics_pattern = re.compile(
            r"(\{\s*value:\s*)\d+(,\s*suffix:\s*'K',\s*label:\s*'YouTube Subscribers'\s*\})"
        )
        if metrics_pattern.search(text):
            updated = metrics_pattern.sub(
                lambda m: f"{m.group(1)}{new_count_k}{m.group(2)}",
                text,
            )
            if updated != text:
                rel = constants_path.relative_to(REPO_ROOT)
                print(f"  Updated METRICS[YouTube Subscribers] in {rel}: {old} -> {new_count_k}")
                if not dry_run:
                    constants_path.write_text(updated, encoding='utf-8')

    # Refresh the "Last updated" stamp in llms.txt / llms-full.txt so LLMs see
    # that the file is fresh whenever the subscriber count changes.
    today = datetime.now().strftime('%Y-%m-%d')
    for target in (BASE / "public" / "llms.txt", BASE / "public" / "llms-full.txt"):
        if not target.exists():
            continue
        text = target.read_text(encoding='utf-8')
        stamped = re.sub(
            r'(Last updated:\s*)\d{4}-\d{2}-\d{2}',
            f'\\g<1>{today}',
            text,
        )
        if stamped != text and not dry_run:
            target.write_text(stamped, encoding='utf-8')


def fetch_feed_rss(channel_id: str) -> list[VideoItem]:
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


def fetch_feed_ytdlp(handle: str) -> list[VideoItem]:
    """Fallback: use yt-dlp to list recent videos when RSS feed is unavailable."""
    url = f"https://www.youtube.com/@{handle}/videos"
    print(f"Fetching video list via yt-dlp from {url}...")

    # Step 1: get video IDs and titles (fast, no per-video fetch)
    result = subprocess.run(
        ['yt-dlp', '--flat-playlist', '-j', '--playlist-end', '15', url],
        capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp playlist fetch failed: {result.stderr}")

    entries = [json.loads(line) for line in result.stdout.strip().splitlines() if line.strip()]
    if not entries:
        return []

    # Step 2: fetch full metadata per video to get upload dates
    videos = []
    for entry in entries:
        vid = entry.get('id', '')
        title = entry.get('title', '').strip()
        description = entry.get('description', '').strip()
        if not vid or not title:
            continue

        # Get upload date via individual video metadata
        meta_result = subprocess.run(
            ['yt-dlp', '-j', '--no-download', f'https://www.youtube.com/watch?v={vid}'],
            capture_output=True, text=True, timeout=30,
        )
        published = datetime.now()
        if meta_result.returncode == 0:
            meta = json.loads(meta_result.stdout)
            date_str = meta.get('upload_date', '')  # YYYYMMDD
            description = meta.get('description', description).strip()
            if date_str and len(date_str) == 8:
                try:
                    published = datetime.strptime(date_str, '%Y%m%d')
                except ValueError:
                    pass

        videos.append(VideoItem(
            video_id=vid,
            title=title,
            published=published,
            description=description,
        ))

    print(f"  yt-dlp returned {len(videos)} videos")
    return videos


def fetch_feed(channel_id: str) -> list[VideoItem]:
    """Fetch recent videos, trying RSS first then falling back to yt-dlp."""
    try:
        videos = fetch_feed_rss(channel_id)
        return videos
    except requests.HTTPError as e:
        print(f"  RSS feed unavailable ({e}), falling back to yt-dlp...")
    except Exception as e:
        print(f"  RSS feed error ({e}), falling back to yt-dlp...")
    return fetch_feed_ytdlp(CHANNEL_HANDLE)


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
    in YouTube feeds when they contain embedded videos.

    We only flag explicit cross-post indicators, NOT mere mentions of
    the Substack URL (which appear as promotional links in every video).
    """
    desc_lower = video.description.lower()
    substack_signals = [
        'read full post on substack',
        'read the full post on substack',
        'full article on substack',
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

# Whisper model for transcription. We use OpenAI's official turbo distillation
# rather than distil-whisper/distil-large-v3, which suffers from a known
# repetition-loop failure mode on MPS (entire chunks collapse to "!!!!!!").
DEFAULT_WHISPER_MODEL = "openai/whisper-large-v3-turbo"

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


def _is_degenerate_chunk(text: str) -> bool:
    """Detect Whisper's repetition-loop failure mode on a single chunk.

    The model occasionally produces output like "you!!!!!!!!" or a single word
    repeated dozens of times, especially around audio boundaries on MPS. We
    discard these and fill the gap from a second pass with shifted chunks."""
    s = text.strip()
    if len(s) < 15:
        return True
    counts: dict[str, int] = {}
    for c in s:
        counts[c] = counts.get(c, 0) + 1
    if max(counts.values()) / len(s) > 0.45:
        return True
    if re.search(r'[!.,?]{15,}', s):
        return True
    return False


def transcribe_audio(audio_path: str, model_id: str = DEFAULT_WHISPER_MODEL) -> str:
    """Transcribe audio with a two-pass strategy.

    Pass 1 chunks the audio every 30s starting at 0. Pass 2 starts at +15s.
    Each chunk is checked for the repetition-loop failure mode; bad chunks
    from pass 1 are filled in from pass 2 (and vice versa). This recovers
    the ~10-20% of chunks that whisper degenerates on per pass."""
    import time
    import torch
    import librosa

    _load_whisper(model_id)
    duration = _get_audio_duration(audio_path)
    dur_str = f"{duration/60:.1f} min" if duration else "unknown length"

    print(f"  Loading audio ({dur_str})...")
    audio_array, _sr = librosa.load(audio_path, sr=16000)
    chunk_samples = 30 * 16000

    def transcribe_pass(offset_samples: int, label: str) -> list[tuple[float, float, str]]:
        out: list[tuple[float, float, str]] = []
        starts = list(range(offset_samples, len(audio_array), chunk_samples))
        n = len(starts)
        for idx, i in enumerate(starts):
            chunk = audio_array[i:i + chunk_samples]
            if len(chunk) < 5 * 16000:
                break
            input_features = _whisper_processor(
                chunk, sampling_rate=16000, return_tensors="pt",
            ).input_features.to(_whisper_device, dtype=_whisper_dtype)
            with torch.no_grad():
                predicted_ids = _whisper_model.generate(
                    input_features,
                    max_new_tokens=440,
                    language="en",
                    no_repeat_ngram_size=4,
                )
            text = _whisper_processor.batch_decode(
                predicted_ids, skip_special_tokens=True,
            )[0].strip()
            start_s = i / 16000
            end_s = (i + len(chunk)) / 16000
            out.append((start_s, end_s, "" if _is_degenerate_chunk(text) else text))
            print(f"\r  {label}: [{idx+1}/{n}]", end='', flush=True)
        return out

    print(f"  Transcribing pass 1 (offset 0)...")
    start = time.time()
    pass1 = transcribe_pass(0, "P1")
    print(f"\r  Pass 1: {sum(1 for _,_,t in pass1 if t)}/{len(pass1)} good chunks" + " " * 20)

    print(f"  Transcribing pass 2 (offset 15s)...")
    pass2 = transcribe_pass(15 * 16000, "P2")
    print(f"\r  Pass 2: {sum(1 for _,_,t in pass2 if t)}/{len(pass2)} good chunks" + " " * 20)

    # Merge: walk pass 1 in order; for empty regions, take any overlapping pass-2 chunk.
    merged: list[str] = []
    for s, _e, t in pass1:
        if t:
            merged.append(t)
            continue
        for s2, _e2, t2 in pass2:
            # pass2 chunks span [s2, s2+30]; cover the pass1 chunk [s, s+30] if they overlap by >=5s
            if t2 and s2 <= s and s2 + 30 >= s + 5:
                merged.append(t2)
                break

    elapsed = time.time() - start
    speed = duration / elapsed if elapsed > 0 else 0
    print(f"  Transcribed {dur_str} in {elapsed:.0f}s ({speed:.1f}x realtime)")
    return " ".join(merged)


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

    # Build a meta description for SEO from the real video description.
    # Pull the first non-trivial line, collapse whitespace, cap at ~155 chars.
    # Falls back to a title-derived sentence if the description is empty/too short.
    meta_description = build_meta_description(video.title, video.description)

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
    <meta name="description" content="{html.escape(meta_description)}">
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
        "description": {json.dumps(meta_description).replace('</', '<\\/')},
        "uploadDate": "{video.published.strftime('%Y-%m-%dT%H:%M:%S+00:00')}",
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
    # Same description the video page puts in its meta tag, so the index card
    # and the page it links to never disagree.
    description = build_meta_description(video.title, video.description)

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
            f'<div class="video-description">{html.escape(description)}</div>'
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


# Model used to write the one-line LATEST_UPDATES teaser from a video transcript.
SUMMARY_MODEL = "claude-opus-5"

# How much transcript to send. The opening minutes carry the thesis; sending the
# whole thing costs tokens without improving a single sentence.
SUMMARY_TRANSCRIPT_CHARS = 16000

SUMMARY_SYSTEM = (
    "You write one-line teasers for a video listing on an AI engineer's personal "
    "site. Given a talk transcript, write a single sentence describing what the "
    "video covers, in the site owner's plain, concrete, non-promotional voice. "
    "No hype, no marketing adjectives, no 'in this video'. Under 160 characters."
)


def build_video_summary(
    title: str,
    transcript: str | None,
    model: str = SUMMARY_MODEL,
) -> str:
    """One-line teaser for LATEST_UPDATES, written from the video transcript.

    Returns '' when unavailable for any reason (no transcript, SDK missing, no
    credentials, API error) — the card simply renders without a summary rather
    than failing the sync.
    """
    if not transcript or not transcript.strip():
        return ''

    try:
        import anthropic
    except ImportError:
        print("  Summary skipped: `anthropic` not installed "
              "(add --with anthropic, or pass --no-summary)")
        return ''

    excerpt = transcript.strip()[:SUMMARY_TRANSCRIPT_CHARS]
    schema = {
        "type": "object",
        "properties": {"summary": {"type": "string"}},
        "required": ["summary"],
        "additionalProperties": False,
    }

    try:
        client = anthropic.Anthropic()
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            system=SUMMARY_SYSTEM,
            output_config={
                "effort": "low",
                "format": {"type": "json_schema", "schema": schema},
            },
            messages=[{
                "role": "user",
                "content": f"Video title: {title}\n\nTranscript excerpt:\n{excerpt}",
            }],
        )
    except Exception as e:  # noqa: BLE001 - a summary is never worth failing a sync
        print(f"  Summary skipped ({type(e).__name__}): {e}")
        return ''

    if response.stop_reason == "refusal":
        print("  Summary skipped: model declined")
        return ''

    text = next((b.text for b in response.content if b.type == "text"), "")
    try:
        summary = json.loads(text)["summary"]
    except (ValueError, KeyError, TypeError):
        print("  Summary skipped: unparseable response")
        return ''

    summary = re.sub(r'\s+', ' ', summary).strip()
    print(f"  Summary: {summary}")
    return summary


def js_escape(text: str) -> str:
    """Escape text for embedding inside a single-quoted JS string literal."""
    return text.replace('\\', '\\\\').replace("'", "\\'")


# A single-quoted JS string literal, capturing its raw (still-escaped) body.
JS_STRING = r"'((?:[^'\\]|\\.)*)'"


def parse_latest_update_entries(array_body: str) -> list[dict]:
    """Parse LATEST_UPDATES entries field-by-field.

    Reading each key by name (rather than by position) keeps optional fields
    such as the article `summary` written by sync_substack.py from being
    dropped when this script rewrites the array. Values stay in their raw
    escaped form so they round-trip verbatim.
    """
    entries = []
    for block in re.finditer(r'\{[^{}]*\}', array_body):
        entry = {}
        for key in ('title', 'href', 'date', 'icon', 'summary'):
            match = re.search(rf"\b{key}:\s*{JS_STRING}", block.group(0))
            if match:
                entry[key] = match.group(1)
        if {'title', 'href', 'date', 'icon'} <= entry.keys():
            entries.append(entry)
    return entries


def render_latest_updates(entries: list[dict]) -> str:
    """Render the LATEST_UPDATES array literal from parsed entries."""
    entries_str = ',\n  '.join(
        f"{{\n    title: '{e['title']}',\n    href: '{e['href']}',"
        f"\n    date: '{e['date']}',\n"
        + (f"    summary: '{e['summary']}',\n" if e.get('summary') else '')
        + f"    icon: '{e['icon']}',\n  }}"
        for e in entries
    )
    return f"const LATEST_UPDATES: LatestUpdate[] = [\n  {entries_str},\n];"


def update_latest_updates(
    videos: list[VideoItem],
    dry_run: bool,
    transcripts: dict[str, str] | None = None,
    summary_model: str | None = None,
):
    """Update LATEST_UPDATES in HomeContent.tsx."""
    home_path = SRC / "app" / "HomeContent.tsx"
    if not home_path.exists():
        print(f"  Warning: HomeContent.tsx not found: {home_path}")
        return

    content = home_path.read_text(encoding='utf-8')

    updates_match = re.search(
        r'const LATEST_UPDATES(?:\s*:\s*\w+\[\])? = \[(.*?)\];',
        content,
        re.DOTALL,
    )
    if not updates_match:
        print("  Warning: Could not find LATEST_UPDATES array")
        return

    existing_entries = parse_latest_update_entries(updates_match.group(1))

    # Build new entries (newest first)
    new_entries = []
    for video in sorted(videos, key=lambda v: v.published, reverse=True):
        date_str = video.published.strftime('%Y%m%d')
        filename = f"{date_str}_{title_to_filename(video.title)}"
        href = f"/youtube/{video.published.year}/{filename}.html"
        display_date = video.published.strftime('%B %-d, %Y')

        entry = {
            'title': video.title.replace("'", "\\'"),
            'href': href,
            'date': display_date,
            'icon': 'video',
        }
        if summary_model:
            summary = build_video_summary(
                video.title,
                (transcripts or {}).get(video.video_id),
                summary_model,
            )
            if summary:
                entry['summary'] = js_escape(summary)
        new_entries.append(entry)

    # Merge: new first, then existing (no duplicates), sort by date, keep top 5
    seen_hrefs = {e['href'] for e in new_entries}
    unique_existing = [e for e in existing_entries if e['href'] not in seen_hrefs]
    all_entries = new_entries + unique_existing
    all_entries.sort(key=lambda e: datetime.strptime(e['date'], '%B %d, %Y'), reverse=True)
    all_entries = all_entries[:5]

    new_array = render_latest_updates(all_entries)

    content = re.sub(
        r'const LATEST_UPDATES(?:\s*:\s*\w+\[\])? = \[[\s\S]*?\];(?=\s*\nconst )',
        lambda _: new_array,
        content,
    )

    if not dry_run:
        home_path.write_text(content, encoding='utf-8')

    print(f"  Updated LATEST_UPDATES with {len(new_entries)} new videos")


# The LATEST_VIDEOS array literal, with or without a type annotation.
LATEST_VIDEOS_ARRAY = r'export const LATEST_VIDEOS(?:\s*:\s*\w+\[\])? = \[[\s\S]*?\];'


def read_page_transcript(video_id: str, year: int) -> str | None:
    """Pull the transcript text back out of a video's generated page.

    update_latest_videos runs on every sync, including runs that synced no new
    videos, so a summary has to be sourced from the pages already on disk
    rather than from a transcript produced earlier in the same run.
    """
    for base_dir in (PUBLIC / "youtube", REPO_YOUTUBE):
        year_dir = base_dir / str(year)
        if not year_dir.exists():
            continue
        for html_file in year_dir.glob("*.html"):
            if html_file.name == "index.html":
                continue
            content = html_file.read_text(encoding='utf-8', errors='replace')
            if video_id not in content:
                continue
            m = re.search(
                r'<div class="transcript">(.*?)</div>', content, re.DOTALL
            )
            if not m:
                return None
            text = html.unescape(re.sub(r'<[^>]+>', ' ', m.group(1)))
            return re.sub(r'^Transcript\s*', '', re.sub(r'\s+', ' ', text).strip())
    return None


def update_latest_videos(
    feed_videos: list[VideoItem],
    dry_run: bool,
    summary_model: str | None = None,
):
    """Rebuild LATEST_VIDEOS in youtube.ts from the feed's newest videos.

    Unlike update_latest_updates (which merges only newly-synced videos into the
    homepage list), this always rebuilds the array from the current feed, so the
    "Latest Videos" section on /youtube-videos self-heals even on runs with no
    new videos.

    Because it rebuilds rather than merges, summaries already in the array are
    carried over by video id — otherwise every sync would wipe them. A video
    still missing one gets a summary written from its page transcript, so the
    section backfills itself over time.
    """
    ts_path = SRC / "data" / "youtube.ts"
    if not ts_path.exists():
        print(f"  Warning: youtube.ts not found: {ts_path}")
        return

    top = sorted(feed_videos, key=lambda v: v.published, reverse=True)[:3]
    if not top:
        return

    content = ts_path.read_text(encoding='utf-8')
    array_match = re.search(LATEST_VIDEOS_ARRAY, content)
    if not array_match:
        print("  Warning: Could not find LATEST_VIDEOS array")
        return

    existing_summaries = {
        m.group(1): m.group(2)
        for m in re.finditer(
            rf"id:\s*{JS_STRING}[^}}]*?summary:\s*{JS_STRING}",
            array_match.group(0),
        )
    }

    entries = []
    for video in top:
        title = js_escape(video.title)
        date = video.published.strftime('%B %-d, %Y')
        summary = existing_summaries.get(video.video_id, '')
        if not summary and summary_model:
            generated = build_video_summary(
                video.title,
                read_page_transcript(video.video_id, video.published.year),
                summary_model,
            )
            if generated:
                summary = js_escape(generated)
        summary_field = f", summary: '{summary}'" if summary else ''
        entries.append(
            f"  {{ id: '{video.video_id}', title: '{title}', "
            f"date: '{date}'{summary_field} }},"
        )
    new_array = (
        "export const LATEST_VIDEOS: LatestVideo[] = [\n"
        + "\n".join(entries)
        + "\n];"
    )

    new_content, n = re.subn(
        LATEST_VIDEOS_ARRAY,
        lambda _m: new_array,
        content,
        count=1,
    )
    if n == 0:
        print("  Warning: Could not find LATEST_VIDEOS array")
        return
    if new_content == content:
        print("  LATEST_VIDEOS already up to date")
        return

    if not dry_run:
        ts_path.write_text(new_content, encoding='utf-8')
    action = "Would update" if dry_run else "Updated"
    print(f"  {action} LATEST_VIDEOS: {', '.join(v.video_id for v in top)}")


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
    no_summary: bool = False,
    summary_model: str = SUMMARY_MODEL,
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

    # Sync subscriber count (runs even when there are no new videos — the count
    # drifts independently of new uploads and is consumed by JSON-LD + llms.txt).
    new_subs = fetch_subscriber_count(channel_id)
    if new_subs is not None:
        update_subscriber_count(new_subs, dry_run)

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

    summary_model_or_none = None if (no_summary or dry_run) else summary_model

    if not new_videos:
        print("\nNo new videos detected. Site is up to date!")
        # Still refresh /youtube-videos: the array can drift out of date, and a
        # video whose summary failed on an earlier run backfills here.
        update_latest_videos(videos, dry_run, summary_model_or_none)
        # Subscriber count may still have changed above; keep llms files aligned.
        refresh_llms_files(dry_run=dry_run)
        return

    print_summary(new_videos)

    if dry_run:
        update_latest_videos(videos, dry_run, summary_model_or_none)
        print("DRY RUN - No files were modified")
        print("\nRun without --dry-run to apply changes")
        return

    # Create video pages (with transcripts unless --no-transcript)
    transcripts: dict[str, str] = {}
    for video in new_videos:
        transcript = None
        if not no_transcript:
            print(f"\nGenerating transcript for: {video.title}")
            transcript = generate_transcript(video.video_id, whisper_model)
            if not transcript:
                print(f"  Warning: proceeding without transcript")

        if transcript:
            transcripts[video.video_id] = transcript

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

    # Refresh the "Latest Videos" section on /youtube-videos. Runs after the
    # pages are written so a brand-new video's transcript is available to
    # summarize.
    update_latest_videos(videos, dry_run, summary_model_or_none)

    # Update LATEST_UPDATES
    update_latest_updates(
        new_videos,
        dry_run,
        transcripts=transcripts,
        summary_model=summary_model_or_none,
    )

    # Keep AI-facing llms files aligned with the updated data files.
    refresh_llms_files(dry_run=dry_run)

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
    parser.add_argument(
        '--no-summary',
        action='store_true',
        help='Skip the LLM-written one-line summary for new videos',
    )
    parser.add_argument(
        '--summary-model',
        type=str,
        default=SUMMARY_MODEL,
        help=f'Claude model for video summaries (default: {SUMMARY_MODEL})',
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
            no_summary=args.no_summary,
            summary_model=args.summary_model,
        )
    except requests.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
