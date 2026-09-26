---
title: Work
description: Sarth Calhoun’s CV, newest first: Third Wall Studio, the Burlap app, writing, data engineering at Reaktor and Paramount, and the music.
url: https://www.sarth.net/work/
published: 2026-09-22
author: Sarth Calhoun
---
CV · updated September 26, 2026

# Work

What I do and have done, newest first. The things themselves are on [Transmissions](/transmissions/); the people are [Conspirators](/conspirators/).

## Now

- **[Third Wall Studio](/conspiracies/third-wall-studio/).** Founder, May 2025. We make animations with filmmakers and artists, and build new tech for ancient magic. Seven films in 2026 with Doron Lev, Jacob McCoy, Savas and Jonathan Arons, all made in Burlap.

  [thirdwallstudio.com](https://thirdwallstudio.com) · [Instagram](https://www.instagram.com/3rdwallstudio/) · [the films](/transmissions/#optical) · [Through the Brambles](/transmissions/through-the-brambles/)

- **[Burlap](/conspiracies/burlap/).** Creator. A native macOS infinite canvas for visual reference prompting, out of little genAI cubicles and free to roam. Started after Runway’s 48-hour film competition, spring 2025. Built since April 2025 by a team of four senior engineers: three of us worked together as data engineers at Reaktor, and the fourth has twenty years of iOS development.

  [burlap.app](https://burlap.app) · [Introducing Burlap](https://www.youtube.com/watch?v=CP8939UdzSo) · [The AI canvas](https://www.youtube.com/watch?v=UYN5ijezg3k)

- **Ostinato.** A new product.

- **High Shoulder.** A new company.

## Writing

- **Visual Reference Prompting.** July 2026. Using original images to push AI generation into new probability spaces.

  [Essay](/transmissions/visual-reference-prompting/) · [Video](https://www.youtube.com/watch?v=wroKqbXfx5g)

- **An append-only pipeline on external tables**, in five parts, with pages on window functions and SQL, and four essays on data work: Pandas and SQL, why Python is the default, modern Postgres, Node against Rails.

  [The series](/transmissions/external-tables/) · [everything under Lexical](/transmissions/#lexical)

- **Claude driving DuckDB over Burlap's JSON records** of every genAI call, for spend by artist, project and time frame. September 2026.

  [DuckDB, where have you been all my life](/transmissions/duckdb-where-have-you-been-all-my-life/)

## Talks

- **Reaktor Live, June 27, 2023.** “Maximizing Growth Through Accessible and Actionable Data,” with Michele Stone of Paramount, moderated by Ian Fosbery.

  [The page](/sightings/reaktor-live-2023/) · [The recording](https://www.youtube.com/watch?v=Tn0FxV9NKns)

- **“Use of Syntactic Ambiguity in Music.”** Kyma International Sound Symposium, University of California Santa Cruz, September 7, 2018.

  [KISS 2018 program](https://kiss2018.symbolicsound.com/complete-program/)

- **“Emergent Polyrhythmic Drones for Improvised Music.”** Kyma International Sound Symposium, De Montfort University, Leicester, September 9, 2016.

  [KISS 2016 program](https://kiss2016.symbolicsound.com/program/)

- **Panelist, Master Ren and Lou Reed’s Drones, following Laurie Anderson’s talk.** Live Ideas festival, New York Live Arts, April 17, 2015.

  [New York Live Arts, archived](https://web.archive.org/web/20160204033351/http://www.newyorklivearts.org/event/live_ideas_master_ren)

- **“The Making of the Universe,” with Bob Ezrin.** Carpenter Performing Arts Center, Cal State Long Beach, January 27, 2012, opening the University Art Museum’s installation of *The Creation of the Universe*.

  [Los Angeles Times](https://www.latimes.com/archives/la-xpm-2012-jan-27-la-et-lou-reed-20120127-story.html)

## Data engineering

- **Lead Data Architect at [Reaktor](https://reaktor.com), 2022 to March 2025,** embedded in Paramount’s Advanced Advertising data organization, on a fifteen-person team enabling household-level ad delivery. The team built and ran the advertising data pipeline: household ad delivery, attribution, and the warehouse behind Paramount’s convergent ad products. I designed and built the pipeline’s QA and logging system, in Node, TypeScript, io-ts and Postgres.

  [Reaktor Live, June 2023](/sightings/reaktor-live-2023/), a webinar with Michele Stone of Paramount

- **Redshift to Snowflake.** Moving the advertising pipeline off Redshift. My work included QA and reload, making sure the data that moved was the data that arrived. Schema on read and external tables in Snowflake made state idempotent and cut reload time by 90%. The team later presented that re-architecture on the main stage at Snowflake Summit 2025.

  [The append-only pattern, written up](/transmissions/external-tables/)

- **Mastercard Circle of Honor, 2025.** Paramount was recognized in the Honors for Innovation for its data-driven media measurement: cookie-less, cross-screen, measuring incremental transactions for retail and restaurant advertisers. Swathi Chandrasekaran, who leads product for Always-On Attribution, received the Award for Innovation. 13 billion impressions analyzed, $1 billion in incremental revenue measured, 3.5% average spend lift. I worked on the data side of that pipeline.

  [Mastercard](https://www.mastercard.com/global/en/business/services/mastercard-circle-of-honor/paramount-2025.html)

- **Snowflake Summit 2025**, Moscone Center, June 2–5. Swathi Chandrasekaran presented Paramount’s Always-On Attribution product; Ian Fosbery and Alexey Novikov presented the team’s data re-architecture.

- **Viasat.** An SDK that gives front-end developers one API across satellite providers, for in-flight entertainment on major airlines.

- **Uniqlo.** Real-time customer targeting for in-store offers and discounts.

- **blacktonature.org.** I built the website. The domain no longer resolves.

## Building automation and product

- **T.E.C. Systems, Long Island City, 2004 to 2022.** Building automation and control interfaces for New York facilities: Yankee Stadium, Hudson Yards, the Museum of Modern Art, the American Museum of Natural History, One World Trade Center, One Bryant Park, Memorial Sloan Kettering. I joined in 2004 as a UI designer, moved into UX engineering, and led product and development teams from 2010; Director of Product and Developer Manager by the end. Teams of three to nine, on budgets of $20k to $200k.

- **Ingather**, an integrated control system for a cannabis cultivation facility. August 2021 to March 2022. Rooms and zones, plant groups and strains, fertigation and lighting routines, dosing recipes and machines. A SvelteKit front end over a REST API, with its own server-side endpoints so the client never talks to the backend directly. Named for the archaic sense of the word: to gather in, to harvest. A T.E.C. Systems product: I led a nine-person team, six developers and two designers, as Director of Product, and it ran a 120,000 square foot indoor agriculture facility.

  [Ingather](/conspiracies/ingather/) · [Playable demo](https://ingather-demo.marshy-runner.workers.dev)

- **The T.E.C. front-end framework.** I wrote the JavaScript framework behind all of the company’s Honeywell control interfaces. Designers configure it in their own tools, and it ran stably for more than seven years.

- **UItracker.** A job-progress tracker for the company’s installations, product design and management with a team of three. It cut deployment errors from 3% to 0.1%.

- **Re# Digital, Brooklyn, 2014 to 2017.** Front-end contract work on the MEAN stack, for clients from Nike to the Prospect Park Alliance.

- **Webmogul, 2001 to 2005.** Co-founder of an early search and internet marketing firm in New York, with a white-hat SEO, pay-per-click and content practice. Number19’s first record was paid for with mp3.com royalties from that kind of marketing.

## Instruments and synthesis

- **About five kinds of synthesis,** invented. SeqOSC, a relative of AM synthesis, was built in Kyma.

- **Contraptions.** Small software machines: FM / 6, a six-operator synthesizer, 2026; Image Compare Workbench, 2026; Soundscape One, 2021.

  [Contraptions](/contraptions/) · [contraptions.bookofsarth.com](https://contraptions.bookofsarth.com)

- **Devices.** The Kyma, the Haken Continuum Fingerboard, Ableton Live, Runway, and what they were used on.

  [Devices](/devices/)

- **Continuum against the Linnstrument**, round one. March 2015.

  [Watch](https://www.youtube.com/watch?v=8MqhRQI84Os)

## Music

- **Drone and noise shows,** many of them, including the Cathedral of St. John the Divine. Listed on [Sightings](/sightings/).

- **Singles as Sarth,** 2020 to 2025, on Noise | Groove.

  [Singles](/transmissions/singles/)

- **Beautiful Tornado,** the podcast with [Dom Bouffard](/conspirators/dominic-bouffard/). 2020 to 2021.

  [Beautiful Tornado](/transmissions/beautiful-tornado/)

- **A score for a film directed by [Joe Kelly](/conspirators/joe-kelly/).** The main melody of “Softly Questioning,” for [*Poughkeepsie*](/conspiracies/poughkeepsie/).

- **Burned House Horizon.**

- **A video with [Moldover](/conspirators/moldover/).**

- **I Just Believe in Christmas.** December 2015. It started as an argument with my neighbors about squirrels in the attic. Sung by [Michael Patrick Flanagan Smith](/conspirators/michael-patrick-flanagan-smith/), words with Jesse Schoen, Virginia Piazza, and [Doron Lev](/conspirators/doron-lev/).

  [The song](/conspiracies/i-just-believe-in-christmas/) · [Bandcamp](https://sarth.bandcamp.com/track/i-just-believe-in-christmas)

- **Reflections, Vol. 1 (A Noise Akin to a Flight of Deranged Swallows in Combat).** November 2015. Improvised duets. The name came from [Scott Hampton](/conspirators/scott-hampton/), who took it from a review of a Metal Machine Trio show.

  [The record](/conspiracies/reflections-vol-1/) · [Apple Music](https://music.apple.com/us/album/reflections-vol-1-a-noise-akin-to-a-flight/1061852160)

- **Introspections.** 2015. Improvised drone duets on Continuum and Kyma, with [Jacob McCoy](/conspirators/jacob-mccoy/), [Sxip Shirey](/conspirators/sxip-shirey/) and others.

  [Introspections](/transmissions/introspections/)

- **Solsbury Hill and Peggy Sue.** Lou Reed’s recordings for *And I’ll Scratch Yours*, 2013, which I produced and played electronics on, and *Rave On Buddy Holly*, 2011, on which I played bass.

  [Solsbury Hill](/transmissions/solsbury-hill/) · [Peggy Sue](/transmissions/peggy-sue/)

- **The Gralbum Collective.** Founded 2012; the (gr)album app launched April 2014 with five titles. I designed the product and led developers who came from video games, and wrote the rules and algorithms that guide the reader’s path through the visuals in time with the music. Every title was made with its artist.

  [The Gralbum Collective](/conspiracies/gralbum-collective/)

- **The Book of Sarth.** 2012 to 2013. A graphic novel and concept album as one iPad app, two and a half years in the making, and my first full-length solo release.

  [Book of Sarth](/conspiracies/book-of-sarth/) · [bookofsarth.com](https://bookofsarth.com) · [The Verge](https://www.theverge.com/2013/1/3/3828314/the-book-of-sarth-ipad-app-graphic-novel-concept-album)

- **Lulu.** Score composed with Lou Reed for [Robert Wilson](/conspirators/robert-wilson/)'s Berliner Ensemble production, premiered April 2011; rehearsals directed in Berlin; then the Lou Reed and [Metallica](/conspirators/metallica/) album, and its first live performances with Metallica in November 2011.

  [Lulu](/conspiracies/lulu/) · [Junior Dad](/conspiracies/junior-dad/)

- **Lou Reed’s touring band**, 2008 to 2011, on Continuum and Kyma, and **Yellow Pony** with Lou Reed and Laurie Anderson, 2009.

  [The song band](/conspiracies/lou-reed-song-band/) · [Yellow Pony](/conspiracies/yellow-pony/) · [Live at Lollapalooza 2009](/transmissions/lou-reed-live-at-lollapalooza-2009/)

- **Power and Serenity**, with Lou Reed. Six pieces of tai chi meditation music, composed and performed together over four years for Master Ren Guangyi’s DVD, on sale from July 2010. The first thing we worked on together; the same music ran under *Hidden Books, Hidden Stories* at the New York Photo Festival, May 2010.

  [Power and Serenity](/conspiracies/power-and-serenity/) · [Hidden Books, Hidden Stories](/conspiracies/hidden-books-hidden-stories/)

- **Metal Machine Trio**, with Lou Reed and Ulrich Krieger. From the REDCAT premiere in October 2008 through São Paulo in 2010, on Continuum and live processing. *The Creation of the Universe*, 2009.

  [Metal Machine Trio](/conspiracies/metal-machine-trio/) · [Sightings](/sightings/)

- **Lucibel Crater.** My band, founded 2005, with Leah Coloff and Paul Chuffo. *Miracles*, 2007; *The Family Album*, 2008.

  [Lucibel Crater](/conspiracies/lucibel-crater/) · [Masticate](https://www.youtube.com/watch?v=nwfygEI3Mzs) · [Rumors](/rumors/)

- **Number19.** 1999 to 2005, with Tony Diodore, Leah Coloff and Mark Righter, on bass and a [Yamaha EX5](/devices/yamaha-ex5/). *Suspension*, 2001, paid for by mp3.com downloads.

  [Number19](/conspiracies/number19/)
