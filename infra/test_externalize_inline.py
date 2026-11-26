"""Run: python3 -I infra/test_externalize_inline.py"""
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import externalize_inline as e  # noqa: E402


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


PAGE = (
    "<html><head>"
    '<script src="/_next/static/chunks/a.js" async=""></script>'
    "<script>(self.__next_f=self.__next_f||[]).push([0])</script>"
    '<script type="application/ld+json">{"@type":"Person"}</script>'
    "</head><body><p>hi</p>"
    '<script>self.__next_f.push([1,"a"])</script>'
    '<script>self.__next_f.push([1,"b"])</script>'
    "</body></html>"
)
BODIES = ['(self.__next_f=self.__next_f||[]).push([0])', 'self.__next_f.push([1,"a"])', 'self.__next_f.push([1,"b"])']
JOINED = ";\n".join(BODIES)


class Scripts(unittest.TestCase):
    def test_inline_scripts_become_one_synchronous_external_script(self):
        # Not defer, not async: Next.js closes its data stream once the page stops loading, and a
        # deferred script runs after that point (found by a browser test: "Connection closed").
        html, files = e.transform(PAGE)
        name = digest(JOINED)
        self.assertEqual(files, {f"{name}.js": JOINED})
        self.assertIn(f'<script src="/_next/static/inline/{name}.js"></script>', html)
        self.assertNotRegex(html, r'inline/[0-9a-f]+\.js"[^>]*(defer|async)')
        self.assertNotIn("self.__next_f", html)

    def test_external_script_goes_where_the_first_inline_script_was(self):
        html, _ = e.transform(PAGE)
        self.assertLess(html.index("a.js"), html.index("/_next/static/inline/"))
        self.assertLess(html.index("/_next/static/inline/"), html.index("ld+json"))

    def test_json_ld_and_external_scripts_are_untouched(self):
        html, _ = e.transform(PAGE)
        self.assertIn('<script type="application/ld+json">{"@type":"Person"}</script>', html)
        self.assertIn('<script src="/_next/static/chunks/a.js" async=""></script>', html)

    def test_page_without_inline_code_is_returned_unchanged(self):
        src = '<html><script src="/x.js"></script><script type="application/json">{}</script></html>'
        self.assertEqual(e.transform(src), (src, {}))

    def test_second_run_changes_nothing(self):
        once, _ = e.transform(PAGE)
        self.assertEqual(e.transform(once), (once, {}))

    def test_scripts_are_joined_with_a_semicolon_so_a_line_starting_with_a_paren_cannot_call_the_previous_one(self):
        _, files = e.transform("<script>a=1</script><script>(b=2)</script>")
        self.assertEqual(list(files.values()), ["a=1;\n(b=2)"])

    def test_a_script_inside_an_html_comment_is_left_alone(self):
        src = "<!-- <script>old()</script> --><p>x</p>"
        self.assertEqual(e.transform(src), (src, {}))

    def test_inline_module_importmap_and_unknown_types_are_refused(self):
        for t in ("module", "importmap", "text/babel"):
            with self.assertRaises(ValueError, msg=t):
                e.transform(f'<script type="{t}">x</script>')

    def test_classic_javascript_types_are_accepted(self):
        for t in ("text/javascript", "application/javascript"):
            _, files = e.transform(f'<script type="{t}">x()</script>')
            self.assertEqual(len(files), 1, t)

    def test_attributes_that_change_how_an_inline_script_runs_are_refused(self):
        for attrs in ("async", "defer", "nomodule"):
            with self.assertRaises(ValueError, msg=attrs):
                e.transform(f"<script {attrs}>x()</script>")


class Styles(unittest.TestCase):
    def test_style_element_becomes_a_stylesheet_link_in_place(self):
        html, files = e.transform("<head><style>.a{color:red}</style><p>x</p></head>")
        name = digest(".a{color:red}")
        self.assertEqual(files, {f"{name}.css": ".a{color:red}"})
        self.assertEqual(html, f'<head><link rel="stylesheet" href="/_next/static/inline/{name}.css"><p>x</p></head>')

    def test_each_style_element_keeps_its_own_position_so_the_cascade_order_holds(self):
        html, files = e.transform("<style>a{}</style><link rel=stylesheet href=/s.css><style>b{}</style>")
        self.assertEqual(len(files), 2)
        names = [m for m in sorted(files)]
        self.assertTrue(html.index(".css") < html.index("/s.css") < html.rindex(".css"))
        self.assertEqual(len(names), 2)

    def test_media_attribute_is_carried_to_the_link(self):
        html, _ = e.transform('<style media="print">p{}</style>')
        self.assertIn('media="print"', html)

    def test_other_style_attributes_are_refused(self):
        with self.assertRaises(ValueError):
            e.transform('<style nonce="x">p{}</style>')

    def test_empty_style_element_is_dropped(self):
        html, files = e.transform("<p>a</p><style> </style><p>b</p>")
        self.assertEqual((html, files), ("<p>a</p><p>b</p>", {}))


