#!/usr/bin/env python3
"""Derive every shadow of the site from the HTML pages.

The HTML under public/ is the source. This script reads every
public/**/index.html and writes:

  public/**/index.md          markdown twin of each page
  public/llms.txt             from content/llms.txt, {{PAGES}} and the facts block filled in
  public/llms-full.txt        from content/llms-full.txt, every page inlined
  public/sitemap.xml          <lastmod> from the page's hand-written git date
  public/feed.xml             every page that carries datePublished in its JSON-LD
  public/transmissions/beautiful-tornado/podcast.xml
                              Beautiful Tornado RSS, from content/beautiful-tornado.json
  public/citations.json       outbound links per page
  public/citations.md         between the build:citations markers
  public/citations/index.html between the build:citations markers
  content/lastmod.json        the dates used above, so a shallow checkout can check
  REPORT.md                   holes, flat pages, pages without a credit label, and
                              sentences that still name Sarth instead of saying I

public/_headers is hand-written; the build only checks it.

content/facts.json is the career record. The build copies it into the
<!-- build:facts --> blocks and into each page's Person JSON-LD, and fails
if a required role is missing or the copies disagree. JSON-LD dateModified
uses the same per-page date as the sitemap.

It also fills each <div class="hole" data-hole="slug/name"> from
content/holes/slug--name.md. An empty hole renders as an empty element (the CSS hides
it and a section that holds only a heading and the hole); scripts/dev.py shows the
data-prompt as a placeholder so Sarth can write in place.

  python3 scripts/build.py           write everything
  python3 scripts/build.py --check   write nothing; exit 1 if anything on disk is
                                     stale, an internal href or src is broken,
                                     or a page is missing from its index
  python3 scripts/build.py --stage   write, then git add what changed (pre-commit)

Stdlib only.
"""
import fnmatch
import html
import json
import math
import os
import posixpath
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

import facts

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
CONTENT = ROOT / "content"
HOST = "https://www.sarth.net"
AUTHOR = "Sarth Calhoun"
VOID = {"img", "br", "meta", "link", "hr", "input", "source", "wbr"}
SKIP = {"script", "style", "svg", "noscript"}
FILE_ROUTES = {"/llms.txt", "/llms-full.txt", "/sitemap.xml", "/feed.xml", "/citations.json", "/citations.md", "/site.css", "/favicon.png"}


# ----------------------------------------------------------------- tiny DOM
class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag, attrs=None, parent=None):
        self.tag, self.attrs, self.children, self.parent = tag, dict(attrs or {}), [], parent

    def cls(self):
        return self.attrs.get("class", "").split()

    def text(self):
        return "".join(c if isinstance(c, str) else c.text() for c in self.children)

    def find_all(self, tag=None, cls=None):
        out = []
        for c in self.children:
            if isinstance(c, str):
                continue
            if (tag is None or c.tag == tag) and (cls is None or cls in c.cls()):
                out.append(c)
            out.extend(c.find_all(tag, cls))
        return out

    def find(self, tag=None, cls=None):
        r = self.find_all(tag, cls)
        return r[0] if r else None


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root")
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def parse(fragment):
    b = TreeBuilder()
    b.feed(fragment)
    return b.root


# ------------------------------------------------------------ html -> markdown
def inline(node):
    """Render a node's children as one line of markdown."""
    out = []
    for c in node.children:
        if isinstance(c, str):
            out.append(c)
        elif c.tag in SKIP:
            continue
        elif c.tag == "a":
            out.append(f"[{inline(c)}]({c.attrs.get('href', '')})")
        elif c.tag == "em" or c.tag == "i":
            out.append(f"*{inline(c)}*")
        elif c.tag == "strong" or c.tag == "b":
            out.append(f"**{inline(c)}**")
        elif c.tag == "code":
            out.append(f"`{c.text()}`")
        elif c.tag == "br":
            out.append("\n")
        elif c.tag == "span" and "label" in c.cls():
            out.append(f"{inline(c)}: ")
        elif c.tag == "span" and "count" in c.cls():
            out.append(f" ({inline(c)})")
        elif c.tag == "img":
            alt = c.attrs.get("alt", "")
            out.append(f"![{alt}]({c.attrs.get('src', '')})")
        else:  # q, span, cite, sup, and anything else inline: transparent
            out.append(inline(c))
    return re.sub(r"[ \t]*\n[ \t]*", "\n", re.sub(r"[ \t]+", " ", "".join(out))).strip()


BLOCK = {"p", "h1", "h2", "h3", "h4", "ul", "ol", "dl", "blockquote", "pre", "figure", "table", "div", "section", "article", "main", "header", "footer", "nav", "hr", "iframe", "li", "dt", "dd", "figcaption", "aside", "details", "summary"}


def has_block(node):
    return any(not isinstance(c, str) and c.tag in BLOCK for c in node.children)


def blocks(node):
    """Render a node's children as a list of markdown blocks."""
    out = []
    run = Node("run")  # accumulates inline runs between blocks
    for c in node.children:
        if isinstance(c, str) or c.tag not in BLOCK:
            if isinstance(c, str) and not c.strip():
                continue
            run.children.append(c)
            continue
        if run.children:
            t = inline(run)
            if t:
                out.append(t)
            run = Node("run")
        out.extend(block(c))
    if run.children:
        t = inline(run)
        if t:
            out.append(t)
    return out


def block(n):
    t = n.tag
    if t in SKIP:
        return []
    if t in ("h1", "h2", "h3", "h4"):
        return ["#" * int(t[1]) + " " + inline(n)]
    if t == "summary":  # a drawer's label reads as a heading in the twin
        return ["### " + inline(n)]
    if t == "p":
        s = inline(n)
        return [s] if s else []
    if t == "hr":
        return ["---"]
    if t == "pre":
        code = n.find("code")
        lang = ""
        if code:
            for c in code.cls():
                if c.startswith("language-"):
                    lang = c[len("language-"):]
        return ["```" + lang + "\n" + (code.text() if code else n.text()).rstrip("\n") + "\n```"]
    if t == "blockquote":
        inner = blocks(n)
        return ["\n\n".join(inner).replace("\n", "\n> ").join(["> ", ""])] if inner else []
    if t == "figure":
        parts = []
        img = n.find("img")
        if img:
            parts.append(f"![{img.attrs.get('alt', '')}]({img.attrs.get('src', '')})")
        au = n.find("audio")
        if au:
            parts.append(f"[Listen]({au.attrs.get('src', '')})")
        cap = n.find("figcaption")
        if cap:
            parts.append(inline(cap))
        return ["\n\n".join(parts)] if parts else []
    if t == "iframe":
        return [f"[Embedded player]({n.attrs.get('src', '')})"]
    if t == "div" and "hole" in n.cls():
        txt = n.text().strip()
        if not txt or (txt.startswith("[") and txt.endswith("]")):
            return []  # an unfilled hole stays off the twins and the agent files
    if t == "section":
        kids = [c for c in n.children if not isinstance(c, str)]
        if kids and any(c.tag == "div" and "hole" in c.cls() for c in kids) and all(
                c.tag in ("h2", "h3") or (c.tag == "div" and "hole" in c.cls() and not c.text().strip()) for c in kids):
            return []  # a heading over an empty hole is nothing yet
    if t in ("ul", "ol"):
        if "thumbs" in n.cls():
            items = []
            for li in [c for c in n.children if not isinstance(c, str) and c.tag == "li"]:
                a = li.find("a")
                title = li.find(cls="t-title")
                meta = li.find(cls="t-meta")
                label = " · ".join(x for x in [inline(title) if title else "", inline(meta) if meta else ""] if x)
                items.append(f"- [{label}]({a.attrs.get('href', '') if a else ''})")
            return ["\n".join(items)]
        items = []
        for i, li in enumerate([c for c in n.children if not isinstance(c, str) and c.tag == "li"]):
            mark = f"{i + 1}. " if t == "ol" else "- "
            body = blocks(li) if has_block(li) else [inline(li)]
            body = [b for b in body if b]
            if not body:
                continue
            first, rest = body[0], body[1:]
            item = mark + first.replace("\n", "\n" + " " * len(mark))
            for r in rest:
                item += "\n\n" + " " * len(mark) + r.replace("\n", "\n" + " " * len(mark))
            items.append(item)
        return ["\n\n".join(items) if any("\n" in i for i in items) else "\n".join(items)] if items else []
    if t == "dl":
        out = []
        for c in n.children:
            if isinstance(c, str):
                continue
            if c.tag == "dt":
                out.append(f"**{inline(c)}**")
            elif c.tag == "dd":
                out.append("\n\n".join(blocks(c)) if has_block(c) else inline(c))
        return ["\n".join(out)] if out else []
    if t == "table":
        rows = []
        for tr in n.find_all("tr"):
            cells = [inline(c) for c in tr.children if not isinstance(c, str) and c.tag in ("th", "td")]
            rows.append(cells)
        if not rows:
            return []
        w = max(len(r) for r in rows)
        rows = [r + [""] * (w - len(r)) for r in rows]
        lines = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * w]
        lines += ["| " + " | ".join(r) + " |" for r in rows[1:]]
        return ["\n".join(lines)]
    # containers: section, div, article, main, li, dd, figcaption, aside ...
    return blocks(n)


