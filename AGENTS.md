# Agents

Read [`IDENTITY.md`](IDENTITY.md) and [`LEAD.md`](LEAD.md) before writing copy.

## Facts and the build

- Core identity facts (the bio, the tagline “Data Engineering for Art”, and the career roles) change only in `content/facts.json`.
- Generated files are never hand-edited. That includes `public/llms.txt`, `public/llms-full.txt`, Person JSON-LD, `public/sitemap.xml`, `content/lastmod.json`, the markdown twins, and every `<!-- build:facts -->` block. Edit the source and run the build.
- Run `python3 scripts/build.py` and `python3 scripts/build.py --check` before committing.
- When a new identity fact goes into page prose, add it to `content/facts.json` in the same commit.
- The build makes no AI or LLM calls. It has to stay deterministic.
