# Hosting for www.julien.org (S3 + CloudFront)

Why: GitHub Pages cannot send response headers, so Aikido flagged a missing HSTS and CSP header
(2026-11-26). CloudFront adds them. AWS account 631572398268.

| Part | Id |
|---|---|
| Bucket (eu-west-1, private, read by CloudFront only) | `julien-org-site` |
| Distribution | `E33LGHPJE58WUF`, `d3tepxum7uc9z1.cloudfront.net` |
| Routing function (apex to www, `/dir` to `/dir/`, `/dir/` to index, page routes) | `julien-org-site`, source `site-fn.js` |
| Headers policy (HSTS, CSP, nosniff, frame DENY, referrer, permissions) | `julien-org-security`, `84a492de-1008-497f-a397-98ba3329f4a3`, source `headers-policy.json` |
| Certificate (us-east-1, julien.org and www) | `1cb5998c-88e4-484f-88f9-9cb58ef68676` |
| Route 53 zone | `Z049260635GEX3HDSX4EH`, copy of the Squarespace zone, checked record by record on 2026-11-26 |

## Publish

```sh
cd next-site && npm run build && cd ..
sh infra/deploy.sh --dry-run     # lists changes
sh infra/deploy.sh
```

The script refuses to run if the build holds Umami or a host the CSP blocks, runs the function
tests, uploads with the right cache and content types, refuses if a `CLAUDE.md` is in the bucket,
updates the function when `site-fn.js` changed, and clears the cache.

Edit the headers policy: change `headers-policy.json`, then
`aws cloudfront update-response-headers-policy --id <id> --if-match <etag> --response-headers-policy-config file://infra/headers-policy.json`.
After any CSP change, load these pages in a browser and read the console: `/`, `/speaking` (map),
a Gist post, a YouTube-embed post, `/podcast`. The static check `check_csp.py` cannot see what a
script fetches at run time (it missed the Umami and Hugging Face redirect hosts once).

## Checks

- `node --test infra/test_site_fn.mjs` (routing function)
- `python3 -I infra/test_migrate_analytics.py`
- `python3 -I infra/check_csp.py next-site/out`
- `python3 -I infra/gen_pages.py next-site/out` (rewrites the page list in `site-fn.js`)

## Analytics

Cloudflare Web Analytics, site `www.julien.org` (created 2026-11-26). The token is public and sits
in `next-site/src/lib/constants.ts` and in every page. Umami was removed from the pages, the layout
and the generators. `infra/migrate_analytics.py` swaps the tag in static pages.

## Choices

- HSTS is `max-age=31536000` with no `includeSubDomains`: `erebor` and `teleport` may not be HTTPS only.
- `script-src` keeps `'unsafe-inline'`: the Next.js export puts its data in inline scripts.
- An unknown path such as `/nope` is a 301 to `/nope/` and then a 404 (GitHub Pages gave a 404 at once).
- `archive/` is not deployed and still mentions Umami.

## DNS (zone moved from Squarespace to Route 53)

julien.org had DNSSEC on (DS 38282 at .org). Moving to an unsigned zone with the DS left in place
breaks resolution for validating resolvers, so the order is fixed:

1. DNSSEC off at Squarespace (done 2026-11-26 11:46Z).
2. Wait until the DS has left `.org` (`dig DS julien.org @a0.org.afilias-nst.info`) and then 1 hour for resolver caches.
3. Set the nameservers at Squarespace to the four Route 53 servers of the zone.
4. The ACM validation CNAMEs are already in the Route 53 zone; wait for the certificate to be ISSUED.
5. Attach `julien.org` and `www.julien.org` plus the certificate to the distribution; in Route 53 replace the apex A records and the `www` CNAME with alias records to the distribution.
6. Check headers on both hosts, mail (`dig MX`, send a test mail) and the other subdomains.
7. Enable DNSSEC signing in Route 53 (KMS key in us-east-1, key-signing key) and publish the new DS at Squarespace, as for solfird.ai.

### Done 2026-11-26 (log)

- 11:46Z DNSSEC off at Squarespace; DS gone from `.org` by 13:57Z; nameservers switched to Route 53 at 15:02Z.
- The first ACM certificate FAILED with `CAA_ERROR`: `www` was a CNAME to `juliensimon.github.io`, so the CA read GitHub's CAA list (no Amazon). Fix: `www` became A records to GitHub Pages for a few minutes, then a new certificate (`8ecea507-...`) was issued and attached.
- 15:33Z apex and `www` became alias A and AAAA records to the distribution. `teleport` was removed (Julien).
- Resolvers keep the old answers for their TTL (old zone: `www` CNAME 1 h, apex A 4 h). Until then those visitors still reach GitHub Pages, which keeps serving; do not shut Pages down yet.
- Check with `dig +short` or a real answer count, never `grep ' DS '` on a plain dig (it matches dig's own header line).

### Still open

- Enable DNSSEC in Route 53 and publish the new DS at Squarespace only after the old nameservers have left every cache (wait at least 24 h after 15:02Z), otherwise resolvers that still ask Google get an unsigned answer and fail validation.
- After that: set the alias TTL, remove the GitHub Pages deploy job, and rescan in Aikido.

### Verified 2026-11-26 16:41Z

Both hosts served by CloudFront with HSTS, CSP, nosniff and X-Frame-Options. Mail checked by a real send and receive test (SPF, DKIM, DMARC pass). The Cloudflare beacon posts to `cloudflareinsights.com/cdn-cgi/rum` and gets 204; no CSP violations in the browser console. The old zone gave `www` a 1 h cache lifetime and the apex 4 h, so a resolver may serve GitHub Pages until about 19:35Z.
