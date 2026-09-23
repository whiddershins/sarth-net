---
title: External Tables, Partitions, CTEs, Window Functions, and Partitions
description: A five-part tutorial on building an append-only data pipeline on external tables: why append-only, external tables, window functions for the current truth, runtime type checking at the boundary, and living with the code.
url: https://www.sarth.net/transmissions/external-tables/
published: 2026-09-22
originally_written: 2024-07-13
author: Sarth Calhoun
---
Five parts

# External Tables, Partitions, CTEs, Window Functions, and Partitions

*Adapted from a piece I wrote in July 2024, about work I did starting in the fall of 2022.*

*What I think about after building a pipeline. It's based on a pipeline for reports from a bunch of suppliers, each with their own file formats and delivery schedules. Nothing here is specific to that domain, though. If third parties send you files, and newer files contain updated versions of stuff that was in older files, and you need to serve whatever is current, this is for you.*

This pipeline uses [external tables](https://docs.snowflake.com/en/user-guide/tables-external-intro) for the primary data store instead of a typical time series (CRUD style) database. That decision affects everything else, including the fact that the word PARTITION ends up meaning two different things in the same query.

## The architecture

The pipeline consists of:

Supplier A
Supplier B
Supplier C

- 
copy, any order

Your S3 bucket (raw)

decode

Transform + validate (io-ts)

Left

QA report

write CSV

transformed/acme_readings/

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

acme_readings_current
ROW_NUMBER() … = 1

views on views

Aggregates / materialized

API

Everything above the dashed line happens at load time and doesn't care about order. The ordering happens at query time. Click a stage for what it does and which part covers it.

[](#)

In a CRUD system, the state of the database depends on the order the updates were applied, so if you ever need to rebuild it, you have to replay all your inputs from the beginning, in order. Here, the ordering doesn't happen at load time at all. It happens at query time. So you can load all your files in parallel, in any order, retry whichever ones failed, and you still get the same result.

## ETL, ELT, and where the transforms happen

The usual way to explain this is the letter order. ETL means you shape the data before it lands. ELT means you land it raw and shape it inside the warehouse. This pipeline does both.

io-ts parses the supplier file and encodes the types before anything gets written. That is the T in ETL, and it happens once. Then the views do the rest. All the logic about what data is current and what is valid lives on the query side. Window functions surface the most recent version of a record, joins handle exceptions and replace bad identifiers, and when faster access is required the view gets materialized or copied into a delivery table. Some of them run well over a hundred lines of SQL. That is the T in ELT, and it happens on every query. [Defending the boundary](/transmissions/external-tables/defending-the-boundary/) is about the first one. [Current truth with window functions](/transmissions/external-tables/current-truth-with-window-functions/) is about the second.

## Schema on read

External tables are read only and schema on read. You define the table columns after the fact, and you can always alter the column definitions in the future without concern about altering data. Some of that comes free with [external tables](/transmissions/external-tables/building-on-external-tables/).

You can change your mind. Suppliers change their formats, and you get things wrong, and you can redefine a column later without reloading anything.

And the raw file is still sitting there, untouched. That is what makes the whole thing rebuildable, and it is the same property as loading in any order.

io-ts is not there to make up for schema on read. It is there because third parties will send you broken files no matter what your store does.

[DuckDB](/transmissions/duckdb-where-have-you-been-all-my-life/) will do it over a folder of files, figure out on its own that one field is a timestamp and another is a number, and answer the question.

Which means there is a version of this where you skip the io-ts step entirely. Burlap writes a generation manifest every time it makes something, and that format has changed a lot over the year and a half I have been building it. I pointed DuckDB at all of them at once, every version of the format, with no parsing step in between, and materialized the whole thing.

At scale, though, you probably don't want that.

## The series

[Why append-only](/transmissions/external-tables/why-append-only/)

- [Building on external tables](/transmissions/external-tables/building-on-external-tables/)

- [Current truth with window functions](/transmissions/external-tables/current-truth-with-window-functions/)

- [Defending the boundary](/transmissions/external-tables/defending-the-boundary/)

- [Living with the code](/transmissions/external-tables/living-with-the-code/)

Also: [SQL as the data language](/transmissions/sql-as-the-data-language/) · [Window functions, the mental model](/transmissions/window-functions/) · [DuckDB, where have you been all my life](/transmissions/duckdb-where-have-you-been-all-my-life/)
