#!/usr/bin/env python3
"""Build the human-executable removal checklist and the reversal log from
manifest.md. No browser needed — titles come from the synced repo HTML."""
import re
import html
import pathlib

manifest = pathlib.Path("medium-removal-log/manifest.md").read_text(encoding="utf-8")

# Parse manifest data rows: post_folder | medium_url | ordinal |
# audit_description | medium_caption | repo_source | verdict
posts = {}
for line in manifest.splitlines():
    if not line.startswith("| ") or "aws-medium-posts-and-images" not in line:
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    folder, _url, ordinal, desc, _cap, repo_source, _verdict = cells
    p = posts.setdefault(folder, {"images": [], "repo_any": repo_source})
    p["images"].append((int(ordinal), desc, repo_source))


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


checklist = [
    "# Medium Image Removal — Checklist",
    "",
    "Execute in your normal browser, logged into Medium. For each post below:",
    "open it, enter the editor, **confirm** each listed image matches its",
    "description, delete it, then save/publish. Delete images **highest number",
    "first** so earlier positions don't shift. Image # = position in the post",
    "(1 = first image). The post link is a best-effort slug URL — if it 404s,",
    "find the post by title in your Stories list.",
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

total_images = 0
for folder in sorted(posts):
    p = posts[folder]
    idx = pathlib.Path(p["repo_any"]).parent / "index.html"
    title = folder
    if idx.exists():
        m = re.search(r"<title>(.*?)</title>", idx.read_text(encoding="utf-8"), re.S)
        if m:
            title = html.unescape(m.group(1).strip())
    date = folder[:10]
    url = "https://julsimon.medium.com/" + slugify(title)
    imgs_desc = sorted(p["images"], key=lambda x: -x[0])  # highest first

    checklist.append(f"## {title}")
    checklist.append(f"- Date: {date} | Post: [{url}]({url})")
    checklist.append(f"- Remove {len(imgs_desc)} image(s), highest # first:")
    for ordn, desc, _src in imgs_desc:
        checklist.append(f"  - [ ] Image #{ordn} — {desc}")
    checklist.append("  - [ ] Post saved / published")
    checklist.append("")

    for ordn, desc, src in sorted(p["images"], key=lambda x: x[0]):
        reversal.append(f"| {title} | {url} | {ordn} | {desc} | {src} | pending |")
        total_images += 1

pathlib.Path("medium-removal-log/checklist.md").write_text(
    "\n".join(checklist) + "\n", encoding="utf-8")
pathlib.Path("medium-removal-log/reversal-log.md").write_text(
    "\n".join(reversal) + "\n", encoding="utf-8")
print(f"checklist: {len(posts)} posts | reversal-log: {total_images} images")
