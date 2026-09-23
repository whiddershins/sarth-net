#!/usr/bin/env python3
"""One-shot HTML projector. Source of truth is the written public/*.html after this runs."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("/Users/burlapcalhoun/git_repos/sarth_net/public")
HOST = "https://www.sarth.net"
OG = f"{HOST}/images/og.jpg"
PERSON = {
    "@type": "Person",
    "@id": f"{HOST}/#person",
    "name": "Sarth Calhoun",
    "url": f"{HOST}/",
    "jobTitle": "Founder of Third Wall Studio",
    "homeLocation": {"@type": "Place", "name": "Brooklyn"},
    "sameAs": [
        "https://www.wikidata.org/wiki/Q7424654",
        "https://x.com/noisegroove",
        "https://github.com/whiddershins",
        "https://sarth.net",
    ],
}

NAV = [
    ("/", "Sarth", "home"),
    ("/conspiracies/", "Conspiracies", "conspiracies"),
    ("/conspirators/", "Conspirators", "conspirators"),
    ("/sightings/", "Sightings", "sightings"),
    ("/appearances/", "Appearances", "appearances"),
    ("/devices/", "Devices", "devices"),
    ("/transmissions/", "Transmissions", "transmissions"),
    ("/contact/", "Contact", "contact"),
]


def ld(graph):
    payload = {"@context": "https://schema.org", "@graph": graph}
    return json.dumps(payload, indent=2, ensure_ascii=False)


def chrome(current):
    links = []
    for href, label, key in NAV:
        cur = ' aria-current="page"' if key == current else ""
        links.append(f'      <a href="{href}"{cur}>{label}</a>')
    return "\n".join(links)


def page(
    *,
    path,
    title,
    description,
    canonical,
    current,
    body,
    graph_html,
    jsonld,
    og_type="website",
    extra_head="",
):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical}">
  <link rel="author" href="{HOST}/">
  <link rel="icon" type="image/png" href="/favicon.png">
  <meta name="robots" content="index,follow">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="Sarth Calhoun">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{OG}">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@noisegroove">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{OG}">
{extra_head}  <script type="application/ld+json">
{jsonld}
  </script>
  <link rel="stylesheet" href="/site.css">
</head>
<body>
  <header class="top">
    <a class="mark" href="/">Sarth</a>
    <nav>
{chrome(current)}
    </nav>
  </header>
{body}
  <aside class="graph" aria-label="Context">
    <h2>Context</h2>
{graph_html}
  </aside>
  <footer>
    <p>
      <a href="https://x.com/noisegroove">@noisegroove</a>
      · <a href="https://github.com/whiddershins">GitHub</a>
      · <a href="https://www.wikidata.org/wiki/Q7424654">Wikidata</a>
      · <a href="mailto:whiddershins@gmail.com">email</a>
    </p>
    <p>
      <a href="https://bookofsarth.com">Book of Sarth</a>
      · <a href="https://contraptions.bookofsarth.com">Contraptions</a>
      · <a href="https://burlap.app">Burlap</a>
      · <a href="https://thirdwallstudio.com">Third Wall Studio</a>
    </p>
    <p class="host">All rights reserved</p>
  </footer>
</body>
</html>
"""
    dest = ROOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)
    print("wrote", dest)


# --- home ---
home_body = r'''
  <section class="hero" aria-label="Sarth Calhoun at the Continuum">
    <img src="/images/continuum.jpg" width="1000" height="664" alt="Sarth Calhoun playing a Haken Continuum Fingerboard.">
  </section>
  <main>
    <section>
      <p class="kicker">Machine · Dream · Message</p>
      <h1>Sarth Calhoun</h1>
      <p class="lede">Founder of <a href="https://thirdwallstudio.com">Third Wall Studio</a>, builder of the <a href="https://burlap.app">Burlap</a> app.</p>
      <p class="links">
        <a href="https://thirdwallstudio.com">Third Wall Studio</a>
        <a href="https://burlap.app/download">Download Burlap</a>
        <a href="https://x.com/noisegroove">@noisegroove</a>
      </p>
    </section>

    <section class="now">
      <p class="kicker">Now</p>
      <h2>Current work</h2>

      <article id="third-wall">
        <h3><a href="https://thirdwallstudio.com">Third Wall Studio</a></h3>
        <p>Third Wall Studio makes animation with filmmakers and artists. We mix live action, animation, and generative AI in the same production—not as a gimmick, but as part of the craft. New tools for ancient magic.</p>
        <p>Writers, animators, directors, and visual artists bring their own worlds. <a href="https://burlap.app">Burlap</a> is the canvas underneath it all.</p>
        <p>Recent work includes Savas’s <em>Kubler-Ross Model</em>; Doron Lev’s <em>Watching Shadows</em>, <em>Pigeon Problems</em>, and <em>Truck Stop Love</em>; Jacob McCoy’s <em>Meatsuitz</em>; and Jonathan Arons’s <em>The Trinary Matrix</em>. Doron Lev, Tetiana Khodakivska, and Jonathan Arons have also joined us as artists in residence. See the films, meet the artists, or bring us something strange.</p>
        <p class="meta"><a href="https://thirdwallstudio.com">thirdwallstudio.com</a> · <a href="mailto:studio@thirdwallstudio.com">studio@thirdwallstudio.com</a></p>
      </article>

      <article id="burlap">
        <h3><a href="https://burlap.app">Burlap</a></h3>
        <p>Burlap is an infinite canvas for making images and motion on the Mac. I built it at Third Wall Studio because the usual AI tools felt like a row of tiny boxes. The work needed room to spread out.</p>
        <p>Sketch, import, or grab anything already on the canvas, then use it to steer the next generation. Keep a character consistent. Chase a style. Run several ideas at once through Runway, OpenAI—including Sora—and other providers, without losing the thread while the models work.</p>
        <p>It’s made for animation, storyboards, illustration, and design. The references, generations, and assets all live together, so the canvas becomes the workflow. It’s also how we make films at Third Wall Studio.</p>
        <figure class="shot">
          <a href="https://burlap.app/download"><img src="/images/burlap.jpg" width="1400" height="1050" alt="Burlap, infinite canvas for visual reference prompting."></a>
          <figcaption>Burlap. Download at burlap.app.</figcaption>
        </figure>
        <p class="links">
          <a href="https://burlap.app/download">Download for Mac</a>
          <a href="https://burlap.app">burlap.app</a>
          <a href="/transmissions/visual-reference-prompting/">Visual Reference Prompting</a>
        </p>
      </article>

      <article id="through-the-brambles">
        <h3><a href="https://www.thirdwallstudio.com/through-the-brambles">Through the Brambles</a></h3>
        <p>A VR story built entirely inside Burlap. Every scene began as a prompted 360° image, then became part of a single journey for headset playback. Gemini made the stills, Veo brought them to life, ElevenLabs handled narration, and Resolve held the edit and ambisonic mix.</p>
        <p class="meta"><a href="https://www.thirdwallstudio.com/through-the-brambles">thirdwallstudio.com/through-the-brambles</a></p>
      </article>

      <article id="contraptions">
        <h3><a href="https://contraptions.bookofsarth.com">Contraptions</a></h3>
        <p>Small tools made to solve very particular problems. <a href="https://contraptions.bookofsarth.com/image-compare-workbench">Image Compare Workbench</a> makes it fast to compare a folder full of generations: lock one image, then walk the other. Soundscape One turns a 2D field into an instrument. Burlap is the main machine; these are the odd little ones beside it.</p>
        <p class="meta"><a href="https://contraptions.bookofsarth.com">contraptions.bookofsarth.com</a></p>
      </article>

      <article id="transmission">
        <h3><a href="/transmissions/visual-reference-prompting/">Visual Reference Prompting</a></h3>
        <p>Use an image for where it can take you, not only for what it shows. A character can hold the subject together; a painting can pull the style somewhere new. The essay names the practice and <a href="https://www.youtube.com/watch?v=wroKqbXfx5g">Frogs and Goblins</a> shows it in motion.</p>
      </article>
    </section>

    <div class="photos">
      <figure class="wide">
        <img src="/images/sarth-1.jpg" width="1000" height="750" alt="Sarth Calhoun.">
      </figure>
      <figure>
        <img src="/images/sarth-7.jpg" width="1000" height="667" alt="Sarth Calhoun.">
      </figure>
      <figure>
        <img src="/images/lolla.jpg" width="750" height="337" alt="Sarth Calhoun, Lollapalooza.">
      </figure>
    </div>

    <section>
      <p class="kicker">Lineage</p>
      <h2>Also</h2>
      <p>Before the studio and Burlap: Number19 with Leah Coloff, Tony Diodore, and Marcus Righter; Lucibel Crater with Coloff and Paul Chuffo; and <a href="https://bookofsarth.com">Book of Sarth</a>, the first gralbum. With Lou Reed and Ulrich Krieger, I made <a href="/conspiracies/metal-machine-trio/">Metal Machine Trio</a> and recorded <em>The Creation of the Universe</em> over two nights at REDCAT. Lou and I later wrote the original <a href="/conspiracies/lulu/"><em>Lulu</em> score</a> for Robert Wilson’s Berliner Ensemble production; the Metallica album grew from those recordings. <a href="/conspiracies/junior-dad/">Junior Dad</a> began in Lou’s apartment, with <a href="/conspirators/rob-wasserman/">Rob Wasserman</a>’s electric upright running through Kyma. I still use Kyma and the Haken Continuum.</p>
      <p class="links">
        <a href="/appearances/">Appearances</a>
        <a href="/sightings/">Sightings</a>
        <a href="/devices/">Devices</a>
        <a href="https://bookofsarth.com">Book of Sarth</a>
        <a href="https://open.spotify.com/artist/6uUtOazhiVXfNU8KAglFv9">Spotify</a>
      </p>
    </section>
  </main>
'''

