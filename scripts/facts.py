"""Core identity facts. content/facts.json is the only record the build renders.

scripts/build.py fills the <!-- build:facts --> blocks in llms.txt, llms-full.txt,
and the About key facts, and the Person career fields in every page's JSON-LD.
This module is the check that those copies agree with the file, and that the
file still carries the roles the site is willing to state.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FACTS_PATH = ROOT / "content" / "facts.json"
TAGLINE = "Data Engineering for Art"

# Ids, names, and kinds are the contract. Dates live in facts.json and are
# checked by the prose below, which the renderer builds from those dates.
REQUIRED = (
    {"id": "third-wall", "org": "Third Wall Studio", "title": "Founder", "kind": "employment", "current": True},
    {"id": "burlap", "org": "Third Wall Studio", "product": "Burlap", "title": "Creator", "kind": "product", "current": True},
    {"id": "reaktor", "org": "Reaktor", "title": "Lead Data Architect", "kind": "employment", "current": False},
    {"id": "ingather", "org": "T.E.C. Systems", "product": "Ingather", "title": "Director of Product", "kind": "product", "current": False, "demo": "https://ingather-demo.marshy-runner.workers.dev"},
    {"id": "tec", "org": "T.E.C. Systems", "title": "UI Designer to Director of Product", "kind": "employment", "current": False},
)

# Phrases the rendered career block has to carry, on every surface. The dates
# inside them are produced from facts.json, so a wrong start or end fails here.
CAREER_PHRASES = (
    "Founder, May 2025",
    "Built since April 2025 by a team of four senior engineers",
    "Lead Data Architect, 2022 to March 2025",
    "Paramount’s Redshift-to-Snowflake migration",
    "A T.E.C. Systems product Sarth led, August 2021 to March 2022",
    "SvelteKit, a nine-person team",
    "https://ingather-demo.marshy-runner.workers.dev",
    "2004 to 2022",
    "Yankee Stadium",
    "Hudson Yards",
    "Museum of Modern Art",
    "American Museum of Natural History",
    "One World Trade Center",
    "One Bryant Park",
    "Memorial Sloan Kettering",
    "Joined as a UI designer",
    "Director of Product and Developer Manager by the end",
)

MONTHS = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
)
LD_RE = re.compile(r'<script type="application/ld\+json">\n(.*?)\n  </script>', re.S)
MARK_START = "<!-- build:facts -->"
MARK_END = "<!-- /build:facts -->"
STAMP_TYPES = {
    "WebPage", "AboutPage", "ContactPage", "CollectionPage", "ProfilePage",
    "ItemPage", "SearchResultsPage", "TechArticle", "Article", "NewsArticle",
    "BlogPosting",
}


def locked_lead():
    """LEAD.md states the lead as the two paragraphs under the title."""
    body = (ROOT / "LEAD.md").read_text().split("##", 1)[0]
    paras = []
    for para in body.split("\n\n"):
        para = " ".join(para.split())
        if para and not para.startswith("#"):
            paras.append(para)
    return " ".join(paras)


def identity_lead():
    """The same two lines, quoted under Locked lead in IDENTITY.md."""
    lines = []
    for line in (ROOT / "IDENTITY.md").read_text().splitlines():
        if line.startswith("> "):
            lines.append(line[2:].strip())
        elif lines:
            break
    return " ".join(lines)


def human_date(iso):
    parts = str(iso).split("-")
    if len(parts) == 1:
        return parts[0]
    month = MONTHS[int(parts[1]) - 1]
    if len(parts) == 2:
        return f"{month} {parts[0]}"
    return f"{month} {int(parts[2])}, {parts[0]}"


def human_span(role):
    start = human_date(role["start"])
    end = role.get("end")
    if not end:
        return start
    return f"{start} to {human_date(end)}"


def role_sentence(role):
    """One line. Every date in it comes from start/end, not from detail."""
    detail = (role.get("detail") or "").strip()
    if role["id"] == "third-wall":
        return f"{role['title']}, {human_date(role['start'])}."
    if role["id"] == "burlap":
        return f"{role['title']}. Built since {human_date(role['start'])} {detail}."
    if role["id"] == "ingather":
        return f"A {role['org']} product Sarth led, {human_span(role)}. {detail}"
    if role["id"] == "tec":
        return f"{human_span(role)}, {detail}"
    span = human_span(role)
    if detail:
        return f"{role['title']}, {span}, {detail}"
    return f"{role['title']}, {span}."


def role_description(role):
    """Plain sentence. The URL lives on the Role or the Organization, not here."""
    return role_sentence(role)


def role_label(role):
    return role.get("product") or role["org"]


def load_facts():
    """Return (facts, problems). problems is empty when the file may be rendered."""
    problems = []
    try:
        facts = json.loads(FACTS_PATH.read_text())
    except (OSError, json.JSONDecodeError) as e:
        return None, [f"content/facts.json cannot be read: {e}"]
    lead = locked_lead()
    if identity_lead() != lead:
        problems.append("IDENTITY.md locked lead does not match LEAD.md")
    if facts.get("lead") != lead:
        problems.append("content/facts.json lead does not match the locked lead in LEAD.md")
    if facts.get("tagline") != TAGLINE:
        problems.append(f"content/facts.json tagline must be {TAGLINE!r}")
    roles = facts.get("roles")
    if not isinstance(roles, list):
        return facts, problems + ["content/facts.json has no roles list"]
    by_id = {}
    for role in roles:
        if not isinstance(role, dict) or "id" not in role:
            problems.append("content/facts.json has a role without an id")
            continue
        if role["id"] in by_id:
            problems.append(f"content/facts.json repeats role {role['id']}")
        by_id[role["id"]] = role
        for key in ("url", "demo"):
            url = role.get(key) or ""
            if "github.com" in url and "ingather" in url.lower():
                problems.append("content/facts.json links the Ingather repo; the public demo is the only Ingather URL")
    ids = [r.get("id") for r in roles if isinstance(r, dict)]
    if tuple(ids) != tuple(r["id"] for r in REQUIRED):
        problems.append(
            "content/facts.json roles must be "
            + ", ".join(r["id"] for r in REQUIRED)
            + ", newest first"
        )
    for spec in REQUIRED:
        role = by_id.get(spec["id"])
        if role is None:
            problems.append(f"content/facts.json is missing required role {spec['id']} ({spec['org']}, {spec['title']})")
            continue
        for key in ("org", "title", "kind", "current"):
            if role.get(key) != spec[key]:
                problems.append(
                    f"content/facts.json role {spec['id']} {key} is {role.get(key)!r}, required {spec[key]!r}"
                )
        if spec.get("product") and role.get("product") != spec["product"]:
            problems.append(
                f"content/facts.json role {spec['id']} product is {role.get('product')!r}, required {spec['product']!r}"
            )
        if spec.get("demo") and role.get("demo") != spec["demo"]:
            problems.append(
                f"content/facts.json role {spec['id']} demo is {role.get('demo')!r}, required {spec['demo']!r}"
            )
        if not _date_ok(role.get("start")):
            problems.append(f"content/facts.json role {spec['id']} needs a start date")
        if role.get("current"):
            if role.get("end"):
                problems.append(f"content/facts.json role {spec['id']} is current and must not have an end")
        elif not _date_ok(role.get("end")):
            problems.append(f"content/facts.json role {spec['id']} needs an end date")
    if not problems:
        block = render_llms_block(facts)
        problems += missing_phrases("content/facts.json renders a career block that", block, (facts["lead"], facts["tagline"], *CAREER_PHRASES))
    return facts, problems


def render_llms_block(facts):
    lines = [facts["lead"], "", facts["tagline"], "", "Career, newest first:", ""]
    for role in facts["roles"]:
        link = role.get("demo") or role.get("url") or ""
        suffix = f" {link}" if link else ""
        lines.append(f"- {role_label(role)} — {role_sentence(role)}{suffix}")
    return "\n".join(lines) + "\n"


def _host(url):
    return re.sub(r"^https?://", "", url).strip("/")


def _anchor(href, text):
    return f'<a href="{html.escape(href, quote=True)}">{html.escape(text)}</a>'


def render_about_inner(facts):
    """Definition rows for the About key facts. The markers stay put around them."""
    rows = []
    for role in facts["roles"]:
        body = html.escape(role_sentence(role))
        links = []
        if role.get("demo"):
            links.append(_anchor(role["demo"], "demo"))
        elif role.get("url"):
            links.append(_anchor(role["url"], _host(role["url"])))
        if role["id"] == "ingather":
            links.append(_anchor("/conspiracies/ingather/", "Ingather"))
        if links:
            body += " " + " &middot; ".join(links)
        rows.append(f"      <dt>{html.escape(role_label(role))}</dt>\n      <dd>{body}</dd>")
    return "\n".join(rows) + "\n"


def _org_node(role):
    org = {"@type": "Organization", "name": role["org"]}
    if role.get("orgId"):
        org["@id"] = role["orgId"]
    if role.get("url"):
        org["url"] = role["url"]
    return org


def _employment_node(role, prop):
    node = {
        "@type": "OrganizationRole",
        "roleName": role["title"],
        "startDate": role["start"],
    }
    if role.get("end"):
        node["endDate"] = role["end"]
    node[prop] = _org_node(role)
    node["description"] = role_description(role)
    return node


def _occupation_node(role):
    shown = f"{role['title']}, {role.get('product') or role['org']}"
    node = {
        "@type": "Role",
        "roleName": shown,
        "startDate": role["start"],
    }
    if role.get("end"):
        node["endDate"] = role["end"]
    node["hasOccupation"] = {"@type": "Occupation", "name": role["title"]}
    node["description"] = role_description(role)
    link = role.get("demo") or role.get("url")
    if link:
        node["url"] = link
    return node


def career_fields(facts):
    current = [r for r in facts["roles"] if r["kind"] == "employment" and r["current"]]
    past = [r for r in facts["roles"] if r["kind"] == "employment" and not r["current"]]
    return {
        "worksFor": [_employment_node(r, "worksFor") for r in current],
        "alumniOf": [_employment_node(r, "alumniOf") for r in past],
        "hasOccupation": [_occupation_node(r) for r in facts["roles"]],
    }


def apply_person(person, facts):
    """Career fields and the tagline, leaving the rest of the Person node alone."""
    knows = [x for x in (person.get("knowsAbout") or []) if x != facts["tagline"]]
    knows.append(facts["tagline"])
    career = career_fields(facts)
    out = {}
    inserted = False
    for key, value in person.items():
        if key in ("worksFor", "alumniOf", "hasOccupation", "knowsAbout"):
            continue
        if key == "sameAs" and not inserted:
            out.update(career)
            out["knowsAbout"] = knows
            inserted = True
        out[key] = value
    if not inserted:
        out.update(career)
        out["knowsAbout"] = knows
    return out


def stamp_modified(node, date, page_url=None):
    """Page and article nodes, and anything that already publishes a date.

    page_url is accepted so callers can pass the canonical URL. It is not used
    to stamp WebSite or SoftwareApplication nodes that share that URL.
    """
    del page_url
    types = node.get("@type")
    types = set(types if isinstance(types, list) else [types])
    if types & {"Person", "Organization", "MusicGroup", "FAQPage", "WebSite", "SoftwareApplication"}:
        node.pop("dateModified", None)
        return
    if "datePublished" in node or "dateModified" in node or types & STAMP_TYPES:
        node["dateModified"] = date


def _date_ok(value):
    if not re.fullmatch(r"\d{4}(-\d{2}){0,2}", str(value or "")):
        return False
    parts = str(value).split("-")
    if len(parts) >= 2 and not 1 <= int(parts[1]) <= 12:
        return False
    if len(parts) == 3 and not 1 <= int(parts[2]) <= 31:
        return False
    return True


def apply_jsonld(page_html, facts, date, page_url=None):
    match = LD_RE.search(page_html)
    if not match:
        return page_html
    data = json.loads(match.group(1))
    for node in data.get("@graph", []):
        if node.get("@type") == "Person" and str(node.get("@id", "")).endswith("#person"):
            fresh = apply_person(node, facts)
            node.clear()
            node.update(fresh)
        stamp_modified(node, date, page_url)
    rendered = json.dumps(data, indent=2, ensure_ascii=False)
    return page_html[:match.start(1)] + rendered + page_html[match.end(1):]


def extract_block(text):
    if MARK_START not in text or MARK_END not in text:
        return None
    return text.split(MARK_START, 1)[1].split(MARK_END, 1)[0]


def person_from_html(page_html):
    match = LD_RE.search(page_html)
    if not match:
        return None
    try:
        graph = json.loads(match.group(1)).get("@graph", [])
    except json.JSONDecodeError:
        return None
    for node in graph:
        if node.get("@type") == "Person" and str(node.get("@id", "")).endswith("#person"):
            return node
    return None


def modified_dates(page_html):
    match = LD_RE.search(page_html)
    if not match:
        return []
    try:
        graph = json.loads(match.group(1)).get("@graph", [])
    except json.JSONDecodeError:
        return []
    out = []
    for node in graph:
        if "dateModified" in node:
            out.append(node["dateModified"])
    return out


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _org_name(node):
    for key in ("worksFor", "alumniOf"):
        value = node.get(key)
        if isinstance(value, dict) and value.get("name"):
            return value["name"]
    return ""


def _role_nodes(person):
    nodes = []
    for key in ("worksFor", "alumniOf", "hasOccupation"):
        for item in _as_list(person.get(key)):
            if isinstance(item, dict):
                nodes.append((key, item))
    return nodes


def _matches(node, role):
    if node.get("startDate") != role["start"]:
        return False
    if (node.get("endDate") or None) != (role.get("end") or None):
        return False
    title = node.get("roleName") or ""
    desc = node.get("description") or ""
    org = _org_name(node)
    if role["title"] not in title and role["title"] not in desc:
        return False
    label = role.get("product") or role["org"]
    named = label == org or label in desc or label in title or role["org"] == org or role["org"] in desc
    return named


def jsonld_problems(path, person, facts):
    """Career fields on one Person, against facts.json. Empty if they agree."""
    if person is None:
        return [f"{path} JSON-LD has no Person"]
    problems = []
    nodes = _role_nodes(person)
    for role in facts["roles"]:
        if not any(_matches(node, role) for _, node in nodes):
            problems.append(
                f"{path} JSON-LD is missing {role_label(role)} "
                f"({role['title']}, {role['start']}"
                + (f" to {role['end']}" if role.get("end") else "")
                + ")"
            )
    for key, node in nodes:
        if any(_matches(node, role) for role in facts["roles"]):
            continue
        label = _org_name(node) or node.get("roleName") or key
        end = node.get("endDate") or "present"
        problems.append(
            f"{path} JSON-LD {label} {node.get('roleName')} {node.get('startDate')} to {end} "
            "disagrees with content/facts.json"
        )
    by_key = {"worksFor": [], "alumniOf": [], "hasOccupation": []}
    for key, node in nodes:
        by_key[key].append(node)
    for role in facts["roles"]:
        if role["kind"] == "employment" and role["current"]:
            if not any(_matches(node, role) for node in by_key["worksFor"]):
                problems.append(f"{path} JSON-LD worksFor is missing current role {role['org']}")
        if role["kind"] == "employment" and not role["current"]:
            if not any(_matches(node, role) for node in by_key["alumniOf"]):
                problems.append(f"{path} JSON-LD alumniOf is missing {role['org']}")
            if any(_matches(node, role) for node in by_key["worksFor"]):
                problems.append(f"{path} JSON-LD lists past role {role['org']} under worksFor")
        if role["kind"] != "employment" and any(_matches(node, role) for node in by_key["worksFor"]):
            problems.append(f"{path} JSON-LD lists {role_label(role)} under worksFor")
    knows = person.get("knowsAbout") or []
    if facts["tagline"] not in knows:
        problems.append(f"{path} JSON-LD knowsAbout is missing {facts['tagline']!r}")
    blob = json.dumps(person, ensure_ascii=False)
    problems += missing_phrases(f"{path} JSON-LD", blob, CAREER_PHRASES)
    return problems


def missing_phrases(label, text, phrases):
    missing = [phrase for phrase in phrases if phrase not in text]
    return [f"{label} is missing {phrase!r}" for phrase in missing]


def block_problems(label, actual, expected):
    if actual is None:
        return [f"{label} is missing {MARK_START} markers"]
    if actual.strip() == expected.strip():
        return []
    missing = [phrase for phrase in CAREER_PHRASES if phrase not in actual]
    if missing:
        return [f"{label} is missing {phrase!r}" for phrase in missing]
    return [f"{label} does not match content/facts.json"]


def published_block_problems(label, text, expected):
    """The public llms files carry the career block without the source markers."""
    if MARK_START in text or MARK_END in text:
        return [f"{label} still contains {MARK_START} markers"]
    if expected.strip() not in text:
        missing = [phrase for phrase in CAREER_PHRASES if phrase not in text]
        if missing:
            return [f"{label} is missing {phrase!r}" for phrase in missing]
        return [f"{label} does not match content/facts.json"]
    return []
