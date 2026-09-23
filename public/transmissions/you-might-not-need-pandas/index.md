---
title: You might not need Pandas
description: Why most day to day Pandas work is better done in SQL, with a side by side average-sales-by-category example, and where Pandas still earns its place.
url: https://www.sarth.net/transmissions/you-might-not-need-pandas/
published: 2026-09-22
author: Sarth Calhoun
---
Essay

# You might not need Pandas

*Adapted from a piece I wrote in April 2024, about work I did starting in the fall of 2022.*

I don't want to be boring and keep talking about how great Pandas is, but, Pandas is great. Many people who learn data science think they were learning Python or data analysis or whatever but actually they were learning Pandas and that's a good thing.

However.

I was on a project dealing with huge data sets. My task was to make a QA system, because we were ingesting data from many … uh … friendly but not always consistent sources, and this information was being piped, stored, transformed, and used by business people trying to do sales and accounting. Those people wanted the information to be right.

So the mission was to stop bad information from making it all the way down to the PowerPoint or excel or whatever the hell they were doing with this. Coming in knowing nothing, the system was equipped with a bunch of analysis tools built in Python using Pandas. We spent a minute getting up to speed, but soon developed a working understanding of Pandas and did a bunch of troubleshooting.

After a few days of this we came back to the project lead and said "ok, cool, we will implement this QA system using pandas" because, obviously that was correct. And he said "no, just use Postgres."

What.

Well, let's do a fairly simple, but actually *not contrived* example. Let's calculate the average sales by category for a business.

In Pandas:

```python
import pandas as pd

# Load data into a DataFrame
df = pd.read_csv('sales_data.csv')

# Calculate average sales by category
average_sales = df.groupby('category')['sales'].mean()

print(average_sales)
```

In SQL:

```sql
SELECT category, AVG(sales) AS average_sales
FROM sales_data
GROUP BY category;
```

These are each just three lines of code, and I acknowledge perhaps I made it seem longer in the Pandas version by adding comments and line breaks.

Except I don't feel bad. Obviously the comments and linebreaks in the Pandas version are there because it isn't blindingly obvious how it works or what it is doing.

SQL, for all its reputation as being arcane, is a declarative language where the designers made an attempt to have it read like what it is doing. I'm not arguing the SQL is obvious and easy to read. I'm observing it is *at least* as easy to read as the Pandas (to say it kindly).

But also, SQL queries are executed against your database, are freakishly optimized, often distributed by default, and definitely don't make you worry about the memory this process has to work with. Also, and by the way, any data engineer doing any serious work is dealing with SQL all day long. With that in mind, what about Pandas?

Depending on how you count it, 80% of what people are doing with Pandas day to day can be handled faster, better, and with less errors by doing reasonable SQL queries.

For the remainder? Yes, use Pandas. Pandas is great.

Just don't use it to filter your sales by 3rd quarter of 2022, because that is a noob move.