home_graph = """    <dl>
      <dt>About</dt>
      <dd>Sarth Calhoun · Brooklyn, New York</dd>
      <dt>Current work</dt>
      <dd><a href="https://thirdwallstudio.com">Third Wall Studio</a> · <a href="https://burlap.app">Burlap</a> · <a href="https://www.thirdwallstudio.com/through-the-brambles">Through the Brambles</a> · <a href="https://contraptions.bookofsarth.com">Contraptions</a> · <a href="https://bookofsarth.com">Book of Sarth</a></dd>
      <dt>Conspirators</dt>
      <dd>Third Wall Studio: Savas · Jacob McCoy · Doron Lev · Tetiana Khodakivska · Jonathan Arons. Lineage: Lou Reed · Ulrich Krieger · Leah Coloff · Paul Chuffo · Rob Wasserman · Robert Wilson</dd>
      <dt>Tools</dt>
      <dd>Burlap · <a href="/devices/">Kyma</a> · <a href="/devices/">Haken Continuum</a></dd>
      <dt>source</dt>
      <dd><a href="https://github.com/whiddershins">github.com/whiddershins</a></dd>
    </dl>"""

page(
    path="index.html",
    title="Sarth Calhoun",
    description="Sarth Calhoun. Founder of Third Wall Studio, builder of the Burlap app.",
    canonical=f"{HOST}/",
    current="home",
    body=home_body,
    graph_html=home_graph,
    jsonld=ld(
        [
            PERSON,
            {
                "@type": "WebSite",
                "@id": f"{HOST}/#website",
                "name": "Sarth Calhoun",
                "url": f"{HOST}/",
                "description": "Citable identity for Sarth Calhoun. Third Wall Studio, Burlap, Visual Reference Prompting.",
                "author": {"@id": f"{HOST}/#person"},
                "publisher": {"@id": f"{HOST}/#person"},
            },
            {
                "@type": "WebPage",
                "@id": f"{HOST}/#webpage",
                "url": f"{HOST}/",
                "name": "Sarth Calhoun",
                "isPartOf": {"@id": f"{HOST}/#website"},
                "about": {"@id": f"{HOST}/#person"},
                "primaryImageOfPage": OG,
            },
        ]
    ),
)


# --- conspiracies and conspirators ---
def context_list(items):
    return " · ".join(f'<a href="{url}">{name}</a>' for name, url in items)


def story_page(record):
    canonical = f"{HOST}{record['path']}"
    kind = record["kind"]
    current = "conspirators" if kind == "Conspirator" else "conspiracies"
    body = f'''\n  <main class="page story">\n    <p class="breadcrumbs"><a href="/{current}/">{current.title()}</a> / {record['name']}</p>\n    <p class="kicker">{kind}</p>\n    <h1>{record['display']}</h1>\n    <p class="lede">{record['dek']}</p>\n{record['body']}\n  </main>\n'''
    graph = f'''    <dl>
      <dt>On this site</dt>
      <dd><a href="/">Sarth Calhoun</a> · <a href="/{current}/">{current.title()}</a></dd>
      <dt>Related work</dt>
      <dd>{context_list(record['related'])}</dd>
      <dt>{'People in this story' if kind == 'Conspirator' else 'Conspirators'}</dt>
      <dd>{context_list(record['people'])}</dd>
      <dt>Tools</dt>
      <dd>{context_list(record.get('tools', [])) if record.get('tools') else '—'}</dd>
    </dl>'''
    schema_type = record["schema"]
    entity = {
        "@type": schema_type,
        "@id": f"{canonical}#entity",
        "name": record["name"],
        "url": canonical,
        "description": record["description"],
    }
    if kind == "Conspirator":
        entity["knows"] = {"@id": f"{HOST}/#person"}
    else:
        entity["creator"] = {"@id": f"{HOST}/#person"}
    page(
        path=f"{record['path'].strip('/')}/index.html",
        title=f"{record['name']} — Sarth Calhoun",
        description=record["description"],
        canonical=canonical,
        current=current,
        body=body,
        graph_html=graph,
        jsonld=ld([
            PERSON,
            entity,
            {
                "@type": "ProfilePage" if kind == "Conspirator" else "WebPage",
                "@id": f"{canonical}#page",
                "name": record["name"],
                "url": canonical,
                "about": {"@id": f"{canonical}#entity"},
                "isPartOf": {"@id": f"{HOST}/#website"},
                "author": {"@id": f"{HOST}/#person"},
            },
        ]),
        og_type="profile" if kind == "Conspirator" else "article",
    )


conspiracies_intro = r'''
  <main class="page directory">
    <p class="kicker">Projects</p>
    <h1>Conspiracies</h1>
    <p class="lede">Bands, tours, records, theater pieces, films, and machines. The point is not a list of credits. Each page is about how the thing came together and what happened once it did.</p>
    <ol class="story-list">
      <li><a href="/conspiracies/lou-reed-song-band/"><strong>Lou Reed’s song band</strong><span>Lou wanted fresh sounds. Sarth became the place he went for them.</span></a></li>
      <li><a href="/conspiracies/lou-reed-spring-2008-tour/"><strong>Lou Reed spring 2008 U.S. tour</strong><span>Northampton, a bus south, Beale Street, and the beginning of the band.</span></a></li>
      <li><a href="/conspiracies/metal-machine-trio/"><strong>Metal Machine Trio</strong><span>Three people walked into REDCAT without a band name and came out with one.</span></a></li>
      <li><a href="/conspiracies/lulu/"><strong><em>Lulu</em></strong><span>Interstitial music at Lou’s house became a theater score, then something else again with Metallica.</span></a></li>
      <li><a href="/conspiracies/junior-dad/"><strong>“Junior Dad”</strong><span>A bowed electric upright, Kyma, and a first session that refused to stay small.</span></a></li>
    </ol>
  </main>
'''

page(
    path="conspiracies/index.html",
    title="Conspiracies — Sarth Calhoun",
    description="Projects made by Sarth Calhoun with other people: Lou Reed's song band, Metal Machine Trio, Lulu, Junior Dad, and more.",
    canonical=f"{HOST}/conspiracies/",
    current="conspiracies",
    body=conspiracies_intro,
    graph_html='''    <dl><dt>On this site</dt><dd><a href="/">Sarth Calhoun</a> · <a href="/conspirators/">Conspirators</a></dd><dt>What belongs here</dt><dd>Bands · tours · records · performances · theater · films · tools</dd></dl>''',
    jsonld=ld([PERSON, {"@type": "CollectionPage", "name": "Conspiracies", "url": f"{HOST}/conspiracies/", "about": {"@id": f"{HOST}/#person"}}]),
)

conspirators_intro = r'''
  <main class="page directory">
    <p class="kicker">People</p>
    <h1>Conspirators</h1>
    <p class="lede">People I have made things with. These are not miniature résumés. They are notes about the relationship, the work, and the part you cannot get from a credit line.</p>
    <ol class="story-list">
      <li><a href="/conspirators/lou-reed/"><strong>Lou Reed</strong><span>Tai Chi, meditation music, rock shows, deep noise, and the search for a sound that did not exist yet.</span></a></li>
      <li><a href="/conspirators/rob-wasserman/"><strong>Rob Wasserman</strong><span>A hero who treated the new guy as though he already belonged.</span></a></li>
    </ol>
  </main>
'''

page(
    path="conspirators/index.html",
    title="Conspirators — Sarth Calhoun",
    description="People Sarth Calhoun has made, performed, recorded, toured, designed, or built work with.",
    canonical=f"{HOST}/conspirators/",
    current="conspirators",
    body=conspirators_intro,
    graph_html='''    <dl><dt>On this site</dt><dd><a href="/">Sarth Calhoun</a> · <a href="/conspiracies/">Conspiracies</a></dd><dt>What belongs here</dt><dd>People with whom Sarth made the work—not everyone who shared a bill.</dd></dl>''',
    jsonld=ld([PERSON, {"@type": "CollectionPage", "name": "Conspirators", "url": f"{HOST}/conspirators/", "about": {"@id": f"{HOST}/#person"}}]),
)

