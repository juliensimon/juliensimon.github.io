# Medium Copyright-Image Removal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. This plan drives a **single persistent authenticated browser session** — execute it inline, not via fresh subagents (a new subagent would lose the Medium login).

**Goal:** Remove the 46 HIGH-risk copyright images from the live Medium posts on `julsimon.medium.com`, with a committed reversal log.

**Architecture:** Two phases driven by Chrome DevTools MCP against a logged-in Medium session. Phase 1 (read-only) resolves each post's Medium URL from the synced repo HTML and visually confirms each flagged image at its expected position, producing a manifest. After a user checkpoint, Phase 2 opens each post in Medium's editor and deletes the confirmed images highest-ordinal-first, then verifies. The repo's `aws-medium-posts-and-images/` is the permanent image archive — reversal re-inserts from there.

**Tech Stack:** Chrome DevTools MCP (browser automation), Python 3 (audit parsing), Bash/git. No application code or test suite — verification is visual confirmation and post-edit re-checks.

---

## File Structure

- Create: `medium-removal-log/build_manifest.py` — one-off parser, audit → manifest skeleton
- Create: `medium-removal-log/manifest.md` — Phase 1 working doc (target list + verdicts)
- Create: `medium-removal-log/reversal-log.md` — committed reversal record
- Create: `medium-removal-log/final-report.md` — end-of-run summary
- Read-only: `IMAGE_COPYRIGHT_AUDIT.md`, `next-site/public/blog/aws-medium-posts-and-images/**/index.html`

---

## Task 1: Scaffold the log directory and build the manifest skeleton

**Files:**
- Create: `medium-removal-log/build_manifest.py`
- Create: `medium-removal-log/manifest.md` (generated)

- [ ] **Step 1: Create the directory**

```bash
mkdir -p medium-removal-log
```

- [ ] **Step 2: Write the audit parser**

Create `medium-removal-log/build_manifest.py`:

```python
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
```

- [ ] **Step 3: Run the parser**

Run: `python3 medium-removal-log/build_manifest.py`
Expected: `Wrote medium-removal-log/manifest.md with 46 rows`

- [ ] **Step 4: Verify the row count**

Run: `grep -c '| pending |' medium-removal-log/manifest.md`
Expected: `46`

If the count is not 46, stop — the audit file's HIGH-risk Medium tables changed since the spec. Reconcile against `IMAGE_COPYRIGHT_AUDIT.md` before continuing.

- [ ] **Step 5: Commit**

```bash
git add medium-removal-log/build_manifest.py medium-removal-log/manifest.md
git commit -m "medium-removal: scaffold log dir and manifest skeleton (46 images)"
```

---

## Task 2: Phase 0 — open the browser and confirm the Medium session

**Files:** none (browser state only).

- [ ] **Step 1: Open Medium**

Use Chrome DevTools MCP: open a new page and navigate to `https://medium.com/me/stories`.

- [ ] **Step 2: Confirm login (manual step for the user)**

Take a snapshot of the page. Two outcomes:
- The page shows a story list ("Your stories" / "Published" tab) → session is active, continue.
- The page shows a sign-in prompt → ask the user to log into Medium in that browser window (magic link or Google), then re-snapshot.

- [ ] **Step 3: Verify the Stories dashboard is reachable**

Confirm the snapshot of `medium.com/me/stories` contains the published-stories list. This dashboard is the fallback URL source for Task 4. Do not proceed to Task 3 until a logged-in dashboard is confirmed.

---

## Task 3: Phase 1 calibration — establish the image-enumeration method

**Files:** none (calibration; the working snippet is recorded below).

Use the post `2017-04-05_Fascinating-Tales-of-a-Strange-Tomorrow` (5 flagged images — a good calibration case).

- [ ] **Step 1: Resolve this post's Medium URL from the repo HTML**

Run:

```bash
grep -oE 'medium\.com/(%40|@)julsimon/[a-z0-9-]+' \
  "next-site/public/blog/aws-medium-posts-and-images/2017/2017-04-05_Fascinating-Tales-of-a-Strange-Tomorrow/index.html" \
  | sed 's/%40/@/' | sort -u
```

Expected: one or more `medium.com/@julsimon/<slug>-<hash>` strings. The post's **own** URL is the one whose slug matches the post title (`fascinating-tales-of-a-strange-tomorrow-...`); others are cross-references. Prefer the slug embedded in a `facebook.com/sharer` or `twitter.com/...status=` link in that file — share links always carry the current post's own URL.

- [ ] **Step 2: Open the post on Medium**

Navigate the browser to `https://<resolved-url>`. Confirm the page is the article (title matches "Fascinating Tales of a Strange Tomorrow").

- [ ] **Step 3: Enumerate images in document order**

Run this via Chrome DevTools MCP `evaluate_script`:

```js
JSON.stringify(
  [...document.querySelectorAll('article figure')].map((f, i) => ({
    ordinal: i + 1,
    src: f.querySelector('img')?.currentSrc || f.querySelector('img')?.src || null,
    caption: f.querySelector('figcaption')?.innerText?.trim() || ''
  })), null, 1)
```

