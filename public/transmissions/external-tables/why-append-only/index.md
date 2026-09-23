---
title: Why append-only
description: Why you would keep every file forever instead of upserting: an append-only store makes loads idempotent, order-independent, and parallelizable.
url: https://www.sarth.net/transmissions/external-tables/why-append-only/
published: 2026-09-22
originally_written: 2024-07-13
author: Sarth Calhoun
---
Append-only pipelines · Part 1 of 5

# Why append-only

*Adapted from a piece I wrote in July 2024, about work I did starting in the fall of 2022.*

This pipeline uses [external tables](https://docs.snowflake.com/en/user-guide/tables-external-intro) for the primary data store instead of a typical time series (CRUD style) database. That decision affects everything else, including the fact that the word PARTITION ends up meaning two different things in the same query.

## Why you'd build it this way

Suppliers send files on some cadence, but typically the files contain data across a time window that is larger than the cadence you receive them on. For example, you might receive a file three times a week that has data from a two week time period. This gets you numbers as soon as possible, and then you receive updated numbers that are more accurate in subsequent files. So the same record shows up in many files, and the most recent version is the one that counts.

The CRUD way to handle this is to upsert: parse each file, match rows on a key, and update in place. If you don't do that, and instead keep every file and never change anything, you keep every version of everything, and all the logic about which version is current lives in queries. If that logic needs to change, you change the view, not the data.

But the huge advantage is that loading becomes independent and parallelizable. In a CRUD system, the state of the database depends on the order the updates were applied, so if you ever need to rebuild it, you have to replay all your inputs from the beginning, in order. Here, the ordering doesn't happen at load time at all. It happens at query time, for example it might be by `received_at`. Loads are idempotent, so you can load all your files in parallel, in any order, retry whichever ones failed, and you still get the same result.

The cost is that the queries do more work.

## The pipeline

The pipeline consists of:

```
Supplier S3 bucket
→ Extract (copy) →
Your S3 bucket
→ Load / Transform (io-ts) →
Snowflake external tables (CSV in S3)
→ Views →
Aggregate / materialized tables
→ API
```

The jobs are initiated by DAGs that run once per day. There are different jobs per supplier, per file/report type, and for other things including QA.

The extract / load / transform stages first copy the files from the supplier S3 buckets to your S3 bucket. They then parse the files, use io-ts to check and encode the data types ([part 4](/transmissions/external-tables/defending-the-boundary/)), and save the output CSVs into the transformed directories.

[← Series overview](/transmissions/external-tables/) [Part 2: Building on external tables →](/transmissions/external-tables/building-on-external-tables/)