STORIES = [
    {
        "name": "Rob Wasserman",
        "display": "Rob Wasserman",
        "path": "/conspirators/rob-wasserman/",
        "kind": "Conspirator",
        "schema": "Person",
        "description": "Sarth Calhoun on meeting bassist Rob Wasserman, touring together with Lou Reed, and the first Kyma session that became the basis of Junior Dad.",
        "dek": "I met one of my bass heroes backstage. Not long afterward, he made sure the new guy in Lou’s band felt like he belonged there.",
        "body": r'''
    <section>
      <h2>“A huge fan”</h2>
      <p>I first met Rob backstage at Lou Reed’s <em>Berlin</em> at St. Ann’s Warehouse. I walked up, shook his hand, and said, “Rob Wasserman! I’m a huge fan.” He just chuckled: “A huge fan…”</p>
      <p>Bass was my first instrument. Rob’s <em>Solo</em>, <em>Duets</em>, and <em>Trios</em> records had changed what the upright bass could be for me. I also knew his electric upright—the instrument Ned Steinberger helped create with him. Before we played a note together, Rob was already part of how I heard.</p>
    </section>
    <section>
      <h2>The first sound</h2>
      <p>The first time we played together was at Lou’s apartment. Lou had asked me to demonstrate what live processing could do onstage. The source material turned out to be Rob bowing his electric upright while I processed it through Kyma.</p>
      <p>We recorded the session. That sound became the basis of “Junior Dad,” the long closing piece on <em>Lulu</em>. It is a funny origin for something so enormous: three people in an apartment, testing a stage idea.</p>
    </section>
    <section>
      <h2>The part I kept</h2>
      <p>Rob had every reason to be skeptical of the younger person arriving with unfamiliar machinery. Instead, he was unfailingly gracious. He spoke to me with dignity and respect—like I belonged beside him—at a moment when I was not yet sure that I did.</p>
      <p>That generosity is what I remember most. The playing was heroic. The welcome mattered just as much.</p>
      <p class="source-note">Sarth first wrote this remembrance after Rob’s death in 2016. The backstage meeting was during <em>Berlin</em> at St. Ann’s Warehouse, 14–17 December 2006. Their first documented tour together was Lou Reed’s spring 2008 U.S. tour.</p>
    </section>''',
        "related": [("“Junior Dad”", "/conspiracies/junior-dad/"), ("Lou Reed’s song band", "/conspiracies/lou-reed-song-band/"), ("Spring 2008 tour", "/conspiracies/lou-reed-spring-2008-tour/"), ("Lulu", "/conspiracies/lulu/")],
        "people": [("Lou Reed", "/conspirators/lou-reed/")],
        "tools": [("Kyma", "/devices/")],
    },
    {
        "name": "Lou Reed",
        "display": "Lou Reed",
        "path": "/conspirators/lou-reed/",
        "kind": "Conspirator",
        "schema": "Person",
        "description": "Sarth Calhoun on working with Lou Reed: Tai Chi and meditation music, the touring band, Metal Machine Trio, Lulu, and the sounds Lou asked him to invent.",
        "dek": "We started with Tai Chi and meditation music. From there came rock tours, deep noise, theater, and years of Lou asking for sounds that did not have names yet.",
        "body": r'''
    <section>
      <h2>Before the noise</h2>
      <p>Lou and I met through a shared love of Tai Chi. The first sustained music we made together was meditation music—drones and melody, improvised, revised, edited, remixed, and transformed over several years. That quiet work is the root of everything that followed.</p>
      <p>It meant that when the projects became loud, the listening underneath them was already there. The touring band, Metal Machine Trio, and <em>Lulu</em> look like separate chapters from the outside. To me, the line between them is much less tidy.</p>
    </section>
    <section>
      <h2>Lou’s imagination</h2>
      <p>Lou made the decisions about his bands. He invited me because he wanted fresh sounds and wanted the music to feel modern. My job was not a normal instrumental chair. When he wanted something wild—or just something outside the vocabulary the band already had—I was there to find it.</p>
      <p>Tony Diodore later called me “Lou’s imagination.” That feels accurate. Lou could ask for a result before either of us knew what machine, gesture, or accident would produce it.</p>
    </section>
    <section>
      <h2>Follow the work</h2>
      <p>In 2008 Lou called about an improvised noise concert at REDCAT with Ulrich Krieger. Those nights became Metal Machine Trio. Later he called me to his house to make interstitial music for Robert Wilson’s <em>Lulu</em>. That became a score, songs, rehearsals in Berlin, and then a record with Metallica.</p>
      <p>The scale kept changing, but the invitation was consistent: come over, listen closely, and make the sound the project needs.</p>
    </section>''',
        "related": [("Lou Reed’s song band", "/conspiracies/lou-reed-song-band/"), ("Metal Machine Trio", "/conspiracies/metal-machine-trio/"), ("Lulu", "/conspiracies/lulu/"), ("“Junior Dad”", "/conspiracies/junior-dad/")],
        "people": [("Rob Wasserman", "/conspirators/rob-wasserman/")],
        "tools": [("Kyma", "/devices/"), ("Haken Continuum", "/devices/")],
    },
    {
        "name": "Lou Reed’s song band",
        "display": "Lou Reed’s song band",
        "path": "/conspiracies/lou-reed-song-band/",
        "kind": "Conspiracy",
        "schema": "MusicGroup",
        "description": "How Sarth Calhoun joined Lou Reed's song-based touring band to bring live processing, electronics, and fresh sounds to the music.",
        "dek": "Lou did not hire me to reproduce a keyboard part. He invited me because he wanted the familiar songs to have somewhere unfamiliar to go.",
        "body": r'''
    <section>
      <h2>The invitation</h2>
      <p>Lou invited me into the band himself. He made those decisions, and he was direct about what he wanted: fresh sounds. He wanted to modernize the sound of the band without turning the songs into demonstrations of technology.</p>
      <p>That made my role deliberately slippery. I processed instruments already onstage, sampled and reshaped the band in real time, and played electronic instruments that could move between melody, texture, and noise. The point was not to announce the machinery. The point was to give Lou another direction to turn.</p>
    </section>
    <section>
      <h2>A role without a chair</h2>
      <p>Tony Diodore joined the band later and described me as “Lou’s imagination.” If Lou wanted a wild sound, or a completely different kind of sound, that was what I brought. Sometimes that meant changing what another musician was already doing. Sometimes it meant putting something into the room that had no obvious source.</p>
      <p>The songs gave the experiments weight. You could leave the expected sound because everyone—including Lou—knew exactly where the song was.</p>
    </section>
    <section>
      <h2>The first version</h2>
      <p>The first documented rehearsals were at SIR in New York in April 2008. The band around Lou included Rob Wasserman, Kevin Hearn, Mike Rathke, Steve Hunter, and Tony “Thunder” Smith. We started in the Northeast, went south by bus, played Beale Street in Memphis, and came back to New York.</p>
      <p>Later versions of Lou’s touring band changed personnel and grew more electronically elaborate. The assignment stayed the same: listen to the band that exists, then open a door in it.</p>
    </section>''',
        "related": [("Spring 2008 U.S. tour", "/conspiracies/lou-reed-spring-2008-tour/"), ("Metal Machine Trio", "/conspiracies/metal-machine-trio/"), ("Lulu", "/conspiracies/lulu/")],
        "people": [("Lou Reed", "/conspirators/lou-reed/"), ("Rob Wasserman", "/conspirators/rob-wasserman/")],
        "tools": [("Kyma", "/devices/"), ("Haken Continuum", "/devices/")],
    },
    {
        "name": "Lou Reed spring 2008 U.S. tour",
        "display": "Lou Reed<br>spring 2008 U.S. tour",
        "path": "/conspiracies/lou-reed-spring-2008-tour/",
        "kind": "Conspiracy",
        "schema": "EventSeries",
        "description": "Lou Reed's spring 2008 U.S. tour with Sarth Calhoun, Rob Wasserman, Kevin Hearn, Mike Rathke, Steve Hunter, and Tony Smith.",
        "dek": "Massachusetts first, then a bus south. This was not a <em>Berlin</em> tour and it was not tied to a new album. It was the run where the band became real to me.",
        "body": r'''
    <section>
      <h2>The route I remembered</h2>
      <p>I remembered Massachusetts—Northampton, as it turned out—and then taking a bus south. I remembered Beale Street. That shape was enough to recover the tour even though later listings sometimes confused it with <em>Berlin</em>.</p>
      <p>It began with rehearsals at SIR in New York on 14 April. The surviving route runs from Philadelphia and Northampton through Washington, Asbury Park, Norfolk, Richmond, Durham, Asheville, Knoxville, Nashville, and Memphis, then home to the Highline Ballroom on 5 May.</p>
    </section>
    <section>
      <h2>The people on the bus</h2>
      <p>Lou was singing and playing guitar. Rob Wasserman played bass; Kevin Hearn keyboards; Mike Rathke and Steve Hunter guitars; Tony “Thunder” Smith drums. I handled electronics and live processing. It was a large band full of people with unmistakable sounds, which made changing those sounds both delicate and exciting.</p>
      <p>Rob was one of my heroes before he was my bandmate. On this tour he treated me—the younger person arriving with strange instruments—as though I already belonged. That changed the experience of becoming the new guy.</p>
    </section>
    <section>
      <h2>Beale Street</h2>
      <p>We reached the Beale Street Music Festival in Memphis on 3 May. Festivals flatten every band into a line on a poster, but for me that date is a pin in the map: proof that the half-remembered bus ride and the southern run were this tour.</p>
      <p class="source-note">Verified dates include Northampton on 20 April, <a href="https://www.memphisflyer.com/beale-street-music-fest-2008-lineup-announced">Beale Street</a> on 3 May, and New York on 5 May 2008. Public itineraries omit some engagements; the route here also uses the Lou Reed papers and surviving band correspondence.</p>
    </section>''',
        "related": [("Lou Reed’s song band", "/conspiracies/lou-reed-song-band/"), ("Metal Machine Trio", "/conspiracies/metal-machine-trio/"), ("Appearances", "/appearances/")],
        "people": [("Lou Reed", "/conspirators/lou-reed/"), ("Rob Wasserman", "/conspirators/rob-wasserman/")],
        "tools": [("Kyma", "/devices/")],
    },
    {
        "name": "Metal Machine Trio",
        "display": "Metal Machine Trio",
        "path": "/conspiracies/metal-machine-trio/",
        "kind": "Conspiracy",
        "schema": "MusicGroup",
        "description": "Sarth Calhoun on forming Metal Machine Trio with Lou Reed and Ulrich Krieger at REDCAT in 2008 and recording The Creation of the Universe.",
        "dek": "We arrived at REDCAT as three people playing an improvised noise gig under the name <em>Unclassified</em>. The shows sold out. The music gave the group its real name.",
        "body": r'''
    <section>
      <h2>The phone call</h2>
      <p>In 2008 Lou called and said he was doing a free-improvised noise show at REDCAT in Los Angeles with the saxophonist and composer Ulrich Krieger. Ulrich had done the improbable thing of arranging <em>Metal Machine Music</em> for an ensemble. I had already toured in Lou’s song band, processing and sampling the instruments onstage, and Lou and I had been making meditation music out of drones, melody, and noise. Joining them felt less like a detour than the next obvious step.</p>
      <p>Ulrich billed the concerts as <em>Unclassified</em> because there was no group name yet. That was honest. We did not know what the thing was until we played it.</p>
    </section>
    <section>
      <h2>Three different kinds of danger</h2>
      <p>Lou had guitar, electronics, and a small Continuum. Ulrich had tenor saxophone and live electronics. I played Continuum and processed the entire field through Kyma. Nobody was accompanying anybody else. Each of us could destabilize the music, and each had to leave enough room for the other two to do it.</p>
      <p>The shows sold out quickly and REDCAT added a late set. We recorded the room with a matched pair of Schoeps microphones and a stereo Royer—ambient microphones, no direct lines—and released the performances essentially as they happened.</p>
    </section>
    <section>
      <h2>The Creation of the Universe</h2>
      <p>Those Los Angeles nights became the double live album <em>The Creation of the Universe</em>. Afterward the trio played New York, Europe, Australia, and Brazil. “No songs. No vocals.” was useful poster copy, but it was not the meaning of the music. The meaning was three people building and wrecking a structure fast enough to remain inside it.</p>
      <p class="source-note">Metal Machine Trio began at <a href="https://web.archive.org/web/20110927041818/http://www.redcat.org/event/lou-reed-and-ulrich-krieger">REDCAT</a> on 2–3 October 2008. The album documents those nights. A later <a href="https://cranbrookartmuseum.org/exhibition/lou-reed-metal-machine-trio-the-creation-of-the-universe/">installation</a> with the same title uses the second Gramercy performance from 24 April 2009, with John Zorn—not the REDCAT album tape.</p>
    </section>''',
        "related": [("Appearances", "/appearances/"), ("Lou Reed’s song band", "/conspiracies/lou-reed-song-band/"), ("Lulu", "/conspiracies/lulu/")],
        "people": [("Lou Reed", "/conspirators/lou-reed/")],
        "tools": [("Kyma", "/devices/"), ("Haken Continuum", "/devices/")],
    },
    {
        "name": "Lulu",
        "display": "<em>Lulu</em>",
        "path": "/conspiracies/lulu/",
        "kind": "Conspiracy",
        "schema": "CreativeWork",
        "description": "How Sarth Calhoun and Lou Reed made music for Robert Wilson's 2011 Berliner Ensemble Lulu, then took the material to Metallica in San Francisco.",
        "dek": "Lou called me over to make interstitial music for a Robert Wilson production. It became songs, a score, rehearsals in Berlin, and then a record none of us could have predicted.",
        "body": r'''
    <section>
      <h2>Go over to Lou’s house</h2>
      <p>The assignment sounded small: make some “interstitial” music for Robert Wilson’s production of Frank Wedekind’s <em>Lulu</em> at the Berliner Ensemble. I went to Lou’s house. The interstitial music kept opening into larger pieces; in my account, it turned into co-writing eight more songs with Lou.</p>
      <p>The original tapes were spare and strange: Lou’s guitar, long cello drones, and Continuum. This was before Metallica. That was the material we made before Berlin—not the instrumentation of the band that later played the production.</p>
    </section>
    <section>
      <h2>Berlin without Lou</h2>
      <p>Lou was not in Berlin for rehearsals. I was. I helped turn the music we had sent into something the theater’s live band could perform night after night. It was a confusing situation, with the score, the songs, and the staging all moving at once.</p>
      <p>The band was Stefan Rager on drums and musical direction; Ulrich Maiß on keyboards and cello; Dominic Bouffard on guitar; Friedrich Paravicini on bugle, cello, and harmonica; Andreas Walter on bass; and Joe Bauer on sound effects. Touring programs sometimes list Ulf Borgwardt and Ofer Wetzler in the keyboard/cello and bass chairs. No Continuum or Kyma performer appears in the surviving production programs, and I do not remember bringing the Continuum to Berlin.</p>
      <p>The production was not simply playing finished Lou Reed songs under a play. The music had to become theater in the room: timed, embodied, and playable by the company night after night. <em>Lulu</em> premiered at the Berliner Ensemble on 12 April 2011 and remained in its repertoire through 2014, with guest runs in Paris, Spoleto, and São Paulo.</p>
    </section>
    <section>
      <h2>Then Metallica heard it</h2>
      <p>After Berlin, we took the material to San Francisco. Metallica did not decorate the score; they completely reinterpreted it. The scale, weight, and attack changed. The connective tissue remained the earlier tapes and songs—the quieter, otherworldly object underneath the album.</p>
      <p>That is the version of <em>Lulu</em> I want remembered: not one album credit, but a work that crossed Lou’s apartment, a Berlin rehearsal room, Robert Wilson’s stage, and Metallica’s studio without staying the same in any two places.</p>
      <p class="source-note"><a href="https://robertwilson.com/lulu">Robert Wilson’s production</a> premiered 12 April 2011. The <a href="https://www.festival-automne.com/fr/edition-2011/berliner-ensemble-lou-reed-robert-wilson-lulu">Festival d’Automne program</a> documents the live ensemble; David Fricke documented the earlier Continuum-and-cello tapes in <a href="https://www.rollingstone.com/music/music-news/when-metallica-met-lou-reed-78019/"><em>Rolling Stone</em></a>.</p>
    </section>''',
        "related": [("“Junior Dad”", "/conspiracies/junior-dad/"), ("Metal Machine Trio", "/conspiracies/metal-machine-trio/"), ("Sightings", "/sightings/")],
        "people": [("Lou Reed", "/conspirators/lou-reed/"), ("Rob Wasserman", "/conspirators/rob-wasserman/")],
        "tools": [("Kyma", "/devices/"), ("Haken Continuum", "/devices/")],
    },
    {
        "name": "Junior Dad",
        "display": "“Junior Dad”",
        "path": "/conspiracies/junior-dad/",
        "kind": "Conspiracy",
        "schema": "MusicRecording",
        "description": "The origin of Junior Dad: Rob Wasserman bowing electric upright at Lou Reed's apartment while Sarth Calhoun processed it through Kyma.",
        "dek": "The nineteen-minute end of <em>Lulu</em> began as a practical demonstration: Rob Wasserman bowing electric upright while I processed him through Kyma in Lou’s apartment.",
        "body": r'''
    <section>
      <h2>A stage test</h2>
      <p>Lou invited me over to show him what live processing might be like onstage. Rob Wasserman was there with his electric upright. He bowed; I listened through Kyma and began changing the sound around him.</p>
      <p>It was the first time Rob and I played together. I had known his records since I was a young bassist, so the source material was not abstract to me. I was processing the sound of one of the people who had taught me what a bass could be.</p>
    </section>
    <section>
      <h2>Keep the machine listening</h2>
      <p>Live processing is a conversation with consequences. If Rob changed pressure, pitch, or bow speed, the system gave me different material; what I did changed what he heard and therefore what he played next. The useful unit was not bass plus electronics. It was the loop between us.</p>
      <p>We recorded that first session. The recording became the basis for “Junior Dad,” the long closing track on <em>Lulu</em>. Later sessions and Metallica transformed the piece, but the seed was already there: Rob’s bowed string stretched into an environment.</p>
    </section>
    <section>
      <h2>Nineteen minutes later</h2>
      <p>On the album, “Junior Dad” arrives after everything else has spent itself. It is not an appendix. It changes the emotional scale of the record—less an ending than a landscape left behind when the characters are gone.</p>
      <p>Then Metallica dropped that guitar part right on top of the piece, and everything worked. It was basically the first edit: put the guitar there, and suddenly the whole thing was present. Pretty much everybody in the room was crying.</p>
      <p>For me it also preserves a first meeting in sound. Before the tours, before the finished record, there was Rob in Lou’s apartment, being generous enough to play into an unfamiliar process and hear where it went.</p>
      <p class="source-note">Sarth described this session in his 2016 remembrance of Rob. Surviving 2011 correspondence also discusses whether Rob’s original “Junior Dad” bass part remained in the evolving album track.</p>
    </section>''',
        "related": [("Lulu", "/conspiracies/lulu/"), ("Lou Reed’s song band", "/conspiracies/lou-reed-song-band/")],
        "people": [("Rob Wasserman", "/conspirators/rob-wasserman/"), ("Lou Reed", "/conspirators/lou-reed/")],
        "tools": [("Kyma", "/devices/")],
    },
]