Expected: a JSON array of image entries in document order.

- [ ] **Step 4: Validate the enumeration against the audit**

The audit flags ordinals 1, 4, 6, 7, 9 for this post. Confirm the array has at least 9 entries and that `take_screenshot` of entries 1/4/6/7/9 visually matches the audit descriptions (Robby the Robot; Marvin Minsky; "I, Robot" book cover; Arthur C. Clarke; HAL 9000).

If the `article figure` selector returns an empty or wrong-length array, adjust the selector (try `section figure`, or `figure` scoped to the post body) until enumeration is stable, and record the working selector here before continuing:

> **Working enumeration selector (fill in during calibration):** `article figure`

---

## Task 4: Phase 1 discovery — resolve URLs and confirm every flagged image

**Files:**
- Modify: `medium-removal-log/manifest.md` (fill `medium_url`, `medium_caption`, `verdict`)

Process posts grouped by `post_folder`. For each distinct folder in `manifest.md`:

- [ ] **Step 1: Resolve the Medium URL**

Run the Step-1 grep from Task 3 against that folder's `index.html`. Pick the post's own URL (slug matches the folder's title; prefer the slug inside a share link).
- If no `medium.com/@julsimon/...` URL is found, search the Stories dashboard (`medium.com/me/stories`) for the post by title and read its URL.
- If still unresolved, set `verdict = url-unresolved` for every row of this post and skip to the next folder.

- [ ] **Step 2: Open the post and enumerate images**

Navigate to the resolved URL. Run the Task 3 Step 3 enumeration snippet. Record the total image count.

- [ ] **Step 3: Confirm each flagged ordinal**

For each manifest row of this post, `take_screenshot` of the image at that ordinal and compare to `audit_description`:
- Matches → `verdict = confirmed`; fill `medium_caption` from the enumeration's `caption` field.
- Wrong content → `verdict = mismatch`.
- That ordinal does not exist / no image there → `verdict = not-found`.

- [ ] **Step 4: Write the verdicts into the manifest**

Edit `medium-removal-log/manifest.md`, filling `medium_url`, `medium_caption`, and `verdict` for every row of this post.

- [ ] **Step 5: Commit after every ~10 posts**

```bash
git add medium-removal-log/manifest.md
git commit -m "medium-removal: Phase 1 discovery progress"
```

- [ ] **Step 6: Final discovery commit**

After all folders are processed:

```bash
git add medium-removal-log/manifest.md
git commit -m "medium-removal: Phase 1 discovery complete"
```

Run: `grep -c '| confirmed |' medium-removal-log/manifest.md` — note the confirmed count for the checkpoint.

---

## Task 5: Checkpoint — build the reversal log and get user approval

**Files:**
- Create: `medium-removal-log/reversal-log.md`

- [ ] **Step 1: Generate the reversal-log skeleton from confirmed rows**

Create `medium-removal-log/reversal-log.md` with this header and one row per `confirmed` manifest row:

```markdown
# Medium Image Removal — Reversal Log

Each row records an image removed from a live Medium post.

**To reverse a removal:** open the post at `medium_url` in Medium's editor,
navigate to the position described by `ordinal` / `neighbour_context`, insert
the image from `repo_source` (the file still exists in this repo), re-add the
`caption` text, and save. No image data was discarded — `repo_source` is the
permanent archive.

| post_title | medium_url | ordinal | neighbour_context | caption | repo_source | status | timestamp |
|---|---|---|---|---|---|---|---|
```

Populate `post_title`, `medium_url`, `ordinal`, `caption`, `repo_source` from the
manifest; set `neighbour_context` to a short note (e.g. "after heading 'The AI Winter'"),
`status = pending`, `timestamp` blank.

- [ ] **Step 2: Commit the skeleton**

```bash
git add medium-removal-log/reversal-log.md
git commit -m "medium-removal: reversal-log skeleton from confirmed targets"
```

- [ ] **Step 3: Present the checkpoint summary to the user**

Report: number of `confirmed` images and posts; list every `mismatch`, `not-found`, and
`url-unresolved` row with its reason. State that Phase 2 will make destructive live edits.

- [ ] **Step 4: STOP — wait for explicit user approval**

Do not start Task 6 until the user approves the manifest. If the user requests changes,
update `manifest.md` / `reversal-log.md` accordingly and re-present.

---

## Task 6: Phase 2 calibration — establish the editor delete-and-save method

**Files:** none (calibration; record the working method below).

Use the first `confirmed` post from the reversal log.

- [ ] **Step 1: Open the post in the Medium editor**

Navigate to the post, then to its editor. The editor URL is the post URL with `/edit`
appended, or reached via the "..." menu → "Edit story" on the post page. Confirm the
editor loaded (the body is contentEditable; an editing toolbar is present).

- [ ] **Step 2: Enumerate images in the editor**

Run the Task 3 Step 3 enumeration snippet in the editor page. Confirm the count and order
match what Phase 1 recorded for this post. If they differ, this post must be `skipped` —
record that and pick the next confirmed post for calibration.

- [ ] **Step 3: Select and delete one image**

For the highest flagged ordinal in this post: `click` the image element to select it
(Medium shows a selected image with a highlight/outline), then `press_key` `Backspace`.
Re-run the enumeration snippet — the image count must drop by exactly 1 and the target
image must be gone. Confirm the caption went with it.

If `click` + `Backspace` does not delete the figure, try: click the image, then use the
image's own delete control if Medium shows one on hover. Record the working method here:

> **Working delete method (fill in during calibration):** click image + Backspace

- [ ] **Step 4: Determine and perform the save/publish action**

Identify how the editor commits changes to the live post (a "Publish" / "Save and publish"
control, or an autosave + publish-changes flow). Perform it. Record the working method:

> **Working save method (fill in during calibration):** _____

- [ ] **Step 5: Verify the live post**

Navigate to the public post URL (not the editor), re-run the enumeration snippet, and
confirm the deleted image is absent and the remaining count is `original − 1`.

- [ ] **Step 6: Update the reversal log for this image**

In `reversal-log.md`, set this image's row to `status = removed` and fill `timestamp`
(UTC, ISO 8601). Commit:

```bash
git add medium-removal-log/reversal-log.md
git commit -m "medium-removal: Phase 2 calibration post complete"
```

---

## Task 7: Phase 2 execution — remove confirmed images post by post

**Files:**
- Modify: `medium-removal-log/reversal-log.md` (status + timestamp per image)

For each remaining post with `confirmed` images (skip the post already done in Task 6):

- [ ] **Step 1: Open the editor and re-enumerate**

Open the post's editor. Run the enumeration snippet. Assert the image count and order
match Phase 1. On any mismatch: set every remaining row of this post to
`status = skipped (count mismatch)`, and move to the next post.

- [ ] **Step 2: Delete flagged images, highest ordinal first**

Sort this post's confirmed ordinals descending. For each: select the image (Task 6 Step 3
working method), `press_key` `Backspace`, re-run enumeration to confirm the count dropped
by 1. Deleting highest-first keeps lower ordinals valid.

