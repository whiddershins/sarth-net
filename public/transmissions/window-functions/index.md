---
title: Window functions, the mental model
description: The mental model for SQL window functions: compare them to aggregates, PARTITION BY vs GROUP BY, ROW_NUMBER vs RANK, and why the window grows.
url: https://www.sarth.net/transmissions/window-functions/
published: 2026-09-22
author: Sarth Calhoun
---
SQL

# Window functions, the mental model

*Adapted from a piece I wrote in July 2024, about work I did starting in the fall of 2022.*

In addition to the [official Postgres docs for window functions](https://www.postgresql.org/docs/current/tutorial-window.html), there are some examples in the [Snowflake documentation](https://docs.snowflake.com/en/user-guide/functions-window-using) that might help you have an "aha!" moment. I find that the easiest way to grok window functions is to first compare them to aggregate functions such as `SUM()` or `COUNT()`. Where SUM or COUNT will return a single row, or a row for each GROUP BY, the window function will return all the rows, but they can contain a column with a value that is the result of calculations performed across some or all of the rows (within a partition, which again, is just a subset of rows). Here are a couple of things worth clearing up:

- GROUP BY in an aggregate function is analogous to PARTITION BY in a window function. Each group in the aggregate function would return one row that has the result of the aggregate; each partition of the window function is treated separately when having the function applied across it, but then returns the same number of rows as in the original (partitioned) data set.
- This is further obscured by the fact that this pipeline uses `RANK()` or `ROW_NUMBER() <...stuff...>` followed by `= 1` in many of the views, which means that the window function, as used here, usually only returns 1 row. Because that `= 1` just means return the first of the result rows.
- Speaking of which: `ROW_NUMBER() = 1` will always return only 1 result, but `RANK() = 1` can return more than one result if two rows have the same value.
- The word window can be confusing at first, because in computer science usually a window is a fixed size number of values (like audio samples). However, the default behavior for some window functions is to have a window of varying size. For example, if you are summing it might do a running total where the first row has one row of value, the next row has that value plus the previous row, and so forth. So the window grows during this evaluation. This is actually just default behavior and great for doing a running total. But if you dive into the Snowflake documentation you will find you can specify the window be of a fixed size (x rows before, x rows after) or other ways to customize the window.
- There's other handy stuff in window functions, like `LAG()`, which always references the previous row. Fun times.
