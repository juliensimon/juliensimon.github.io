#!/bin/sh
# Publish next-site/out to www.julien.org (S3 + CloudFront).
# Usage, from the repo root, after `npm run build` in next-site:  sh infra/deploy.sh [--dry-run]
# Needs AWS credentials for account 631572398268 (see infra/DEPLOY.md).
set -euf   # -f: no shell globbing, the exclude patterns go to aws as written

BUCKET=julien-org-site
DIST=E33LGHPJE58WUF
FN=julien-org-site
OUT=next-site/out
DRY=""
[ "${1:-}" = "--dry-run" ] && DRY="--dryrun"

[ -f "$OUT/index.html" ] || { echo "no build in $OUT: run npm run build in next-site first" >&2; exit 1; }

echo "== guards"
if grep -rIli umami "$OUT" >/dev/null 2>&1; then echo "Umami is still in the build" >&2; exit 1; fi
python3 -I infra/gen_pages.py "$OUT"
node --test infra/test_site_fn.mjs >/dev/null
python3 -I infra/check_csp.py "$OUT"

CC_SHORT="public, max-age=600"
CC_LONG="public, max-age=31536000, immutable"
EXCL="--exclude .DS_Store --exclude */.DS_Store --exclude CNAME --exclude CLAUDE.md --exclude */CLAUDE.md"

echo "== upload"
# 1. everything except the typed groups and the hashed assets
aws s3 sync "$OUT" "s3://$BUCKET" $DRY $EXCL --exclude '_next/static/*' --exclude '*.html' --exclude '*.txt' --exclude '*.md' --exclude feed \
  --cache-control "$CC_SHORT" --delete --only-show-errors
# 2. hashed assets, one year
aws s3 sync "$OUT/_next/static" "s3://$BUCKET/_next/static" $DRY $EXCL --cache-control "$CC_LONG" --only-show-errors
# 3. text types with an explicit charset (GitHub Pages sent one).
#    $EXCL goes LAST: in aws s3 sync the last matching filter wins, and --include '*.md' would re-add CLAUDE.md.
aws s3 sync "$OUT" "s3://$BUCKET" $DRY --exclude '*' --include '*.html' $EXCL --content-type 'text/html; charset=utf-8' --cache-control "$CC_SHORT" --delete --only-show-errors
aws s3 sync "$OUT" "s3://$BUCKET" $DRY --exclude '*' --include '*.txt' $EXCL --content-type 'text/plain; charset=utf-8' --cache-control "$CC_SHORT" --delete --only-show-errors
aws s3 sync "$OUT" "s3://$BUCKET" $DRY --exclude '*' --include '*.md' $EXCL --content-type 'text/markdown; charset=utf-8' --cache-control "$CC_SHORT" --delete --only-show-errors
# 4. the extensionless RSS file
if [ -z "$DRY" ]; then
  aws s3 cp "$OUT/feed" "s3://$BUCKET/feed" --content-type 'application/rss+xml; charset=utf-8' --cache-control "$CC_SHORT" --only-show-errors
fi

if [ -z "$DRY" ]; then
  # Agent instruction files must never be public (claude-mem writes CLAUDE.md into public/ locally).
  if aws s3 ls "s3://$BUCKET" --recursive | grep -q 'CLAUDE\.md$'; then
    echo "CLAUDE.md found in the bucket: remove it with aws s3 rm --recursive --exclude '*' --include '*CLAUDE.md'" >&2
    exit 1
  fi
fi

echo "== routing function"
if [ -z "$DRY" ]; then
  LIVE_ETAG=$(aws cloudfront describe-function --name "$FN" --stage LIVE --query ETag --output text)
  aws cloudfront get-function --name "$FN" --stage LIVE /tmp/julien-org-fn-live.js >/dev/null
  if cmp -s /tmp/julien-org-fn-live.js infra/site-fn.js; then
    echo "function unchanged"
  else
    DEV_ETAG=$(aws cloudfront describe-function --name "$FN" --stage DEVELOPMENT --query ETag --output text)
    NEW_ETAG=$(aws cloudfront update-function --name "$FN" --if-match "$DEV_ETAG" \
      --function-config '{"Comment":"julien.org routing: apex to www; directory index; page routes","Runtime":"cloudfront-js-2.0"}' \
      --function-code fileb://infra/site-fn.js --query ETag --output text)
    aws cloudfront publish-function --name "$FN" --if-match "$NEW_ETAG" >/dev/null
    echo "function updated and published (was $LIVE_ETAG)"
  fi
  rm -f /tmp/julien-org-fn-live.js
fi

if [ -z "$DRY" ]; then
  echo "== invalidate"
  aws cloudfront create-invalidation --distribution-id "$DIST" --paths '/*' --query 'Invalidation.Id' --output text
fi
echo "done"
