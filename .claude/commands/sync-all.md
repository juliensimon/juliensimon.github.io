---
description: Sync Substack + YouTube + GitHub repo stats + HF dataset count, build, commit, push, and deploy in one go
---

Run a full content sync: fetch new Substack posts, YouTube videos, GitHub repo stats, and Hugging Face dataset count, build the site, commit, push, and monitor deployment.

## Steps

### Phase 1: Substack Sync

1. Dry-run first:
   ```bash
   python3 scripts/sync_substack.py --dry-run
   ```

2. If new posts are detected, run the actual sync:
   ```bash
   python3 scripts/sync_substack.py
   ```

3. Report what was synced (post titles, dates).

### Phase 2: YouTube Sync

4. Dry-run first:
   ```bash
   python3 scripts/sync_youtube.py --dry-run
   ```

5. If new videos are detected, run the actual sync:
   ```bash
   python3 scripts/sync_youtube.py
   ```

6. Report what was synced (video titles, dates).

### Phase 3: GitHub Repo Stats Sync

7. Fetch current stars, forks, and descriptions for all repos in `PINNED_REPOSITORIES`:
   ```bash
   gh api repos/juliensimon/REPO --jq '{stars: .stargazers_count, forks: .forks_count, description: .description}'
   ```

8. If any stats changed, update `next-site/src/data/code.ts` with the new values.

9. Report what changed (or "all stats up to date").

### Phase 4: Hugging Face Dataset Count Sync

10. Fetch the current public dataset count for `juliensimon` from the Hugging Face API:
    ```bash
    python3 -c "import urllib.request, json; r = urllib.request.urlopen('https://huggingface.co/api/datasets?author=juliensimon&limit=1000'); print(len(json.loads(r.read())))"
    ```

11. If the count differs from `TOTAL_DATASETS` in `next-site/src/data/datasets.ts`, update that constant with the new value.

12. Report what changed (or "dataset count up to date").

### Phase 5: Build & Verify

13. Build the site to catch any errors:
    ```bash
    cd next-site && npm run build
    ```

14. If the build fails, fix the issue before proceeding.

### Phase 6: Ship

15. If anything was synced in Phase 1, 2, 3, or 4:
    - Stage all sync-related files (new HTML pages, updated data files, updated index pages)
    - Commit with a message like: `Sync N Substack posts, M YouTube videos, repo stats, and dataset count`
   - Push to origin master
   - Monitor the deployment:
     ```bash
     gh run list --repo juliensimon/juliensimon.github.io --limit 1 --json databaseId --jq '.[0].databaseId'
     ```
     ```bash
     gh run watch <run-id> --repo juliensimon/juliensimon.github.io --exit-status
     ```

16. If nothing new was found in any source, report: "Everything is up to date. No new content to sync."

## Important

- Always dry-run before syncing
- If only one source has new content, still build and ship
- If the deployment fails, investigate with `gh run view <run-id> --log-failed`
- Never skip the build step — broken HTML in sync output can break the deploy