def cls(value: str) -> str:
    return "s-" + hashlib.sha256(value.encode()).hexdigest()[:8]


def rule(value: str) -> str:
    # the class is repeated so the rule weighs more than the site's own CSS, like the inline style it replaces
    c = cls(value)
    return f".{c}.{c}.{c}{{{value}}}"


class StyleAttributes(unittest.TestCase):
    def page(self, body: str, head: str = "") -> str:
        return f"<html><head>{head}</head><body>{body}</body></html>"

    def test_style_attribute_becomes_a_class_with_a_rule_in_a_stylesheet_linked_last_in_head(self):
        html, files = e.transform(self.page('<p style="color:red">x</p>'))
        c = cls("color:red")
        name = digest(rule("color:red"))
        self.assertEqual(files, {f"{name}.css": rule("color:red")})
        self.assertEqual(
            html,
            f'<html><head><link rel="stylesheet" href="/_next/static/inline/{name}.css"></head>'
            f'<body><p class="{c}">x</p></body></html>',
        )

    def test_class_is_merged_into_an_existing_class_attribute_whatever_the_order_and_quotes(self):
        c = cls("a:b")
        for src, want in (
            ('<p class="x y" style="a:b">', f'<p class="x y {c}">'),
            ('<p style="a:b" class="x">', f'<p class="x {c}">'),
            ("<p style='a:b' class='x'>", f"<p class='x {c}'>"),
        ):
            html, _ = e.transform(self.page(src + "t</p>"))
            self.assertIn(want, html, src)
            self.assertNotIn("style=", html, src)

    def test_the_same_value_on_two_elements_gives_one_rule_and_one_class(self):
        html, files = e.transform(self.page('<p style="a:b">1</p><p style="a:b">2</p>'))
        (css,) = files.values()
        self.assertEqual(css.count("{"), 1)
        self.assertEqual(html.count(cls("a:b")), 2)  # one class on each element

    def test_rules_keep_the_order_of_first_appearance(self):
        _, files = e.transform(self.page('<p style="a:b">1</p><i style="c:d">2</i><b style="a:b">3</b>'))
        (css,) = files.values()
        self.assertEqual(css, rule("a:b") + "\n" + rule("c:d"))

    def test_entities_in_the_value_are_decoded_in_the_rule(self):
        _, files = e.transform(self.page('<p style="background-image:url(&quot;/a.png?x=1&amp;y=2&quot;)">x</p>'))
        (css,) = files.values()
        self.assertIn('url("/a.png?x=1&y=2")', css)

    def test_an_empty_style_attribute_is_dropped(self):
        html, files = e.transform(self.page('<p style="">x</p><p style=" ">y</p>'))
        self.assertEqual(files, {})
        self.assertNotIn("style", html)

    def test_a_value_that_could_break_out_of_its_rule_is_refused(self):
        for v in ("a:b}.x{c:d", "a:{b", "a:b/*c"):
            with self.assertRaises(ValueError, msg=v):
                e.transform(self.page(f'<p style="{v}">x</p>'))

    def test_style_text_in_comments_scripts_and_escaped_code_is_left_alone(self):
        src = self.page('<!-- <p style="a:b"> --><pre>&lt;p style="a:b"&gt;</pre><script type="application/json">{"h":"<p style=1>"}</script>')
        self.assertEqual(e.transform(src), (src, {}))

    def test_self_closing_and_void_tags_keep_their_ending(self):
        html, _ = e.transform(self.page('<img src="a.png" style="a:b" /><br style="c:d">'))
        self.assertIn(f'<img src="a.png" class="{cls("a:b")}" />', html)
        self.assertIn(f'<br class="{cls("c:d")}">', html)

    def test_a_value_containing_a_greater_than_sign_does_not_end_the_tag_early(self):
        html, files = e.transform(self.page('<p style="content:\'>\'" id="k">x</p>'))
        self.assertIn(f'<p id="k" class="{cls(chr(99)+"ontent:\'>\'")}">', html)
        self.assertEqual(len(files), 1)

    def test_a_tag_with_a_style_and_a_known_handler_gets_both_fixes(self):
        dead = "try {parent.deselectBloggerImageGracefully();} catch(e) {}"
        html, _ = e.transform(self.page(f'<a onblur="{dead}" style="a:b" href="x">t</a>'))
        self.assertIn(f'<a href="x" class="{cls("a:b")}">', html)

    def test_a_rule_weighs_more_than_one_class_so_it_beats_the_sites_own_selectors(self):
        _, files = e.transform(self.page('<p style="transition-delay:.1s">x</p>'))
        (css,) = files.values()
        c = cls("transition-delay:.1s")
        self.assertTrue(css.startswith(f".{c}.{c}.{c}{{"))

    def test_broken_markup_where_a_less_than_sign_sits_inside_an_attribute_name_is_still_converted(self):
        # seen in an archived post: <youtube enabled="yes" <span="" style="font-weight: bold;">
        html, files = e.transform(self.page('<youtube enabled="yes" <span="" style="font-weight: bold;">t</youtube>'))
        self.assertNotIn("style=", html)
        self.assertIn(f'<youtube enabled="yes" <span="" class="{cls("font-weight: bold;")}">', html)
        self.assertEqual(len(files), 1)

    def test_quote_characters_inside_attribute_names_are_handled(self):
        # seen in an archived post: a bad export left style="font-family: " courier="" new",courier,monospace;"="">
        src = self.page('<span style="font-family: " courier="" new",courier,monospace;"="">$ x</span>')
        html, files = e.transform(src)
        self.assertNotIn("style=", html)
        self.assertIn('courier="" new",courier,monospace;"=""', html)
        self.assertIn(f'class="{cls("font-family:")}"', html)
        self.assertEqual(len(files), 1)

    def test_check_flags_a_style_attribute_in_a_tag_the_converter_cannot_parse(self):
        # unterminated quote: the converter leaves the tag alone, the independent check must still see it
        root = Tree().make({"a.html": '<p style="a:b>text</p>', "b.html": "<p>style=\"a:b\" in text</p>"})
        self.assertEqual(e.check(root), ["a.html"])

    def test_check_does_not_flag_style_text_that_is_not_an_attribute(self):
        root = Tree().make({"a.html": '<p>use style="a:b" or onclick=x in HTML</p><pre>&lt;p style="a:b"&gt;</pre>'})
        self.assertEqual(e.check(root), [])

    def test_check_ignores_tag_like_text_inside_script_data_and_comments(self):
        root = Tree().make({"a.html": '<script type="application/ld+json">{"h":"<p style=x>"}</script><!-- <b onclick=y> --><p>ok</p>'})
        self.assertEqual(e.check(root), [])

    def test_run_refuses_a_page_whose_style_attribute_it_cannot_convert(self):
        root = Tree().make({"a.html": '<p style="a:b>text</p>'})
        with self.assertRaises(ValueError):
            e.run(root)

    def test_second_run_changes_nothing(self):
        once, _ = e.transform(self.page('<p style="a:b">x</p>'))
        self.assertEqual(e.transform(once), (once, {}))

    def test_page_without_head_gets_the_link_at_the_end(self):
        html, files = e.transform('<p style="a:b">x</p>')
        name = next(iter(files))
        self.assertTrue(html.endswith(f'<link rel="stylesheet" href="/_next/static/inline/{name}">'))

    def test_the_attribute_stylesheet_comes_after_the_converted_style_elements(self):
        html, files = e.transform(self.page('<p style="a:b">x</p>', head="<style>z{}</style>"))
        self.assertEqual(len(files), 2)
        self.assertLess(html.index(digest("z{}")), html.index(digest(rule("a:b"))))

    def test_check_flags_pages_with_a_style_attribute(self):
        root = Tree().make({"a.html": '<p style="a:b">x</p>', "b.html": "<p>x</p>"})
        self.assertEqual(e.check(root), ["a.html"])

    def test_run_writes_the_stylesheet_and_leaves_no_style_attribute(self):
        root = Tree().make({"a.html": self.page('<p style="a:b">x</p>')})
        e.run(root)
        self.assertEqual(e.check(root), [])
        css = [f.read_text() for f in (root / "_next/static/inline").glob("*.css")]
        self.assertEqual(css, [rule("a:b")])