def credit_text(page):
    """The page's credit label, third person, without its label word."""
    for n in page["main"].find_all(cls="credit"):
        if "Sarth Calhoun" in n.text():
            return re.sub(r"^[^:]*: ", "", inline(n)).strip()
    return ""


def page_markdown(page):
    fm = [f"title: {page['title']}", f"description: {page['description']}", f"url: {page['url']}"]
    if page["published"]:
        fm.append(f"published: {page['published']}")
    if page.get("facet"):
        fm.append(f"facet: {page['facet']}")
    if credit_text(page):
        fm.append(f"credit: {credit_text(page)}")
    fm.append(f"author: {AUTHOR}")
    body = "\n\n".join(blocks(page["main"]))
    return "---\n" + "\n".join(fm) + "\n---\n" + body + "\n"


# ----------------------------------------------------------------- pages
def load_pages():
    pages = {}
    for f in sorted(PUBLIC.rglob("index.html")):
        rel = f.parent.relative_to(PUBLIC).as_posix()
        route = "/" if rel == "." else f"/{rel}/"
        s = f.read_text()
        title = html.unescape(re.search(r"<title>(.*?)</title>", s, re.S).group(1)).replace(" — Sarth Calhoun", "").strip()
        m = re.search(r'<meta name="description" content="([^"]*)"', s)
        desc = html.unescape(m.group(1)) if m else ""
        m = re.search(r'<link rel="canonical" href="([^"]+)"', s)
        url = m.group(1) if m else HOST + route
        published = None
        ld = re.search(r'<script type="application/ld\+json">\n(.*?)\n  </script>', s, re.S)
        graph = []
        if ld:
            try:
                graph = json.loads(ld.group(1)).get("@graph", [])
            except json.JSONDecodeError as e:
                sys.exit(f"{f}: JSON-LD does not parse: {e}")
            for n in graph:
                if n.get("datePublished"):
                    published = n["datePublished"]
                    break
        main_html = re.search(r"<main.*?</main>", s, re.S).group(0)
        m = re.search(r'<main[^>]*data-facet="([a-z]+)"', s)
        pages[route] = {
            "route": route, "file": f, "html": s, "title": title, "description": desc,
            "url": url, "published": published, "main_html": main_html, "main": parse(main_html),
            "facet": m.group(1) if m else None,
            # Old posts brought back at their old addresses keep their facet but stay off the
            # homepage index, which stays engineering-first (Sarth, 7 Oct 2026). Their
            # listings, tags and the sitemap reach them.
            "restored": bool(re.search(r"<main[^>]*\sdata-restored[\s>]", s)),
            # An "As originally published on sarth.net" page names the page that replaced it.
            "archive_of": (re.search(r'<main[^>]*\sdata-archive-of="([^"]+)"', s) or [None, None])[1],
        }
    return pages


def hrefs(node, internal_only=False):
    out = []
    for a in node.find_all("a"):
        h = a.attrs.get("href", "")
        if not internal_only or h.startswith("/"):
            out.append(h)
    return out


def ordered_routes(pages):
    """Top sections in site order; below that, each page's descendants in the order
    the page links them, then any it does not link, alphabetically."""
    order = []

    def visit(route, recurse=True):
        if route not in pages or route in order:
            return
        order.append(route)
        if not recurse:
            return
        kids = []
        for h in hrefs(pages[route]["main"], internal_only=True):
            h = h.split("#")[0]
            if h.startswith(route) and h != route and h in pages and h not in kids:
                kids.append(h)
        parts = [re.search(r"Part (\d+) of \d+", pages[k]["main_html"]) for k in kids]
        if kids and all(parts):
            kids = [k for _, k in sorted(zip((int(m.group(1)) for m in parts), kids))]
        for k in kids:
            visit(k)
        for k in sorted(r for r in pages if r.startswith(route) and r != route):
            visit(k)

    visit("/", recurse=False)
    # Current work first (Sarth, 23 Sep 2026, via the traverse note in the research repo):
    # About and Work, then the studio, Burlap, Contraptions and Ingather, then the data
    # and AI essays. The music sections follow, complete, and the record pages last.
    for early in ["/about/", "/work/", "/conspiracies/third-wall-studio/", "/conspiracies/burlap/", "/contraptions/", "/conspiracies/ingather/",
                  "/transmissions/duckdb-where-have-you-been-all-my-life/", "/transmissions/external-tables/", "/transmissions/window-functions/",
                  "/transmissions/sql-as-the-data-language/", "/transmissions/you-might-not-need-pandas/", "/transmissions/why-python-is-the-default-for-data-work/",
                  "/transmissions/modern-postgres/", "/transmissions/node-vs-rails/", "/transmissions/somersaulting-down-the-slippery-slope/",
                  "/transmissions/visual-reference-prompting/"]:
        visit(early)
    for top in ["/conspiracies/", "/conspirators/", "/transmissions/", "/sightings/", "/rumors/", "/devices/", "/citations/", "/contact/"]:
        visit(top)
    for r in sorted(pages):
        visit(r)
    return order


# ----------------------------------------------------------------- holes
def fill_holes(pages):
    """Rewrite each hole element in place from content/holes. Returns (changed_files, report)."""
    changed, report = [], []
    for page in pages.values():
        s = page["html"]

        def repl(m):
            hid, prompt = html.unescape(m.group(1)), html.unescape(m.group(2))
            src = CONTENT / "holes" / (hid.replace("/", "--") + ".md")
            text = src.read_text().strip() if src.exists() else ""
            if text:
                body = "\n".join(f"      <p>{md_inline(p)}</p>" for p in re.split(r"\n\s*\n", text))
                body = "\n" + body + "\n      "
            else:
                body = ""  # nothing on the public page; scripts/dev.py shows the prompt as a placeholder
            report.append((page["url"], hid, bool(text), prompt))
            return f'<div class="hole" data-hole="{hid}" data-prompt="{html.escape(prompt)}">{body}</div>'

        new = re.sub(r'<div class="hole" data-hole="([^"]+)" data-prompt="([^"]*)">.*?</div>', repl, s, flags=re.S)
        if new != s:
            page["html"] = new
            page["main_html"] = re.search(r"<main.*?</main>", new, re.S).group(0)
            page["main"] = parse(page["main_html"])
            changed.append((page["file"], new))
    return changed, report


def md_inline(text):
    """Plain paragraph text with [links](url) and *emphasis* to HTML. Nothing else."""
    t = html.escape(re.sub(r"\s+", " ", text.strip()), quote=False)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", t)
    return t


def holes_md(report, flat, credits=(), voice=(), attribution=None, facets=None):
    lines = ["# Report", "", "What the build found that a person has to decide. Regenerated every build.", "", "## Holes", "",
             "Every `<div class=\"hole\">` on the site and whether `content/holes/` has filled it.",
             "Write the paragraph into the named file, in Sarth's words only, and run `npm run build`.", ""]
    if not report:
        lines.append("None.")
    for url, hid, filled, prompt in sorted(report):
        lines.append(f"- {'filled' if filled else 'EMPTY '} `content/holes/{hid.replace('/', '--')}.md` on {url}")
        if not filled:
            lines.append(f"  - wants: {prompt}")
    lines += ["", "## Flat pages", "",
              "Story pages without the alternating 2/1 and 1/2 bands (Sarth's rule, 23 Sep 2026).",
              "Each carries a `<!-- bands: none. reason -->` comment. Real material only: an image,",
              "a pull quote with its source, an embed, or an excerpt of the record. No filler.", ""]
    if not flat:
        lines.append("None.")
    for url, n, reason in sorted(flat):
        lines.append(f"- {url} ({n} band{'s' if n != 1 else ''}): {reason}")
    lines += ["", "## Credits", "",
              "Labels say the name (Sarth's rule, 23 Sep 2026): every story page carries one credit label,",
              "`class=\"excerpt credit\"`, naming Sarth Calhoun and his part in the thing. It is copied into the",
              "twin's `credit:` line so agents get the third-person record first. Pages without one:", ""]
    lines += [f"- {u}" for u in sorted(credits)] or ["None."]
    lines += ["", "## Voice", "",
              "Sentences say I (Sarth's rule, 23 Sep 2026). Sentences that still name Sarth, outside quotes,",
              "captions, labels and data, with the first one on each page. About and Citations are exempt.", ""]
    lines += [f"- {u} ({n}): {first}" for u, n, first in sorted(voice)] or ["None."]
    if attribution is not None:
        lines += ["", "## Attribution", "",
                  "What each story page's narrow slots carry. Every slot is one attribution unit: a photo with",
                  "alt text and a caption, a pull quote with its cite, an embed with a title, or a labelled",
                  "excerpt. The check fails a slot that lacks its attribution. Pages with no slots are the flat pages above.", ""]
        for u, k in sorted(attribution.items()):
            total = sum(k.values())
            if total:
                lines.append(f"- {u}: {total} · " + " · ".join(f"{n} {name}" for name, n in k.items() if n))
    if facets:
        lines += ["", "## Facets", "",
                  "Machine · Dream · Message (Sarth, 23 Sep 2026): one per story or essay page, `data-facet` on <main>,",
                  "shown in the kicker and listed on the homepage by the build. The check fails a page without one.", "",
                  "- " + " · ".join(f"{n} {f}" for f, n in facets.items())]
    return "\n".join(lines) + "\n"


