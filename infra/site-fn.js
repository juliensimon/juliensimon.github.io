// CloudFront Function (cloudfront-js-2.0), viewer-request, for www.julien.org and julien.org.
// Source of truth. `gen_pages.py` rewrites the PAGES block from the build output.
//
// It reproduces what GitHub Pages did with the static export:
//   julien.org            -> 301 to https://www.julien.org (path and query kept)
//   /dir/                 -> /dir/index.html
//   /dir                  -> 301 /dir/            (so relative links in archived posts keep working)
//   /page                 -> /page.html           (Next.js pages: only those listed in PAGES)
//   a "+" in the path     -> %2B                  (S3 would read it as a space)
//   /youtube/y/name       -> /youtube/y/name.html (and the same under /blog/legacy-posts-and-images/:
//                            GitHub Pages served the extensionless form, the canonical URL has .html)
//   /feed                 -> served as is         (the extensionless RSS file)
// Responses built by a function skip the headers policy, so the redirect carries HSTS itself.

// BEGIN PAGES
var PAGES = {"/404":1,"/arcee-blog-posts":1,"/aws-blog-posts":1,"/aws-medium-posts":1,"/blog-posts/arcee":1,"/blog-posts/aws-medium":1,"/blog-posts/aws":1,"/blog-posts/huggingface":1,"/blog-posts/legacy":1,"/blog-posts/medium":1,"/books":1,"/certifications":1,"/code":1,"/computers":1,"/datasets":1,"/experience":1,"/fr/conferencier-ia":1,"/huggingface-blog-posts":1,"/media-analysts":1,"/media":1,"/medium-blog-posts":1,"/podcast":1,"/publications":1,"/speaking/2016":1,"/speaking/2017":1,"/speaking/2018":1,"/speaking/2019":1,"/speaking/2020":1,"/speaking/2021":1,"/speaking/2022":1,"/speaking/2023":1,"/speaking/2024":1,"/speaking/2025":1,"/speaking/2026":1,"/speaking-2016":1,"/speaking-2017":1,"/speaking-2018":1,"/speaking-2019":1,"/speaking-2020":1,"/speaking-2021":1,"/speaking-2022":1,"/speaking-2023":1,"/speaking-2024":1,"/speaking":1,"/topics/ai-chips":1,"/topics/ai-infrastructure-economics":1,"/topics/ai-sovereignty-europe":1,"/topics/small-and-open-models":1,"/topics":1,"/yandex_c7bbb7413b1be2ca":1,"/youtube-videos":1,"/youtube":1};
// END PAGES

var PASS = { '/feed': 1 };

// Folders whose pages are files named x.html. Extensionless URLs there are served from x.html.
// A name is a real file only when it ends in one of these (video titles contain dots: "MQTT.fx", "2.0").
var HTML_FILE_PREFIXES = ['/youtube/', '/blog/legacy-posts-and-images/'];
var FILE_EXT = /\.(html|css|js|json|xml|txt|md|png|jpe?g|gif|webp|svg|ico|pdf|mp3|mp4|woff2?)$/i;

function qs(q) {
  var parts = [];
  for (var k in q) {
    var e = q[k];
    if (e.multiValue) {
      for (var i = 0; i < e.multiValue.length; i++) {
        parts.push(k + '=' + encodeURIComponent(e.multiValue[i].value));
      }
    } else {
      parts.push(e.value === '' ? k : k + '=' + encodeURIComponent(e.value));
    }
  }
  return parts.length ? '?' + parts.join('&') : '';
}

function redirect(location) {
  return {
    statusCode: 301,
    statusDescription: 'Moved Permanently',
    headers: {
      location: { value: location },
      'strict-transport-security': { value: 'max-age=31536000' },
      'cache-control': { value: 'max-age=3600' },
    },
  };
}

function handler(event) {
  var request = event.request;
  var host = (request.headers.host ? request.headers.host.value : '').toLowerCase();
  var uri = request.uri;

  if (host === 'julien.org') {
    return redirect('https://www.julien.org' + uri + qs(request.querystring));
  }

  // S3 reads a raw "+" in a path as a space; the encoded form finds the object. Four video pages have a
  // "+" in their name and the sitemap lists it raw.
  if (uri.indexOf('+') !== -1) {
    uri = uri.replace(/\+/g, '%2B');
    request.uri = uri;
  }

  if (uri.charAt(uri.length - 1) === '/') {
    request.uri = uri + 'index.html';
    return request;
  }

  var last = uri.substring(uri.lastIndexOf('/') + 1);
  for (var i = 0; i < HTML_FILE_PREFIXES.length; i++) {
    // a four-digit name is a year folder (it has an index.html): it keeps the slash redirect below
    if (uri.indexOf(HTML_FILE_PREFIXES[i]) === 0 && !FILE_EXT.test(last) && !/^\d{4}$/.test(last)) {
      request.uri = uri + '.html';
      return request;
    }
  }

  if (last.indexOf('.') !== -1 || PASS[uri]) {
    return request;
  }

  if (PAGES[uri]) {
    request.uri = uri + '.html';
    return request;
  }

  return redirect(uri + '/' + qs(request.querystring));
}