class Tree(unittest.TestCase):
    def make(self, pages: dict[str, str]) -> Path:
        root = Path(tempfile.mkdtemp())
        for name, text in pages.items():
            p = root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
        return root

    def test_files_are_written_under_next_static_inline_and_pages_rewritten(self):
        root = self.make({"index.html": PAGE, "a/b.html": PAGE})
        self.assertEqual(e.run(root), 2)
        name = digest(JOINED)
        self.assertEqual((root / "_next/static/inline" / f"{name}.js").read_text(), JOINED)
        self.assertEqual(len(list((root / "_next/static/inline").iterdir())), 1)  # identical content: one file
        self.assertNotIn("__next_f", (root / "a/b.html").read_text())

    def test_identical_style_blocks_on_many_pages_share_one_file(self):
        root = self.make({f"p{i}.html": "<style>.x{a:b}</style>" for i in range(5)})
        e.run(root)
        self.assertEqual(len(list((root / "_next/static/inline").iterdir())), 1)

    def test_check_lists_pages_with_inline_scripts_or_style_elements(self):
        root = self.make({"index.html": PAGE, "s.html": "<style>a{}</style>", "ok.html": "<p>x</p>"})
        self.assertEqual(e.check(root), ["index.html", "s.html"])

    def test_check_is_empty_after_run(self):
        root = self.make({"index.html": PAGE, "s.html": "<style>a{}</style>"})
        e.run(root)
        self.assertEqual(e.check(root), [])

    def test_check_ignores_json_ld_and_external_scripts(self):
        root = self.make({"i.html": '<script src="/a.js"></script><script type="application/ld+json">{}</script><p>x</p>'})
        self.assertEqual(e.check(root), [])

    def test_check_finds_a_redirect_stub_script(self):
        root = self.make({"old.html": "<body><script>window.location.replace('/x')</script></body>"})
        self.assertEqual(e.check(root), ["old.html"])

    def test_non_utf8_bytes_survive_a_rewrite(self):
        root = self.make({})
        (root / "x.html").write_bytes(b"<p>caf\xe9</p><script>a()</script>")
        e.run(root)
        self.assertIn(b"caf\xe9", (root / "x.html").read_bytes())


