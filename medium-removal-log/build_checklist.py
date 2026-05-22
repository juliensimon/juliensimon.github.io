#!/usr/bin/env python3
"""Build the human-executable removal checklist and reversal log from
manifest.md.

Real Medium URLs are resolved by harvesting cross-reference and share links
out of the synced repo HTML (Medium itself is unreachable behind Cloudflare,
and a guessed julsimon.medium.com/<slug> 404s for posts published under a
Medium publication). Posts whose URL cannot be harvested are listed without a
link, to be found by title in the Medium Stories dashboard.
"""
import re
import html
import glob
import pathlib
import urllib.parse

REPO_MEDIUM = "next-site/public/blog/aws-medium-posts-and-images"
HASH = r"[0-9a-f]{12}"  # Medium post IDs are 12 hex chars
URL_PATTERNS = [
    re.compile(r"https?://medium\.com/(?:@[\w.]+|[\w-]+)/([\w-]+?)-" + HASH + r"\b"),
    re.compile(r"https?://[\w-]+\.medium\.com/([\w-]+?)-" + HASH + r"\b"),
]


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def harvest_real_urls():
    """slug -> real Medium URL, harvested from every synced post's HTML."""
    slug_to_url = {}
    for idx in glob.glob(f"{REPO_MEDIUM}/**/index.html", recursive=True):
        text = html.unescape(
            pathlib.Path(idx).read_text(encoding="utf-8", errors="ignore"))
        for _ in range(2):  # share links can be double URL-encoded
            text = urllib.parse.unquote(text)
        for pattern in URL_PATTERNS:
            for m in pattern.finditer(text):
                slug_to_url.setdefault(m.group(1), m.group(0))
    return slug_to_url


# --- Parse manifest ----------------------------------------------------------
manifest = pathlib.Path("medium-removal-log/manifest.md").read_text(encoding="utf-8")
posts = {}
for line in manifest.splitlines():
    if not line.startswith("| ") or "aws-medium-posts-and-images" not in line:
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    folder, _url, ordinal, desc, _cap, repo_source, _verdict = cells
    p = posts.setdefault(folder, {"images": [], "repo_any": repo_source})
    p["images"].append((int(ordinal), desc, repo_source))

slug_to_url = harvest_real_urls()

# --- Build outputs -----------------------------------------------------------
checklist = [
    "# Medium Image Removal — Checklist",
    "",
    "Execute in your normal browser, logged into Medium. For each post below:",
    "open it, enter the editor, **confirm** each listed image matches its",
    "description, delete it, then save/publish. Delete images **highest number",
    "first** so earlier positions don't shift. Image # = position in the post",
    "(1 = first image).",
    "",
    "Posts marked **(find by title)** had no link harvestable from the repo —",
    "open them from your Medium Stories dashboard by searching the title.",
    "",
]
reversal = [
    "# Medium Image Removal — Reversal Log",
    "",
    "Record of images removed from live Medium posts. To restore one: open the",
    "post editor, go to the image's position, insert the file from `repo_source`",
    "(it still exists in this repo), re-add the caption, save.",
    "",
    "| post_title | medium_url | ordinal | audit_description | repo_source | status |",
    "|---|---|---|---|---|---|",
]

total_images = resolved = 0
for folder in sorted(posts):
    p = posts[folder]
    idx = pathlib.Path(p["repo_any"]).parent / "index.html"
    title = folder
    if idx.exists():
        m = re.search(r"<title>(.*?)</title>", idx.read_text(encoding="utf-8"), re.S)
        if m:
            title = html.unescape(m.group(1).strip())
    date = folder[:10]
    url = slug_to_url.get(slugify(title))
    if url:
        resolved += 1
        post_field = f"[{url}]({url})"
        rev_url = url
    else:
        post_field = "**(find by title)**"
        rev_url = "(find by title)"
    imgs_desc = sorted(p["images"], key=lambda x: -x[0])  # highest first

    checklist.append(f"## {title}")
    checklist.append(f"- Date: {date} | Post: {post_field}")
    checklist.append(f"- Remove {len(imgs_desc)} image(s), highest # first:")
    for ordn, desc, _src in imgs_desc:
        checklist.append(f"  - [ ] Image #{ordn} — {desc}")
    checklist.append("  - [ ] Post saved / published")
    checklist.append("")

    for ordn, desc, src in sorted(p["images"], key=lambda x: x[0]):
        reversal.append(f"| {title} | {rev_url} | {ordn} | {desc} | {src} | pending |")
        total_images += 1

pathlib.Path("medium-removal-log/checklist.md").write_text(
    "\n".join(checklist) + "\n", encoding="utf-8")
pathlib.Path("medium-removal-log/reversal-log.md").write_text(
    "\n".join(reversal) + "\n", encoding="utf-8")
print(f"checklist: {len(posts)} posts ({resolved} URLs resolved, "
      f"{len(posts) - resolved} need find-by-title) | "
      f"reversal-log: {total_images} images")
