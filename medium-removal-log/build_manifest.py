#!/usr/bin/env python3
"""Parse IMAGE_COPYRIGHT_AUDIT.md HIGH-risk section -> manifest.md skeleton.
Only rows under aws-medium-posts-and-images/ are included (Medium scope)."""
import re
import pathlib

audit = pathlib.Path("IMAGE_COPYRIGHT_AUDIT.md").read_text(encoding="utf-8")

# Isolate the HIGH-risk section only
high = audit.split("## HIGH risk", 1)[1].split("## MEDIUM risk", 1)[0]

rows = []
for line in high.splitlines():
    if "aws-medium-posts-and-images" not in line or ".webp" not in line:
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    path = cells[0]
    desc = cells[1] if len(cells) > 1 else ""
    m = re.search(
        r"aws-medium-posts-and-images/\d+/([^/]+)/image(\d+)\.webp", path
    )
    if not m:
        continue
    folder, ordinal = m.group(1), int(m.group(2))
    rows.append({"folder": folder, "ordinal": ordinal,
                 "desc": desc, "repo_source": path})

rows.sort(key=lambda r: (r["folder"], r["ordinal"]))

out = ["# Medium Removal Manifest",
       "",
       f"Generated from IMAGE_COPYRIGHT_AUDIT.md — {len(rows)} HIGH-risk Medium images.",
       "",
       "| post_folder | medium_url | ordinal | audit_description | medium_caption | repo_source | verdict |",
       "|---|---|---|---|---|---|---|"]
for r in rows:
    out.append(
        f"| {r['folder']} |  | {r['ordinal']} | {r['desc']} |  | {r['repo_source']} | pending |"
    )
pathlib.Path("medium-removal-log/manifest.md").write_text(
    "\n".join(out) + "\n", encoding="utf-8")
print(f"Wrote medium-removal-log/manifest.md with {len(rows)} rows")