for story in STORIES:
    story_page(story)

# --- sightings ---
sight_body = r'''
  <main class="page">
    <p class="kicker">Press</p>
    <h1>Sightings</h1>
    <p>Press tends to file Sarth Calhoun under “electronics,” but the work is composition. He made Metal Machine Trio with Lou Reed and Ulrich Krieger, and later wrote the original <em>Lulu</em> score with Reed for Robert Wilson. The Metallica album grew from those recordings. All quotes below appear exactly as published.</p>

    <section>
      <h2>Spine</h2>
      <ol>
        <li><a href="https://www.theverge.com/2013/1/3/3828314/the-book-of-sarth-ipad-app-graphic-novel-concept-album">The Verge</a> — Bryan Bishop — 3 Jan 2013 — Book of Sarth</li>
        <li><a href="https://web.archive.org/web/20140812122953/http://storyboard.tumblr.com/post/41358319321/the-book-of-sarth-an-interactive-cyberpunk-tale">Tumblr Storyboard</a> — 24 Jan 2013 — interview</li>
        <li><a href="https://www.vogue.it/people-are-talking-about/vogue-arts/2013/09/app-musicali">Vogue Italia</a> — Sep 2013 — “Hi-Tech Music” — Book of Sarth</li>
        <li><a href="https://gizmodo.com/tabletop-translator-book-of-sarth-and-more-5970597">Gizmodo</a> — Leslie Horn — 21 Dec 2012 — Apps of the Week</li>
        <li><a href="https://news.symbolicsound.com/2012/11/the-book-of-sarth/">The Eighth Nerve</a> — Nov 2012 — Symbolic Sound</li>
        <li><a href="https://www.stereophile.com/content/gralbum-re-thinking-concept-album">Stereophile</a> — Ariel Bitran — 23 Apr 2014 — Gralbum launch</li>
        <li><a href="https://www.nytimes.com/2009/04/25/arts/music/25reed.html">The New York Times</a> — Ben Ratliff — 25 Apr 2009 — Metal Machine Trio</li>
        <li><a href="https://www.billboard.com/music/music-news/lou-reed-oct-3-2008-los-angeles-redcatcalarts-theater-1043833/">Billboard</a> — Jeffrey Overwood — 8 Oct 2008 — REDCAT</li>
        <li><a href="https://variety.com/2009/music/markets-festivals/lou-reed-3-1117940137/">Variety</a> — David Sprague — 27 Apr 2009 — Gramercy</li>
        <li><a href="https://www.rollingstone.com/music/music-news/when-metallica-met-lou-reed-78019/">Rolling Stone</a> — David Fricke — 30 Sep 2011 — Lulu / Continuum</li>
        <li><a href="https://www.thewire.co.uk/in-writing/essays/lou-reed-1942-2013_ulrich-krieger_unclassifiable">The Wire</a> — Ulrich Krieger — 2013 — “Unclassifiable”</li>
        <li><a href="https://web.archive.org/web/20110621012417/http://www.buzzbinmagazine.com/home/2008/07/02/lucibel-crater-the-family-album/">Buzzbin Magazine</a> — Samson Stryker — 2 Jul 2008 — Lucibel Crater <em>The Family Album</em></li>
      </ol>
    </section>

    <section>
      <h2>Book of Sarth</h2>
      <ul class="press">
        <li>
          <blockquote>Things really come alive in what’s called the ‘director’s view’: tap an image and the artwork fills the screen, putting the reader in the same place as the characters.</blockquote>
          <blockquote>Calhoun’s music is no doubt experimental, but his tracks and the artwork play nimbly off one another.</blockquote>
          <cite><a href="https://www.theverge.com/2013/1/3/3828314/the-book-of-sarth-ipad-app-graphic-novel-concept-album">The Verge</a> · Bryan Bishop · 3 Jan 2013</cite>
        </li>
        <li>
          <blockquote>The app format seems like a completely new medium to work in. Music always needs a new medium, because it’s always changing. I think if music doesn’t have technology on its side, it tends to have the problem of where to go, it starts to run out of steam.</blockquote>
          <cite>Sarth Calhoun, <a href="https://web.archive.org/web/20140812122953/http://storyboard.tumblr.com/post/41358319321/the-book-of-sarth-an-interactive-cyberpunk-tale">Tumblr Storyboard</a> · ~24 Jan 2013</cite>
        </li>
        <li>
          <blockquote>a narrative about an ear worm that is, itself, an ear worm! The Book of Sarth is the first example of an entirely new art form for the early 21st century.</blockquote>
          <cite><a href="https://news.symbolicsound.com/2012/11/the-book-of-sarth/">The Eighth Nerve</a> · Nov 2012</cite>
        </li>
        <li>
          <blockquote>I wouldn’t mind rolling a j before playing with this trippy app.</blockquote>
          <cite><a href="https://gizmodo.com/tabletop-translator-book-of-sarth-and-more-5970597">Gizmodo</a> · Leslie Horn · 21 Dec 2012</cite>
        </li>
        <li>
          <blockquote>Chi invece è riuscito a coniare un nuovo concetto di ‘album musicale’ è Sarth Calhoun con il suo sorprendente The Book of Sarth.</blockquote>
          <cite><a href="https://www.vogue.it/people-are-talking-about/vogue-arts/2013/09/app-musicali">Vogue Italia</a> · Sep 2013 · “Hi-Tech Music”</cite>
        </li>
        <li>
          <p>Launch at SOHO Digital Arts.</p>
          <cite><a href="https://www.stereophile.com/content/gralbum-re-thinking-concept-album">Stereophile</a> · Ariel Bitran · 23 Apr 2014</cite>
        </li>
        <li>
          <cite><a href="https://laughingsquid.com/gralbum-an-ipad-app-that-turns-records-into-a-multimedia-experience/">Laughing Squid</a> · Brian Heater · 8 Apr 2014</cite>
        </li>
        <li>
          <cite><a href="https://www.chaindlk.com/reviews/7353">Chain D.L.K.</a></cite>
        </li>
      </ul>
    </section>

    <section>
      <h2>Lucibel Crater</h2>
      <ul class="press">
        <li>
          <blockquote>this is totally music to get high to.</blockquote>
          <cite><a href="https://web.archive.org/web/20110621012417/http://www.buzzbinmagazine.com/home/2008/07/02/lucibel-crater-the-family-album/">Buzzbin Magazine</a> · Samson Stryker · 2 Jul 2008</cite>
        </li>
        <li>
          <blockquote>Something like Bjork and maybe like White Stripes; But the truth is that their sound is unique and not easy to label, to the extent that even Lou Reed has fallen in love with it.</blockquote>
          <cite>Urban Magazine (Italia) · Simone Tempia · 2009</cite>
        </li>
        <li>
          <blockquote>Lucibel Crater surprise us with a schizoid, unpredictable sound made of both live improvisations and thoughtful studio recordings.</blockquote>
          <cite>Vogue Italia · Simone Tempia · 2009 · Lucibel, not the 2013 Book of Sarth piece</cite>
        </li>
      </ul>
    </section>

    <section>
      <h2>Metal Machine Trio</h2>
      <ul class="press">
        <li>
          <blockquote>The duo took the stage along with Sarth Calhoun, a computer-based sound designer… Calhoun, seated behind a desk with computers and mixers, added chunky layers of sub-frequency bass vibrations to the mix.</blockquote>
          <cite><a href="https://www.billboard.com/music/music-news/lou-reed-oct-3-2008-los-angeles-redcatcalarts-theater-1043833/">Billboard</a> · Jeffrey Overwood · 8 Oct 2008 · REDCAT</cite>
        </li>
        <li>
          <blockquote>On Thursday night at the Blender Theater at Gramercy, onstage between Sarth Calhoun and Ulrich Krieger, two much younger musicians, he was making noise — improvised, loud, heavily processed, and some of it ugly enough to make people leave.</blockquote>
          <cite><a href="https://www.nytimes.com/2009/04/25/arts/music/25reed.html">The New York Times</a> · Ben Ratliff · 25 Apr 2009</cite>
        </li>
        <li>
          <blockquote>teaming with the composer and saxophonist Ulrich Krieger and the multi-instrumentalist Sarth Calhoun to create ‘a night of deep noise.’</blockquote>
          <cite><a href="https://www.nytimes.com/2009/04/17/arts/music/17pop.html">The New York Times</a> · listing · 17 Apr 2009</cite>
        </li>
        <li>
          <blockquote>It would be too warm and fuzzy to suggest that he engaged bandmate Sarth Calhoun — who did much of his work on a laptop — in any sort of interplay, but the two did combine to create a formidable wall of sound.</blockquote>
          <cite><a href="https://variety.com/2009/music/markets-festivals/lou-reed-3-1117940137/">Variety</a> · David Sprague · 27 Apr 2009</cite>
        </li>
        <li>
          <blockquote>Calhoun started playing his Continuum as if it was a throbbing Hammond organ, creating a low undulating swarm of sound.</blockquote>
          <cite><a href="https://www.rollingstone.com/music/music-news/lou-reed-brings-controversial-metal-machine-music-to-life-114478/">Rolling Stone</a> · Apr 2009</cite>
        </li>
        <li>
          <blockquote>Lou decided to bring Sarth along at the last minute; he met him at tai chi practice, played with him at home and wanted his electronic sounds for this concert.</blockquote>
          <cite>Ulrich Krieger, <a href="https://www.thewire.co.uk/in-writing/essays/lou-reed-1942-2013_ulrich-krieger_unclassifiable">The Wire</a> · 2013 · “Unclassifiable”</cite>
        </li>
        <li>
          <blockquote>Lou said, I don’t want to play duo, I have this electronic guy in New York and I’d like to bring him along. So he brought Sarth Calhoun in.</blockquote>
          <cite>Ulrich Krieger, <a href="https://www.ocweekly.com/metal-machine-trios-ulrich-krieger-the-trio-is-an-update-of-lou-reeds-metal-machine-music-in-philosophical-and-aesthetic-sense-6581450/">OC Weekly</a> · 27 Jan 2012</cite>
        </li>
        <li>
          <cite><a href="https://www.spinmagazine.com/2009/04/lou-reed-unleashes-metal-machine-music-nyc/">SPIN</a> · John Macdonald · 24 Apr 2009 · names the Continuum Fingerboard</cite>
        </li>
        <li>
          <cite><a href="https://www.villagevoice.com/lou-reeds-metal-machine-trio/">Village Voice</a> · 15 Apr 2009</cite>
        </li>
      </ul>
    </section>

    <section>
      <h2>Lulu</h2>
      <ul class="press">
        <li>
          <blockquote>long drones on cello and an electronic instrument, the Continuum, played by Reed and Sarth Calhoun, a member of Reed’s band. (Calhoun also appears on Lulu.)</blockquote>
          <cite>David Fricke, <a href="https://www.rollingstone.com/music/music-news/when-metallica-met-lou-reed-78019/">Rolling Stone</a> · 30 Sep 2011 · describing the original Wilson-era tapes</cite>
        </li>
      </ul>
    </section>

    <section>
      <h2>Books</h2>
      <ul class="press">
        <li>
          <p>Sarth is in Anthony DeCurtis, <em>Lou Reed: A Life</em> (2017, Little, Brown / Dey Street).</p>
        </li>
        <li>
          <p>Interviewed for Lou Reed, <em>The Art of the Straight Line: My Tai Chi</em> (14 Mar 2023, HarperOne). Named as an interviewee by <a href="https://kitchensisters.org/podcast/lou-reeds-tai-chi/">The Kitchen Sisters</a>. Brookfield Place Winter Garden, Lou Reed’s 81st birthday, 2 Mar 2023: guest performance with Kevin Hearn, Shahzad Ismaily, Laurie Anderson, against Lou Reed’s Musical Drones (Stewart Hurwood).</p>
        </li>
      </ul>
    </section>
  </main>
'''