class Handlers(unittest.TestCase):
    DEAD = "try {parent.deselectBloggerImageGracefully();} catch(e) {}"

    def test_dead_blogger_onblur_handler_is_removed(self):
        src = f'<a onblur="{self.DEAD}" href="x"><img src="y"></a>'
        self.assertEqual(e.transform(src), ('<a href="x"><img src="y"></a>', {}))

    def test_async_css_idiom_becomes_a_plain_stylesheet(self):
        src = """<link href="/a.css" rel="stylesheet" media="print" onload="this.media='all'">"""
        self.assertEqual(e.transform(src), ('<link href="/a.css" rel="stylesheet">', {}))

    def test_async_css_idiom_with_attributes_in_another_order(self):
        src = """<link rel="stylesheet" onload="this.media='all'" href="/a.css" media="print">"""
        self.assertEqual(e.transform(src), ('<link rel="stylesheet" href="/a.css">', {}))

    def test_onload_on_a_link_with_another_media_is_refused(self):
        with self.assertRaises(ValueError):
            e.transform("""<link rel="stylesheet" href="/a.css" media="screen" onload="this.media='all'">""")

    def test_any_other_inline_handler_is_refused(self):
        for src in ('<button onclick="go()">x</button>', "<img src=a onerror='x()'>", '<body onload="init()">'):
            with self.assertRaises(ValueError, msg=src):
                e.transform(src)

    def test_handler_text_in_comments_scripts_and_escaped_code_is_left_alone(self):
        src = '<!-- <a onclick="x()"> --><pre>&lt;a onclick="x()"&gt;</pre><script type="application/json">{"a":"<b onclick=1>"}</script>'
        self.assertEqual(e.transform(src), (src, {}))

    def test_only_the_exact_dead_onblur_is_removed(self):
        with self.assertRaises(ValueError):
            e.transform('<input onblur="save()">')

    def test_the_onload_media_trick_is_accepted_only_on_a_link(self):
        with self.assertRaises(ValueError):
            e.transform("""<img media="print" onload="this.media='all'">""")

    def test_check_flags_a_page_with_a_handler(self):
        root = Tree().make({"a.html": f'<a onblur="{self.DEAD}">x</a>', "b.html": "<p>x</p>"})
        self.assertEqual(e.check(root), ["a.html"])

    def test_check_flags_a_page_with_a_handler_it_cannot_fix(self):
        root = Tree().make({"a.html": '<button onclick="go()">x</button>'})
        self.assertEqual(e.check(root), ["a.html"])


if __name__ == "__main__":
    unittest.main()
