#!/usr/bin/env python3
"""Decouple blog/youtube HTML content from legacy /css/ directory.

Rewrites CSS references from ../../css/styles.css (etc.) to use the local
style.css files that already exist in each blog/youtube section.
After this, the /css/ directory in public/ can be safely deleted.
"""

import re
from pathlib import Path

PUBLIC = Path(__file__).parent.parent / "next-site" / "public"


def fix_css_refs(filepath: Path) -> bool:
    """Rewrite /css/*.css references to use local style.css."""
    html = filepath.read_text(encoding="utf-8")
    original = html

    # Remove references to legacy CSS files (styles.css, social-icons.css,
    # critical.css, minimal-blog-styles.css) from the /css/ directory.
    # These are replaced by the local style.css already linked in each page.
    html = re.sub(
        r'\s*<link\s+rel="stylesheet"\s+href="[^"]*?/css/[^"]*\.css"[^>]*>',
        '',
        html,
    )

    # Also remove any inline style tags referencing /css/
    html = re.sub(
        r'\s*<link\s+href="[^"]*?/css/[^"]*\.css"[^>]*>',
        '',
        html,
    )

    if html != original:
        # Clean up excessive blank lines
        html = re.sub(r'\n{3,}', '\n\n', html)
        filepath.write_text(html, encoding="utf-8")
        return True
    return False


def main():
    print("Decoupling blog/youtube HTML from legacy /css/ directory...\n")
    count = 0

    for html_file in sorted(PUBLIC.rglob("*.html")):
        rel = html_file.relative_to(PUBLIC)
        parts = str(rel).split("/")
        if parts[0] not in ("blog", "youtube"):
            continue

        if fix_css_refs(html_file):
            count += 1

    print(f"Done. Fixed CSS references in {count} file(s).")


if __name__ == "__main__":
    main()
