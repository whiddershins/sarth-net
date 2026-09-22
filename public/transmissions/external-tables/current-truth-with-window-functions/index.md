---
title: Current truth with window functions
description: Unique keys, ROW_NUMBER() OVER (PARTITION BY ... ORDER BY file_date DESC) = 1, and views: surfacing the current version of every record from an append-only store.
url: https://www.sarth.net/transmissions/external-tables/current-truth-with-window-functions/
published: 2026-09-22
originally_written: 2024-07-13
author: Sarth Calhoun
---
Append-only pipelines · Part 3 of 5

# Current truth with window functions

*Adapted from a piece I wrote in July 2024, about work I did starting in the fall of 2022.*

## The unique key

Because this is an append-only system, all logic about what data is current and valid is performed on the query side. Which raises the question: how do you know data is an update rather than a new row?

For this, each file format has a unique key, which is a combination of columns, for example `audience_segment_name`, `date`, and `time`. If an entry matches existing data on those columns, it should replace the old data.

Consider the following example. Let's say all you have in a certain table is this:

audience_segment_name
date
time
impressions

Movie Lovers
2022-01-01
19:00
2000

Sports Fans
2022-01-03
12:00
1000

Suppose you receive an updated file with the following data:

audience_segment_name
date
time
impressions

Sports Fans
2022-01-03
12:00
1100

Cat Fanatics
2022-01-05
12:00
1900

Since the Sports Fans entry in the new file matches on the unique key `(audience_segment_name, date, time)`, the new file should be considered the source of truth, and your current data is:

audience_segment_name
date
time
impressions

Movie Lovers
2022-01-01
19:00
2000

Sports Fans
2022-01-03
12:00
1100

Cat Fanatics
2022-01-05
12:00
1900

If you aren't using a CRUD model that replaces that entry with updated data, but instead keep every version of everything in the database, how do you surface only the most current information?

## Window functions

For this you use window functions. (If window functions are new to you, [this page](/transmissions/window-functions/) has the mental model.) They take the form of:

```
ROW_NUMBER() OVER (PARTITION BY <...unique keys...> ORDER BY file_date DESC) = 1
```

Here is an example of that for the external table from [part 2](/transmissions/external-tables/building-on-external-tables/):

```
SELECT * FROM analytics.ext_acme_delivery
QUALIFY ROW_NUMBER() OVER (
PARTITION BY
campaign_name,
audience_segment_name,
report_date,
report_time
ORDER BY file_date DESC
) = 1
```

[`QUALIFY`](https://docs.snowflake.com/en/sql-reference/constructs/qualify) filters on the result of a window function, the way WHERE filters on columns.

`PARTITION BY` creates a subset of rows the window function acts upon. Each PARTITION in this context is treated as its own thing.

[`ROW_NUMBER()`](https://docs.snowflake.com/en/sql-reference/functions/row_number) will assign a unique number starting from 1 to each row in the PARTITION.

The rows are numbered by `file_date DESC`, in other words, the row with the highest value for `file_date` gets a row number of 1, the next 2, and so forth.

And then `= 1` means only return the entry with a row number of 1.

This only works if the column you order by can't tie within a partition. If two rows can have the same `file_date`, `ROW_NUMBER()` will pick one of them arbitrarily, so either make sure the value is unique or add more columns to the ORDER BY to break the tie.

In other words, take all the data and create subsets based on the unique key, then return the most recent from each subset.

One thing worth noting here is the overloading of the term PARTITION in this pipeline. When using window functions, PARTITION is the subset of data that will be compared (because in this case, these share a unique key and are different versions of the same entry). For these purposes you return one, most recent, result from each PARTITION.

When setting up external tables, PARTITION is a subset of the data that Snowflake uses for optimization, and corresponds to a file path, which in this case is generated based on the file date.

So in the above query, you select all the data in the external table for a certain partner's data, you PARTITION it by the unique key, and then you ORDER BY `file_date`... which just so happens to be the external table PARTITION.

You order the contents of the PARTITION by PARTITION.

## Views

The window function logic, plus any other cleanup, goes in views, such as `acme_delivery_current` or `weekly_by_partner`. In the view definitions you use joins to handle exceptions, such as overriding bad identifiers, and window functions to surface the most recent version of data. Downstream code consumes the views.

When faster access is required, the view can be materialized or the data copied into regular tables.

It helps to pick a naming convention and stick to it. For example:

- **External table**: `ext_<feed>`, partitioned by file date, containing all the files loaded to date.

- **Current view**: `<feed>_current`, presenting the most current data and filtering out problematic stuff.

- **Aggregate views and tables**: named for what they aggregate, like `weekly_by_partner`.

[← Part 2: Building on external tables](/transmissions/external-tables/building-on-external-tables/) [Part 4: Defending the boundary →](/transmissions/external-tables/defending-the-boundary/)
