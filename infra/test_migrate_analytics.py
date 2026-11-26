"""Run: python3 -I infra/test_migrate_analytics.py"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import migrate_analytics as m  # noqa: E402

TOKEN = m.TOKEN
CF = f"""<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "{TOKEN}"}}'></script>"""
ID = "27550dad-d418-4f5d-ad1b-dab573da1020"


class Transform(unittest.TestCase):
    def test_script_tag_plain_defer(self):
        src = f'<head>\n<script defer src="https://cloud.umami.is/script.js" data-website-id="{ID}"></script>\n</head>'
        self.assertEqual(m.transform(src), f"<head>\n{CF}\n</head>")

    def test_script_tag_serialized_defer(self):
        src = f'<script defer="" src="https://cloud.umami.is/script.js" data-website-id="{ID}"></script>'
        self.assertEqual(m.transform(src), CF)

    def test_dns_prefetch_removed_with_its_line(self):
        src = 'a\n    <link rel="dns-prefetch" href="//cloud.umami.is">\nb'
        self.assertEqual(m.transform(src), "a\nb")

    def test_preconnect_removed_with_its_line(self):
        src = 'a\n<link rel="preconnect" href="https://cloud.umami.is" />\nb'
        self.assertEqual(m.transform(src), "a\nb")

    def test_dynamic_loader_block_replaced(self):
        src = f"""<!-- Umami Analytics -->
    <script>
        window.addEventListener('load', function() {{
            var script = document.createElement('script');
            script.src = 'https://cloud.umami.is/script.js';
            script.setAttribute('data-website-id', '{ID}');
            document.head.appendChild(script);
        }});
    </script>
x"""
        out = m.transform(src)
        self.assertNotIn("umami", out.lower())
        self.assertIn(CF, out)
        self.assertTrue(out.endswith("\nx"))

    def test_idempotent(self):
        src = f'<script defer src="https://cloud.umami.is/script.js" data-website-id="{ID}"></script>'
        once = m.transform(src)
        self.assertEqual(m.transform(once), once)

    def test_unrelated_text_untouched(self):
        src = "<p>nothing here</p>"
        self.assertEqual(m.transform(src), src)

    def test_comment_renamed(self):
        self.assertEqual(m.transform("<!-- Umami Analytics -->\n"), "<!-- Cloudflare Web Analytics -->\n")


if __name__ == "__main__":
    unittest.main()