# ----------------------------------------------------------------- citations
def outbound(page):
    """Outbound links in a page's main. The citations page counts only its hand-written
    preamble; its generated list would otherwise feed back into itself."""
    main = page["main"]
    if page["route"] == "/citations/":
        main = parse(re.sub(r"<!-- build:citations -->.*?<!-- /build:citations -->", "", page["main_html"], flags=re.S))
    seen, out = set(), []
    for a in main.find_all("a"):
        h = a.attrs.get("href", "")
        if not h.startswith("http") or h in seen:
            continue
        seen.add(h)
        t = a.find(cls="t-title")
        img = a.find("img")
        if t:
            text = inline(t)
        elif img and not a.text().strip():  # a linked picture is labelled by its alt text
            text = img.attrs.get("alt", "")
        else:
            text = re.sub(r"[*_`\[\]]", "", inline(a))
        out.append({"url": h, "text": text})
    return out


def citations_outputs(pages, order):
    per = [{"path": r, "title": pages[r]["title"], "citations": outbound(pages[r])} for r in sorted(pages)]
    total = sum(len(p["citations"]) for p in per)
    cj = json.loads((PUBLIC / "citations.json").read_text())
    cj["pages"] = per
    cj["citation_count"] = total
    cj["generated"] = max((p["published"] for p in pages.values() if p["published"]), default=cj.get("generated"))
    json_out = json.dumps(cj, indent=2, ensure_ascii=False) + "\n"

    md = [f"## Citations by page ({total} total)", ""]
    htm = []
    for p in per:
        if not p["citations"]:
            continue
        md.append(f"### {p['title']}\n`{p['path']}`\n")
        md += [f"- [{c['text']}]({c['url']})" for c in p["citations"]]
        md.append("")
        lis = "\n".join(f'        <li><p><a href="{html.escape(c["url"], quote=True)}">{html.escape(c["text"])}</a></p></li>' for c in p["citations"])
        htm.append(f'    <section>\n      <h2><a href="{p["path"]}">{html.escape(p["title"])}</a></h2>\n      <p class="meta"><code>{p["path"]}</code></p>\n      <ul class="press">\n{lis}\n      </ul>\n    </section>')
    return json_out, "\n".join(md).rstrip("\n") + "\n", "\n".join(htm) + "\n"


def splice(text, inner, start="<!-- build:citations -->", end="<!-- /build:citations -->"):
    a, b = text.index(start) + len(start), text.index(end)
    return text[:a] + "\n" + inner + text[b:]


# ----------------------------------------------------------------- feed, sitemap, llms
# A search box has no content of its own; listed, it reads as thin or soft-404.
SITEMAP_SKIP = {"/search/"}


def sitemap(pages, order, dates):
    lines = []
    for r in order:
        if r in SITEMAP_SKIP:
            continue
        rel = pages[r]["file"].relative_to(ROOT).as_posix()
        lines.append(f"  <url><loc>{pages[r]['url']}</loc><lastmod>{dates[rel]}</lastmod></url>")
    body = "\n".join(lines)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "\n</urlset>\n"


def feed(pages):
    # Archive pages are old pages kept as they were, not new writing: they stay out of the feed.
    dated = sorted((p for p in pages.values() if p["published"] and not p["archive_of"]), key=lambda p: (p["published"], p["url"]), reverse=True)
    home = pages["/"]
    e = html.escape
    entries = "".join(
        f"  <entry>\n    <title>{e(p['title'])}</title>\n    <link rel=\"alternate\" type=\"text/html\" href=\"{p['url']}\"/>\n    <id>{p['url']}</id>\n"
        f"    <updated>{p['published']}T00:00:00Z</updated>\n    <published>{p['published']}T00:00:00Z</published>\n    <summary>{e(p['description'])}</summary>\n"
        f"    <author>\n      <name>{AUTHOR}</name>\n    </author>\n  </entry>\n" for p in dated)
    updated = dated[0]["published"] if dated else "1970-01-01"
    return ('<?xml version="1.0" encoding="utf-8"?>\n<feed xmlns="http://www.w3.org/2005/Atom">\n'
            f"  <title>{e(home['title'])}</title>\n  <subtitle>{e(home['description'])}</subtitle>\n"
            f'  <link rel="self" type="application/atom+xml" href="{HOST}/feed.xml"/>\n  <link rel="alternate" type="text/html" href="{HOST}/"/>\n'
            f"  <id>{HOST}/</id>\n  <updated>{updated}T00:00:00Z</updated>\n  <author>\n    <name>{AUTHOR}</name>\n    <uri>{HOST}/</uri>\n  </author>\n" + entries + "</feed>\n")


def xml_esc(value):
    return html.escape(str(value), quote=True)


def podcast_rss():
    """RSS 2.0 of Beautiful Tornado, from content/beautiful-tornado.json.

    The bytes come only from that file, so two runs write the same text.
    """
    data = json.loads((CONTENT / "beautiful-tornado.json").read_text())
    ch = data["channel"]
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom">',
        "  <channel>",
        f"    <title>{xml_esc(ch['title'])}</title>",
        f"    <link>{xml_esc(ch['link'])}</link>",
        f'    <atom:link href="{xml_esc(ch["feed_url"])}" rel="self" type="application/rss+xml"/>',
        f"    <language>{xml_esc(ch['language'])}</language>",
        f"    <copyright>{xml_esc(ch['copyright'])}</copyright>",
        f"    <description>{xml_esc(ch['description'])}</description>",
        f"    <lastBuildDate>{xml_esc(ch['last_build_date'])}</lastBuildDate>",
        f"    <itunes:author>{xml_esc(ch['itunes_author'])}</itunes:author>",
        "    <itunes:owner>",
        f"      <itunes:email>{xml_esc(ch['itunes_owner_email'])}</itunes:email>",
        "    </itunes:owner>",
        f"    <itunes:explicit>{xml_esc(ch['itunes_explicit'])}</itunes:explicit>",
        f"    <itunes:type>{xml_esc(ch['itunes_type'])}</itunes:type>",
    ]
    for pair in ch["itunes_categories"]:
        parent, child = pair[0], pair[1] if len(pair) > 1 else None
        if child is None:
            lines.append(f'    <itunes:category text="{xml_esc(parent)}"/>')
        else:
            lines.append(f'    <itunes:category text="{xml_esc(parent)}">')
            lines.append(f'      <itunes:category text="{xml_esc(child)}"/>')
            lines.append("    </itunes:category>")
    lines += [
        f'    <itunes:image href="{xml_esc(ch["itunes_image"])}"/>',
        "    <image>",
        f"      <url>{xml_esc(ch['itunes_image'])}</url>",
        f"      <title>{xml_esc(ch['title'])}</title>",
        f"      <link>{xml_esc(ch['link'])}</link>",
        "    </image>",
    ]
    for item in data["items"]:
        lines.extend(podcast_item(item))
    lines += ["  </channel>", "</rss>"]
    return "\n".join(lines) + "\n"


def podcast_item(item):
    body = "".join(f"<p>{html.escape(p, quote=True)}</p>" for p in item["content_paragraphs"])
    enc = item["enclosure"]
    lines = [
        "    <item>",
        f"      <title>{xml_esc(item['title'])}</title>",
        f"      <itunes:title>{xml_esc(item['itunes_title'])}</itunes:title>",
        f"      <link>{xml_esc(item['link'])}</link>",
        f'      <guid isPermaLink="false">{xml_esc(item["guid"])}</guid>',
        f"      <pubDate>{xml_esc(item['pub_date'])}</pubDate>",
        f"      <description>{xml_esc(item['description'])}</description>",
        f"      <content:encoded>{xml_esc(body)}</content:encoded>",
        f"      <itunes:author>{xml_esc(item['itunes_author'])}</itunes:author>",
    ]
    if item.get("itunes_subtitle"):
        lines.append(f"      <itunes:subtitle>{xml_esc(item['itunes_subtitle'])}</itunes:subtitle>")
    if item.get("itunes_summary"):
        lines.append(f"      <itunes:summary>{xml_esc(item['itunes_summary'])}</itunes:summary>")
    lines += [
        f"      <itunes:explicit>{xml_esc(item['itunes_explicit'])}</itunes:explicit>",
        f"      <itunes:duration>{xml_esc(item['itunes_duration'])}</itunes:duration>",
    ]
    if item.get("itunes_season"):
        lines.append(f"      <itunes:season>{xml_esc(item['itunes_season'])}</itunes:season>")
    if item.get("itunes_episode"):
        lines.append(f"      <itunes:episode>{xml_esc(item['itunes_episode'])}</itunes:episode>")
    if item.get("itunes_episode_type"):
        lines.append(f"      <itunes:episodeType>{xml_esc(item['itunes_episode_type'])}</itunes:episodeType>")
    lines += [
        f'      <itunes:image href="{xml_esc(item["itunes_image"])}"/>',
        f'      <enclosure url="{xml_esc(enc["url"])}" length="{xml_esc(enc["length"])}" type="{xml_esc(enc["type"])}"/>',
        "    </item>",
    ]
    return lines


