#!/usr/bin/env python3
"""Derive every shadow of the site from the HTML pages.

The HTML under public/ is the source. This script reads every
public/**/index.html and writes:

  public/**/index.md          markdown twin of each page
  public/llms.txt             from content/llms.txt, {{PAGES}} filled in
  public/llms-full.txt        from content/llms-full.txt, every page inlined
  public/sitemap.xml
  public/feed.xml             every page that carries datePublished in its JSON-LD
  public/citations.json       outbound links per page
  public/citations.md         between the build:citations markers
  public/citations/index.html between the build:citations markers
  REPORT.md                   holes, flat pages, pages without a credit label, and
                              sentences that still name Sarth instead of saying I

It also fills each <div class="hole" data-hole="slug/name"> from
content/holes/slug--name.md, leaving the bracketed prompt when the file is empty.

  python3 scripts/build.py           write everything
  python3 scripts/build.py --check   write nothing; exit 1 if anything on disk is
                                     stale, an internal link is dead, or a page
                                     is missing from its index
  python3 scripts/build.py --stage   write, then git add what changed (pre-commit)

Stdlib only.
"""
import html
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

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
        elif c.tag == "img":
            alt = c.attrs.get("alt", "")
            out.append(f"![{alt}]({c.attrs.get('src', '')})")
        else:  # q, span, cite, sup, and anything else inline: transparent
            out.append(inline(c))
    return re.sub(r"[ \t]*\n[ \t]*", "\n", re.sub(r"[ \t]+", " ", "".join(out))).strip()


BLOCK = {"p", "h1", "h2", "h3", "h4", "ul", "ol", "dl", "blockquote", "pre", "figure", "table", "div", "section", "article", "main", "header", "footer", "nav", "hr", "iframe", "li", "dt", "dd", "figcaption", "aside"}


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
        if txt.startswith("[") and txt.endswith("]"):
            return []  # an unfilled hole stays off the twins and the agent files
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
        pages[route] = {
            "route": route, "file": f, "html": s, "title": title, "description": desc,
            "url": url, "published": published, "main_html": main_html, "main": parse(main_html),
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
    for top in ["/about/", "/work/", "/transmissions/", "/conspiracies/", "/conspirators/", "/sightings/", "/appearances/", "/devices/", "/citations/", "/contact/"]:
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
                body = f"<p>[{prompt}]</p>"
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


def holes_md(report, flat, credits=(), voice=()):
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
        out.append({"url": h, "text": inline(t) if t else re.sub(r"[*_`\[\]]", "", inline(a))})
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
def sitemap(pages, order):
    body = "\n".join(f"  <url><loc>{pages[r]['url']}</loc></url>" for r in order)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "\n</urlset>\n"


def feed(pages):
    dated = sorted((p for p in pages.values() if p["published"]), key=lambda p: (p["published"], p["url"]), reverse=True)
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


def llms(pages, order, twins):
    lines = []
    for r in order:
        p = pages[r]
        indent = "  " if r.count("/") > 3 else ""
        lines.append(f"{indent}- {p['title']} {p['url']}")
    short = (CONTENT / "llms.txt").read_text().replace("{{PAGES}}", "\n".join(lines))
    inl = []
    for r in order:
        body = twins[r].split("---\n", 2)[2].strip()
        inl.append(f"# {pages[r]['title']}\n\n{pages[r]['url']}\n\n{body}")
    full = (CONTENT / "llms-full.txt").read_text().replace("{{COUNT}}", str(len(order))).replace("{{PAGES}}", "\n\n---\n\n".join(inl))
    return short, full


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


def prose_paragraphs(main):
    """<p> elements, and unclassed <span>s such as index blurbs, that are sentences: not quotes, captions, labels, credits or data."""
    out = []
    def walk(n, blocked):
        for c in n.children:
            if isinstance(c, str):
                continue
            b = blocked or c.tag in ("blockquote", "figure", "figcaption", "cite", "dl", "table", "pre") or any(k in c.cls() for k in ("excerpt", "kicker", "breadcrumbs", "meta", "label", "hole", "credit"))
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


def check_links(pages):
    problems = []
    for p in pages.values():
        for h in hrefs(p["main"], internal_only=True) + [i.attrs.get("src", "") for i in p["main"].find_all("img") + p["main"].find_all("audio")]:
            h = h.split("#")[0].split("?")[0]
            if not h or not h.startswith("/"):
                continue
            target = PUBLIC / h.lstrip("/")
            ok = (target / "index.html").exists() if h.endswith("/") else target.exists()
            if not ok:
                problems.append(f"{p['route']} links to {h}, which does not exist")
    inbound = {r: 0 for r in pages}
    for p in pages.values():
        for h in set(re.findall(r'href="(/[^"#?]*)"', p["html"])):
            if h in inbound and h != p["route"]:
                inbound[h] += 1
    for r, n in inbound.items():
        if n == 0 and r != "/":
            problems.append(f"{r} is an orphan: no other page links to it")
    return problems


# ----------------------------------------------------------------- main
def build(mode):
    pages = load_pages()
    outputs = []  # (path, text)
    hole_changes, report = fill_holes(pages)
    outputs += hole_changes
    band_problems, flat = check_bands(pages)
    outputs.append((ROOT / "REPORT.md", holes_md(report, flat, check_credits(pages), check_voice(pages))))

    cj, cmd, chtml = citations_outputs(pages, None)
    outputs.append((PUBLIC / "citations.json", cj))
    outputs.append((PUBLIC / "citations.md", splice((PUBLIC / "citations.md").read_text(), cmd)))
    cit_page = pages["/citations/"]
    new_cit_html = splice(cit_page["html"], chtml)
    if new_cit_html != cit_page["html"]:
        cit_page["html"] = new_cit_html
        cit_page["main_html"] = re.search(r"<main.*?</main>", new_cit_html, re.S).group(0)
        cit_page["main"] = parse(cit_page["main_html"])
        outputs.append((cit_page["file"], new_cit_html))

    order = ordered_routes(pages)
    twins = {r: page_markdown(pages[r]) for r in order}
    for r in order:
        outputs.append((pages[r]["file"].with_name("index.md"), twins[r]))
    outputs.append((PUBLIC / "sitemap.xml", sitemap(pages, order)))
    outputs.append((PUBLIC / "feed.xml", feed(pages)))
    short, full = llms(pages, order, twins)
    outputs.append((PUBLIC / "llms.txt", short))
    outputs.append((PUBLIC / "llms-full.txt", full))

    stale = [p for p, t in outputs if not p.exists() or p.read_text() != t]
    problems = check_links(pages) + band_problems
    if mode == "check":
        for p in stale:
            print(f"stale: {p.relative_to(ROOT)}")
        for x in problems:
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