- [ ] **Step 3: Save / publish**

Perform the Task 6 Step 4 working save method.

- [ ] **Step 4: Verify the live post**

Navigate to the public post URL, re-run enumeration, confirm all targeted images are gone
and the remaining count is `original − removed`. On failure: set the affected rows to
`status = skipped (verification failed)` and note it.

- [ ] **Step 5: Update the reversal log and commit**

Set each removed image's row to `status = removed` with a `timestamp`. Commit per post:

```bash
git add medium-removal-log/reversal-log.md
git commit -m "medium-removal: remove images from <post_folder>"
```

- [ ] **Step 6: Pace the run**

Wait ~10–20 seconds between posts to reduce bot-throttling risk. If Medium shows a
challenge or the session drops, stop, record progress, and report — the run resumes from
the first `pending` row.

---

## Task 8: Final report

**Files:**
- Create: `medium-removal-log/final-report.md`

- [ ] **Step 1: Tally results from the reversal log**

Run:

```bash
echo "removed: $(grep -c '| removed |' medium-removal-log/reversal-log.md)"
echo "skipped: $(grep -c '| skipped' medium-removal-log/reversal-log.md)"
echo "pending: $(grep -c '| pending |' medium-removal-log/reversal-log.md)"
```

- [ ] **Step 2: Write the final report**

Create `medium-removal-log/final-report.md`: total images removed; posts fully processed;
every skipped image with its reason (count mismatch, verification failed, url-unresolved,
mismatch, not-found); and a pointer to `reversal-log.md` for the reversal procedure.

- [ ] **Step 3: Commit**

```bash
git add medium-removal-log/final-report.md
git commit -m "medium-removal: final report"
```

- [ ] **Step 4: Report to the user**

Summarize: images removed, posts skipped with reasons, and confirm the reversal log is
committed. Flag any `url-unresolved` / `mismatch` / `not-found` rows as needing manual
attention.

---

## Self-review notes

- **Spec coverage:** Phase 0 → Task 2; Phase 1 → Tasks 3–4; checkpoint → Task 5; Phase 2 →
  Tasks 6–7; verification → Steps in Tasks 4/6/7; reversal log → Tasks 5/7; final report →
  Task 8. Scope (46 HIGH Medium images) → Task 1 Step 4 asserts the count.
- **No archiving / no screenshots committed** — consistent with the revised spec; only
  `manifest.md`, `reversal-log.md`, `final-report.md`, and the parser script are committed.
- **Highest-ordinal-first deletion** is specified in Tasks 6 Step 3 and 7 Step 2 to avoid
  index shift.
- **Undocumented Medium DOM** is handled by calibration Tasks 3 and 6, which record the
  working selectors/methods reused by Tasks 4 and 7.