page(
    path="sightings/index.html",
    title="Sightings — Sarth Calhoun",
    description="Press on Sarth Calhoun: Book of Sarth, Metal Machine Trio, Lulu, Lucibel Crater. Verbatim quotes. The Verge, New York Times, Billboard, Rolling Stone, The Wire.",
    canonical=f"{HOST}/sightings/",
    current="sightings",
    body=sight_body,
    graph_html="""    <dl>
      <dt>On this site</dt>
      <dd><a href="/">Sarth Calhoun</a> · sarth.net</dd>
      <dt>Related work</dt>
      <dd><a href="/appearances/">Appearances</a> · <a href="https://bookofsarth.com">Book of Sarth</a></dd>
      <dt>source</dt>
      <dd>Outlet pages linked in each entry. Quotes verbatim from the live page or a Wayback capture.</dd>
    </dl>""",
    jsonld=ld(
        [
            PERSON,
            {
                "@type": "CollectionPage",
                "name": "Sightings",
                "url": f"{HOST}/sightings/",
                "about": {"@id": f"{HOST}/#person"},
                "description": "Press, interviews, and reviews of Sarth Calhoun.",
                "isPartOf": {"@id": f"{HOST}/#website"},
                "author": {"@id": f"{HOST}/#person"},
            },
        ]
    ),
)

