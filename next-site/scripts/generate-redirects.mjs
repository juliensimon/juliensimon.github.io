import { writeFileSync, existsSync } from 'fs';
import { join } from 'path';

const OUT_DIR = join(process.cwd(), 'out');

// Only include redirects where the OLD filename differs from what Next.js outputs.
// Next.js creates e.g. experience.html for /experience, so we must NOT overwrite those.
// We only redirect old paths that have no corresponding Next.js output file.
const REDIRECTS = [
  // These old filenames don't match any Next.js output:
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

let count = 0;
let skipped = 0;
for (const { from, to } of REDIRECTS) {
  const filePath = join(OUT_DIR, from);
  // Safety check: never overwrite a file that Next.js already generated
  if (existsSync(filePath)) {
    console.log(`  SKIP (already exists): ${from}`);
    skipped++;
    continue;
  }
  writeFileSync(filePath, redirectHtml(to));
  count++;
}

console.log(`Generated ${count} redirect files (skipped ${skipped} existing)`);
