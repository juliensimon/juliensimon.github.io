#!/usr/bin/env python3 -I
"""Move inline <script> and <style> code of a static export into content-hashed external files.

Why: the CSP must not allow 'unsafe-inline' for scripts or style elements. The Next.js export puts
its data in inline scripts (self.__next_f.push) and some archived posts carry <style> blocks.

Usage:
  python3 -I infra/externalize_inline.py next-site/out           rewrite pages in place
  python3 -I infra/externalize_inline.py --check next-site/out   exit 1 if any page still has inline code

Rules:
- all executable inline scripts of a page become ONE synchronous external script, placed where the
  first one was. They only push data, so running them together is equivalent, but they must run
  while the page is still parsing: Next.js closes its data stream when the page stops loading, and
  a deferred or async script arrives too late ("Connection closed", the page never hydrates);
- each <style> element becomes a <link rel=stylesheet> at the same position (cascade order holds);
- files are named by the hash of their content, so identical blocks share one file under
  /_next/static/inline/ (deploy.sh gives that folder a one-year immutable cache);
- JSON data blocks (application/ld+json, application/json) are left alone: CSP does not run them;
- the two inline event handlers the archive holds are removed: Blogger's dead onblur and the
  media=print + onload="this.media='all'" CSS trick (the link becomes a plain stylesheet); any other
  on*= attribute raises;
- every style="..." attribute becomes a CSS class (s-<hash of the value>); the rules of a page go into
  one stylesheet linked last in <head>, so they come after the page's own CSS. The class is repeated
  three times in the selector because an inline style beats any selector: a single class lost to the
  site's own `.js-reveal-ready [data-reveal]{transition:...}` and reset transition-delay. It stays a
  plain rule, not !important, so a script that sets the style later (React, Next image blur-up) still
  wins. The build test compares computed styles before and after;
- a second, looser scan fails the build for any style= or on*= attribute still in a tag after the
  rewrite, so markup the converter cannot parse cannot slip through unseen;
- anything this script cannot move without changing behavior (module or import-map scripts, async or
  nomodule attributes, a <style> with a nonce) raises, so a new kind of inline code stops the build.
"""
import hashlib
import html as htmllib
import re
import sys
from pathlib import Path

INLINE_DIR = "_next/static/inline"
BLOCK = re.compile(
    r"<!--.*?-->"  # comments are skipped
    r"|<script\b(?P<sattrs>[^>]*)>(?P<sbody>.*?)</script\s*>"
    r"|<style\b(?P<tattrs>[^>]*)>(?P<tbody>.*?)</style\s*>"
    r"|<(?P<htag>[a-zA-Z][a-zA-Z0-9]*)"
    r"(?P<hattrs>(?:\s+[^\s>=/]+(?:\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s\"'<>=`]+))?)+)\s*/?>",
    re.S | re.I,
)
ATTR = re.compile(r"""\s+(?P<name>[^\s>=/]+)(?:\s*=\s*(?P<val>"[^"]*"|'[^']*'|[^\s"'<>=`]+))?""")
# A looser, independent test: any tag that still carries style= or on*= after the rewrite. It does not
# share the strict tag pattern, so markup the converter cannot parse is still seen.
PROTECTED = re.compile(r"<!--.*?-->|<script\b.*?</script\s*>|<style\b.*?</style\s*>", re.S | re.I)
LOOSE = re.compile(r"<[a-zA-Z][^>]*?\s(?:style|on[a-z]+)\s*=", re.I)
DEAD_ONBLUR = "try {parent.deselectBloggerImageGracefully();} catch(e) {}"
ASYNC_CSS = "this.media='all'"
UNSAFE_CSS_VALUE = re.compile(r"[{}]|/\*")
DATA_TYPES = {"application/ld+json", "application/json"}
CLASSIC_TYPES = {"", "text/javascript", "application/javascript"}
UNSUPPORTED_SCRIPT_ATTR = re.compile(r"(?:^|\s)(?:async|defer|nomodule)(?=[\s=]|$)", re.I)
TYPE = re.compile(r"""\btype\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", re.I)
SRC = re.compile(r"(?:^|\s)src\s*=", re.I)
MEDIA = re.compile(r"""\bmedia\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.I)


def _name(content: str, ext: str) -> str:
    return f"{hashlib.sha256(content.encode('utf-8', 'surrogateescape')).hexdigest()[:16]}.{ext}"


def _script_type(attrs: str) -> str:
    m = TYPE.search(attrs)
    return next((g for g in m.groups() if g is not None), "").strip().lower() if m else ""


def _unquote(raw: str | None) -> str:
    if not raw:
        return ""
    return raw[1:-1] if raw[0] in "\"'" else raw


