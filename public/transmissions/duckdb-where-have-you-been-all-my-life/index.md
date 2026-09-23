---
title: DuckDB, where have you been all my life
description: Using Claude and DuckDB to query Burlap's JSON records of genAI calls, and running the whole append-only pipeline pattern on a laptop.
url: https://www.sarth.net/transmissions/duckdb-where-have-you-been-all-my-life/
published: 2026-09-22
facet: message
author: Sarth Calhoun
---
22 Sep 2026 · Message

# DuckDB, where have you been all my life

I've been building Burlap, a local-first macOS app for visual AI work, and it keeps JSON records of every genAI call it makes.

At some point I wanted to know stuff like how much a particular artist spent on a particular project, in a particular time frame. Normally that means loading everything into a database and setting up tables, and probably a view built for that exact question.

I didn't do any of that. I just ask Claude, and Claude uses [DuckDB](https://duckdb.org/) on the JSON files (from outside the app, for now).

I had always heard about DuckDB but never had the pleasure of using it until one of the LLMs turned me on to it. It's just so badass. Such a great combination.

Here's a simplified version of what the records look like:

```json
{"created_at":"2026-09-01T14:02:11Z","artist":"maya","project":"album-cover","model":"image-model-a","cost_usd":0.04}
{"created_at":"2026-09-01T16:30:00Z","artist":"dev","project":"music-video","model":"video-model-b","cost_usd":1.20}
```

Ask how much each artist spent on each project in September, and this is the kind of query that ends up running:

```sql
SELECT artist, project, round(sum(cost_usd), 2) AS spent
FROM 'calls/*.jsonl'
WHERE created_at >= '2026-09-01' AND created_at < '2026-10-01'
GROUP BY artist, project
ORDER BY spent DESC;
```

```
┌─────────┬─────────────┬────────┐
│ artist  │   project   │ spent  │
├─────────┼─────────────┼────────┤
│ dev     │ music-video │    3.6 │
│ maya    │ music-video │    1.2 │
│ maya    │ album-cover │   0.16 │
└─────────┴─────────────┴────────┘
```

So to be clear, I never created a table, never imported anything, never even wrote the SQL, and nobody (meaning me) ever sat down and thought "someday I'm going to want spend per artist per project per month, better make a view for that." DuckDB looked at the JSON, figured out on its own that `created_at` is a timestamp and `cost_usd` is a number, and just... answered. Which is what a database does, except there isn't one here. It's a folder of files.

And tomorrow when I want spend by model, or by day, or whatever I get curious about next, that's just a different question.

## It also runs my whole pipeline pattern

In [the external tables tutorial](/transmissions/external-tables/) I wrote about an append-only pipeline where suppliers send files, newer files contain updated versions of older records, and a window function surfaces whatever is current. On Snowflake, that took a table definition with a column for every field, a nested `SPLIT_PART` to get the date out of the file path, and a refresh every time a file landed.

In DuckDB it's this:

```sql
CREATE VIEW acme_readings AS
SELECT * FROM read_csv(
  'lake/acme_readings/*/*.csv',
  hive_partitioning = true,
  filename = true
);

CREATE VIEW acme_readings_current AS
SELECT * FROM acme_readings
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY station_id, date, time
  ORDER BY file_date DESC
) = 1;
```

With the two files from the tutorial example sitting in `file_date=2022-01-04/` and `file_date=2022-01-06/`, you get the same answer as the tutorial:

```
┌───────────────────────┬────────────┬──────────┬─────────────┐
│ station_id │    date    │   time   │ readings │
├───────────────────────┼────────────┼──────────┼─────────────┤
│ North Bridge          │ 2022-01-01 │ 19:00:00 │        2000 │
│ Harbour West           │ 2022-01-03 │ 12:00:00 │        1100 │
│ Old Mill          │ 2022-01-05 │ 12:00:00 │        1900 │
└───────────────────────┴────────────┴──────────┴─────────────┘
```

`hive_partitioning = true` reads `file_date=2022-01-04` out of the path and makes it a column (it even types it as a DATE, which, thank you). `filename = true` gives you the path itself. And the glob gets re-read every time you query, so a new file just shows up. So all that stuff about defining the table and remembering to refresh it... you just don't do it.

The same queries work against S3 if you swap the local path for an `s3://` one and [set up credentials](https://duckdb.org/docs/current/core_extensions/httpfs/s3api).

And all of this runs on a laptop, with nothing to install except DuckDB itself.
