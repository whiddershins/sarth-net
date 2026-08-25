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
    "jobTitle": "Musician, software, artist",
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
      <p class="lede">Brooklyn. Musician, software, artist. Founded <a href="https://thirdwallstudio.com">Third Wall Studio</a> (May 2025) and The (Gr)album Collective (<a href="https://bookofsarth.com">Book of Sarth</a>, 2012). <a href="/transmissions/visual-reference-prompting/">Visual Reference Prompting</a> is a core practice. <a href="https://burlap.app">Burlap</a> is the flagship machine. Used at Third Wall Studio.</p>
      <p class="links">
        <a href="https://burlap.app/download">Download Burlap</a>
        <a href="https://contraptions.bookofsarth.com">Contraptions</a>
        <a href="https://contraptions.bookofsarth.com/image-compare-workbench">Image Compare Workbench</a>
        <a href="https://x.com/noisegroove">@noisegroove</a>
        <a href="https://github.com/whiddershins">GitHub</a>
        <a href="https://www.wikidata.org/wiki/Q7424654">Wikidata Q7424654</a>
      </p>
    </section>

    <section>
      <p class="kicker">Now</p>
      <h2>Current work</h2>
      <p><a href="https://burlap.app">Burlap</a> is a native macOS infinite canvas for visual reference prompting: original images used to push generation into new probability spaces. A year of life and serious money. The main machine, used at <a href="https://thirdwallstudio.com">Third Wall Studio</a>. Adult animation as drama. <a href="https://burlap.app/download">Download</a>.</p>
      <p><a href="https://contraptions.bookofsarth.com">Contraptions</a> is the shelf of things built. <a href="https://contraptions.bookofsarth.com/image-compare-workbench">Image Compare Workbench</a> lives there.</p>
      <p>Current transmission: <a href="/transmissions/visual-reference-prompting/">Visual Reference Prompting</a>. Short explanation: <a href="https://www.youtube.com/watch?v=wroKqbXfx5g">Frogs and Goblins</a>.</p>
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
      <h2>Who</h2>
      <p>Sarth Calhoun began playing music and writing lyrics at age six. In his teens he stopped buying comic books to save up for his first bass. He played in rock bands around New York while getting acquainted with the cyber world in a time he calls the grey era, when web pages were not yet marked up with color.</p>
      <p>He met cellist and songwriter <a href="https://www.leahcoloff.com">Leah Coloff</a>, who convinced him to combine computers with music. Number19 — Calhoun, Coloff, Tony Diodore, Marcus Righter — funded its first record from mp3.com in 2001. <a href="https://open.spotify.com/album/0EBi9RJO4j2cGeL0CPtYW5">Suspension</a> followed. In 2005 he founded Lucibel Crater with Coloff and drummer Paul Chuffo: keys, bass, loops, Kyma, Continuum. Urban Magazine: “Something like Bjork and maybe like White Stripes; But the truth is that their sound is unique and not easy to label, to the extent that even Lou Reed has fallen in love with it.” <a href="https://open.spotify.com/album/5GWIntdZRNl8zc9rAsIrKD">The Family Album</a> (2008) includes Threadbare Funeral, guitar by Lou Reed.</p>
      <p>He is a beta tester for <a href="https://kyma.symbolicsound.com/">Symbolic Sound Kyma</a> and an Ableton Live endorser. SeqOSC, a relative of AM synthesis, was built in Kyma. The instrument on the table is the <a href="https://www.hakenaudio.com/">Haken Continuum Fingerboard</a>. After watching Lollapalooza video of the Continuum in front of fifty thousand people, Lippold Haken said: “I Lost sleep. I even dreamt about it last night. It was one of those thousands-of-people-watching nightmares.”</p>
      <p>He met Lou Reed through Tai Chi. Meditation music came first — later <a href="https://loureed.com/power/">Power and Serenity</a>. Then the rock band, processing instruments onstage. Then the trio.</p>
    </section>

    <section>
      <h2>Metal Machine Trio</h2>
      <figure>
        <img src="/images/mm3-nyc.jpg" width="1000" height="411" alt="Metal Machine Trio onstage in New York: Sarth Calhoun, Lou Reed, Ulrich Krieger.">
        <figcaption>Metal Machine Trio, New York. Equal collaboration: Sarth Calhoun, Lou Reed, Ulrich Krieger.</figcaption>
      </figure>
      <p>Metal Machine Trio is an equal collaboration. Sarth Calhoun, Lou Reed, Ulrich Krieger. Continuum, live Kyma processing, guitar, tenor sax. Deep noise.</p>
      <blockquote class="pull">In 2008 Lou called me up and told me he was doing a free improvised noise gig at The REDCAT in LA with saxophonist and composer Ulrich Krieger. Ulrich had made a real impression on Lou by arranging Metal Machine Music for orchestral ensemble … a rare and some might say unnatural feat that should be impossible. I had done a tour with Lou’s rock band, processing and sampling the various instruments on stage, and we had talked talked about doing some duet shows performing the meditation music we’d been working on. That stuff was drones and melodies combined with pure noise, so this seemed only natural. Ulrich had billed us as “Unclassified” because obviously the group had no name yet.</blockquote>
      <p>The REDCAT nights sold out. They added a second set. Recorded with a matched pair of Schoeps and a stereo Royer, no direct lines, released as the double live album <a href="https://www.discogs.com/release/1583151-Lou-Reed-s-Metal-Machine-Trio-The-Creation-Of-The-Universe"><em>The Creation of the Universe</em></a> — those two nights, 2–3 Oct 2008. Then Europe, Brazil, Sydney Opera House. <a href="/appearances/">Appearances</a>.</p>
    </section>

    <section>
      <h2>Lulu</h2>
      <p>Sarth composed the original <em>Lulu</em> score with Lou Reed for Robert Wilson’s Berliner Ensemble production of Frank Wedekind. Premiere 12 April 2011, Theater am Schiffbauerdamm, Berlin. Kyma processing, Continuum/Kyma playing, dual Continuum improvisations with a live string section. He directed rehearsals of that score in Berlin. Symbolic Sound, April 2011: “Composer/performer Sarth Calhoun is directing rehearsals of Lou Reed’s music.”</p>
      <blockquote class="pull">I got a call from Lou one day to go over to his house and make some “interstitial” music for a theater production. Robert Wilson was staging “Lulu” with the Berliner Ensemble. This turned into co-writing 8 more songs with Lou Reed. Hells yeah. After I got back from Berlin, we took the project to San Francisco and recorded it with Metallica. What a blast. They completely reinterpreted all the stuff, of course. They were awesome. Of course.</blockquote>
      <p>The <a href="https://open.spotify.com/album/3FgLMfp5o2h2rAny7S6h57">Lou Reed &amp; Metallica album</a> grew from those tapes. He composed and performed on it. Wilson first. Metallica second. All songs on the record are based on songs originally written for the play.</p>
      <p>Junior Dad, the 19-minute outro, grew from the first session at Lou’s apartment: Rob Wasserman bowing electric upright, Sarth processing through Kyma. They recorded it. That recording is the basis of the piece. Source: Sarth’s letter, 30 June 2016, the day after Wasserman died. <a href="https://www.youtube.com/watch?v=iJ_VBkdsS0U">Junior Dad</a>.</p>
    </section>

    <section>
      <h2>Yellow Pony, Lucibel, Book of Sarth</h2>
      <p>In 2009, two short tours with Lou Reed and Laurie Anderson, billed <em>The Yellow Pony and Other Songs and Stories</em>. Continuum and live resampling of their voices, center stage.</p>
      <p>Lucibel Crater is the rock/electronic trio: Leah Coloff, Paul Chuffo, Sarth Calhoun. Live looping, cubist grooves, noise that falls into a song.</p>
      <p>The Book of Sarth is the first gralbum: an 8-song album inside an 80-page animated graphic novel, with a 30-minute DirectedView. Andrew Beck, Elik Smith, Leah Coloff, Jacob McCoy. The art object lives at <a href="https://bookofsarth.com">bookofsarth.com</a>. He is the continuum fingerboarding champion of the world.</p>
      <figure>
        <a href="https://bookofsarth.com"><img src="/images/bos-cover.jpg" width="1000" height="523" alt="Book of Sarth cover, illuminated S on weathered ornament."></a>
        <figcaption>Book of Sarth. The object is at bookofsarth.com.</figcaption>
      </figure>
    </section>

    <section>
      <h2>People</h2>
      <p><strong>Leah Coloff</strong> is a Brooklyn cellist, singer, songwriter. First album <em>Dark Sweet Heart</em>. Solo cello and voice. Cello on records for Ziggy Marley, Rufus Wainwright, Dr. John, Nancy Sinatra, Joel Thome, David Bowie. In Lucibel she is beat poet, upright-bass cello, Hendrix cello, soul singing, feedback.</p>
      <p><strong>Paul Chuffo</strong> is the original drummer for Gutbucket. In Lucibel he is the feet.</p>
      <p><strong>Tony Diodore</strong> formed Number19 with Sarth, Leah Coloff, and Marcus Righter in 1999. After <em>Suspension</em>, Puracane, BM Linx, then Lou Reed’s band again with Sarth.</p>
      <p>Ulrich Krieger’s page is the Metal Machine Trio essay above. Rob Wasserman: Solo, Duo, Trio; Ned Steinberger electric upright; first session at Lou’s apartment; Junior Dad.</p>
    </section>

    <section>
      <h2>Catalog</h2>
      <p>One current transmission on this page. The rest of the music:</p>
      <ul>
        <li>Sarth — <a href="https://open.spotify.com/artist/6uUtOazhiVXfNU8KAglFv9">Spotify</a></li>
        <li>Lucibel Crater, <em>The Family Album</em> — <a href="https://open.spotify.com/artist/1uzV1v4GhWST5v9xLbGJFV">Spotify</a></li>
        <li>Number 19, <em>Suspension</em> — <a href="https://open.spotify.com/artist/3gcviraWowfAK8g1jMIvoO">Spotify</a></li>
        <li><em>Lulu</em>, Lou Reed &amp; Metallica — <a href="https://open.spotify.com/album/3FgLMfp5o2h2rAny7S6h57">Spotify</a>. He composed and performed. Spotify does not list him as album artist.</li>
      </ul>
    </section>
  </main>