def _rewrite_tag(whole: str, tag: str, attrs_text: str, rules: dict[str, str]) -> str:
    """Handle the on*= and style= attributes of one tag; any tag without them is returned as it was.

    Known harmless handlers are removed, any other handler raises (the CSP would block it), and a
    style attribute becomes a class whose rule is recorded in `rules`."""
    toks = list(ATTR.finditer(attrs_text))
    low = [t.group("name").lower() for t in toks]
    if not any(n == "style" or (n.startswith("on") and n[2:].isalpha()) for n in low):
        return whole
    tail = whole[1 + len(tag) + len(attrs_text):]
    kept = []
    drop_print_media = False
    css_class = None
    for t, name in zip(toks, low):
        val = _unquote(t.group("val"))
        if name == "style":
            value = htmllib.unescape(val).strip()
            if value:
                if UNSAFE_CSS_VALUE.search(value):
                    raise ValueError(f"style value cannot be moved safely: {whole[:80]}")
                css_class = "s-" + hashlib.sha256(value.encode("utf-8", "surrogateescape")).hexdigest()[:8]
                rules.setdefault(css_class, value)
            continue
        if name.startswith("on") and name[2:].isalpha():
            if name == "onblur" and val == DEAD_ONBLUR:
                continue
            if name == "onload" and val == ASYNC_CSS and tag.lower() == "link":
                drop_print_media = True
                continue
            raise ValueError(f"inline event handler {name}= cannot be moved: {whole[:80]}")
        kept.append((t, name, val))
    if drop_print_media and not any(n == "media" and v.strip().lower() == "print" for _, n, v in kept):
        raise ValueError(f"onload media trick without media=print: {whole[:80]}")
    parts = []
    merged = False
    for t, name, val in kept:
        text = t.group(0)
        if drop_print_media and name == "media":
            continue
        if css_class and name == "class" and not merged:
            quote = t.group("val")[0] if t.group("val") and t.group("val")[0] in "\"'" else '"'
            lead = text[: len(text) - len(text.lstrip())]
            text = f"{lead}{t.group('name')}={quote}{(val.strip() + ' ' + css_class).strip()}{quote}"
            merged = True
        parts.append(text)
    if css_class and not merged:
        parts.append(f' class="{css_class}"')
    return "<" + tag + "".join(parts) + tail


def transform(html: str) -> tuple[str, dict[str, str]]:
    """Return the page with inline code moved out, and {file name: content} for the files it needs."""
    files: dict[str, str] = {}
    scripts: list[str] = []
    rules: dict[str, str] = {}
    state = {"first": None}

    def pieces(m: re.Match) -> str:
        whole = m.group(0)
        if whole.startswith("<!--"):
            return whole
        if m.group("htag") is not None:
            return _rewrite_tag(whole, m.group("htag"), m.group("hattrs"), rules)
        if m.group("sattrs") is not None:
            attrs = m.group("sattrs")
            if SRC.search(attrs):
                return whole
            kind = _script_type(attrs)
            if kind in DATA_TYPES:
                return whole
            if kind not in CLASSIC_TYPES:
                raise ValueError(f"inline script of type {kind!r} cannot be moved: {whole[:80]}")
            if UNSUPPORTED_SCRIPT_ATTR.search(attrs):
                raise ValueError(f"inline script attribute changes how it runs: {whole[:80]}")
            scripts.append(m.group("sbody"))
            if state["first"] is None:
                state["first"] = m.start()
                return "\x00SCRIPT\x00"
            return ""
        attrs = m.group("tattrs")
        leftover = MEDIA.sub("", attrs).strip()
        if leftover:
            raise ValueError(f"<style> attribute cannot be moved: {whole[:80]}")
        body = m.group("tbody")
        if not body.strip():
            return ""
        name = _name(body, "css")
        files[name] = body
        media = MEDIA.search(attrs)
        extra = f' media="{next(g for g in media.groups() if g is not None)}"' if media else ""
        return f'<link rel="stylesheet" href="/{INLINE_DIR}/{name}"{extra}>'

    out = BLOCK.sub(pieces, html)
    if scripts:
        joined = ";\n".join(scripts)
        name = _name(joined, "js")
        files[name] = joined
        out = out.replace("\x00SCRIPT\x00", f'<script src="/{INLINE_DIR}/{name}"></script>')
    if rules:
        css = "\n".join(f".{c}.{c}.{c}{{{v}}}" for c, v in rules.items())
        name = _name(css, "css")
        files[name] = css
        link = f'<link rel="stylesheet" href="/{INLINE_DIR}/{name}">'
        at = out.lower().rfind("</head>")
        out = out + link if at < 0 else out[:at] + link + out[at:]
    if out == html:
        return html, {}
    return out, files


def _leftover(page_text: str) -> bool:
    return bool(LOOSE.search(PROTECTED.sub("", page_text)))


def _read(p: Path) -> str:
    return p.read_bytes().decode("utf-8", "surrogateescape")


def run(root: Path) -> int:
    """Rewrite every page under root. Returns the number of pages changed."""
    root = Path(root)
    target = root / INLINE_DIR
    changed = 0
    for page in sorted(root.rglob("*.html")):
        text = _read(page)
        try:
            new, files = transform(text)
        except ValueError as err:
            raise ValueError(f"{page.relative_to(root)}: {err}") from None
        if _leftover(new):
            raise ValueError(f"{page.relative_to(root)}: a style or event-handler attribute is left that the converter cannot parse")
        if new == text:
            continue
        target.mkdir(parents=True, exist_ok=True)
        for name, content in files.items():
            (target / name).write_bytes(content.encode("utf-8", "surrogateescape"))
        page.write_bytes(new.encode("utf-8", "surrogateescape"))
        changed += 1
    return changed


def check(root: Path) -> list[str]:
    """Pages (relative paths) that still hold inline script code, a <style> element or an event handler."""
    root = Path(root)
    bad = []
    for page in sorted(root.rglob("*.html")):
        text = _read(page)
        try:
            new, _ = transform(text)
        except ValueError:
            bad.append(str(page.relative_to(root)))
            continue
        if new != text or _leftover(new):
            bad.append(str(page.relative_to(root)))
    return bad


def main(argv: list[str]) -> int:
    args = [a for a in argv if a != "--check"]
    if len(args) != 1:
        print(__doc__)
        return 2
    root = Path(args[0])
    if not root.is_dir():
        print(f"no such folder: {root}", file=sys.stderr)
        return 2
    if "--check" in argv:
        bad = check(root)
        for p in bad[:20]:
            print(f"inline code left in {p}", file=sys.stderr)
        if bad:
            print(f"{len(bad)} page(s) still hold inline script or style code: the CSP would block them", file=sys.stderr)
            return 1
        print("no inline script or style code left")
        return 0
    n = run(root)
    print(f"externalized inline code in {n} page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
