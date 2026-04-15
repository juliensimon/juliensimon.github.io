---
description: Sync GitHub stars, forks, and descriptions for repos listed in the code section
---

Fetch current stars, forks, and descriptions from GitHub for every repository in `PINNED_REPOSITORIES` and update `next-site/src/data/code.ts`.

**GitHub is the source of truth** for `stars`, `forks`, and `description`. Any drift in `code.ts` must be overwritten to match the API response exactly — including cosmetic differences like trailing punctuation, capitalization, or whitespace. Do not treat those as "cosmetic and skippable".

## Steps

1. Read `next-site/src/data/code.ts` to get the current list of repositories.

2. For each repository, extract the owner/repo from its `url` field and fetch stats from the GitHub API:
   ```bash
   gh api repos/OWNER/REPO --jq '{stars: .stargazers_count, forks: .forks_count, description: .description}'
   ```

3. Compare fetched values against the current data file. Report a table of changes:
   ```
   Repo                              Stars  Forks  Description Changed
   starlink-viz                      8→12   1→2    no
   cache-commander                   11→11  1→1    no
   ```

4. If there are changes, update `next-site/src/data/code.ts`:
   - Update `stars` and `forks` values to match GitHub exactly
   - Update `description` to match GitHub verbatim (including trailing punctuation and whitespace). The only exception: skip the description update if GitHub returns an empty/null description — never overwrite a non-empty description with an empty string.
   - Preserve all other fields (name, url, language, tags) exactly as they are

5. Build and verify:
   ```bash
   cd next-site && npm run build
   ```

6. If changes were made, commit and push:
   - Commit message: `Sync GitHub repo stats: stars and forks`
   - Push and monitor deployment

7. If nothing changed, report: "All repo stats are up to date."

## Important

- Never overwrite a description with an empty string
- Preserve the exact TypeScript formatting of `code.ts`
- Only update numeric stats and descriptions — never change tags, language, or URL
- GitHub is the source of truth: do not skip description diffs because they "look cosmetic"
