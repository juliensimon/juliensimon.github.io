// Run: node --test infra/test_site_fn.mjs
// Loads site-fn.js the way CloudFront does (a plain script that defines handler()).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const src = readFileSync(join(dirname(fileURLToPath(import.meta.url)), 'site-fn.js'), 'utf8');
const ctx = vm.createContext({});
vm.runInContext(src, ctx);

function call(host, uri, qs = {}) {
  return ctx.handler({
    request: {
      uri,
      querystring: qs,
      headers: { host: { value: host } },
    },
  });
}

test('apex host redirects 301 to www and keeps path and query', () => {
  const r = call('julien.org', '/speaking', { a: { value: '1' }, b: { value: 'x y' } });
  assert.equal(r.statusCode, 301);
  assert.equal(r.headers.location.value, 'https://www.julien.org/speaking?a=1&b=x%20y');
});

test('apex host root redirects to www root', () => {
  const r = call('julien.org', '/');
  assert.equal(r.statusCode, 301);
  assert.equal(r.headers.location.value, 'https://www.julien.org/');
});

test('apex redirect sends HSTS on its own (function responses skip the headers policy)', () => {
  const r = call('julien.org', '/');
  assert.match(r.headers['strict-transport-security'].value, /^max-age=\d+/);
});

test('host match is case-insensitive', () => {
  assert.equal(call('JULIEN.ORG', '/').statusCode, 301);
});

test('www root serves index.html', () => {
  assert.equal(call('www.julien.org', '/').uri, '/index.html');
});

test('directory with trailing slash serves its index.html', () => {
  assert.equal(call('www.julien.org', '/blog/x/').uri, '/blog/x/index.html');
});

test('known page route without extension maps to .html', () => {
  assert.equal(call('www.julien.org', '/speaking').uri, '/speaking.html');
  assert.equal(call('www.julien.org', '/fr/conferencier-ia').uri, '/fr/conferencier-ia.html');
});

test('directory without trailing slash gets a 301 to the slash form, query kept', () => {
  const r = call('www.julien.org', '/blog/x', { q: { value: '1' } });
  assert.equal(r.statusCode, 301);
  assert.equal(r.headers.location.value, '/blog/x/?q=1');
});

test('files with an extension pass through untouched', () => {
  for (const u of ['/youtube/2025/a.html', '/assets/a.webp', '/.well-known/ai.json', '/llms.txt', '/feed.xml']) {
    assert.equal(call('www.julien.org', u).uri, u);
  }
});

test('the extensionless feed file passes through', () => {
  assert.equal(call('www.julien.org', '/feed').uri, '/feed');
});

test('a page route is not treated as a directory', () => {
  const r = call('www.julien.org', '/speaking');
  assert.equal(r.statusCode, undefined);
});

// GitHub Pages served /youtube/x and /blog/legacy-posts-and-images/x from x.html. The canonical URLs
// carry .html, but old links do not, so the function does the same rewrite (no redirect, status 200).
test('an extensionless video URL is served from its .html file', () => {
  const r = call('www.julien.org', '/youtube/2018/20180410_Building_Your_Smart_Applications');
  assert.equal(r.uri, '/youtube/2018/20180410_Building_Your_Smart_Applications.html');
  assert.equal(r.statusCode, undefined);
});

test('an extensionless legacy blog URL is served from its .html file', () => {
  const r = call('www.julien.org', '/blog/legacy-posts-and-images/2013/2013-08-21-arduino-lcd-thermometer');
  assert.equal(r.uri, '/blog/legacy-posts-and-images/2013/2013-08-21-arduino-lcd-thermometer.html');
});

test('a video title with a dot in it still gets .html (the dot is not an extension)', () => {
  for (const name of ['20170727_Utiliser_le_client_MQTT.fx_et_l_AWS_IoT_button', '20220621_Machine_Learning_2.0_with_Hugging_Face_Conf42']) {
    const r = call('www.julien.org', `/youtube/2017/${name}`);
    assert.equal(r.uri, `/youtube/2017/${name}.html`, name);
  }
});

test('real files under those prefixes are passed through untouched', () => {
  for (const p of ['/youtube/2018/x.html', '/blog/legacy-posts-and-images/2013/pic.webp', '/blog/legacy-posts-and-images/style.css', '/youtube/CLAUDE.md']) {
    assert.equal(call('www.julien.org', p).uri, p, p);
  }
});

test('year folders, the prefix folders and every other archive folder keep the slash redirect', () => {
  for (const p of ['/youtube/2013', '/blog/legacy-posts-and-images', '/blog/aws-posts-and-images/2018-01-22_speeding-up', '/blog/industry-perspectives/2026-11-11_x']) {
    const r = call('www.julien.org', p);
    assert.equal(r.statusCode, 301, p);
    assert.equal(r.headers.location.value, p + '/', p);
  }
});

test('the .html rewrite keeps the query string', () => {
  const r = call('www.julien.org', '/youtube/2018/x', { a: { value: '1' } });
  assert.equal(r.uri, '/youtube/2018/x.html');
  assert.deepEqual(r.querystring, { a: { value: '1' } });
});

test('a slash URL under the prefixes still serves the folder index', () => {
  assert.equal(call('www.julien.org', '/youtube/2018/').uri, '/youtube/2018/index.html');
});

test('the apex still redirects first for an extensionless video URL', () => {
  const r = call('julien.org', '/youtube/2018/x');
  assert.equal(r.statusCode, 301);
  assert.equal(r.headers.location.value, 'https://www.julien.org/youtube/2018/x');
});

// S3 reads a raw "+" in a path as a space, so /x_+_y.html was a 404 (GitHub Pages served it). The sitemap
// lists the raw form for four videos, so the function sends S3 the encoded form, which works.
test('a plus sign in the path is sent to S3 as %2B', () => {
  const r = call('www.julien.org', '/youtube/2017/20170413_Object_detection_-_MXNet_+_Raspberry_Pi_+_Amazon_Polly.html');
  assert.equal(r.uri, '/youtube/2017/20170413_Object_detection_-_MXNet_%2B_Raspberry_Pi_%2B_Amazon_Polly.html');
});

test('an already encoded %2B and a literal percent sequence are left as they are', () => {
  assert.equal(call('www.julien.org', '/youtube/2017/a_%2B_b.html').uri, '/youtube/2017/a_%2B_b.html');
  assert.equal(call('www.julien.org', '/youtube/2015/100%25_cloud.html').uri, '/youtube/2015/100%25_cloud.html');
});

test('a plus sign works together with the extensionless .html rewrite', () => {
  assert.equal(call('www.julien.org', '/youtube/2022/SageMaker_+_VS_Code').uri, '/youtube/2022/SageMaker_%2B_VS_Code.html');
});

test('a plus sign in a redirected path keeps the redirect and the encoded form', () => {
  const r = call('www.julien.org', '/blog/aws-posts-and-images/a+b');
  assert.equal(r.statusCode, 301);
  assert.equal(r.headers.location.value, '/blog/aws-posts-and-images/a%2Bb/');
});

test('the apex redirect keeps a plus sign exactly as the visitor sent it', () => {
  const r = call('julien.org', '/youtube/2017/a_+_b.html');
  assert.equal(r.headers.location.value, 'https://www.julien.org/youtube/2017/a_+_b.html');
});

test('a plus sign in the query string is not touched by the path rewrite', () => {
  const r = call('www.julien.org', '/youtube/2017/a_+_b.html', { q: { value: 'x+y' } });
  assert.deepEqual(r.querystring, { q: { value: 'x+y' } });
});