print("sightings ok")

# --- appearances ---
appear_body = r'''
  <main class="page">
    <p class="kicker">Live</p>
    <h1>Appearances</h1>
    <p>A record of the shows and installations I could verify. <em>The Creation of the Universe</em> comes from two nights at REDCAT, October 2–3, 2008. The later ambisonic installation uses a different recording, made at the Gramercy show on April 24, 2009.</p>

    <section>
      <h2>Spine</h2>
      <ol>
        <li><strong>Metal Machine Trio (Unclassified) at REDCAT, Los Angeles — 2–3 Oct 2008.</strong> World premiere billed as <em>Unclassified: Lou Reed and Ulrich Krieger</em>. Three performances: Thu 2 Oct 8:30pm, added late show Thu 2 Oct 10:30pm, Fri 3 Oct 8:30pm. Sarth on Continuum / live processing. Official live album <em>The Creation of the Universe</em> is the unedited recording of those two nights. <span class="tag">confirmed</span></li>
        <li><strong>Metal Machine Trio, Blender Theater at Gramercy, New York — 23–24 Apr 2009.</strong> First NYC stand. John Zorn sat in on the 24th. This night’s recording later became the CSULB / Cranbrook ambisonic installation. <span class="tag">confirmed</span></li>
        <li><strong>Yellow Pony with Lou Reed and Laurie Anderson — Europe, Jul and Aug–Sep 2009.</strong> Eight-city tour billed <em>The Yellow Pony and Other Songs and Stories</em>. Sarth on Continuum and live voice re-sampling, center stage. Two short tours. <span class="tag">confirmed</span></li>
        <li><strong>Metal Machine Trio Europe — “A Night of Deep Noise,” 17–30 Apr 2010.</strong> Nine announced dates, UK through Palma de Mallorca. Mallorca is MM3, not Yellow Pony. <span class="tag">confirmed</span></li>
        <li><strong>Metal Machine Trio, Sydney Opera House (Opera Theatre) — 30 May 2010.</strong> Vivid LIVE. Sarth on the bill. Anderson’s <em>Transitory Life</em> was a separate Drama Theatre program, 1–2 Jun. <span class="tag">confirmed</span></li>
        <li><strong>Metal Machine Trio, Sesc Pinheiros, São Paulo — 20–21 Nov 2010.</strong> Two nights. <span class="tag">confirmed</span></li>
        <li><strong>Ambisonic installation <em>The Creation of the Universe</em></strong> — CSULB University Art Museum, Long Beach, 27 Jan–15 Apr 2012; restaged Cranbrook Art Museum, Bloomfield Hills, 21 Nov 2015–26 Mar 2016. Playback of the Gramercy 2009 recording, not a live Sarth performance. <span class="tag">confirmed</span></li>
      </ol>
      <p>The public record shows no Metal Machine Trio concerts after São Paulo. Wikipedia’s 2008–2013 span follows the life of the project through Reed’s death; it does not point to additional shows.</p>
    </section>

    <section>
      <h2>Metal Machine Trio</h2>
      <p>Billing unless noted: Lou Reed (guitar, electronics, Continuum), Ulrich Krieger (tenor sax, live electronics), Sarth Calhoun (Continuum, live processing / Kyma). Flyers: “No songs. No vocals.” / “A Night of Deep Noise.”</p>
      <ul class="dates">
        <li>
          <p><strong>2008-10-02</strong> — REDCAT / CalArts Theater, Walt Disney Concert Hall complex, Los Angeles. Unclassified: Lou Reed and Ulrich Krieger. World premiere. 8:30pm and added late show 10:30pm. <span class="tag">confirmed</span></p>
          <p class="meta"><a href="https://web.archive.org/web/20110927041818/http://www.redcat.org/event/lou-reed-and-ulrich-krieger">REDCAT archive</a> · recording: album Night 1</p>
        </li>
        <li>
          <p><strong>2008-10-03</strong> — REDCAT, Los Angeles. 8:30pm. <span class="tag">confirmed</span></p>
          <p class="meta"><a href="https://www.billboard.com/music/music-news/lou-reed-oct-3-2008-los-angeles-redcatcalarts-theater-1043833/">Billboard</a> · recording: album Night 2</p>
        </li>
        <li>
          <p><strong>2009-04-23</strong> — Blender Theater at Gramercy, New York. A Night of Deep Noise. 8:30pm. <span class="tag">confirmed</span></p>
          <p class="meta"><a href="https://www.nytimes.com/2009/04/25/arts/music/25reed.html">NYT Ratliff</a> · <a href="https://www.villagevoice.com/lou-reeds-metal-machine-trio/">Village Voice</a></p>
        </li>
        <li>
          <p><strong>2009-04-24</strong> — Blender Theater at Gramercy, New York. Special guest John Zorn. Source tape for the CSULB/Cranbrook installation. Not commercially issued. <span class="tag">confirmed</span></p>
          <p class="meta"><a href="https://variety.com/2009/music/markets-festivals/lou-reed-3-1117940137/">Variety</a></p>
        </li>
        <li>
          <p><strong>2010-04-17</strong> — The Junction, Cambridge, UK. Start of nine-date Europe tour. <span class="tag">confirmed</span></p>
        </li>
        <li>
          <p><strong>2010-04-18</strong> — O2 Academy, Oxford, UK. <span class="tag">confirmed</span></p>
        </li>
        <li>
          <p><strong>2010-04-19</strong> — Royal Festival Hall, London, UK (Ether Festival). <span class="tag">confirmed</span></p>
        </li>
        <li>
          <p><strong>2010-04-21</strong> — La Cigale, Paris, France. Announced widely. <span class="tag">mentioned</span></p>
        </li>
        <li>
          <p><strong>2010-04-22</strong> — Ancienne Belgique, Brussels, Belgium (Domino Festival). <span class="tag">mentioned</span></p>
        </li>
        <li>
          <p><strong>2010-04-24</strong> — DR Koncerthuset, Copenhagen, Denmark. <span class="tag">mentioned</span></p>
        </li>
        <li>
          <p><strong>2010-04-26</strong> — Oslo, Norway. The date happened. Announced as Sentrum Scene; eyewitness blogs say Rockefeller. Sister rooms in the same complex. Venue name not settled. <span class="tag">confirmed as a night; venue unresolved</span></p>
        </li>
        <li>
          <p><strong>2010-04-27</strong> — Ole Bull Scene, Bergen, Norway (Bergenfest). Calhoun at the laptop table. <span class="tag">confirmed</span></p>
        </li>
        <li>
          <p><strong>2010-04-30</strong> — Teatre Principal, Palma de Mallorca, Spain (Festival Alternatilla). MM3, not Yellow Pony. Start time 21:00 vs 22:00 unresolved. <span class="tag">confirmed</span></p>
        </li>
        <li>
          <p><strong>2010-05-30</strong> — Opera Theatre, Sydney Opera House. Vivid LIVE. <span class="tag">confirmed</span></p>
        </li>
        <li>
          <p><strong>2010-11-20</strong> and <strong>2010-11-21</strong> — Teatro Paulo Autran, Sesc Pinheiros, São Paulo. <span class="tag">confirmed</span></p>
        </li>
      </ul>
    </section>

    <section>
      <h2>Installations — not concerts</h2>
      <ul class="dates">
        <li>
          <p><strong>2012-01-27 – 2012-04-15</strong> — University Art Museum, CSULB, Long Beach. Ambisonic playback of Gramercy 2009 night 2 (Zorn). Visitors stand in Lou’s, Ulrich’s, or Sarth’s onstage position. Recorded performer. Not documented as appearing live at the museum. <span class="tag">confirmed</span></p>
        </li>
        <li>
          <p><strong>2015-11-21 – 2016-03-26</strong> — Cranbrook Art Museum, Bloomfield Hills, Michigan. Restaging. 12 loudspeakers. After Reed’s death; playback only. <span class="tag">confirmed</span></p>
          <p class="meta"><a href="https://cranbrookartmuseum.org/exhibition/lou-reed-metal-machine-trio-the-creation-of-the-universe/">Cranbrook</a></p>
        </li>
      </ul>
    </section>

    <section>
      <h2>Yellow Pony — Lou Reed and Laurie Anderson</h2>
      <p>Continuum fingerboard and live resampling of their voices. Center of the stage, like a drummer.</p>
      <ul class="dates">
        <li>
          <p><strong>2009-07-10</strong> — Festival de la Porta Ferrada, Sant Feliu de Guíxols, Spain. Present at the press conference. <span class="tag">confirmed</span></p>
        </li>
        <li>
          <p><strong>2009-07-12</strong> — Plaza del Obradoiro, Santiago de Compostela, Spain. <span class="tag">mentioned</span></p>
        </li>
        <li>
          <p><strong>2009-07-14</strong> — Los Veranos de la Villa, Madrid, Spain. <span class="tag">mentioned</span></p>
        </li>
        <li>
          <p><strong>2009-07-16</strong> — DR Koncerthuset, Copenhagen, Denmark. Named onstage. <span class="tag">confirmed</span></p>
        </li>
        <li>
          <p><strong>2009-07-18</strong> — Palace Theatre, Manchester, UK. “electronic sound manipulator… between them” (<a href="https://www.theguardian.com/music/2009/jul/20/laurie-anderson-lou-reed-review">The Guardian</a>). <span class="tag">confirmed</span></p>
        </li>
        <li>
          <p><strong>2009-08-30</strong> — Huvilateltta, Helsinki, Finland. <span class="tag">mentioned</span></p>
        </li>
        <li>
          <p><strong>2009-09-02</strong> — Jahrhunderthalle, Frankfurt, Germany. Electronics, named in program and reviews. <span class="tag">confirmed</span></p>
        </li>
        <li>
          <p><strong>2009-09-04</strong> — Salle Pleyel, Paris. Billed “claviers et électronique.” <span class="tag">confirmed</span></p>
        </li>
      </ul>
    </section>

    <section>
      <h2>Lucibel Crater</h2>
      <p>Sarth — keys, bass, loops, Kyma, Continuum. Leah Coloff, Paul Chuffo.</p>
      <ul class="dates">
        <li><strong>2007-02-27</strong> — Knitting Factory main space, NYC, with Subtle. <span class="tag">confirmed</span></li>
        <li><strong>2007-03-08</strong> — FatBaby, 112 Rivington St, NYC. <span class="tag">confirmed</span></li>
        <li><strong>2007-04-03</strong> — The Delancey, NYC (WARPER). <span class="tag">confirmed</span></li>
        <li><strong>2008-11-23</strong> — RAW-Tempel, Berlin. Lucibel Crater N.Y. Video <em>Holy, Then, Now — Berlin Live</em> shot here. <span class="tag">confirmed</span></li>
        <li><strong>2009-03-04</strong> — The Delancey, NYC (WARPER). Downstairs 8:20, Sarth solo slot on the printed bill. <span class="tag">confirmed as Sarth</span></li>
      </ul>
    </section>

    <section>
      <h2>Lou Reed song band, 2011</h2>
      <p>Not MM3. Symbolic Sound: Sarth Calhoun on Continuum, multiple Kyma/Paca systems, Europe, July 2011. Announced lineup also: Kevin Hearn, Ulrich Krieger, Tony Smith, Rob Wasserman. Individual nights are announced; this page does not treat a conflicted Pescara row as fact.</p>
      <ul class="dates">
        <li>2011-07-02 Hop Farm, Paddock Wood · 07-04 Hammersmith Apollo, London · 07-05 Le Grand Rex, Paris · 07-08 Arena Civica, Milan (on some lists) · 07-10 Piazza Duomo, Pistoia · 07-16 Italia Wave, Lecce · 07-17 Les Vieilles Charrues, Carhaix · 07-18 Greek Theatre, Taormina · 07-22 Nuovo Festival Del Vittoriale, Gardone Riviera · 07-23 Piazza Matteotti, Sogliano al Rubicone · 07-25 Parco della Musica Cavea, Rome · 07-26 Les Nuits de Fourvière, Lyon. <span class="tag">Sarth on the tour: confirmed. Nights: mentioned</span></li>
      </ul>
    </section>

    <section>
      <h2>Lulu</h2>
      <p>Studio: electronics on <em>Lulu</em> (2011). Continuum drones on Reed’s pre-Metallica tapes (Fricke). No public live date with Calhoun was found. Reed+Metallica played television without a Calhoun credit. Wilson’s Berlin <em>Lulu</em> used the score; Sarth directed rehearsals in Berlin. Junior Dad began at Lou’s apartment with Rob Wasserman and Kyma.</p>
    </section>

    <section>
      <h2>Later</h2>
      <ul class="dates">
        <li>
          <p><strong>2014-04-09</strong> — SOHO Gallery for Digital Arts, New York. Gralbum / Book of Sarth app launch. Exhibition, not a concert. <span class="tag">confirmed</span></p>
          <p class="meta"><a href="https://www.stereophile.com/content/gralbum-re-thinking-concept-album">Stereophile</a></p>
        </li>
        <li>
          <p><strong>2019-03-13</strong> — Cathedral of St. John the Divine, New York. Lou Reed Drones for Reed’s 77th birthday. Continuum / electronics, with Laurie Anderson, John Zorn, Stewart Hurwood, Stan Harrison, Shahzad Ismaily. <span class="tag">confirmed</span></p>
        </li>
        <li>
          <p><strong>2019-08-03</strong> — Prospect Park Bandshell, Brooklyn. International Lou Reed Tai Chi Day / BRIC Celebrate Brooklyn! Laurie Anderson, John Zorn, Sarth Calhoun, Stewart Hurwood. <span class="tag">confirmed as billed</span></p>
        </li>
        <li>
          <p><strong>2023-03-02</strong> — Brookfield Place Winter Garden. Lou Reed’s 81st birthday. Guest performance with Kevin Hearn, Shahzad Ismaily, Laurie Anderson, against Lou Reed’s Musical Drones (Stewart Hurwood). <span class="tag">confirmed</span></p>
        </li>
      </ul>
    </section>
  </main>
'''