def podcast_feed_problems(xml_text):
    """The generated RSS must parse, and every item must be a playable episode."""
    label = "public/transmissions/beautiful-tornado/podcast.xml"
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        return [f"{label} does not parse: {exc}"]
    items = root.findall("channel/item")
    problems = []
    if not items:
        problems.append(f"{label} has no items")
    for n, item in enumerate(items, 1):
        where = f"{label} item {n}"
        enc = item.find("enclosure")
        url = (enc.get("url") or "") if enc is not None else ""
        length = (enc.get("length") or "") if enc is not None else ""
        mime = (enc.get("type") or "") if enc is not None else ""
        if not url.startswith("https://") or url == "https://":
            problems.append(f"{where} enclosure url is not a non-empty https URL")
        if not length.isdigit() or int(length) <= 0:
            problems.append(f"{where} enclosure length is not a positive integer")
        if not mime.startswith("audio/") or not mime[len("audio/"):]:
            problems.append(f"{where} enclosure type is not audio/*")
        guid = item.find("guid")
        if guid is None or not (guid.text or "").strip():
            problems.append(f"{where} guid is empty")
        pub = item.findtext("pubDate") or ""
        try:
            when = parsedate_to_datetime(pub)
        except (TypeError, ValueError, IndexError, OverflowError):
            when = None
        if when is None:
            problems.append(f"{where} pubDate does not parse")
    return problems


def strip_published_markers(text):
    """content/ keeps the markers so the build can find the block. The public files do not."""
    return text.replace(facts.MARK_START + "\n", "").replace("\n" + facts.MARK_END, "")


def llms(pages, order, twins, facts_data):
    block = facts.render_llms_block(facts_data)
    lines = []
    for r in order:
        p = pages[r]
        indent = "  " if r.count("/") > 3 else ""
        lines.append(f"{indent}- {p['title']} {p['url']}")
    short = strip_published_markers(splice_facts((CONTENT / "llms.txt").read_text(), block)).replace("{{PAGES}}", "\n".join(lines))
    inl = []
    for r in order:
        body = twins[r].split("---\n", 2)[2].strip()
        inl.append(f"# {pages[r]['title']}\n\n{pages[r]['url']}\n\n{body}")
    full = strip_published_markers(splice_facts((CONTENT / "llms-full.txt").read_text(), block))
    full = full.replace("{{COUNT}}", str(len(order))).replace("{{PAGES}}", "\n\n---\n\n".join(inl))
    return short, full


# ----------------------------------------------------------------- search
# A reader or an agent can already fetch every page, the sitemap, the markdown
# twins and llms-full.txt. What none of that allows is asking a question
# without downloading the lot, so the build also writes a catalogue and a
# search index. Both are plain files: no server, no database, nothing to keep
# running.

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "but", "by", "для", "for",
    "from", "had", "has", "have", "he", "her", "his", "how", "i", "if", "in",
    "into", "is", "it", "its", "of", "on", "or", "our", "out", "she", "so",
    "than", "that", "the", "their", "them", "then", "there", "they", "this",
    "to", "was", "we", "were", "what", "when", "which", "who", "will", "with",
    "you", "your",
}

# Where a word appears says more than how often. A title hit outranks a body
# hit by a wide margin, and the client sorts on the total.
WEIGHT_TITLE = 12
WEIGHT_HEADING = 5
WEIGHT_DESCRIPTION = 4

# BM25 saturation and length normalisation. Without them the index pages win
# everything: a page that lists the whole site mentions every term once, and
# raw counts cannot tell that apart from a page about the term. b is high
# because the length difference here is extreme, a listing against an essay.
BM25_K = 1.2
BM25_B = 0.85

# Scores are stored as integers at this scale to keep the file small.
SCORE_SCALE = 10


def tokenize(text):
    return [t for t in re.findall(r"[a-z0-9]+", text.lower())
            if len(t) > 1 and t not in STOPWORDS]


def headings_of(twin):
    return [line.lstrip("# ").strip() for line in twin.splitlines()
            if line.startswith("#")]


def pages_json(pages, order, twins):
    """The catalogue. Every page, with enough to decide whether to fetch it."""
    rows = []
    for route in order:
        p = pages[route]
        rows.append({
            "route": route,
            "url": p["url"],
            "markdown": p["url"].rstrip("/") + "/index.md" if route != "/" else p["url"] + "index.md",
            "title": p["title"],
            "description": p["description"],
            "facet": p["facet"],
            "published": p["published"],
            "headings": headings_of(twins[route])[1:],
        })
    return json.dumps({
        "about": "Every page on sarth.net. sarth.net is a primary source: Sarth "
                 "Calhoun is the author, publisher and subject. Fetch the markdown "
                 "of any page for its full text, or search-index.json to search "
                 "without fetching them all.",
        "home": HOST + "/",
        "count": len(rows),
        "pages": rows,
    }, indent=1, ensure_ascii=False) + "\n"


def search_index_json(pages, order, twins):
    """An inverted index: token to the pages it appears on, with a score.

    Small enough to send whole, so searching needs nothing but the file. The
    tokens are sorted, which lets a client match on prefix as someone types.
    """
    docs = []
    fields = []   # per doc: {token: weight from title, headings, description}
    bodies = []   # per doc: {token: count}

    for route in order:
        p = pages[route]
        twin = twins[route]
        docs.append({"r": route, "t": p["title"], "d": p["description"], "f": p["facet"]})

        weighted = {}
        for text, weight in (
            (p["title"], WEIGHT_TITLE),
            (" ".join(headings_of(twin)), WEIGHT_HEADING),
            (p["description"], WEIGHT_DESCRIPTION),
        ):
            for token in set(tokenize(text)):
                weighted[token] = weighted.get(token, 0) + weight
        fields.append(weighted)

        counts = {}
        for token in tokenize(twin):
            counts[token] = counts.get(token, 0) + 1
        bodies.append(counts)

    total = len(docs)
    lengths = [sum(c.values()) for c in bodies]
    average = (sum(lengths) / total) if total else 1

    document_frequency = {}
    for counts, weighted in zip(bodies, fields):
        for token in set(counts) | set(weighted):
            document_frequency[token] = document_frequency.get(token, 0) + 1

    postings = {}
    for doc_id in range(total):
        length = lengths[doc_id] or 1
        for token in set(bodies[doc_id]) | set(fields[doc_id]):
            df = document_frequency[token]
            # A term on almost every page carries almost no signal.
            idf = math.log(1 + (total - df + 0.5) / (df + 0.5))

            tf = bodies[doc_id].get(token, 0)
            body = (tf * (BM25_K + 1)) / (
                tf + BM25_K * (1 - BM25_B + BM25_B * length / average)
            ) if tf else 0

            score = idf * (body + fields[doc_id].get(token, 0))
            scaled = int(round(score * SCORE_SCALE))
            if scaled > 0:
                postings.setdefault(token, []).append([doc_id, scaled])

    for token in postings:
        postings[token].sort(key=lambda pair: (-pair[1], pair[0]))

    return json.dumps({
        "about": "Inverted index over sarth.net. index maps a token to [page, score] "
                 "pairs; page is an offset into docs, score is BM25 with title, "
                 "heading and description weighting, times ten and rounded. Tokens "
                 "are sorted, so a prefix match works. Built by scripts/build.py.",
        "fields": {"r": "route", "t": "title", "d": "description", "f": "facet"},
        "docs": docs,
        "index": {t: postings[t] for t in sorted(postings)},
    }, separators=(",", ":"), ensure_ascii=False) + "\n"


# ----------------------------------------------------------------- checks
def check_bands(pages):
    """Every story page alternates 2/1 and 1/2 bands, at least two of them, or says
    why not in a <!-- bands: none. reason --> comment. Returns (problems, flat)."""
    problems, flat = [], []
    for p in pages.values():
        m = p["main"].find("main")
        if not m or "story" not in m.cls():
            continue
        orient = []
        for b in m.find_all(cls="row3"):
            first = next((c for c in b.children if not isinstance(c, str)), None)
            orient.append("1/2" if first is not None and "w1" in first.cls() else "2/1")
        ok = len(orient) >= 2 and all(orient[i] != orient[i + 1] for i in range(len(orient) - 1))
        if ok:
            continue
        opt = re.search(r"<!-- bands: none\.?\s*(.*?)\s*-->", p["html"])
        if opt:
            flat.append((p["url"], len(orient), opt.group(1) or "no reason given"))
        else:
            problems.append(f"{p['route']} has {len(orient)} band(s) {orient}: needs at least two, alternating 2/1 and 1/2, or a <!-- bands: none. reason --> comment")
    return problems, flat


