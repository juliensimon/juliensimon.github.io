# Design — Medium copyright-image removal

- **Date:** 2026-05-22
- **Status:** Approved design (revised) — pending implementation plan
- **Author:** Julien Simon (with Claude)
- **Related:** `IMAGE_COPYRIGHT_AUDIT.md`, repo commit `06e86a91` (images hidden in repo HTML)

## 1. Background

An audit (`IMAGE_COPYRIGHT_AUDIT.md`) flagged 53 high-risk, likely-copyrighted images
across the legacy and AWS-era Medium blog posts. In the repository, those images were
**hidden** by wrapping their markup in HTML comments (commit `06e86a91`).

The same images also appear in the original posts published on Medium
(`julsimon.medium.com`). On Medium, hiding via HTML comments is not possible — the images
must be **removed** from the live posts. This document specifies that removal.

## 2. Key constraints and what the repo already gives us

Medium has **no API for editing published posts** (the Medium API only ever supported
*creating* posts and was deprecated years ago). The only way to remove an image from a
published Medium post is the **Medium web editor**, so this work is done by **browser
automation** driving a logged-in Medium session.

The repo directory `next-site/public/blog/aws-medium-posts-and-images/` is a **synced copy**
of these Medium posts. This is decisive and simplifies the job:

- **No archiving is needed.** The repo already contains every flagged image file. Reversal
  means re-inserting the image from its existing repo file — there is nothing extra to
  capture, screenshot, or back up.
- **Medium URLs are recoverable from the repo.** The synced post HTML carries Medium post
  URLs of the form `https://medium.com/@julsimon/<slug>-<hash>` (in cross-reference and
  social-share links). A logged-in Stories-dashboard lookup is only a **fallback** for the
  minority of posts whose own URL is not present in their synced HTML.
- On the **live** Medium post, images are served from `miro.medium.com` with hashed URLs —
  no identifier shared with the repo files. So the specific image to delete is located by
  **document position** (the repo numbers images `imageNN.webp` sequentially, so `image04`
  is the 4th image) cross-checked against the audit's **visual description**.

## 3. Scope

### In scope
- The **46 HIGH-risk images** listed in `IMAGE_COPYRIGHT_AUDIT.md` under the section
  `## HIGH risk`, whose paths begin with
  `next-site/public/blog/aws-medium-posts-and-images/` (~36 posts, 2016–2021).

### Out of scope
- The 7 HIGH-risk **legacy** images (2008–2016) — that was a personal blog, never on Medium.
- All **Medium-risk** and **Low-risk** images — scope matches the repo job: HIGH only.
- The repository blog HTML — already completed in commit `06e86a91`.

## 4. Decisions (confirmed with user)

| Decision | Choice |
|---|---|
| Execution method | Full browser automation |
| Removal style | Clean removal — delete the image **and** its caption, no placeholder |
| Failure handling | Skip the problem post, continue, report all skips at the end |
| Approach | Two-phase (Discovery → Execution) with a manual checkpoint after Phase 1 |
| Archiving | None — the repo is the archive (see Section 2) |

## 5. Tooling

Chrome DevTools MCP driving a real Chrome instance. If the user is already logged into
Medium in Chrome, that session is reused; otherwise the user logs in once (magic link or
Google sign-in) — the single unavoidable manual step. The automation confirms the session
by loading the Stories dashboard (`medium.com/me/stories`).

## 6. Architecture — three phases

### Phase 0 — Setup & login
1. Launch / attach to Chrome via Chrome DevTools MCP.
2. Navigate to `medium.com`; user signs in if not already authenticated.
3. Confirm the session by loading `medium.com/me/stories` and detecting the story list.

### Phase 1 — Discovery (read-only, zero edits)
For each audited post:
1. **Resolve the Medium URL** by extracting it from the synced repo `index.html`
   (cross-reference / social-share links). If the post's own URL is not present, fall back
   to a Stories-dashboard lookup by title.
2. Open the published post; enumerate all images in document order.
3. For each flagged ordinal (`imageNN` → N), **visually confirm** the Nth image matches the
   audit description (e.g. "Robby the Robot", "HAL 9000").
4. Record a verdict per flagged image: `confirmed`, `mismatch`, or `not-found`.

**Output:** the manifest (Section 7.1). Posts whose URL cannot be resolved, already-removed
images, and visual mismatches are recorded and **excluded from deletion**. No screenshots or
image copies are committed; any screenshots taken are transient verification aids only.

