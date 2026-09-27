# sarth.net


**Identity first:** read [`IDENTITY.md`](IDENTITY.md) and [`LEAD.md`](LEAD.md) before writing or rearranging any page copy. Wrong silhouette = musician stub; right = data engineer / artist / musician / AI (Lanier–Rubin shaped).

## How to use

```bash
npm install            # also points git at .githooks (pre-commit build)
npx wrangler dev
```

Preview at `http://127.0.0.1:8787`. Pages are static HTML in `public/`.

**The HTML is the source. Everything else is derived.** `scripts/build.py` reads
every `public/**/index.html` and writes the markdown twins, `llms.txt`,
`llms-full.txt`, `sitemap.xml`, `feed.xml`, the citations layer, and `REPORT.md`.
The pre-commit hook runs it and stages what changed; the GitHub Action runs
`--check` and fails the push if anything is stale, a link is dead, a page is
an orphan, or the career facts disagree. Sitemap `<lastmod>` and JSON-LD
`dateModified` use the last commit that changed the page’s hand-written HTML.
Generated regions (Person career fields, `dateModified`, and the build blocks)
do not move the date. `content/lastmod.json` holds those dates so a shallow
checkout, which cannot see per-file history, still checks cleanly.

```bash
python3 scripts/build.py          # regenerate
python3 scripts/build.py --check  # what CI runs
```

Hand-written sources outside `public/`: `content/facts.json` (the locked lead,
the line “Data Engineering for Art”, and the dated career roles), `content/llms.txt` and
`content/llms-full.txt` (the preambles; `{{PAGES}}` and the `<!-- build:facts -->`
block are filled in) and
`content/holes/*.md`, one file per `<div class="hole">` on a page, for Sarth's
own paragraph. An empty file leaves the bracketed prompt on the page and lists
it in `REPORT.md`, which also lists every story page still without the
alternating 2/1 and 1/2 bands (a page opts out with a `<!-- bands: none. reason -->`
comment; the check fails a flat page without one). `npm run dev:holes` serves the site at `http://127.0.0.1:8788`
with every hole editable in place: click, type, click away, and the file is
written and the build re-run. The old page generator is retired under `scripts/legacy/`. Old Squarespace and WordPress addresses are 301s in `public/_redirects`, except the five inbound-linked ones at its top, which serve their real page with a 200 rewrite. `src/index.js` runs before the assets. It 301s every other host, and any http request, to the same path and query on `https://www.sarth.net`, then passes a canonical request to the asset binding, so those `_redirects` rules, trailing slashes, and the 404 page still apply. `workers_dev` and `preview_urls` are off. A page view counts as a Worker request. `node --test scripts/canonical.test.mjs` checks the redirect decision.

Publish by connecting Workers Builds on the `sarth-net` Worker in Sarth@sarth.net's Account to this GitHub repo, production branch `main`, deploy command `npx wrangler deploy`. Cloudflare runs that on each push. A GitHub Action is not the publish path. `account_id` in `wrangler.jsonc` is that same account, so a manual `npx wrangler deploy --profile sarth-net` cannot land on Marshy Runner.

Canonical host: `https://www.sarth.net`. Both `www.sarth.net` and `sarth.net` stay attached to the `sarth-net` deployment on Sarth@sarth.net's Account, so the Worker can see the bare name and redirect it. Pages declare the `www` address in their canonical tag. Mail records stay on Fastmail. The old Squarespace site remains at `https://sarth-stuff.squarespace.com`. The older Worker on Marshy Runner, `https://sarth-net.marshy-runner.workers.dev`, is a separate deployment and is not changed by this repo.

## Cloudflare accounts

Two logins on this machine, same email `sarth@sarth.net`:

| Login | What it can reach |
|---|---|
| `default` (`wrangler whoami`) | Marshy Runner only, `a750b82b27285ba96770503fbb636e64`. The preview Worker `sarth-net` is here, along with `bookofsarth.com` and `contraptions`. |
| profile `sarth-net` | Both accounts. The second is Sarth@sarth.net's Account, `cc4dcff1642e97ee3283755e696a3c40`, which holds the `sarth.net` zone (`elisa` / `miles`) and `highshoulder.com`. |

The `sarth-net` profile refuses to guess an account. Name one:

```bash
# the zone that serves sarth.net
CLOUDFLARE_ACCOUNT_ID=cc4dcff1642e97ee3283755e696a3c40 npx wrangler <cmd> --profile sarth-net

# the preview Worker
CLOUDFLARE_ACCOUNT_ID=a750b82b27285ba96770503fbb636e64 npx wrangler <cmd> --profile sarth-net
```

`bookofsarth` and `contraptions` pin Marshy Runner with `account_id` in their Wrangler config. `highshoulder` pins the other account. This repo pins Sarth@sarth.net's Account. `www.sarth.net` and `sarth.net` are attached to that Worker (`https://sarth-net.sarth.workers.dev`). A second, older copy remains on Marshy Runner at `https://sarth-net.marshy-runner.workers.dev`. Do not connect Builds to that copy. A local deploy uses the same pin: `npx wrangler deploy --profile sarth-net`. The default login cannot see the pinned account, so it refuses instead of publishing the preview.

## What it is

The public home for Sarth Calhoun’s current work and history. Vanilla HTML/CSS, served as static files. Identity, Conspiracies, Conspirators, Sightings, Appearances, Devices, the Visual Reference Prompting essay, contact.

The homepage leads with Third Wall Studio and Burlap. Lineage is texture after current work. No Squarespace. No Svelte.

## Why

Wikipedia and search freeze Sarth Calhoun as a 2008–2012 experimental musician. This site is a present-tense record of current work and the real credits. Lineage is texture, not the lead.

Sarth made Metal Machine Trio with Lou Reed and Ulrich Krieger. He later wrote the original *Lulu* score with Reed for Robert Wilson’s Berliner Ensemble production (12 Apr 2011); the Metallica album grew from those recordings. Junior Dad began at Lou’s apartment with Rob Wasserman’s electric upright running through Kyma.

## Context

- **partOf** — sarth.net, domain since 30 Nov 1997
- **relatedTo** — [bookofsarth.com](https://bookofsarth.com), [contraptions.bookofsarth.com](https://contraptions.bookofsarth.com), [burlap.app](https://burlap.app), [thirdwallstudio.com](https://thirdwallstudio.com)
- **sameAs** — [Wikidata Q7424654](https://www.wikidata.org/wiki/Q7424654), [x.com/noisegroove](https://x.com/noisegroove), [github.com/whiddershins](https://github.com/whiddershins)
- **source** — this repo. Cloudflare Workers are a projection.

All rights reserved.
