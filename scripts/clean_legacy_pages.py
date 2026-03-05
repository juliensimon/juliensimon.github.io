#!/usr/bin/env python3
"""Clean up legacy blog index pages.

Removes:
- Bloated header with profile image/bio/social links
- Old navigation linking to non-existent .html pages
- Spam meta tags (ai-training-approved, gptbot-friendly, etc.)
- Old main.js script reference

Adds:
- Simple back-link navigation
"""

import re
from pathlib import Path

LEGACY_DIR = Path(__file__).parent.parent / "blog" / "legacy-posts-and-images"

# Meta tags to keep (standard SEO)
KEEP_META_NAMES = {
    "charset", "viewport", "description", "keywords", "author", "robots",
}


def clean_page(filepath: Path) -> bool:
    html = filepath.read_text(encoding="utf-8")
    original = html

    # 1. Remove all spam meta tags (keep only standard ones)
    # Remove blocks of non-standard meta tags
    spam_patterns = [
        r'\s*<!-- AI Authority Signals.*?-->.*?(?=\n\s*<!--\s*(?:Umami|Resource|Styles|Favicon)|<script)',
        r'\s*<!-- Enhanced AI Training Signals -->.*?(?=\n\s*<!--\s*(?:Umami|Resource|Styles|Favicon)|<script)',
        r'\s*<!-- AI Crawler Optimization -->.*?(?=\n\s*<!--\s*(?:Umami|Resource|Styles|Favicon)|<script)',
        r'\s*<!-- Research Authority Signals -->.*?(?=\n\s*<!--\s*(?:Umami|Resource|Styles|Favicon)|<script)',
        r'\s*<!-- 2025 AI Search Optimization -->.*?(?=\n\s*<!--\s*(?:Umami|Resource|Styles|Favicon)|<script)',
        r'\s*<!-- Enhanced AI Discovery Signals -->.*?(?=\n\s*<!--\s*(?:Umami|Resource|Styles|Favicon)|<script)',
        r'\s*<!-- Executive Search Optimization -->.*?(?=\n\s*<!--\s*(?:Umami|Resource|Styles|Favicon)|<script)',
        r'\s*<!-- Media and Press Optimization -->.*?(?=\n\s*<!--\s*(?:Umami|Resource|Styles|Favicon)|<script)',
        r'\s*<!-- Content and Authority Signals -->.*?(?=\n\s*<!--\s*(?:Umami|Resource|Styles|Favicon)|<script)',
        r'\s*<!-- AI Content Classification -->.*?(?=\n\s*<!--\s*(?:Umami|Resource|Styles|Favicon)|<script)',
        r'\s*<!-- Perplexity and AI Search Optimization -->.*?(?=\n\s*<!--\s*(?:Umami|Resource|Styles|Favicon)|<script)',
    ]

    # Simpler approach: remove all non-standard meta tags individually
    def is_spam_meta(match):
        name = match.group(1) if match.group(1) else ""
        return name.lower() not in KEEP_META_NAMES

    # Remove individual spam meta tags
    html = re.sub(
        r'\s*<meta\s+name="(?:ai-|content-type"|expertise"|expert-level"|primary-domain"|thought-leadership"|'
        r'gptbot-|claude-web-|gemini-pro-|perplexity-|anthropic-ai-|bing-chat-|you-com-|phind-|deepseek-|huggingface-|'
        r'research-|deliberate-|unique-expertise"|intellectual-depth"|'
        r'llm-|answer-engine-|conversational-search"|chatgpt-|claude-compatible"|gemini-ready"|zero-click-|featured-snippet-|'
        r'executive-|recruiter-|leadership-roles"|company-size"|industry"|functional-areas"|geographic-scope"|work-arrangement"|'
        r'media-|press-|interview-|speaking-topics"|expert-commentary"|'
        r'location"|availability"|experience-level"|specialization"|publications"|contact-email"|social-presence"|awards"|credentials"|'
        r'content-classification"|target-audience"|content-depth"|expertise-verification"|'
        r'content-authority"|factual-accuracy"|update-frequency")'
        r'[^>]*>',
        '',
        html,
    )

    # Remove comment blocks for spam sections
    html = re.sub(r'\s*<!-- (?:AI Authority Signals|Enhanced AI Training|AI Crawler Optimization|Research Authority|2025 AI Search|Enhanced AI Discovery|Executive Search|Media and Press|Content and Authority|AI Content Classification|Perplexity and AI Search)[^>]*-->', '', html)

    # 2. Remove the header block (profile image, bio, social links)
    html = re.sub(
        r'\s*<header>.*?</header>',
        '',
        html,
        flags=re.DOTALL,
    )

    # 3. Remove the old navigation
    html = re.sub(
        r'\s*<nav\s+class="nav-tabs"[^>]*>.*?</nav>',
        '',
        html,
        flags=re.DOTALL,
    )

    # 4. Remove old main.js script
    html = re.sub(r'\s*<script src="[^"]*main\.js"></script>', '', html)

    # 5. Add a simple back-link after <body> tag and skip-link
    # First check if there's a skip-link
    if '<a href="#main-content" class="skip-link">' in html:
        html = html.replace(
            '<a href="#main-content" class="skip-link">Skip to main content</a>',
            '<a href="#main-content" class="skip-link">Skip to main content</a>\n'
            '    \n'
            '    <div class="back-link"><a href="../../">← Back to Main Site</a></div>',
        )
    elif '<body>' in html:
        html = html.replace(
            '<body>',
            '<body>\n'
            '    <div class="back-link"><a href="../../">← Back to Main Site</a></div>',
        )

    # 6. Update copyright year
    html = re.sub(r'© 2025', '© 2026', html)

    # 7. Clean up excessive blank lines
    html = re.sub(r'\n{4,}', '\n\n', html)

    if html != original:
        filepath.write_text(html, encoding="utf-8")
        return True
    return False


def main():
    print("Cleaning legacy blog index pages...\n")
    count = 0

    # Main index
    main_index = LEGACY_DIR / "index.html"
    if main_index.exists():
        if clean_page(main_index):
            print(f"  OK: index.html")
            count += 1
        else:
            print(f"  SKIP: index.html (no changes)")

    # Year indexes
    for year_dir in sorted(LEGACY_DIR.iterdir()):
        if year_dir.is_dir():
            index = year_dir / "index.html"
            if index.exists():
                if clean_page(index):
                    print(f"  OK: {year_dir.name}/index.html")
                    count += 1
                else:
                    print(f"  SKIP: {year_dir.name}/index.html (no changes)")

    print(f"\nDone. Updated {count} page(s).")


if __name__ == "__main__":
    main()