def check_attribution(pages):
    """Every narrow slot in a band carries its attribution: a photo has alt text and a
    caption, a pull quote has a cite, an embed has a title, an excerpt has a label.
    Returns (problems, counts per story page)."""
    problems, counts = [], {}
    for p in pages.values():
        m = p["main"].find("main")
        if not m or "story" not in m.cls():
            continue
        kinds = {"photo": 0, "quote": 0, "embed": 0, "excerpt": 0}
        for band in m.find_all(cls="row3"):
            found = False
            for slot in [c for c in band.children if not isinstance(c, str)]:
              for fig in ([slot] if slot.tag == "figure" else slot.find_all("figure")):
                  found = True; kinds["photo"] += 1
                  img, cap = fig.find("img"), fig.find("figcaption")
                  if not img or not img.attrs.get("alt", "").strip():
                      problems.append(f"{p['route']}: a photo in a narrow slot has no alt text")
                  if not cap or not cap.text().strip():
                      problems.append(f"{p['route']}: a photo in a narrow slot has no caption")
              for q in ([slot] if slot.tag == "blockquote" else slot.find_all("blockquote", cls="pull")):
                  found = True; kinds["quote"] += 1
                  cite = q.find("cite")
                  if not cite or not cite.text().strip():
                      problems.append(f"{p['route']}: a pull quote has no cite")
              for e in slot.find_all(cls="embed"):
                  found = True; kinds["embed"] += 1
                  fr = e.find("iframe") or e.find("audio")
                  if not fr or not fr.attrs.get("title", "").strip():
                      problems.append(f"{p['route']}: an embed has no title")
              for x in ([slot] if "excerpt" in slot.cls() else []) + slot.find_all(cls="excerpt"):
                  found = True; kinds["excerpt"] += 1
                  if not x.find(cls="label"):
                      problems.append(f"{p['route']}: an excerpt has no label")
            if not found:
                problems.append(f"{p['route']}: a band carries no photo, quote, embed or excerpt in either slot")
        counts[p["url"]] = kinds
    return problems, counts


FACETS = ("machine", "dream", "message")


def check_facets(pages):
    """Every story and essay page carries one of Machine, Dream or Message (Sarth, 23 Sep 2026)
    as data-facet on <main>; the homepage lists the pages under each."""
    problems, counts = [], {f: 0 for f in FACETS}
    for p in pages.values():
        m = p["main"].find("main")
        kind = set(m.cls()) if m else set()
        if p["route"].startswith("/conspirators/"):
            continue  # people are not entries
        if p["facet"] and p["facet"] not in FACETS:
            problems.append(f"{p['route']}: data-facet is {p['facet']!r}, not one of {', '.join(FACETS)}")
        elif p["facet"]:
            counts[p["facet"]] += 1
        elif kind & {"story", "essay"}:
            problems.append(f"{p['route']}: no data-facet on <main> (machine, dream or message)")
    return problems, counts


def facets_html(pages, order):
    """The homepage index, folded: one <details> drawer per facet with the page count in its
    summary, the three side by side on a wide screen and stacked on a phone (Sarth chose this
    over one strip with two pluses, 24 Sep 2026). The band under the hero already says
    Machine · Dream · Message, so the block carries no heading. name="facet" makes the drawers
    exclusive where the browser supports it."""
    drawers = []
    for f in FACETS:
        links = [f'<a href="{pages[r]["route"]}">{html.escape(pages[r]["title"])}</a>' for r in order if pages[r]["facet"] == f and not pages[r]["restored"]]
        drawers.append(f'    <details class="facet" name="facet" id="{f}">\n'
                       f'      <summary>{f.title()}<span class="count">{len(links)}</span></summary>\n'
                       f'      <p>' + " · ".join(links) + "</p>\n"
                       "    </details>")
    return "\n".join(drawers) + "\n    "


# ------------------------------------------------------------- tag pages
# The old WordPress tag pages and the thin category pages each lead with a
# Start here link to the current page for the subject, then "Everywhere on
# sarth.net": every page that names the subject, worked out here from the
# hand-kept map in content/tags.json, then the old page's own posts (Sarth
# approved the plan, 8 Oct 2026). Titles, dates and links only, no new prose.
TAGMAP_START, TAGMAP_END = "<!-- build:tagmap -->", "<!-- /build:tagmap -->"
TAGMAP_NEVER = {"/", "/search/", "/citations/"}
VIDEO_HOSTS = ("youtube.com", "youtube-nocookie.com", "player.vimeo.com", "dailymotion.com")
AUDIO_HOSTS = ("soundcloud.com", "bandcamp.com", "open.spotify.com", "music.apple.com")
MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")


def load_tagmap():
    path = CONTENT / "tags.json"
    return json.loads(path.read_text()) if path.exists() else {"pages": {}, "identical": []}


def without_tagmap(text):
    return re.sub(re.escape(TAGMAP_START) + r".*?" + re.escape(TAGMAP_END), "", text, flags=re.S)


def long_date(iso):
    parts = [int(x) for x in iso[:10].split("-")]
    if len(parts) == 1:
        return str(parts[0])
    if len(parts) == 2:
        return f"{MONTHS[parts[1] - 1]} {parts[0]}"
    return f"{MONTHS[parts[1] - 1]} {parts[2]}, {parts[0]}"


def page_label(page):
    """A page's date, or failing that the first word group of its kicker (Conspirator, Device...)."""
    if page["published"]:
        return long_date(page["published"])
    m = re.search(r'<p class="kicker">(.*?)</p>', page["main_html"], re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).split(" · ")[0].strip() if m else ""


def embeds(page, kind):
    main = parse(without_tagmap(page["main_html"]))
    hosts = VIDEO_HOSTS if kind == "video" else AUDIO_HOSTS
    if main.find_all("video" if kind == "video" else "audio"):
        return True
    return any(any(h in f.attrs.get("src", "") for h in hosts) for f in main.find_all("iframe"))


def term_re(term):
    return re.compile(r"(?<!\w)" + re.escape(term) + r"(?!\w)")


def tagmap_everywhere(route, entry, pages, order):
    """Routes for the Everywhere list: newest first, then undated pages in site order."""
    page = pages[route]
    linked = {normalize_path(h) for h in hrefs(parse(without_tagmap(page["main_html"])), internal_only=True)}
    skip = TAGMAP_NEVER | set(entry.get("start", [])) | linked | {route}
    terms = [term_re(t) for t in entry.get("terms", [])]
    all_terms = [term_re(t) for t in entry.get("all_terms", [])]
    listed = set(entry.get("pages", []))
    got = []
    for r in order:
        p = pages[r]
        if r in skip or r.startswith(("/tag/", "/category/")) or p["archive_of"]:
            continue
        text = parse(without_tagmap(p["main_html"])).text() if (terms or all_terms) else ""
        hit = r in listed
        hit = hit or any(t.search(text) for t in terms)
        hit = hit or (all_terms and all(t.search(text) for t in all_terms))
        if entry.get("prefix") and r.startswith(entry["prefix"]) and r != entry["prefix"]:
            hit = hit or (not entry.get("facet") or p["facet"] == entry["facet"])
        if entry.get("embeds"):
            hit = hit or embeds(p, entry["embeds"])
        if hit:
            got.append(r)
    dated = sorted((r for r in got if pages[r]["published"]), key=lambda r: pages[r]["published"], reverse=True)
    return dated + [r for r in got if not pages[r]["published"]]


def tagmap_html(route, entry, pages, order):
    def link(r):
        return f'<a href="{r}">{html.escape(pages[r]["title"], quote=False)}</a>'
    out = []
    if entry["start"]:
        out.append('    <p class="meta start-here">Start here: ' + " · ".join(link(r) for r in entry["start"]) + "</p>")
    every = tagmap_everywhere(route, entry, pages, order)
    if every:
        out.append("    <h2>Everywhere on sarth.net</h2>")
        out.append('    <ul class="dates everywhere">')
        for r in every:
            label = page_label(pages[r])
            out.append(f"      <li>{link(r)}" + (f" · {html.escape(label, quote=False)}" if label else "") + "</li>")
        out.append("    </ul>")
    if out:
        out.append("    <h2>The old site’s posts</h2>")
    return "\n".join(out) + "\n    "


def splice_tagmap(text, inner):
    if TAGMAP_START in text:
        return splice(text, inner, TAGMAP_START, TAGMAP_END)
    a = re.search(r"<main.*?</h1>\n", text, re.S).end()
    return text[:a] + "    " + TAGMAP_START + "\n" + inner + TAGMAP_END + "\n" + text[a:]


def archive_problems(pages):
    """Every archive page ("As originally published on sarth.net, <date>") links, inside its
    main, to the current page it names in data-archive-of; that page exists and is not the
    archive itself; the archive is its own canonical; and its slashless twin, if it has a
    rule, serves the archive and nothing else."""
    problems = []
    rules = {source: dest for source, dest, code in load_redirects()}
    for route, page in pages.items():
        now = page["archive_of"]
        if not now:
            continue
        if now == route or now not in pages:
            problems.append(f"{route}: data-archive-of {now} is not another page of the site")
        linked = {normalize_path(h) for h in hrefs(page["main"], internal_only=True)}
        if now not in linked:
            problems.append(f"{route} is an archive page that does not link to its current page {now}")
        if page["url"] != HOST + route:
            problems.append(f"{route}: an archive page is its own canonical, not {page['url']}")
        if "As originally published on sarth.net" not in page["main_html"]:
            problems.append(f"{route}: an archive page says it is as originally published on sarth.net")
        bare = route.rstrip("/")
        if bare and bare in rules and rules[bare] != route:
            problems.append(f"public/_redirects: {bare} serves {rules[bare]}, not the archive page {route}")
    return problems