page(
    path="appearances/index.html",
    title="Appearances — Sarth Calhoun",
    description="Verified live appearances: Metal Machine Trio REDCAT 2008, Gramercy 2009, Europe and Sydney 2010, Yellow Pony with Lou Reed and Laurie Anderson, Lucibel Crater, Lulu studio, Lou Reed Drones.",
    canonical=f"{HOST}/appearances/",
    current="appearances",
    body=appear_body,
    graph_html="""    <dl>
      <dt>On this site</dt>
      <dd><a href="/">Sarth Calhoun</a> · sarth.net</dd>
      <dt>Related work</dt>
      <dd><a href="/sightings/">Sightings</a> · <a href="/devices/">Devices</a></dd>
      <dt>Conspirators</dt>
      <dd>Lou Reed · Ulrich Krieger · Laurie Anderson · Leah Coloff · Paul Chuffo · Rob Wasserman · John Zorn</dd>
      <dt>priorArt</dt>
      <dd><em>The Creation of the Universe</em> = REDCAT 2–3 Oct 2008. Installation tape = Gramercy 24 Apr 2009. Junior Dad = first session at Lou’s apartment, Wasserman through Kyma.</dd>
    </dl>""",
    jsonld=ld(
        [
            PERSON,
            {
                "@type": "CollectionPage",
                "name": "Appearances",
                "url": f"{HOST}/appearances/",
                "about": {"@id": f"{HOST}/#person"},
                "description": "Verified live appearances of Sarth Calhoun.",
                "isPartOf": {"@id": f"{HOST}/#website"},
                "author": {"@id": f"{HOST}/#person"},
            },
        ]
    ),
)

# --- devices ---
devices_body = r'''
  <main class="page">
    <p class="kicker">Physical objects</p>
    <h1>Devices</h1>
    <p>Physical objects on the table. Kyma, Continuum, the performance DAW, the motion studio. Software machines live on <a href="https://contraptions.bookofsarth.com">Contraptions</a>.</p>

    <article class="device">
      <h2>Symbolic Sound Kyma (Paca / Pacarana)</h2>
      <p>A graphical sound-design environment. The Paca is dedicated DSP hardware — a small orange box, rack-mountable, not a plugin inside a laptop. Maker: Symbolic Sound Corporation (Carla Scaletti and Kurt Hebel), Champaign, Illinois. <a href="https://kyma.symbolicsound.com/">kyma.symbolicsound.com</a></p>
      <p>Beta-tested Kyma (credited on the Kyma X startup screen). Lucibel Crater looping and processing. Metal Machine Trio: live Kyma processing of the band. 2011 Lou Reed European tour: multiple rack-mounted Pacas. <em>Lulu</em> at the Berliner Ensemble: Kyma processing and Continuum/Kyma playing. The Book of Sarth score is Kyma-drenched. SeqOSC was built in it. Junior Dad: Wasserman’s electric upright through Kyma, first session at Lou’s apartment.</p>
      <p>The orange box does the math so the fingers can lie.</p>
      <p class="meta"><a href="https://news.symbolicsound.com/2011/07/lou-reeds-euro-tour/">Euro tour</a> · <a href="https://news.symbolicsound.com/2012/11/the-book-of-sarth/">Book of Sarth</a></p>
    </article>

    <article class="device">
      <h2>Haken Continuum Fingerboard</h2>
      <p>A long neoprene playing surface that tracks finger position and pressure in three dimensions. Continuous pitch, not keys. Often driving Kyma. Maker: Lippold Haken / Haken Audio, Champaign, Illinois. <a href="https://www.hakenaudio.com/">hakenaudio.com</a></p>
      <p>Lucibel and the Reed years. In Metal Machine Trio, he and Lou both had Continuums onstage. Yellow Pony: Continuum plus live resampling of Reed and Anderson’s voices. <em>Lulu</em>: dual Continuum improvisations with a live string section. Wikipedia names him as an advocate.</p>
      <p>A surface, not a keyboard. Lou had one too.</p>
      <p class="meta"><a href="https://en.wikipedia.org/wiki/Continuum_Fingerboard">Continuum Fingerboard</a> · <a href="https://news.symbolicsound.com/2012/10/walking-the-road-that-only-you-can-see/">Walking the road that only you can see</a></p>
    </article>

    <article class="device">
      <h2>Ableton Live</h2>
      <p>A DAW that treats clips, warping, and devices as a performance instrument. Maker: Ableton AG, Berlin. <a href="https://www.ableton.com/en/live/">ableton.com</a></p>
      <p>Public bios call him an Ableton Live endorser: the 2008 REDCAT program and the 2014 Asia Society <em>Sunken Cathedral</em> notes. Book of Sarth track “Awakening (To Blacklist)” was built in Live — 60-cycle hum run through plugins until a frequency shifter became the melody.</p>
      <p>Endorsed it. Then I made a melody out of wall hum.</p>
    </article>

    <article class="device">
      <h2>Runway</h2>
      <p>Generative video and image studio. The motion end of Visual Reference Prompting. Maker: Runway AI, Inc. <a href="https://runwayml.com/">runwayml.com</a></p>
      <p>Burlap lists Runway as a first-class provider. He entered Runway’s Gen:48 48-hour AI film challenge (2024).</p>
      <p>Forty-eight hours, their credits, my pictures. Motion from a still I already made.</p>
    </article>

    <article class="device">
      <h2>Bass</h2>
      <p>First instrument he saved for. Stopped buying comics. Number19: bass and keys. Lucibel: keys, bass, loops. Reed’s “Peggy Sue” (<em>Rave On Buddy Holly</em>): bass. Which factory made the bass on the table is not in the public record.</p>
    </article>
  </main>
'''

