---
title: External Tables, Partitions, CTEs, Window Functions, and Partitions
description: A five-part tutorial on building an append-only data pipeline on external tables: why append-only, external tables, window functions for the current truth, runtime type checking at the boundary, and living with the code.
url: https://www.sarth.net/transmissions/external-tables/
published: 2026-09-22
originally_written: 2024-07-13
author: Sarth Calhoun
---
Tutorial series

# External Tables, Partitions, CTEs, Window Functions, and Partitions

*Adapted from a piece I wrote in July 2024, about work I did starting in the fall of 2022.*

*This is a tutorial for building an append-only data pipeline on Snowflake external tables. It's based on a pipeline for ad delivery reports from a bunch of partners, each with their own file formats and delivery schedules. Nothing here is specific to that domain, though. If third parties send you files, and newer files contain updated versions of stuff that was in older files, and you need to serve whatever is current, this is for you.*

This pipeline uses [external tables](https://docs.snowflake.com/en/user-guide/tables-external-intro) for the primary data store instead of a typical time series (CRUD style) database. That decision affects everything else, including the fact that the word PARTITION ends up meaning two different things in the same query.

## The architecture

The pipeline consists of:

Partner A
Partner B
Partner C

- 
copy, any order

Your S3 bucket (raw)

decode

Transform + validate (io-ts)

Left

QA report

write CSV

transformed/acme_delivery/

file_date=2023-04-01/report.csv

file_date=2023-04-02/report.csv

LOAD TIME
no ordering, idempotent
QUERY TIME
ordered by file_date

read

External table
PARTITION BY (file_date)

latest per unique key

acme_delivery_current
ROW_NUMBER() … = 1

views on views

Aggregates / materialized

API

Everything above the dashed line happens at load time and doesn't care about order. The ordering happens at query time. Click a stage for what it does and which part covers it.

[](#)

In a CRUD system, the state of the database depends on the order the updates were applied, so if you ever need to rebuild it, you have to replay all your inputs from the beginning, in order. Here, the ordering doesn't happen at load time at all. It happens at query time. So you can load all your files in parallel, in any order, retry whichever ones failed, and you still get the same result.

## The series

[Why append-only](/transmissions/external-tables/why-append-only/)

- [Building on external tables](/transmissions/external-tables/building-on-external-tables/)

- [Current truth with window functions](/transmissions/external-tables/current-truth-with-window-functions/)

- [Defending the boundary](/transmissions/external-tables/defending-the-boundary/)

- [Living with the code](/transmissions/external-tables/living-with-the-code/)

Also: [SQL as the data language](/transmissions/sql-as-the-data-language/) · [Window functions, the mental model](/transmissions/window-functions/) · [DuckDB, where have you been all my life](/transmissions/duckdb-where-have-you-been-all-my-life/)
