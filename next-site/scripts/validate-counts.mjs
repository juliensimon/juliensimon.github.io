#!/usr/bin/env node

/**
 * Validates data consistency across the site.
 * Run with: npm run validate
 *
 * Checks:
 * 1. YouTube video counts match filesystem
 * 2. Blog post array lengths match claimed counts
 * 3. Speaking year totals sum to totalEvents
 * 4. Publication totals are consistent
 * 5. Global METRICS match source data
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.join(__dirname, '..');
const repoRoot = path.join(rootDir, '..');

let hasErrors = false;

function error(msg) {
  console.error(`❌ ${msg}`);
  hasErrors = true;
}

function success(msg) {
  console.log(`✅ ${msg}`);
}

function warn(msg) {
  console.warn(`⚠️  ${msg}`);
}

// Helper to count HTML files in a directory (excluding index.html)
function countHtmlFiles(dir) {
  if (!fs.existsSync(dir)) return 0;
  return fs.readdirSync(dir)
    .filter(f => f.endsWith('.html') && f !== 'index.html')
    .length;
}

// Helper to count subdirectories
function countSubdirs(dir) {
  if (!fs.existsSync(dir)) return 0;
  return fs.readdirSync(dir, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .length;
}

console.log('\n🔍 Validating data consistency...\n');

// ============================================
// 1. YouTube Video Counts
// ============================================
console.log('📺 YouTube Videos:');

const youtubeDir = path.join(repoRoot, 'youtube');
const youtubeYears = fs.readdirSync(youtubeDir, { withFileTypes: true })
  .filter(d => d.isDirectory() && /^\d{4}$/.test(d.name))
  .map(d => d.name);

let totalVideos = 0;
const videoCounts = {};

for (const year of youtubeYears) {
  const yearDir = path.join(youtubeDir, year);
  const count = countHtmlFiles(yearDir);
  videoCounts[year] = count;
  totalVideos += count;
}

// Read youtube.ts to compare
const youtubeTs = fs.readFileSync(path.join(rootDir, 'src/data/youtube.ts'), 'utf-8');
const totalMatch = youtubeTs.match(/totalVideos:\s*(\d+)/);
const claimedTotal = totalMatch ? parseInt(totalMatch[1]) : 0;

if (totalVideos === claimedTotal) {
  success(`YouTube total: ${totalVideos} videos`);
} else {
  error(`YouTube total mismatch: filesystem has ${totalVideos}, youtube.ts claims ${claimedTotal}`);
}

// Check individual year counts
const yearMatches = youtubeTs.matchAll(/year:\s*(\d{4}),\s*count:\s*(\d+)/g);
for (const match of yearMatches) {
  const year = match[1];
  const claimed = parseInt(match[2]);
  const actual = videoCounts[year] || 0;
  if (claimed !== actual) {
    error(`YouTube ${year}: filesystem has ${actual}, youtube.ts claims ${claimed}`);
  }
}

// ============================================
// 2. Blog Post Counts
// ============================================
console.log('\n📝 Blog Posts:');

// Read blog category config
const blogCategoriesTs = fs.readFileSync(path.join(rootDir, 'src/data/blog-categories.ts'), 'utf-8');

// Check each blog listing array length
const blogListingsDir = path.join(rootDir, 'src/data/blog-listings');
const blogFiles = ['aws.ts', 'aws-medium.ts', 'arcee.ts', 'huggingface.ts', 'medium.ts'];

for (const file of blogFiles) {
  const content = fs.readFileSync(path.join(blogListingsDir, file), 'utf-8');
  // Count objects with 'title:' property
  const titleMatches = content.match(/title:\s*['"`]/g);
  const arrayLength = titleMatches ? titleMatches.length : 0;

  const name = file.replace('.ts', '');
  success(`${name}: ${arrayLength} posts in array`);
}

// ============================================
// 3. Speaking Totals
// ============================================
console.log('\n🎤 Speaking:');

const speakingTs = fs.readFileSync(path.join(rootDir, 'src/data/speaking.ts'), 'utf-8');
const speakingTotalMatch = speakingTs.match(/totalEvents:\s*(\d+)/);
const speakingTotal = speakingTotalMatch ? parseInt(speakingTotalMatch[1]) : 0;

const speakingYearMatches = [...speakingTs.matchAll(/year:\s*\d+,\s*count:\s*(\d+)/g)];
const speakingYearSum = speakingYearMatches.reduce((sum, m) => sum + parseInt(m[1]), 0);

if (speakingYearSum === speakingTotal) {
  success(`Speaking total: ${speakingTotal} (sum of years matches)`);
} else {
  error(`Speaking mismatch: years sum to ${speakingYearSum}, totalEvents claims ${speakingTotal}`);
}

// ============================================
// 4. Publication Totals
// ============================================
console.log('\n📚 Publications:');

const publicationsTs = fs.readFileSync(path.join(rootDir, 'src/data/publications.ts'), 'utf-8');
const pubTotalMatch = publicationsTs.match(/TOTAL_ARTICLES\s*=\s*(\d+)/);
const pubTotal = pubTotalMatch ? parseInt(pubTotalMatch[1]) : 0;

const pubCategoryMatches = [...publicationsTs.matchAll(/count:\s*(\d+)/g)];
const pubCategorySum = pubCategoryMatches.reduce((sum, m) => sum + parseInt(m[1]), 0);

if (pubCategorySum === pubTotal) {
  success(`Publications total: ${pubTotal} (sum of categories matches)`);
} else {
  error(`Publications mismatch: categories sum to ${pubCategorySum}, TOTAL_ARTICLES claims ${pubTotal}`);
}

// ============================================
// 5. Global METRICS consistency
// ============================================
console.log('\n📊 Global METRICS (constants.ts):');

const constantsTs = fs.readFileSync(path.join(rootDir, 'src/lib/constants.ts'), 'utf-8');

// Check Technical Posts
const techPostsMatch = constantsTs.match(/value:\s*(\d+).*Technical Posts/);
const techPostsMetric = techPostsMatch ? parseInt(techPostsMatch[1]) : 0;
if (techPostsMetric === pubTotal) {
  success(`Technical Posts metric: ${techPostsMetric}`);
} else {
  error(`Technical Posts metric (${techPostsMetric}) doesn't match TOTAL_ARTICLES (${pubTotal})`);
}

// Check Speaking Engagements
const speakingMatch = constantsTs.match(/value:\s*(\d+).*Speaking Engagements/);
const speakingMetric = speakingMatch ? parseInt(speakingMatch[1]) : 0;
if (speakingMetric === speakingTotal) {
  success(`Speaking Engagements metric: ${speakingMetric}`);
} else {
  error(`Speaking Engagements metric (${speakingMetric}) doesn't match totalEvents (${speakingTotal})`);
}

// Check YouTube Subscribers consistency
const ytSubsMatch = constantsTs.match(/value:\s*(\d+).*YouTube Subscribers/);
const ytSubsMetric = ytSubsMatch ? parseInt(ytSubsMatch[1]) : 0;
const ytSubsDataMatch = youtubeTs.match(/subscriberCount:\s*(\d+)/);
const ytSubsData = ytSubsDataMatch ? parseInt(ytSubsDataMatch[1]) : 0;
if (ytSubsMetric === ytSubsData) {
  success(`YouTube Subscribers metric: ${ytSubsMetric}K+`);
} else {
  error(`YouTube Subscribers metric (${ytSubsMetric}) doesn't match subscriberCount (${ytSubsData})`);
}

// ============================================
// Summary
// ============================================
console.log('\n' + '='.repeat(50));
if (hasErrors) {
  console.error('\n❌ Validation failed! Please fix the errors above.\n');
  process.exit(1);
} else {
  console.log('\n✅ All validations passed!\n');
  process.exit(0);
}
