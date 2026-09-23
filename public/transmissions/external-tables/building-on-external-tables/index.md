---
title: Building on external tables
description: Laying out object storage so file paths are partitions, and defining external tables over directories of CSVs, with Snowflake as the worked example.
url: https://www.sarth.net/transmissions/external-tables/building-on-external-tables/
published: 2026-09-22
author: Sarth Calhoun
---
Append-only pipelines · Part 2 of 5

# Building on external tables

*Adapted from a piece I wrote in July 2024, about work I did starting in the fall of 2022.*

An external table is a table definition over files that stay where they are. The files sit in object storage, S3 or GCS or a local directory, and the database reads them in place instead of ingesting them into its own storage. You get a name and a schema and you can write SQL against it, but there is no import step and no second copy of the data. Snowflake, BigQuery, Athena and Trino, Redshift Spectrum, and DuckDB all have a version of this. The examples here are Snowflake, and the [Snowflake docs on external tables](https://docs.snowflake.com/en/user-guide/tables-external-intro) are the reference; what follows is how I laid one out so that the file paths did the partitioning for me.

## Lay out S3 so the paths are the partitions

The CSVs inside directories are the external tables, where each root directory equals a table and the individual file paths represent partitions. The typical partitioning scheme relies on the path having the string `file_date=some-iso-date`, where `some-iso-date` is the partition:

```
.../transformed/acme_readings/file_date=2023-04-01/report.csv
.../transformed/acme_readings/file_date=2023-04-02/report.csv
```

Snowflake supports creating a multidimensional structure by having multiple partition columns. For example, if a supplier can send more than one file for the same date, you can add another partition column to the path to tell them apart. Overall this doesn't factor much into a typical daily feed.

## Define the external tables

External tables are read only and schema on read: you define the table columns after the fact, and you can always alter the column definitions in the future without concern about altering data.

Here is an example of the [command](https://docs.snowflake.com/en/sql-reference/sql/create-external-table) used to define an external table in Snowflake:

```sql
create or replace external table analytics.ext_acme_readings (
  site_name         VARCHAR(256) NOT NULL     as (value:c1::VARCHAR),
  station_id VARCHAR(256) NOT NULL     as (value:c2::VARCHAR),
  report_date           DATE NOT NULL             as (value:c3::DATE),
  report_time           TIME NOT NULL             as (value:c4::TIME),
  readings           INTEGER                   as (value:c5::INTEGER),
  clicks                INTEGER                   as (value:c6::INTEGER),
  spend                 NUMBER(12,2)              as (value:c7::NUMBER(12,2)),
  file_name             VARCHAR(256) NOT NULL     as (value:c8::VARCHAR),
  updated_at            TIMESTAMP_NTZ(9) NOT NULL as (value:c9::TIMESTAMP_NTZ),
  file_date             DATE NOT NULL as (
    SPLIT_PART(SPLIT_PART(metadata$filename, 'file_date=', -1), '/', 1)::date
  )
)
PARTITION BY (file_date)
WITH LOCATION = @analytics.lake_stage/acme_readings
FILE_FORMAT = (
  TYPE='CSV', SKIP_HEADER=1, EMPTY_FIELD_AS_NULL=TRUE,
  FIELD_OPTIONALLY_ENCLOSED_BY='"'
);
```

Note the `file_date` column isn't in the CSV. It's parsed out of `metadata$filename`, the file path. That's the column you `PARTITION BY`, so queries that filter or sort on `file_date` only touch the files they need.

This is an append-only system. Every time you receive a valid file, it is added to the database and the table is refreshed to include it.

These days Snowflake also supports [Apache Iceberg tables](https://docs.snowflake.com/en/user-guide/tables-iceberg), which store the data as columnar files that other engines can read too. The append-only approach, the unique keys, and the [window functions in part 3](/transmissions/external-tables/current-truth-with-window-functions/) work the same way on Iceberg tables.

[← Part 1: Why append-only](/transmissions/external-tables/why-append-only/) [Part 3: Current truth with window functions →](/transmissions/external-tables/current-truth-with-window-functions/)