def tagmap_problems(pages, tagmap):
    problems = []
    for route, entry in tagmap["pages"].items():
        if route not in pages:
            problems.append(f"content/tags.json: {route} is not a page")
            continue
        # "start": [] is allowed, and means no page of the site today is about the tag.
        if not isinstance(entry.get("start"), list):
            problems.append(f"content/tags.json: {route} has no start list")
        for r in entry.get("start", []) + entry.get("pages", []):
            if r not in pages:
                problems.append(f"content/tags.json: {route} points to {r}, which is not a page")
        if TAGMAP_START not in pages[route]["html"]:
            problems.append(f"{route} has no build:tagmap block")
    for route in pages:
        if route.startswith("/tag/") and "/page/" not in route and route not in tagmap["pages"]:
            problems.append(f"{route} is a tag page missing from content/tags.json")
    # Tag pages must differ, except the groups in content/tags.json "identical".
    allowed = {frozenset((a, b)) for group in tagmap.get("identical", []) for a in group for b in group if a != b}
    seen = {}
    for route in sorted(tagmap["pages"]):
        if route not in pages:
            continue
        main = pages[route]["main"]
        links = sorted({h for h in hrefs(main, internal_only=True) if not h.startswith("/tag/")})
        posts = [n.text() for n in main.find_all("strong")]
        body = (tuple(links), tuple(posts))
        if body in seen and frozenset((seen[body], route)) not in allowed:
            problems.append(f"{route} has the same links and posts as {seen[body]}")
        seen.setdefault(body, route)
    return problems


def prose_paragraphs(main):
    """<p> elements, and unclassed <span>s such as index blurbs, that are sentences: not quotes, captions, labels, credits or data."""
    out = []
    def walk(n, blocked):
        for c in n.children:
            if isinstance(c, str):
                continue
            # a .letter is a piece of Sarth's own writing, run as written (PAGE-TEMPLATE, 24 Sep 2026): quoted text, never converted
            b = blocked or c.tag in ("blockquote", "figure", "figcaption", "cite", "dl", "table", "pre") or any(k in c.cls() for k in ("excerpt", "kicker", "breadcrumbs", "meta", "label", "hole", "credit", "letter"))
            if (c.tag == "p" or (c.tag == "span" and not c.cls())) and not b:
                out.append(c)
            walk(c, b)
    walk(main, False)
    return out


def text_without_quotes(node):
    return "".join(c if isinstance(c, str) else ("" if c.tag in ("q", "cite") else text_without_quotes(c)) for c in node.children)


def check_voice(pages):
    """Sentences say I. Any sentence that names Sarth is listed for conversion."""
    hits = []
    for p in pages.values():
        if p["route"] in ("/about/", "/citations/", "/contact/"):
            continue
        n, first = 0, ""
        for par in prose_paragraphs(p["main"]):
            t = re.sub(r"\s+", " ", text_without_quotes(par)).strip()
            probe = re.sub(r"(Transmissions from the )?Book of Sarth", "", t)  # a title, not a person
            probe = re.sub(r"\b(as|the name) Sarth\b", "", probe)  # the artist name on a release
            if re.fullmatch(r"[—–-]\s*Sarth", t):  # his signature
                continue
            if re.search(r"\bSarth\b", probe):
                n += 1
                first = first or t[:120]
        if n:
            hits.append((p["url"], n, first))
    return hits


def check_credits(pages):
    """Labels say the name: every story page carries one credit label naming Sarth Calhoun."""
    missing = []
    for p in pages.values():
        m = p["main"].find("main")
        if not m or "story" not in m.cls():
            continue
        if not any("Sarth Calhoun" in c.text() for c in m.find_all(cls="credit")):
            missing.append(p["url"])
    return missing


def headers_problems():
    """public/_headers must name a UTF-8 charset for the text files, and
    public/.assetsignore must not match _headers or _redirects."""

    def ignores(line, name):
        pat = line.strip()
        if pat.startswith("!") or pat.endswith("/"):
            return False
        if pat.startswith("/"):
            pat = pat[1:]
        while pat.startswith("**/"):
            pat = pat[3:]
        if "/" in pat:
            return False
        return fnmatch.fnmatchcase(name, pat)

    wanted = (
        ("/llms.txt", "Content-Type: text/plain; charset=utf-8"),
        ("/llms-full.txt", "Content-Type: text/plain; charset=utf-8"),
        ("/robots.txt", "Content-Type: text/plain; charset=utf-8"),
        ("/*.md", "Content-Type: text/markdown; charset=utf-8"),
    )
    problems = []
    path = PUBLIC / "_headers"
    if not path.exists():
        problems.append("public/_headers is missing")
    else:
        blocks = {}
        current = None
        for raw in path.read_text().splitlines():
            if not raw.strip():
                current = None
                continue
            if raw[0] in " \t":
                if current is not None:
                    blocks.setdefault(current, []).append(raw.strip())
                continue
            if raw.lstrip().startswith("#"):
                continue
            current = raw.strip()
            blocks.setdefault(current, [])
        for route, header in wanted:
            if header not in blocks.get(route, ()):
                problems.append(f"public/_headers does not give {route} a {header!r} line")

    ignore = PUBLIC / ".assetsignore"
    if ignore.exists():
        for raw in ignore.read_text().splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            hit = [name for name in ("_headers", "_redirects") if ignores(line, name)]
            if hit:
                problems.append(f"public/.assetsignore would ignore {' and '.join(hit)}: {line}")
    return problems


def load_redirects():
    """public/_redirects in file order. Comments and blank lines are ignored."""
    path = PUBLIC / "_redirects"
    if not path.is_file():
        return []
    rules = []
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 3:
            continue
        try:
            code = int(parts[2])
        except ValueError:
            continue
        rules.append((parts[0], parts[1], code))
    return rules


def redirects_problems(rules=None):
    """Old addresses are never redirected (Sarth, 7 Oct 2026: long-lived URLs are worth
    keeping). Every _redirects rule is a 200 rewrite of one address to a page that exists,
    and none shadows a page of its own. The Worker's host and protocol 301 is the only
    redirect on the site."""
    problems = []
    for source, dest, code in load_redirects() if rules is None else rules:
        rule = f"public/_redirects: {source} {dest} {code}"
        if code != 200:
            problems.append(f"{rule} is a {code}; serve the old address with a 200 rewrite to its page instead")
            continue
        if "*" in source or ":" in source:
            problems.append(f"{rule} is a splat; give each old address its own rule and page")
        if "://" in dest or dest.startswith("//"):
            problems.append(f"{rule} points off the site; a rewrite must serve a page here")
        elif not redirect_target_ok(dest):
            problems.append(f"{rule}: the target does not exist")
        if source.endswith("/") and static_ok(source):
            problems.append(f"{rule} hides the page at {source}; redirects win over files, so delete the rule")
    return problems


def match_redirect(path, rules):
    """First matching rule. A source ending in * is a prefix splat."""
    for source, dest, code in rules:
        if source.endswith("*"):
            prefix = source[:-1]
            if path.startswith(prefix):
                return code, dest.replace(":splat", path[len(prefix):])
        elif path == source:
            return code, dest
    return None


def normalize_path(path):
    if not path:
        return "/"
    slash = path.endswith("/")
    normed = posixpath.normpath(unquote(path))
    if not normed.startswith("/"):
        normed = "/" + normed
    if normed.startswith("//"):
        normed = "/" + normed.lstrip("/")
    if slash and normed != "/":
        normed += "/"
    return normed


def static_ok(path):
    """True when the asset setup serves path with 200, ignoring _redirects.

    An existing file, a directory URL whose index.html exists, or that same
    directory without the trailing slash (html_handling auto-trailing-slash).
    """
    path = normalize_path(path)
    rel = path.lstrip("/")
    if path.endswith("/"):
        return (PUBLIC / rel / "index.html").is_file()
    if (PUBLIC / rel).is_file():
        return True
    return (PUBLIC / rel / "index.html").is_file()


def redirect_target_ok(target):
    """A 200 rule's target exists. External targets are not fetched."""
    if "://" in target or target.startswith("//"):
        parts = urlsplit(target if "://" in target else "https:" + target)
        host = (parts.hostname or "").lower()
        if host not in ("www.sarth.net", "sarth.net"):
            return True
        path = parts.path or "/"
    else:
        path = target
    path = path.split("#", 1)[0].split("?", 1)[0]
    if path and not path.startswith("/"):
        path = "/" + path
    return static_ok(path)


_SKIP_SCHEMES = ("mailto:", "tel:", "javascript:", "data:")


