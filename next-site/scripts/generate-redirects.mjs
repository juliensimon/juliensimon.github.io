import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';

const OUT_DIR = join(process.cwd(), 'out');
const DATA_DIR = join(process.cwd(), 'src', 'data', 'blog-listings');

// Validate redirect URL to prevent XSS - only allow safe relative paths
function isValidRedirectUrl(url) {
  if (!url || typeof url !== 'string') return false;
  if (!url.startsWith('/')) return false;
  if (url.startsWith('//')) return false;
  if (/[<>"'`]/.test(url)) return false;
  if (/javascript:/i.test(url)) return false;
  if (/data:/i.test(url)) return false;
  return true;
}

function redirectHtml(to) {
  const canonical = `https://www.julien.org${to === '/' ? '' : to}`;
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0;url=${to}">
<link rel="canonical" href="${canonical}">
<title>Redirecting...</title>
</head>
<body>
<script>window.location.replace('${to}')</script>
<p>Redirecting to <a href="${to}">${to}</a></p>
</body>
</html>`;
}

/** Write a redirect file. Returns true if created, false if skipped. */
function writeRedirect(oldPath, newUrl) {
  if (!isValidRedirectUrl(newUrl)) return false;

  let filePath;
  if (oldPath.endsWith('.html')) {
    filePath = join(OUT_DIR, oldPath);
  } else {
    const cleanPath = oldPath.replace(/\/$/, '');
    filePath = join(OUT_DIR, cleanPath, 'index.html');
  }

  if (existsSync(filePath)) return false;

  mkdirSync(dirname(filePath), { recursive: true });
  writeFileSync(filePath, redirectHtml(newUrl));
  return true;
}

// ─── Static redirects (old filename → new Next.js route) ────────────

const STATIC_REDIRECTS = [
  { from: 'youtube.html', to: '/youtube-videos' },
  { from: 'aws-blog-posts.html', to: '/blog-posts/aws' },
  { from: 'huggingface-blog-posts.html', to: '/blog-posts/huggingface' },
  { from: 'arcee-blog-posts.html', to: '/blog-posts/arcee' },
  { from: 'medium-blog-posts.html', to: '/blog-posts/medium' },
  { from: 'aws-medium-posts.html', to: '/blog-posts/aws-medium' },
  { from: 'speaking-2016.html', to: '/speaking/2016' },
  { from: 'speaking-2017.html', to: '/speaking/2017' },
  { from: 'speaking-2018.html', to: '/speaking/2018' },
  { from: 'speaking-2019.html', to: '/speaking/2019' },
  { from: 'speaking-2020.html', to: '/speaking/2020' },
  { from: 'speaking-2021.html', to: '/speaking/2021' },
  { from: 'speaking-2022.html', to: '/speaking/2022' },
  { from: 'speaking-2023.html', to: '/speaking/2023' },
  { from: 'speaking-2024.html', to: '/speaking/2024' },
];

let created = 0;
let skipped = 0;

for (const { from, to } of STATIC_REDIRECTS) {
  const filePath = join(OUT_DIR, from);
  if (existsSync(filePath)) { skipped++; continue; }
  if (!isValidRedirectUrl(to)) continue;
  writeFileSync(filePath, redirectHtml(to));
  created++;
}
console.log(`Static redirects: ${created} created, ${skipped} skipped`);

// ─── Special path redirects ─────────────────────────────────────────

const SPECIAL_REDIRECTS = [
  ['/youtube/youtube.html', '/youtube-videos'],
  ['/certifications.html', '/experience'],
  ['/blog/aws-posts-and-images/', '/blog-posts/aws'],
  ['/blog/huggingface-posts-and-images/', '/blog-posts/huggingface'],
  ['/blog/arcee-posts/', '/blog-posts/arcee'],
  ['/blog/legacy-posts-and-images/', '/blog-posts/legacy'],
  ['/blog/aws-medium-posts-and-images/', '/blog-posts/aws-medium'],
  ['/docs/hub/spaces-gpus', '/'],
  ['/RoyZ/', '/computers'],
  ['/RoyZ/driver_ep.html', '/computers'],
];

created = 0; skipped = 0;
for (const [oldPath, newUrl] of SPECIAL_REDIRECTS) {
  if (writeRedirect(oldPath, newUrl)) created++;
  else skipped++;
}
console.log(`Special redirects: ${created} created, ${skipped} skipped`);

// ─── Blog post redirects: /blog/YYYY-MM-DD-slug/ ────────────────────
//
// Only the date-prefixed pattern — this is what Google Search Console
// actually reports as 404. The /blog/slug/ (no date) and /posts/slug
// patterns were speculative and risk slug collisions.

function parseLocalHrefs(filePath) {
  if (!existsSync(filePath)) return [];
  const content = readFileSync(filePath, 'utf-8');
  const hrefs = [];

  const re1 = /localHref:\s*'([^']+)'/g;
  let m;
  while ((m = re1.exec(content)) !== null) hrefs.push(m[1]);

  const re2 = /(?<![a-zA-Z])href:\s*'(\/blog\/[^']+)'/g;
  while ((m = re2.exec(content)) !== null) {
    if (!hrefs.includes(m[1])) hrefs.push(m[1]);
  }

  return hrefs;
}

const listingFiles = ['aws.ts', 'aws-medium.ts', 'huggingface.ts', 'arcee.ts', 'legacy.ts', 'industry-perspectives.ts'];
const allPosts = [];
for (const file of listingFiles) {
  allPosts.push(...parseLocalHrefs(join(DATA_DIR, file)));
}

console.log(`\nFound ${allPosts.length} blog posts with local paths`);

created = 0; skipped = 0;

for (const localHref of allPosts) {
  if (!isValidRedirectUrl(localHref)) { skipped++; continue; }

  // Pattern A: /blog/CATEGORY/YYYY-MM-DD_slug/index.html
  let match = localHref.match(/\/blog\/[^/]+\/(\d{4}-\d{2}-\d{2})[_](.+?)\/index\.html$/);
  if (match) {
    const [, date, slug] = match;
    // Old URL: /blog/YYYY-MM-DD-slug/
    if (writeRedirect(`/blog/${date}-${slug.toLowerCase()}/`, localHref)) created++;
    else skipped++;
    continue;
  }

  // Pattern B: /blog/CATEGORY/YYYY/YYYY-MM-DD_slug/index.html (aws-medium)
  match = localHref.match(/\/blog\/[^/]+\/\d{4}\/(\d{4}-\d{2}-\d{2})[_](.+?)\/index\.html$/);
  if (match) {
    const [, date, slug] = match;
    if (writeRedirect(`/blog/${date}-${slug.toLowerCase().replace(/\s+/g, '-')}/`, localHref)) created++;
    else skipped++;
    continue;
  }

  // Pattern C: /blog/CATEGORY/YYYY/YYYY-MM-DD-slug.html (legacy)
  match = localHref.match(/\/blog\/[^/]+\/\d{4}\/(\d{4}-\d{2}-\d{2})-(.+?)\.html$/);
  if (match) {
    const [, date, slug] = match;
    if (writeRedirect(`/blog/${date}-${slug.toLowerCase()}/`, localHref)) created++;
    else skipped++;
    continue;
  }
}

console.log(`Blog redirects: ${created} created, ${skipped} skipped`);

// ─── blog.julien.org redirects ──────────────────────────────────────
//
// blog.julien.org resolves to the same GitHub Pages site. Old Blogger
// URLs use /YYYY/MM/slug.html format. We match them to legacy posts
// by finding posts from the same year/month whose slug starts with
// the Blogger slug (Blogger often truncated slugs).

// Build a lookup: { "YYYY/MM": [{slug, href}] } from legacy posts
const legacyByYearMonth = {};
const legacyContent = readFileSync(join(DATA_DIR, 'legacy.ts'), 'utf-8');
const legacyRe = /href:\s*'(\/blog\/legacy-posts-and-images\/(\d{4})\/(\d{4})-(\d{2})-\d{2}-([^']+?)\.html)'/g;
let lm;
while ((lm = legacyRe.exec(legacyContent)) !== null) {
  const [, href, year, , month, slug] = lm;
  const key = `${year}/${month}`;
  if (!legacyByYearMonth[key]) legacyByYearMonth[key] = [];
  legacyByYearMonth[key].push({ slug: slug.toLowerCase(), href });
}

/**
 * Try to find a legacy post matching a Blogger-style slug.
 * Blogger slugs are often truncated prefixes of the full slug.
 */
function findLegacyPost(year, month, bloggerSlug) {
  const key = `${year}/${month}`;
  const posts = legacyByYearMonth[key];
  if (!posts) return null;

  const normalized = bloggerSlug.toLowerCase().replace(/\.html$/, '');

  // Exact match
  for (const p of posts) {
    if (p.slug === normalized) return p.href;
  }

  // Blogger slug is a prefix of the full slug
  for (const p of posts) {
    if (p.slug.startsWith(normalized)) return p.href;
  }

  // Full slug starts with the Blogger slug (handles word drops)
  for (const p of posts) {
    // Check if most words match
    const bloggerWords = normalized.split('-').filter(w => w.length > 2);
    const postWords = p.slug.split('-');
    const matchCount = bloggerWords.filter(w => postWords.includes(w)).length;
    if (bloggerWords.length > 0 && matchCount >= bloggerWords.length * 0.6) return p.href;
  }

  return null;
}

// Extract unique blog.julien.org paths from the 404 report
// These follow /YYYY/MM/slug.html or /YYYY/MM/ patterns
const BLOGGER_404_PATHS = [
  '/2015/12/a-silly-little-script-for-amazon.html',
  '/2016/12/amazon-polly-hello-world-literally.html',
  '/2017/03/exploring-gdelt-data-set-with-amazon.html',
  '/2016/11/a-hands-on-look-at-amazon-rekognition.html',
  '/2008/12/howto-compiling-vlc-with-all-major.html',
  '/2008/12/unix-biography-and-then-some-subtitled.html',
  '/2008/09/virtualbox-20-released.html',
  '/2009/01/uk-record-sales-for-2008.html',
  '/2009/01/divx-311-now-supported-on-ps3.html',
  '/2013/07/virtualbox-ssh-to-guest-vms-in-30.html',
  '/2016/01/upgrading-amazon-ecs-cluster-to-docker.html',
  '/2012/08/viking-laws-for-tech-teams-part-3-find.html',
  '/2016/05/big-data-combo-toulouse-data-science.html',
  '/2011/01/delete-hadoop-cluster-ec2-script-broken.html',
  '/2007/05/effective-java-reloaded-this-time-its.html',
  '/2016/11/3-webinaires-aws-en-francais.html',
  '/2009/02/woz-is-back.html',
  '/2009/03/pirate-bay-trial-defense-speaks.html',
  '/2009/02/what-digital-downloads-mean-for.html',
  '/2008/10/iron-man-blu-ray-online-content-brings.html',
  '/2009/11/oracle-webcast-on-digiplug.html',
  '/2009/12/la-vie-lit.html',
  '/2015/04/test-drive-aws-machine-learning-redshift.html',
  '/2010/03/new-pc-world-website-live.html',
  '/2013/07/fooling-around-with-python-on-friday.html',
  '/2008/12/conference-slides-spring-30-mysql.html',
  '/2014/05/aldebaran-aws-summit-paris-2014.html',
  '/2008/12/new-opensolaris-release.html',
  '/2015/05/reading-list-may-2015.html',
  '/2012/06/only-one-word-awesome.html',
  '/2012/05/audio-mass-encode-on-synology-nas-flac.html',
  '/2012/04/criteo-code-of-duty-2-wwwcode-of.html',
  '/2008/12/howto-quick-reference-on-audio-video.html',
  '/2008/12/unix-biography-and-then-some-subtitled.html',
  '/2015/04/test-drive-real-time-prediction-with.html',
  '/2015/04/test-drive-real-time-prediction-in-java.html',
  '/2008/12/press-release-digiplug-selects-isilon.html',
  '/2009/04/howto-compiling-vlc-099-live555-all.html',
  '/2013/08/howto-compiling-ffmpeg-x264-mp3-aac.html',
  '/2009/01/howto-processing-multichannel-audio-dts.html',
  '/2007/05/jsr-281-ims-services-api.html',
  '/2009/04/global-2008-music-sales.html',
  '/2013/08/arduino-lcd-thermometer.html',
  '/2009/01/howto-compiling-mediainfo-cli-gui-on.html',
  '/2007/05/java-university-keynote-with-james.html',
  '/2013/08/nodejs-part-5-zero-hero.html',
  '/2012/09/viking-laws-for-tech-teams-part-4-keep.html',
  '/2007/05/project-blackbox.html',
  '/2015/12/installing-minecraft-server-on-aws.html',
  '/2017/03/amazon-ai-services-javascript-meetup.html',
  '/2013/10/max-schireson-mongodb-criteo.html',
  '/2008/12/howto-adding-lastfm-scrobbling-to.html',
  '/2012/08/viking-laws-for-tech-teams-part-2-keep.html',
  '/2009/01/howto-processing-multichannel-audio-dts.html',
  '/2012/12/viking-laws-for-tech-teams-part-6-be.html',
  '/2015/11/filtering-aws-cli-with-jq.html',
  '/2010/11/scrum-criteo.html',
  '/2011/07/code-review-criteo.html',
  '/2015/02/cto-crunch-france-digitale.html',
  '/2013/08/howto-aws-mount-s3-buckets-from-linux.html',
  '/2013/08/nodejs-mongodb-part-2-here-comes.html',
  '/2008/12/owasp-testing-guide-v3-available.html',
  '/2008/10/aerosmith-hits-jackpot-with-guitar-hero.html',
  '/2009/03/brick-and-mortar-music-retailers-are.html',
  '/2008/11/spring-conference-in-paris-part-3_13.html',
  '/2008/12/howto-setting-up-vod-server-with-vlc.html',
  '/2015/04/aws-startup-day-moving-viadeo-to-aws.html',
  '/2013/07/mass-rename-on-synology.html',
  '/2008/12/how-to-installing-openoffice-30-on.html',
  '/2010/05/new-pixmania-pixmania-pro-websites.html',
  '/2007/05/high-performance-java-technology-in.html',
  '/2015/11/upcoming-meetup-docker-marseille.html',
  '/2009/01/x264-benchmarks-individual-flags-motion.html',
  '/2016/12/amazon-polly-hello-world-literally.html',
  '/2010/03/new-pc-world-website-live.html',
  '/2008/10/sales-figures-released-for-radioheads.html',
  '/2008/09/linkedin-q-who-came-up-with-word.html',
  '/2009/01/do-not-scream-at-your-hard-drives.html',
  '/2007/05/yummy.html',
  '/2008/09/slotmusic-another-doomed-physical.html',
  '/2007/05/java-platform-performance-on-multicore.html',
  '/2009/05/may-1st-demonstration-in-paris-against.html',
  '/2008/09/linkedin-q-what-is-difference-between.html',
  '/2007/05/nice-relaxing-book-to-read-on-plane-p.html',
  '/2008/11/eu-culture-ministers-on-legal-offers.html',
  '/2013/07/the-billion-dollar-app-nodejs-mongodb.html',
  '/2008/10/dont-taze-my-ipod-bro.html',
  '/2012/08/viking-laws-for-tech-teams-part-1.html',
  '/2008/11/cdoncom-vikings-axe-wma.html',
  '/2007/05/jboss-party.html',
  '/2017/03/advanced-task-scheduling-with-amazon.html',
  '/2008/11/owasp-new-2008-conference-slides-videos.html',
  '/2013/07/mongodb-and-python-gang-thegither.html',
  '/2017/03/building-serverless-apps-with-nodejs.html',
  '/2017/03/amazon-ai-services-javascript-meetup.html',
  '/2015/02/viadeo-devoxx-france-2015.html',
  '/2013/09/viking-laws-for-tech-teams-part-7.html',
  '/2015/12/video-of-our-talk-at-velocity-conf.html',
  '/2007/05/java-persistence-api-best-practices-and.html',
  '/2009/03/ffmpeg-05-released.html',
  '/2009/01/howto-ffmpeg-x264-presets.html',
  '/2009/03/two-new-trailers-for-guitar-hero.html',
  '/2014/03/im-baaack-and-im-hiring.html',
  '/2008/09/gary-allan-he-cant-quit-her-2005.html',
  '/2008/10/brute-force-attack-on-wpawpa2-passwords.html',
  '/2007/05/session-id-ts-1262-session-title-killer.html',
  '/2012/07/learning-about-data-centers.html',
  '/2011/01/installing-hadoop-on-windows-cygwin.html',
  '/2010/02/new-currys-website-live.html',
  '/2008/09/walmart-drops-drm-and-your-music-files.html',
  '/2007/05/after-dark-bash.html',
];

// Also create redirects for archive-style URLs: /YYYY_MM_01_archive.html
const BLOGGER_ARCHIVE_PATHS = [
  '/2013_08_01_archive.html',
  '/2008_01_01_archive.html',
  '/2012_07_01_archive.html',
  '/2011_07_01_archive.html',
  '/2012_09_01_archive.html',
  '/2010_03_01_archive.html',
  '/2010_11_01_archive.html',
  '/2009_02_01_archive.html',
  '/2016_02_01_archive.html',
];

// Year/month directory listing URLs
const BLOGGER_DIR_PATHS = [
  '/2008/10/', '/2008/12/', '/2008/01/', '/2009/01/',
  '/2009/02/', '/2010/03/', '/2010/06/', '/2010/11/',
  '/2011/01/', '/2011/07/', '/2012/07/', '/2013/01/',
  '/2013/08/', '/2013/09/', '/2014/', '/2015/02/',
  '/2015/04/', '/2015/05/', '/2016/02/', '/2016/05/',
  '/2009/', '/2010/02/',
];

created = 0; skipped = 0;
let matched = 0;

for (const bloggerPath of BLOGGER_404_PATHS) {
  const pathMatch = bloggerPath.match(/^\/(\d{4})\/(\d{2})\/(.+)$/);
  if (!pathMatch) continue;

  const [, year, month, filename] = pathMatch;
  const bloggerSlug = filename.replace(/\.html$/, '');

  const legacyHref = findLegacyPost(year, month, bloggerSlug);
  const target = legacyHref || '/blog-posts/legacy';

  if (legacyHref) matched++;
  if (writeRedirect(bloggerPath, target)) created++;
  else skipped++;
}

// Archive paths → legacy listing
for (const archivePath of BLOGGER_ARCHIVE_PATHS) {
  if (writeRedirect(archivePath, '/blog-posts/legacy')) created++;
  else skipped++;
}

// Directory paths → legacy listing
for (const dirPath of BLOGGER_DIR_PATHS) {
  if (writeRedirect(dirPath, '/blog-posts/legacy')) created++;
  else skipped++;
}

console.log(`Blogger redirects: ${created} created (${matched} matched to specific posts), ${skipped} skipped`);
