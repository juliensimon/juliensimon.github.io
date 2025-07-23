# Blog Processing Scripts

This directory contains the essential scripts used to process and organize legacy blog posts from an Atom feed.

## Overview

These scripts were developed to extract, download, and organize a complete blog archive from an Atom XML feed, converting it into a self-contained, organized collection of HTML files with local images.

## Scripts

### 1. `extract_blog_posts.py`
**Purpose:** Extract all blog posts from an Atom XML feed to individual HTML files.

**Features:**
- Parses Atom XML feed format
- Extracts posts with proper date formatting (YYYY-MM-DD)
- Cleans HTML content and wraps code blocks
- Creates styled HTML files with embedded CSS
- Handles image centering and responsive design

**Usage:**
```bash
python extract_blog_posts.py
```

**Requirements:**
- `feed.atom` file in `blog/legacy-posts/` directory
- Python 3.6+

**Output:**
- Individual HTML files in `blog/legacy-posts-and-images/`
- Files named as `YYYY-MM-DD-title.html`

### 2. `download_images.py`
**Purpose:** Download Blogger/Blogspot images and convert to WebP format.

**Features:**
- Smart URL resolution for old blogger image formats
- Handles `/s1600-h/` URL issues with automatic fallbacks
- Converts images to WebP format for better compression
- Per-post image numbering (`post-title-image-01.webp`)
- Updates HTML files to use local image references
- Comprehensive error handling and retry logic

**Usage:**
```bash
python download_images.py
```

**Requirements:**
- Python 3.6+
- `pip install Pillow requests`
- HTML files already extracted

**Output:**
- WebP images saved alongside HTML files
- Updated HTML files with local image references

### 3. `organize_by_year.py`
**Purpose:** Organize blog posts into year-based folders with navigation.

**Features:**
- Organizes posts by year (2008-2016)
- Moves associated images to correct year folders
- Creates beautiful index pages for each year
- Generates main archive index with year overview
- Responsive design with modern CSS styling
- Clean navigation between years

**Usage:**
```bash
python organize_by_year.py
```

**Requirements:**
- Python 3.6+
- Blog posts already extracted

**Output:**
- Year-based folder structure
- Index pages with navigation
- Organized archive ready for deployment

### 4. `fix_image_references.py`
**Purpose:** Comprehensive maintenance tool for image references and cleanup.

**Features:**
- **HREF/SRC Mismatch Detection:** Finds cases where `<a href="image-X.webp"><img src="image-Y.webp">` point to different images
- **Unused Image Cleanup:** Removes orphaned image files not referenced in any HTML
- **Duplicate Detection:** Optional SHA256 hash-based duplicate image identification
- **Dry-run Mode:** Preview changes without making modifications
- **Year-by-year Processing:** Organized analysis with detailed reporting
- **Safe Operation:** Robust error handling and progress reporting

**Usage:**
```bash
# Fix all issues:
python fix_image_references.py

# Preview changes without making them:
python fix_image_references.py --dry-run

# Include duplicate detection:
python fix_image_references.py --check-duplicates
```

**Requirements:**
- Python 3.6+
- hashlib, re, pathlib (built-in)
- Blog posts already organized

**Output:**
- Fixed HREF/SRC mismatches for consistent image links
- Removed unused/orphaned image files
- Detailed report of changes made per year
- Optional duplicate image detection and removal

## Complete Workflow

To process a complete blog archive from scratch:

1. **Extract Posts:**
   ```bash
   python extract_blog_posts.py
   ```

2. **Download Images:**
   ```bash
   python download_images.py
   ```

3. **Organize by Year:**
   ```bash
   python organize_by_year.py
   ```

4. **Fix Image References (Maintenance):**
   ```bash
   python fix_image_references.py
   # Or preview changes without making them:
   python fix_image_references.py --dry-run
   # Include duplicate detection:
   python fix_image_references.py --check-duplicates
   ```

## Technical Details

### Image Processing
- **WebP Conversion:** All images are converted to WebP format for ~30% smaller file sizes
- **URL Resolution:** Handles old Blogger URL formats that return HTML instead of images
- **Naming Convention:** Images named as `YYYY-MM-DD-post-title-image-01.webp`

### HTML Generation
- **Embedded CSS:** All styling is embedded for self-contained files
- **Image Centering:** All images are centered with no text wrapping
- **Responsive Design:** Works on desktop and mobile devices
- **Clean Typography:** Professional styling with proper hierarchy

### Organization
- **Year-based Structure:** Posts organized into folders by year
- **Navigation:** Beautiful index pages with year overview
- **Self-contained:** No external dependencies after processing

## File Structure After Processing

```
blog/legacy-posts-and-images/
├── index.html                 # Main archive index
├── 2007/
│   ├── index.html            # Year index
│   ├── 2007-05-10-post.html # Individual posts
│   └── *.webp               # Local images
├── 2008/
│   ├── index.html
│   ├── *.html
│   └── *.webp
...
└── 2016/
    ├── index.html
    ├── *.html
    └── *.webp
```

## Statistics

From the original processing:
- **90 blog posts** extracted spanning 2008-2016
- **275 images** downloaded and converted to WebP
- **9 year directories** created with index pages
- **15 duplicate images** identified and cleaned up
- **~13MB total size** for complete archive
- **100% local** - no external dependencies

### Posts by Year:
- **2008**: 8 posts
- **2009**: 11 posts
- **2010**: 9 posts
- **2011**: 5 posts
- **2012**: 13 posts
- **2013**: 25 posts
- **2014**: 2 posts
- **2015**: 16 posts
- **2016**: 1 post

## Error Handling

All scripts include comprehensive error handling:
- Network timeouts and retries for image downloads
- Malformed XML graceful handling
- File system permission errors
- Invalid image format detection
- Progress reporting and detailed logging

## Dependencies

- **Python 3.6+**
- **Pillow (PIL):** Image processing and WebP conversion
- **requests:** HTTP requests for image downloads
- **Built-in modules:** xml.etree.ElementTree, pathlib, shutil, re

## Notes

- Scripts are designed to be idempotent (safe to run multiple times)
- Images are skipped if they already exist locally
- HTML files are overwritten with updated content
- All scripts include progress indicators and detailed logging
- Memory efficient - processes files one at a time 