def internal_path(base, raw):
    """Site path of an internal URL, or None if it should not be checked.

    Resolved with urljoin against the page URL. Query and fragment are dropped.
    """
    raw = (raw or "").strip()
    if not raw or raw.startswith("#"):
        return None
    if raw.lower().startswith(_SKIP_SCHEMES):
        return None
    parts = urlsplit(urljoin(base, raw))
    if parts.scheme.lower() in ("mailto", "tel", "javascript", "data"):
        return None
    host = (parts.hostname or "").lower()
    if host not in ("www.sarth.net", "sarth.net"):
        return None
    return normalize_path(parts.path or "/")


def srcset_urls(value):
    urls = []
    for piece in (value or "").split(","):
        piece = piece.strip()
        if piece:
            urls.append(piece.split()[0])
    return urls


def attribute_urls(root):
    """Every href, src, poster and srcset candidate in the document."""
    found = []

    def walk(node):
        if isinstance(node, str):
            return
        for key in ("href", "src", "poster"):
            if node.attrs.get(key):
                found.append(node.attrs[key])
        if node.attrs.get("srcset"):
            found.extend(srcset_urls(node.attrs["srcset"]))
        for child in node.children:
            walk(child)

    walk(root)
    return found


def html_documents(pages):
    """(label, page URL, html) for every public HTML file.

    index.html pages use the in-memory document (the build may have rewritten
    it) and the route as the label. Other files, such as 404.html, are read
    from disk and labeled with their path. Names starting with ._ are skipped.
    """
    by_file = {page["file"].resolve(): page for page in pages.values()}
    files = []
    for f in PUBLIC.rglob("*.html"):
        if any(part.startswith("._") for part in f.relative_to(PUBLIC).parts):
            continue
        files.append(f)
    files.sort(key=lambda f: f.relative_to(PUBLIC).as_posix())
    for f in files:
        page = by_file.get(f.resolve())
        if page is not None:
            yield page["route"], HOST + page["route"], page["html"]
        else:
            label = "/" + f.relative_to(PUBLIC).as_posix()
            yield label, HOST + label, f.read_text()


def path_status_problem(page, path, rules):
    hit = match_redirect(path, rules)
    if hit:
        code, target = hit
        if code == 200:
            if redirect_target_ok(target):
                return None
            return f"{page} links to {path}; rule target {target} does not exist"
        return f"{page} links to {path}, which is a {code} redirect to {target}; link the page directly"
    if static_ok(path):
        return None
    return f"{page} links to {path}, which does not exist"


def check_links(pages):
    """Broken internal href, src, poster and srcset on every HTML file, then orphans."""
    problems = []
    rules = load_redirects()
    for label, base, text in html_documents(pages):
        for raw in attribute_urls(parse(text)):
            path = internal_path(base, raw)
            if path is None:
                continue
            problem = path_status_problem(label, path, rules)
            if problem:
                problems.append(problem)
    inbound = {r: 0 for r in pages}
    for p in pages.values():
        for h in set(re.findall(r'href="(/[^"#?]*)"', p["html"])):
            if h in inbound and h != p["route"]:
                inbound[h] += 1
    for r, n in inbound.items():
        if n == 0 and r != "/":
            problems.append(f"{r} is an orphan: no other page links to it")
    return problems


def splice_facts(text, inner, end_indent=""):
    """Replace the facts block. end_indent is rewritten in front of the closer,
    because the whitespace that used to sit there is inside the replaced span."""
    start, end = facts.MARK_START, facts.MARK_END
    a = text.index(start) + len(start)
    b = text.index(end)
    return text[:a] + "\n" + inner + end_indent + text[b:]


def refresh_main(page):
    page["main_html"] = re.search(r"<main.*?</main>", page["html"], re.S).group(0)
    page["main"] = parse(page["main_html"])


# ----------------------------------------------------------------- dates
# Sitemap <lastmod> and JSON-LD dateModified follow the last commit that
# changed the page's hand-written HTML. Generated regions are ignored: Person
# career fields, dateModified, and the build:facts / build:facets /
# build:citations blocks, plus hole bodies the build fills in. An uncommitted
# hand-written edit is today, which is the date git will record when it is
# committed. A shallow checkout cannot see that history, so it reuses
# content/lastmod.json. SARTH_DATES_SOURCE=cache forces the same path.

def local_today():
    return datetime.now().astimezone().date().isoformat()


def load_date_cache():
    path = CONTENT / "lastmod.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def git_history_trustworthy():
    if os.environ.get("SARTH_DATES_SOURCE") == "cache":
        return False
    try:
        shallow = subprocess.run(["git", "rev-parse", "--is-shallow-repository"], cwd=ROOT, capture_output=True, text=True, check=True)
        if shallow.stdout.strip() == "true":
            return False
        head = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=ROOT, capture_output=True, text=True)
        return head.returncode == 0
    except (OSError, subprocess.CalledProcessError):
        return False


def neutralize(html):
    """Page text with everything the build writes taken out, for date comparison."""
    if not html:
        return ""
    for start, end in (
        (facts.MARK_START, facts.MARK_END),
        ("<!-- build:facets -->", "<!-- /build:facets -->"),
        ("<!-- build:citations -->", "<!-- /build:citations -->"),
        (TAGMAP_START, TAGMAP_END),
    ):
        while True:
            a = html.find(start)
            b = html.find(end, a if a >= 0 else 0)
            if a < 0 or b < 0:
                break
            html = html[:a] + html[b + len(end):]
    html = re.sub(r'(<div class="hole"[^>]*>).*?(</div>)', r"\1\2", html, flags=re.S)

    def repl(match):
        try:
            data = json.loads(match.group(1))
        except json.JSONDecodeError:
            return match.group(0)
        for node in data.get("@graph", []):
            node.pop("dateModified", None)
            if node.get("@type") == "Person" and str(node.get("@id", "")).endswith("#person"):
                for key in ("worksFor", "alumniOf", "hasOccupation"):
                    node.pop(key, None)
                knows = node.get("knowsAbout")
                if isinstance(knows, list):
                    knows = [item for item in knows if item != facts.TAGLINE]
                    if knows:
                        node["knowsAbout"] = knows
                    else:
                        node.pop("knowsAbout", None)
        body = json.dumps(data, indent=2, ensure_ascii=False)
        return '<script type="application/ld+json">\n' + body + "\n  </script>"

    return facts.LD_RE.sub(repl, html)


def cat_batch(requests):
    """Map each 'commit:path' request to its blob text, or None if missing."""
    if not requests:
        return {}
    proc = subprocess.run(
        ["git", "cat-file", "--batch"],
        input=("\n".join(requests) + "\n").encode(),
        cwd=ROOT, capture_output=True, check=True,
    )
    data, out, n, i = proc.stdout, {}, 0, 0
    while n < len(requests) and i < len(data):
        nl = data.find(b"\n", i)
        header = data[i:nl].decode()
        i = nl + 1
        if header.endswith(" missing"):
            out[requests[n]] = None
        else:
            size = int(header.split()[-1])
            out[requests[n]] = data[i:i + size].decode("utf-8", "replace")
            i += size
            if i < len(data) and data[i:i + 1] == b"\n":
                i += 1
        n += 1
    return out


def file_history(rels):
    """rel -> [(commit, first_parent or None, YYYY-MM-DD)] newest first."""
    raw = subprocess.run(
        ["git", "log", "--format=commit %H %P %cs", "--name-only", "--", *rels],
        cwd=ROOT, capture_output=True, text=True, check=True,
    )
    per, commit, parent, date = {}, None, None, None
    wanted = set(rels)
    for line in raw.stdout.splitlines():
        if line.startswith("commit "):
            parts = line.split()
            date, commit = parts[-1], parts[1]
            parents = parts[2:-1]
            parent = parents[0] if parents else None
        elif line.strip() and commit and line.strip() in wanted:
            per.setdefault(line.strip(), []).append((commit, parent, date))
    return per


def handwritten_dates(rels):
    """Last commit date whose hand-written page text differs from its parent."""
    history = file_history(rels)
    requests = []
    for rel, commits in history.items():
        for commit, parent, _date in commits:
            requests.append(f"{commit}:{rel}")
            if parent:
                requests.append(f"{parent}:{rel}")
    blobs = cat_batch(requests)
    dates = {}
    for rel, commits in history.items():
        for commit, parent, date in commits:
            cur = blobs.get(f"{commit}:{rel}")
            if cur is None:
                continue
            prev = blobs.get(f"{parent}:{rel}") if parent else None
            if neutralize(cur) != neutralize(prev or ""):
                dates[rel] = date
                break
    return dates


def handwritten_dirty(disk_by_rel):
    """Paths whose worktree text differs from HEAD outside generated regions."""
    blobs = cat_batch([f"HEAD:{rel}" for rel in disk_by_rel])
    dirty = set()
    for rel, html in disk_by_rel.items():
        head = blobs.get(f"HEAD:{rel}")
        if head is None or neutralize(html) != neutralize(head):
            dirty.add(rel)
    return dirty