page(
    path="devices/index.html",
    title="Devices — Sarth Calhoun",
    description="Physical objects on Sarth Calhoun’s table: Symbolic Sound Kyma, Haken Continuum Fingerboard, Ableton Live, Runway. Used in Metal Machine Trio, Lulu, Lucibel Crater, Book of Sarth, Burlap.",
    canonical=f"{HOST}/devices/",
    current="devices",
    body=devices_body,
    graph_html="""    <dl>
      <dt>On this site</dt>
      <dd><a href="/">Sarth Calhoun</a> · sarth.net</dd>
      <dt>Related work</dt>
      <dd><a href="https://contraptions.bookofsarth.com">Contraptions</a> (software shelf, different page) · <a href="/transmissions/visual-reference-prompting/">Visual Reference Prompting</a></dd>
      <dt>Tools</dt>
      <dd>Kyma · Continuum · Ableton Live · Runway</dd>
      <dt>priorArt</dt>
      <dd>Carla Scaletti and Kurt Hebel, Kyma · Lippold Haken, Continuum</dd>
    </dl>""",
    jsonld=ld(
        [
            PERSON,
            {
                "@type": "CollectionPage",
                "name": "Devices",
                "url": f"{HOST}/devices/",
                "about": {"@id": f"{HOST}/#person"},
                "description": "Physical instruments and systems in Sarth Calhoun’s practice.",
                "isPartOf": {"@id": f"{HOST}/#website"},
                "author": {"@id": f"{HOST}/#person"},
            },
        ]
    ),
)

# --- transmissions index ---
tx_body = r'''
  <main class="page">
    <p class="kicker">Essays</p>
    <h1>Transmissions</h1>
    <p>Notes from the work: images, instruments, generative systems, and whatever happens between them.</p>
    <ul class="press">
      <li>
        <h2><a href="/transmissions/visual-reference-prompting/">Visual Reference Prompting</a></h2>
        <p>31 Jul 2026. How original images can hold a subject together, bend a style, and open up stranger places to go next.</p>
      </li>
    </ul>
  </main>
'''

page(
    path="transmissions/index.html",
    title="Transmissions — Sarth Calhoun",
    description="Essays by Sarth Calhoun. Visual Reference Prompting: original images used to push AI generation into new probability spaces.",
    canonical=f"{HOST}/transmissions/",
    current="transmissions",
    body=tx_body,
    graph_html="""    <dl>
      <dt>On this site</dt>
      <dd><a href="/">Sarth Calhoun</a> · sarth.net</dd>
      <dt>Related work</dt>
      <dd><a href="/transmissions/visual-reference-prompting/">Visual Reference Prompting</a> · <a href="https://burlap.app">Burlap</a> · <a href="https://thirdwallstudio.com">Third Wall Studio</a></dd>
    </dl>""",
    jsonld=ld(
        [
            PERSON,
            {
                "@type": "CollectionPage",
                "name": "Transmissions",
                "url": f"{HOST}/transmissions/",
                "about": {"@id": f"{HOST}/#person"},
                "isPartOf": {"@id": f"{HOST}/#website"},
                "author": {"@id": f"{HOST}/#person"},
            },
        ]
    ),
)

# --- VRP ---
vrp_body = r'''
  <main class="page essay">
    <p class="kicker">31 Jul 2026</p>
    <h1>Visual Reference Prompting</h1>
    <p>We’ve been doing hybrid production at <a href="https://thirdwallstudio.com">Third Wall Studio</a> since before anyone called it that. I made <a href="https://burlap.app">Burlap</a> for this precise use case: Start from original art and use it to style more images, explore variations, and most importantly generate all the “in betweens” that make animation so brutally manual and meticulous.</p>
    <p>I call this <em>visual reference prompting</em> meaning you want to be using visual material as the input to creating visual material. This is axiomatic. There is a reason they say “a picture is worth a thousand words.”</p>
    <p>There are two dimensions of this technique, broadly. One is using a subject reference (for example a character) and the other is a style reference. In both cases you are pushing the genAI into a different probability space. This is how to get a unique style, and also how you chase consistency.</p>
    <p>In the general case this is context management. Actively choosing the elements that are fed into the model with each generation step. And in Burlap you do this in the most intuitive way I could imagine: just select stuff on the canvas and send it to be generated.</p>
    <p>Because the default Burlap interface isn’t a chat mode, to implement chat you would need to manually reselect all the context after each round of generation. Which is pointlessly manual for chat. But it also exposes to the end user what chat is. Resending the entire convo over and over and over. Instead, we are trying to give the model the precise context it needs, for each generation we call. For a concrete example: Frogs and Goblins (below).</p>
    <div class="frame">
      <iframe src="https://www.youtube.com/embed/wroKqbXfx5g" title="Frogs and Goblins — Visual Reference Prompting" allow="fullscreen; picture-in-picture" allowfullscreen></iframe>
    </div>
    <p class="meta"><a href="https://burlap.app/download">Download Burlap</a> · <a href="https://thirdwallstudio.com">Third Wall Studio</a></p>
  </main>
'''

page(
    path="transmissions/visual-reference-prompting/index.html",
    title="Visual Reference Prompting — Sarth Calhoun",
    description="We’ve been doing hybrid production at Third Wall Studio since before anyone called it that. I made Burlap for this precise use case: Start from original art and use it to style more images, explore variations, and generate the in-betweens.",
    canonical=f"{HOST}/transmissions/visual-reference-prompting/",
    current="transmissions",
    og_type="article",
    extra_head='  <meta property="article:published_time" content="2026-07-31">\n  <meta property="article:author" content="Sarth Calhoun">\n',
    body=vrp_body,
    graph_html="""    <dl>
      <dt>On this site</dt>
      <dd><a href="/transmissions/">Transmissions</a> · <a href="/">Sarth Calhoun</a></dd>
      <dt>Related work</dt>
      <dd><a href="https://burlap.app">Burlap</a> · <a href="https://thirdwallstudio.com">Third Wall Studio</a> · <a href="https://contraptions.bookofsarth.com">Contraptions</a></dd>
      <dt>Tools</dt>
      <dd>Burlap · original images as references</dd>
      <dt>inspiredBy</dt>
      <dd>Twenty-five years of pushing strange instruments by hand, on a surface where the whole thing is visible at once.</dd>
      <dt>source</dt>
      <dd>First published 31 Jul 2026 at /words/2026/7/31/visual-reference-prompting on sarth.net.</dd>
    </dl>""",
    jsonld=ld(
        [
            PERSON,
            {
                "@type": "Article",
                "headline": "Visual Reference Prompting",
                "name": "Visual Reference Prompting",
                "url": f"{HOST}/transmissions/visual-reference-prompting/",
                "datePublished": "2026-07-31",
                "author": {"@id": f"{HOST}/#person"},
                "publisher": {"@id": f"{HOST}/#person"},
                "image": OG,
                "isPartOf": {"@id": f"{HOST}/#website"},
                "about": [
                    {"@id": f"{HOST}/#person"},
                    "Visual Reference Prompting",
                    "Burlap",
                    "Third Wall Studio",
                ],
                "description": "Using visual material as the input to creating visual material. Subject reference and style reference. Burlap at Third Wall Studio.",
            },
        ]
    ),
)

# --- contact ---
contact_body = r'''
  <main class="page">
    <p class="kicker">Write</p>
    <h1>Contact</h1>
    <p>Sarth Calhoun. Brooklyn.</p>
    <p><a href="mailto:whiddershins@gmail.com">whiddershins@gmail.com</a></p>
    <p><a href="https://x.com/noisegroove">@noisegroove</a></p>
    <p><a href="https://github.com/whiddershins">github.com/whiddershins</a></p>
  </main>
'''

page(
    path="contact/index.html",
    title="Contact — Sarth Calhoun",
    description="Contact Sarth Calhoun. mailto:whiddershins@gmail.com. X @noisegroove.",
    canonical=f"{HOST}/contact/",
    current="contact",
    body=contact_body,
    graph_html="""    <dl>
      <dt>On this site</dt>
      <dd><a href="/">Sarth Calhoun</a> · sarth.net</dd>
      <dt>Related work</dt>
      <dd><a href="https://x.com/noisegroove">@noisegroove</a> · <a href="https://github.com/whiddershins">GitHub</a></dd>
    </dl>""",
    jsonld=ld(
        [
            PERSON,
            {
                "@type": "ContactPage",
                "name": "Contact",
                "url": f"{HOST}/contact/",
                "about": {"@id": f"{HOST}/#person"},
                "isPartOf": {"@id": f"{HOST}/#website"},
            },
        ]
    ),
)

# --- 404 ---
notfound = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Not found — Sarth Calhoun</title>
  <meta name="robots" content="noindex">
  <link rel="stylesheet" href="/site.css">
</head>
<body>
  <header class="top">
    <a class="mark" href="/">Sarth</a>
  </header>
  <main class="page">
    <h1>Not found</h1>
    <p><a href="/">Sarth Calhoun</a></p>
  </main>
</body>
</html>
"""
(ROOT / "404.html").write_text(notfound)
print("wrote 404")
