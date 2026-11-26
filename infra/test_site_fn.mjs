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
