#!/usr/bin/env python3
"""Strip spam meta tags from all deployed HTML pages.

Removes the ~100-line block of fake "AI Authority Signals", "AI Crawler
Optimization", "Executive Search Optimization", etc. meta tags that were
bulk-injected into every blog and YouTube page.

Also removes old <header>, <nav class="nav-tabs">, and main.js references
from legacy index pages that still have old layout elements.
"""

import re
from pathlib import Path

PUBLIC = Path(__file__).parent.parent / "next-site" / "public"

# The spam block always starts with this comment (possibly with leading whitespace)
# and ends just before <!-- Umami or a <link or <script line.
SPAM_COMMENT_HEADERS = [
    "AI Authority Signals",
    "Enhanced AI Training Signals",
    "AI Crawler Optimization",
    "Research Authority Signals",
    "2025 AI Search Optimization",
    "Enhanced AI Discovery Signals",
    "Executive Search Optimization",
    "Media and Press Optimization",
    "Content and Authority Signals",
    "AI Content Classification",
    "Perplexity and AI Search Optimization",
]

# Individual spam meta tag name prefixes
SPAM_META_PREFIXES = (
    "ai-", "content-type", "expertise", "expert-level", "primary-domain",
    "thought-leadership", "gptbot-", "claude-web-", "gemini-pro-", "perplexity-",
    "anthropic-ai-", "bing-chat-", "you-com-", "phind-", "deepseek-", "huggingface-",
    "research-", "deliberate-", "unique-expertise", "intellectual-depth",
    "llm-", "answer-engine-", "conversational-search", "chatgpt-", "claude-compatible",
    "gemini-ready", "zero-click-", "featured-snippet-",
    "executive-", "recruiter-", "leadership-roles", "company-size", "industry",
    "functional-areas", "geographic-scope", "work-arrangement",
    "media-ready", "media-topics", "media-experience", "press-", "interview-",
    "speaking-topics", "expert-commentary",
    "location", "availability", "experience-level", "specialization", "publications",
    "contact-email", "social-presence", "awards", "credentials",
    "content-classification", "target-audience", "content-depth", "expertise-verification",
    "content-authority", "factual-accuracy", "update-frequency",
)

# Standard meta names to KEEP
KEEP_META_NAMES = {
    "charset", "viewport", "description", "keywords", "author", "robots",
    "generator", "theme-color", "color-scheme",
}


def strip_spam(html: str) -> str:
    # 1. Remove comment blocks for spam sections
    for header in SPAM_COMMENT_HEADERS:
        html = re.sub(
            r'\s*<!--\s*' + re.escape(header) + r'[^>]*-->',
            '',
            html,
        )

    # 2. Remove individual spam meta tags
    def is_spam_meta(match):
        tag = match.group(0)
        # Extract name attribute
        name_match = re.search(r'name="([^"]*)"', tag)
        if not name_match:
            return False
        name = name_match.group(1).lower()
        if name in KEEP_META_NAMES:
            return False
        for prefix in SPAM_META_PREFIXES:
            if name.startswith(prefix) or name == prefix:
                return True
        return False

    html = re.sub(
        r'\s*<meta\s+name="[^"]*"[^>]*>',
        lambda m: '' if is_spam_meta(m) else m.group(0),
        html,
    )

    # 3. Remove old <header> blocks (profile image, bio, social links)
    html = re.sub(r'\s*<header>.*?</header>', '', html, flags=re.DOTALL)

    # 4. Remove old navigation
    html = re.sub(r'\s*<nav\s+class="nav-tabs"[^>]*>.*?</nav>', '', html, flags=re.DOTALL)

    # 5. Remove old main.js script
    html = re.sub(r'\s*<script src="[^"]*main\.js"></script>', '', html)

    # 6. Clean up excessive blank lines
    html = re.sub(r'\n{4,}', '\n\n', html)

    return html


def main():
    print("Stripping spam meta tags from deployed HTML pages...\n")
    count = 0
    errors = 0

    for html_file in sorted(PUBLIC.rglob("*.html")):
        # Skip non-legacy content (Next.js generated pages don't have spam)
        rel = html_file.relative_to(PUBLIC)
        parts = str(rel).split("/")
        if parts[0] not in ("blog", "youtube"):
            continue

        try:
            original = html_file.read_text(encoding="utf-8")
            cleaned = strip_spam(original)
            if cleaned != original:
                html_file.write_text(cleaned, encoding="utf-8")
                count += 1
        except Exception as e:
            print(f"  ERROR: {rel}: {e}")
            errors += 1

    print(f"Done. Cleaned {count} file(s).")
    if errors:
        print(f"Errors: {errors}")


if __name__ == "__main__":
    main()
