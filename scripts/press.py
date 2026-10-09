"""Press and citations list for /category/press/, built from the site's own pages.

Every <cite> in a page's <main> that names outside press is collected, merged when
the same piece is quoted on several pages, and listed newest first with the cite's
own wording, its link as the site publishes it, and the pages that quote it.
Nothing is typed in by hand: change a page's <cite> and the list follows.
"""

import html
import re
from urllib.parse import urlsplit

MARK_START = "<!-- build:press -->"
MARK_END = "<!-- /build:press -->"
ROUTE = "/category/press/"

# Links that are the site itself, Sarth's own studio and uploads, or reference pages, not press.
NOT_PRESS = ("sarth.net", "thirdwallstudio.com", "wikipedia.org", "youtube.com", "vimeo.com")
# A cite with no link counts only if it is dated and is not the site quoting itself.
SELF_WORDS = re.compile(r"\b(sarth|my|own)\b", re.I)

MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}


def text_of(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", fragment))).strip()


def inner_url(url):
    m = re.match(r"https?://web\.archive\.org/web/\d+[a-z_]*/(.*)", url)
    return m.group(1) if m else url


def key_of(url):
    parts = urlsplit(inner_url(url) if "://" in inner_url(url) else "http://" + inner_url(url))
    host = parts.netloc.lower().removeprefix("www.")
    slug = [s for s in parts.path.split("/") if s]
    return host + "/" + (slug[-1] if slug else "")


def date_of(text):
    """(year, month, day) for sorting, from the cite's own wording."""
    years = re.findall(r"\b(19\d\d|20\d\d)\b", text)
    if not years:
        return (0, 0, 0)
    year = int(years[0])
    m = re.search(r"\b(\d{1,2}) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* " + years[0], text)
    if m:
        return (year, MONTHS[m.group(2).lower()], int(m.group(1)))
    m = re.search(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2})?,?\s*" + years[0], text)
    if m:
        return (year, MONTHS[m.group(1).lower()], int(m.group(2) or 0))
    return (year, 0, 0)


def press_link(cite_html):
    for href in re.findall(r'href="([^"]+)"', cite_html):
        href = html.unescape(href)
        if not href.startswith(("http://", "https://")):
            continue
        target = inner_url(href)
        host = urlsplit(target if "://" in target else "http://" + target).netloc.lower()
        if not any(n in host for n in NOT_PRESS):
            return href
    return None


def collect(pages):
    entries = {}
    for route in sorted(pages):
        page = pages[route]
        if route == ROUTE:
            continue
        for cite in re.findall(r"<cite[^>]*>(.*?)</cite>", page["main_html"], re.S):
            text = text_of(cite)
            url = press_link(cite)
            if url is None:
                if re.search(r'href="', cite) or SELF_WORDS.search(text) or date_of(text) == (0, 0, 0):
                    continue
                key = "nolink:" + " ".join(sorted(set(re.findall(r"[A-Z][\w.]+|\d{4}", text))))
            else:
                key = key_of(url)
            e = entries.setdefault(key, {"variants": [], "routes": []})
            e["variants"].append((text, url))
            if route not in e["routes"]:
                e["routes"].append(route)
    # Unlinked cites that say the same thing in other words (outlet, writer, year) merge.
    nolink = [k for k in entries if k.startswith("nolink:")]
    for a in nolink:
        for b in nolink:
            if a != b and a in entries and b in entries and set(a[7:].split()) <= set(b[7:].split()):
                entries[b]["variants"] += entries[a]["variants"]
                entries[b]["routes"] += [r for r in entries[a]["routes"] if r not in entries[b]["routes"]]
                del entries[a]
    out = []
    for e in entries.values():
        # The fullest wording the site gives, and an original link over a Wayback one.
        text = max((v[0] for v in e["variants"]), key=lambda t: (date_of(t), len(t)))
        urls = [v[1] for v in e["variants"] if v[1]]
        url = next((u for u in urls if "web.archive.org" not in u), urls[0] if urls else None)
        dates = [date_of(v[0]) for v in e["variants"]]
        out.append({"text": text, "url": url, "date": max(dates), "routes": e["routes"]})
    out.sort(key=lambda e: (e["date"], e["text"]), reverse=True)
    return out


def render(pages, label):
    items = collect(pages)
    lis = []
    for e in items:
        t = html.escape(e["text"])
        head = f'<a href="{html.escape(e["url"], quote=True)}">{t}</a>' if e["url"] else t
        on = ", ".join(f'<a href="{r}">{html.escape(label(r))}</a>' for r in e["routes"])
        lis.append(f'      <li><p>{head}</p>\n      <p class="meta">Quoted on {on}.</p>\n      </li>')
    inner = (
        "    <h2>Press and citations</h2>\n"
        f"    <p>The press quoted on sarth.net today, newest first, {len(items)} pieces, each in the words of the page that quotes it, with the pages it appears on.</p>\n"
        '    <ul class="dates">\n' + "\n".join(lis) + "\n    </ul>\n    "
    )
    return inner, items