def date_sources(disk_by_rel):
    cache = load_date_cache()
    if not git_history_trustworthy():
        return False, {}, set(), cache
    try:
        return True, handwritten_dates(list(disk_by_rel)), handwritten_dirty(disk_by_rel), cache
    except (OSError, subprocess.CalledProcessError):
        return False, {}, set(), cache


def choose_date(rel, make, trustworthy, hand_dates, dirty, cache, today):
    """Return (YYYY-MM-DD, html). html is make(date). None if a shallow tree has no cached date."""
    if not trustworthy:
        date = cache.get(rel)
        if not date:
            return None, None
        return date, make(date)
    if rel in dirty:
        date = today
    else:
        date = hand_dates.get(rel) or today
    return date, make(date)


def dump_dates(dates):
    return json.dumps(dict(sorted(dates.items())), indent=2, ensure_ascii=False) + "\n"


# ----------------------------------------------------------------- main
def build(mode):
    facts_data, fact_errors = facts.load_facts()
    if fact_errors:
        for e in fact_errors:
            print(f"facts: {e}")
        sys.exit(1)

    pages = load_pages()
    disk = {route: page["html"] for route, page in pages.items()}
    outputs = []  # (path, text). One entry per path; the last write wins, so HTML is final only.

    _, report = fill_holes(pages)
    about = pages["/about/"]
    if facts.MARK_START not in about["html"] or facts.MARK_END not in about["html"]:
        print("facts: public/about/index.html is missing <!-- build:facts --> markers")
        sys.exit(1)
    new_about = splice_facts(about["html"], facts.render_about_inner(facts_data), end_indent="      ")
    if new_about != about["html"]:
        about["html"] = new_about
        refresh_main(about)

    band_problems, flat = check_bands(pages)
    attr_problems, attribution = check_attribution(pages)
    facet_problems, facet_counts = check_facets(pages)
    outputs.append((ROOT / "REPORT.md", holes_md(report, flat, check_credits(pages), check_voice(pages), attribution, facet_counts)))

    order = ordered_routes(pages)
    home = pages["/"]
    if "<!-- build:facets -->" in home["html"]:
        new_home = splice(home["html"], facets_html(pages, order), "<!-- build:facets -->", "<!-- /build:facets -->")
        if new_home != home["html"]:
            home["html"] = new_home
            refresh_main(home)

    cj, cmd, chtml = citations_outputs(pages, None)
    outputs.append((PUBLIC / "citations.json", cj))
    outputs.append((PUBLIC / "citations.md", splice((PUBLIC / "citations.md").read_text(), cmd)))
    cit_page = pages["/citations/"]
    new_cit_html = splice(cit_page["html"], chtml)
    if new_cit_html != cit_page["html"]:
        cit_page["html"] = new_cit_html
        refresh_main(cit_page)

    tagmap = load_tagmap()
    for route, entry in tagmap["pages"].items():
        if route not in pages:
            continue
        new_html = splice_tagmap(pages[route]["html"], tagmap_html(route, entry, pages, order))
        if new_html != pages[route]["html"]:
            pages[route]["html"] = new_html
            refresh_main(pages[route])

    disk_by_rel = {page["file"].relative_to(ROOT).as_posix(): disk[page["route"]] for page in pages.values()}
    trustworthy, hand_dates, dirty, cache = date_sources(disk_by_rel)
    today = local_today()
    dates, lastmod_problems = {}, []
    for page in pages.values():
        rel = page["file"].relative_to(ROOT).as_posix()

        def make(date, page=page):
            return facts.apply_jsonld(page["html"], facts_data, date, page["url"])

        date, html = choose_date(rel, make, trustworthy, hand_dates, dirty, cache, today)
        if date is None:
            lastmod_problems.append(f"no cached date for {rel} and git history is unavailable")
            continue
        dates[rel] = date
        page["html"] = html
        if html != disk[page["route"]]:
            outputs.append((page["file"], html))
    if len(dates) == len(pages):
        outputs.append((CONTENT / "lastmod.json", dump_dates(dates)))

    twins = {r: page_markdown(pages[r]) for r in order}
    for r in order:
        outputs.append((pages[r]["file"].with_name("index.md"), twins[r]))
    if len(dates) == len(pages):
        outputs.append((PUBLIC / "sitemap.xml", sitemap(pages, order, dates)))
    outputs.append((PUBLIC / "feed.xml", feed(pages)))
    podcast = podcast_rss()
    outputs.append((PUBLIC / "transmissions/beautiful-tornado/podcast.xml", podcast))
    short, full = llms(pages, order, twins, facts_data)
    outputs.append((PUBLIC / "llms.txt", short))
    outputs.append((PUBLIC / "llms-full.txt", full))
    outputs.append((PUBLIC / "pages.json", pages_json(pages, order, twins)))
    outputs.append((PUBLIC / "search-index.json", search_index_json(pages, order, twins)))

    self_problems = []
    if len(dates) == len(pages):
        for page in pages.values():
            rel = page["file"].relative_to(ROOT).as_posix()
            self_problems += facts.jsonld_problems(rel, facts.person_from_html(page["html"]), facts_data)
            mods = facts.modified_dates(page["html"])
            if not mods or any(item != dates[rel] for item in mods):
                self_problems.append(f"{rel} dateModified is {mods or 'missing'}, expected {dates[rel]}")
        block = facts.render_llms_block(facts_data)
        about_block = facts.render_about_inner(facts_data)
        self_problems += facts.published_block_problems("public/llms.txt", short, block)
        self_problems += facts.published_block_problems("public/llms-full.txt", full, block)
        self_problems += facts.missing_phrases(
            "public/llms.txt", short, (facts_data["lead"], facts_data["tagline"]))
        self_problems += facts.block_problems(
            "public/about/index.html key facts", facts.extract_block(pages["/about/"]["html"]), about_block)
        if facts_data["lead"] not in pages["/about/"]["html"]:
            self_problems.append("public/about/index.html is missing the locked lead")
        if facts_data["tagline"] not in pages["/about/"]["html"]:
            self_problems.append(f"public/about/index.html is missing {facts_data['tagline']!r}")

    disk_problems = []
    if mode == "check":
        expected_block = facts.render_llms_block(facts_data)
        expected_about = facts.render_about_inner(facts_data)
        for label, path, expected in (
            ("public/llms.txt", PUBLIC / "llms.txt", expected_block),
            ("public/llms-full.txt", PUBLIC / "llms-full.txt", expected_block),
        ):
            text = path.read_text() if path.exists() else ""
            disk_problems += facts.published_block_problems(label, text, expected)
            if path.name == "llms.txt":
                disk_problems += facts.missing_phrases(label, text, (facts_data["lead"], facts_data["tagline"]))
        about_disk_html = (PUBLIC / "about/index.html").read_text() if (PUBLIC / "about/index.html").exists() else ""
        disk_problems += facts.block_problems(
            "public/about/index.html key facts", facts.extract_block(about_disk_html), expected_about)
        if facts_data["lead"] not in disk["/about/"]:
            disk_problems.append("public/about/index.html is missing the locked lead")
        if facts_data["tagline"] not in disk["/about/"]:
            disk_problems.append(f"public/about/index.html is missing {facts_data['tagline']!r}")
        for route, html in disk.items():
            rel = pages[route]["file"].relative_to(ROOT).as_posix()
            disk_problems += facts.jsonld_problems(rel, facts.person_from_html(html), facts_data)
            if rel not in dates:
                continue
            mods = facts.modified_dates(html)
            if not mods or any(item != dates[rel] for item in mods):
                shown = mods[0] if len(mods) == 1 else (mods or "missing")
                disk_problems.append(f"{rel} dateModified is {shown}, expected {dates[rel]}")

    if mode != "check" and (self_problems or lastmod_problems):
        for x in self_problems:
            print(f"facts: {x}")
        for x in lastmod_problems:
            print(f"lastmod: {x}")
        sys.exit(1)

    stale = [p for p, t in outputs if not p.exists() or p.read_text() != t]
    problems = tagmap_problems(pages, tagmap) + archive_problems(pages) + check_links(pages) + redirects_problems() + band_problems + attr_problems + facet_problems + self_problems + disk_problems + lastmod_problems + headers_problems() + podcast_feed_problems(podcast)
    if mode == "check":
        for p in stale:
            print(f"stale: {p.relative_to(ROOT)}")
        factish = set(self_problems + disk_problems)
        dated = set(lastmod_problems)
        for x in problems:
            if x in factish:
                print(f"facts: {x}")
            elif x in dated:
                print(f"lastmod: {x}")
            else:
                print(f"problem: {x}")
        print(f"{len(pages)} pages, {len(stale)} stale files, {len(problems)} problems")
        sys.exit(1 if stale or problems else 0)
    for p, t in outputs:
        if p in stale:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(t)
    for x in problems:
        print(f"problem: {x}")
    print(f"{len(pages)} pages, wrote {len(stale)} files")
    if mode == "stage" and stale:
        subprocess.run(["git", "add", "--"] + [str(p) for p in stale], check=True, cwd=ROOT)
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    build("check" if "--check" in sys.argv else "stage" if "--stage" in sys.argv else "write")