**Checkpoint:** the manifest summary is presented to the user. Phase 2 does not start
until the user approves.

### Phase 2 — Execution (destructive, per post)
For each post with at least one `confirmed` target:
1. Open the post in Medium's editor.
2. Re-enumerate images in the editor; assert count and order match Phase 1 (guards against
   drift). On mismatch, skip the post and log it.
3. Delete the `confirmed` flagged images **highest-ordinal-first**, so deleting one image
   does not shift the indices of images not yet processed. Deleting an image block removes
   the image together with its caption (clean removal).
4. Save / publish — the edit goes live (Medium has no draft state for a published post).
5. Re-fetch the published post and verify: the targeted images are gone and the remaining
   image count equals `(original count − removed count)`.
6. Update the reversal log entry to `status = removed` with a timestamp.
7. Pace between posts (deliberate delay) to limit bot-throttling.

Any anomaly ⇒ skip the post, continue, collect for the final report.

## 7. Data models

Both files live in `medium-removal-log/` and are committed to git. They contain only text
(URLs, ordinals, captions, descriptions) — no images.

### 7.1 Manifest (`medium-removal-log/manifest.md`)
Phase 1 output. One row per flagged image:

| Field | Description |
|---|---|
| post_folder | Repo folder name of the synced post |
| medium_url | Live Medium URL (resolved in Phase 1) |
| ordinal | 1-based image position in the post (`imageNN` → N) |
| audit_description | Expected content, from `IMAGE_COPYRIGHT_AUDIT.md` |
| medium_caption | Caption text on the Medium post, if any |
| repo_source | Path to the image file in the repo |
| verdict | `confirmed` / `mismatch` / `not-found` / `url-unresolved` |

### 7.2 Reversal log (`medium-removal-log/reversal-log.md`)
Built in Phase 1 from the `confirmed` manifest rows, finalized in Phase 2. One row per
image targeted for removal:

| Field | Description |
|---|---|
| post_title | Title as shown on Medium |
| medium_url | Live Medium URL |
| ordinal | 1-based image position before removal |
| neighbour_context | Brief note on the preceding/following block, to locate the slot on re-insertion |
| caption | Caption text removed with the image |
| repo_source | Repo path to the image file — the bytes needed to restore it |
| status | `pending` / `removed` / `skipped` (with reason) |
| timestamp | When the removal was applied |

The log file header documents the **reversal procedure**: open the post editor → navigate
to the recorded position → insert the image from `repo_source` → re-add the `caption` →
save. Reversal needs no extra archiving because the repo permanently retains every image
file (Section 2).

## 8. Error handling

| Situation | Handling |
|---|---|
| Medium URL cannot be resolved (not in repo HTML, not in dashboard) | Mark `url-unresolved`, skip, report |
| Image already removed / count mismatch | Skip the whole post, log, report |
| Phase-1 visual mismatch | Exclude from deletion, flag for manual review |
| Session expires mid-run | Detected on next action failure; log, report; manual re-login needed |
| Medium editor quirk (cannot select/delete) | Skip the post, log, report |
| Within-post index shift | Prevented by deleting highest-ordinal-first |

## 9. Verification

- **Phase 1:** per-image visual confirmation against the audit description.
- **Phase 2:** post-edit re-fetch — confirm targeted images gone and remaining count correct.
- **Final:** a summary report — images removed, posts skipped (with reasons), and the
  complete committed reversal log.

## 10. Deliverables

1. `medium-removal-log/manifest.md` — Phase 1 verified manifest.
2. `medium-removal-log/reversal-log.md` — committed reversal log.
3. A final summary report of removals and skips.

## 11. Risks

- **Medium Terms of Service:** automating the Medium editor may breach Medium's automation
  terms. The user has opted into full automation knowingly.
- **Bot detection** may interrupt the run; skip-and-continue plus the final report absorb
  partial completion, and the run can be resumed.
- **Medium's editor DOM is undocumented** and may change; selectors are best-effort. Phase 1
  verification and Phase 2 post-edit re-checks exist precisely to catch this.

## 12. Assumptions

- The repo `aws-medium-posts-and-images/` is a faithful synced copy of the Medium posts —
  same images in the same order — so it serves as both the image archive and the source of
  Medium URLs.
- The repo numbers `imageNN.webp` in the same order images appear in the published post.
  If false for a given post, Phase 1's visual check catches it as a `mismatch`.
- All target posts are editable under the `julsimon.medium.com` account. Posts published
  under a Medium publication are still author-editable; posts not found are skipped.
