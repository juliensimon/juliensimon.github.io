#!/usr/bin/env python3
"""
Substack HTML Cleaner

Cleans Substack-specific HTML markup to produce clean semantic HTML
suitable for local hosting. Removes tracking, subscription elements,
and platform-specific styling while preserving article content.

Usage:
    from substack_html_cleaner import SubstackHTMLCleaner

    cleaner = SubstackHTMLCleaner()
    cleaned_html, images = cleaner.clean(raw_html)
"""

import re
from bs4 import BeautifulSoup, NavigableString


class SubstackHTMLCleaner:
    """Cleans Substack HTML content for local hosting."""

    # Tags to remove entirely (including their content)
    REMOVE_TAGS = {
        'script', 'style', 'form', 'button', 'noscript',
        'iframe',  # except YouTube - handled specially
        'svg',     # Substack icons
        'input', 'textarea', 'select',
    }

    # Classes that indicate Substack-specific elements to remove
    REMOVE_CLASS_PATTERNS = [
        r'subscribe',
        r'signup',
        r'newsletter',
        r'share',
        r'social',
        r'cta',
        r'button',
        r'footer',
        r'header-with-anchor',
        r'captioned-button',
        r'subscription',
        r'paywall',
        r'sidepanel',
        r'like-button',
        r'comment',
        r'post-ufi',
        r'available-content',
        r'podcast-player',
    ]

    # Attributes to remove from all elements
    REMOVE_ATTRS = {
        'data-component-name',
        'data-attrs',
        'data-toggle',
        'data-target',
        'data-tracking',
        'onclick',
        'onmouseover',
        'onmouseout',
        'onfocus',
        'onblur',
    }

    # Pattern for Medium-style random IDs
    MEDIUM_ID_PATTERN = re.compile(r'^[0-9a-f]{4}$')

    def __init__(self, preserve_youtube: bool = True):
        """
        Initialize the cleaner.

        Args:
            preserve_youtube: Keep YouTube iframes (default True)
        """
        self.preserve_youtube = preserve_youtube
        self._compiled_class_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.REMOVE_CLASS_PATTERNS
        ]

    def clean(self, html: str) -> tuple[str, list[dict]]:
        """
        Clean Substack HTML and extract image information.

        Args:
            html: Raw HTML from Substack

        Returns:
            Tuple of (cleaned_html, list_of_image_dicts)
            Each image dict has: {'src': url, 'alt': alt_text}
        """
        if not html or not html.strip():
            return '', []

        soup = BeautifulSoup(html, 'html.parser')

        # Step 1: Remove unwanted tags
        self._remove_unwanted_tags(soup)

        # Step 2: Remove elements with Substack-specific classes
        self._remove_substack_elements(soup)

        # Step 3: Extract images before further cleaning
        images = self._extract_images(soup)

        # Step 4: Simplify image markup
        self._simplify_images(soup)

        # Step 5: Clean remaining elements
        self._clean_attributes(soup)

        # Step 6: Remove empty containers
        self._remove_empty_elements(soup)

        # Step 7: Normalize whitespace in text
        self._normalize_whitespace(soup)

        # Get cleaned HTML
        cleaned = str(soup)

        # Final cleanup of the HTML string
        cleaned = self._final_cleanup(cleaned)

        return cleaned, images

    def _remove_unwanted_tags(self, soup: BeautifulSoup) -> None:
        """Remove script, style, form, and other unwanted tags."""
        for tag_name in self.REMOVE_TAGS:
            for tag in soup.find_all(tag_name):
                # Special handling for iframes - keep YouTube
                if tag_name == 'iframe' and self.preserve_youtube:
                    src = tag.get('src', '')
                    if 'youtube' in src or 'youtu.be' in src:
                        continue
                tag.decompose()

    def _remove_substack_elements(self, soup: BeautifulSoup) -> None:
        """Remove elements with Substack-specific classes."""
        # Collect all elements first, then filter - decompose() invalidates
        # child elements still in the iterator, setting their attrs to None
        elements = list(soup.find_all(class_=True))
        for element in elements:
            if element.attrs is None:
                continue
            classes = element.get('class', [])
            if isinstance(classes, str):
                classes = [classes]

            class_str = ' '.join(classes)

            # Check if any class matches our removal patterns
            for pattern in self._compiled_class_patterns:
                if pattern.search(class_str):
                    element.decompose()
                    break

    def _extract_images(self, soup: BeautifulSoup) -> list[dict]:
        """Extract image information from the content."""
        images = []

        for img in soup.find_all('img'):
            src = img.get('src', '')
            if not src:
                continue

            # Skip tracking pixels and tiny images
            width = img.get('width', '')
            height = img.get('height', '')
            if width and height:
                try:
                    if int(width) < 10 or int(height) < 10:
                        continue
                except ValueError:
                    pass

            # Skip data URIs and SVGs
            if src.startswith('data:') or src.endswith('.svg'):
                continue

            images.append({
                'src': src,
                'alt': img.get('alt', ''),
            })

        return images

    def _simplify_images(self, soup: BeautifulSoup) -> None:
        """Simplify image markup by unwrapping from Substack containers."""
        # Find all figure/picture containers and simplify to just img
        for container in soup.find_all(['figure', 'picture']):
            img = container.find('img')
            if img:
                # Create a clean img tag
                new_img = soup.new_tag('img')
                new_img['src'] = img.get('src', '')
                if img.get('alt'):
                    new_img['alt'] = img['alt']
                # Replace the container with just the img
                container.replace_with(new_img)

        # Remove captioned-image-container divs, keeping content
        for div in soup.find_all('div', class_=lambda c: c and 'captioned-image-container' in ' '.join(c) if isinstance(c, list) else 'captioned-image-container' in str(c)):
            div.unwrap()

        # Remove image link wrappers (a tags that just wrap images)
        for a in soup.find_all('a', class_=lambda c: c and 'image-link' in str(c)):
            img = a.find('img')
            if img:
                a.replace_with(img)

    def _clean_attributes(self, soup: BeautifulSoup) -> None:
        """Clean up attributes on remaining elements."""
        for element in soup.find_all(True):
            # Remove unwanted attributes
            attrs_to_remove = []
            for attr in element.attrs:
                if attr in self.REMOVE_ATTRS:
                    attrs_to_remove.append(attr)
                # Remove data-* attributes except data-src (for lazy loading)
                elif attr.startswith('data-') and attr != 'data-src':
                    attrs_to_remove.append(attr)

            for attr in attrs_to_remove:
                del element[attr]

            # Remove Medium-style random IDs
            if element.get('id'):
                if self.MEDIUM_ID_PATTERN.match(element['id']):
                    del element['id']

            # Clean up class lists - remove empty or Substack-specific classes
            if element.get('class'):
                classes = element.get('class', [])
                if isinstance(classes, str):
                    classes = [classes]

                # Keep only semantic classes
                cleaned_classes = []
                for cls in classes:
                    # Skip Substack-specific classes
                    skip = False
                    for pattern in self._compiled_class_patterns:
                        if pattern.search(cls):
                            skip = True
                            break
                    if not skip and cls:  # Keep non-empty, non-Substack classes
                        cleaned_classes.append(cls)

                if cleaned_classes:
                    element['class'] = cleaned_classes
                else:
                    del element['class']

    def _remove_empty_elements(self, soup: BeautifulSoup) -> None:
        """Remove empty divs and spans that don't contribute content."""
        # Tags that can be removed if empty
        removable_when_empty = {'div', 'span', 'p', 'section', 'article'}

        # Multiple passes to handle nested empty elements
        for _ in range(3):
            changed = False
            for tag_name in removable_when_empty:
                for element in soup.find_all(tag_name):
                    # Check if element is effectively empty
                    text = element.get_text(strip=True)
                    has_meaningful_children = any(
                        child.name in {'img', 'video', 'audio', 'iframe', 'table', 'pre', 'code'}
                        for child in element.find_all(True)
                    )

                    if not text and not has_meaningful_children:
                        element.decompose()
                        changed = True

            if not changed:
                break

    def _normalize_whitespace(self, soup: BeautifulSoup) -> None:
        """Normalize whitespace in text nodes."""
        for text_node in soup.find_all(string=True):
            if isinstance(text_node, NavigableString):
                # Skip pre/code blocks
                if text_node.parent and text_node.parent.name in {'pre', 'code'}:
                    continue

                # Normalize whitespace
                new_text = ' '.join(text_node.split())
                if new_text != text_node:
                    text_node.replace_with(new_text)

    def _final_cleanup(self, html: str) -> str:
        """Final cleanup of the HTML string."""
        # Remove excessive blank lines
        html = re.sub(r'\n{3,}', '\n\n', html)

        # Remove empty attributes
        html = re.sub(r'\s+(class|id|style)=""', '', html)

        # Clean up spacing around tags
        html = re.sub(r'>\s+<', '>\n<', html)

        return html.strip()


def clean_substack_html(html: str) -> tuple[str, list[dict]]:
    """
    Convenience function to clean Substack HTML.

    Args:
        html: Raw HTML from Substack

    Returns:
        Tuple of (cleaned_html, list_of_image_dicts)
    """
    cleaner = SubstackHTMLCleaner()
    return cleaner.clean(html)


if __name__ == '__main__':
    # Simple test
    test_html = '''
    <div class="post-content">
        <h2>Test Heading</h2>
        <p>This is a paragraph with <strong>bold</strong> text.</p>
        <div class="subscribe-widget">Subscribe now!</div>
        <img src="https://example.com/image.jpg" alt="Test image">
        <script>tracking();</script>
        <p id="3fd9">Medium-style ID paragraph</p>
    </div>
    '''

    cleaned, images = clean_substack_html(test_html)
    print("Cleaned HTML:")
    print(cleaned)
    print("\nImages found:")
    for img in images:
        print(f"  - {img['src']} (alt: {img['alt']})")