'''

home_graph = """    <dl>
      <dt>partOf</dt>
      <dd>sarth.net — citable identity for Sarth Calhoun</dd>
      <dt>relatedTo</dt>
      <dd><a href="https://burlap.app">Burlap</a> · <a href="https://thirdwallstudio.com">Third Wall Studio</a> · <a href="https://contraptions.bookofsarth.com">Contraptions</a> · <a href="https://bookofsarth.com">Book of Sarth</a></dd>
      <dt>collaborator</dt>
      <dd>Lou Reed · Ulrich Krieger · Leah Coloff · Paul Chuffo · Tony Diodore · Rob Wasserman · Laurie Anderson · Robert Wilson · Andrew Beck · Elik Smith · Jacob McCoy</dd>
      <dt>builtWith</dt>
      <dd><a href="/devices/">Kyma</a> · <a href="/devices/">Haken Continuum</a> · Ableton Live · Burlap</dd>
      <dt>priorArt</dt>
      <dd>Metal Machine Trio, REDCAT 2–3 Oct 2008 · Wilson <em>Lulu</em>, Berliner Ensemble, 12 Apr 2011 · Junior Dad from Wasserman/Kyma at Lou’s apartment</dd>
      <dt>source</dt>
      <dd><a href="https://github.com/whiddershins">github.com/whiddershins</a></dd>
    </dl>"""

page(
    path="index.html",
    title="Sarth Calhoun",
    description="Sarth Calhoun. Brooklyn. Musician, software, artist. Third Wall Studio, Burlap, Visual Reference Prompting. Metal Machine Trio with Lou Reed and Ulrich Krieger. Original Lulu score with Reed for Robert Wilson.",
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
                "description": "Citable identity for Sarth Calhoun. Machine · Dream · Message, and the lineage.",
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

# --- sightings ---
sight_body = r'''
  <main class="page">
    <p class="kicker">Press</p>
    <h1>Sightings</h1>
    <p>Sarth Calhoun. Quotes are verbatim. Metal Machine Trio is an equal collaboration with Lou Reed and Ulrich Krieger. The original <em>Lulu</em> score was composed with Reed for Robert Wilson; the Metallica album grew from those tapes. Press often files him under electronics. The work is composition.</p>

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
      <dt>partOf</dt>
      <dd><a href="/">Sarth Calhoun</a> · sarth.net</dd>
      <dt>relatedTo</dt>
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
    <p>Sarth Calhoun. Confirmed dates in the lead. No invented nights. Album <em>The Creation of the Universe</em> is REDCAT, 2–3 Oct 2008. The ambisonic installation tape is Gramercy, 24 Apr 2009. Different nights.</p>

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
      <p>No further MM3 concerts after São Paulo in the public record. Wikipedia’s 2008–2013 span tracks the project until Reed’s death, not extra gigs.</p>
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
      <dt>partOf</dt>
      <dd><a href="/">Sarth Calhoun</a> · sarth.net</dd>
      <dt>relatedTo</dt>
      <dd><a href="/sightings/">Sightings</a> · <a href="/devices/">Devices</a></dd>
      <dt>collaborator</dt>
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
      <dt>partOf</dt>
      <dd><a href="/">Sarth Calhoun</a> · sarth.net</dd>
      <dt>relatedTo</dt>
      <dd><a href="https://contraptions.bookofsarth.com">Contraptions</a> (software shelf, different page) · <a href="/transmissions/visual-reference-prompting/">Visual Reference Prompting</a></dd>
      <dt>builtWith</dt>
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
    <p>Sarth Calhoun. Words from the practice.</p>
    <ul class="press">
      <li>
        <h2><a href="/transmissions/visual-reference-prompting/">Visual Reference Prompting</a></h2>
        <p>31 Jul 2026. Subject reference and style reference. Original images as the input to visual material. Burlap, Third Wall Studio. Frogs and Goblins.</p>
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
      <dt>partOf</dt>
      <dd><a href="/">Sarth Calhoun</a> · sarth.net</dd>
      <dt>relatedTo</dt>
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
      <dt>partOf</dt>
      <dd><a href="/transmissions/">Transmissions</a> · <a href="/">Sarth Calhoun</a></dd>
      <dt>relatedTo</dt>
      <dd><a href="https://burlap.app">Burlap</a> · <a href="https://thirdwallstudio.com">Third Wall Studio</a> · <a href="https://contraptions.bookofsarth.com">Contraptions</a></dd>
      <dt>builtWith</dt>
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
      <dt>partOf</dt>
      <dd><a href="/">Sarth Calhoun</a> · sarth.net</dd>
      <dt>relatedTo</dt>
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

