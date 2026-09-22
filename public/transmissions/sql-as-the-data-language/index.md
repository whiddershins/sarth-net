---
title: SQL as the data language
description: Views, CTEs, joins, and why a handy way to think about SQL is that everything is a table (which is also not true).
url: https://www.sarth.net/transmissions/sql-as-the-data-language/
published: 2026-09-22
originally_written: 2024-07-13
author: Sarth Calhoun
---
SQL

# SQL as the data language

*Adapted from a piece I wrote in July 2024, about work I did starting in the fall of 2022.*

**Views.** If you aren't a SQL-head, you might not know that a view is just a stored SQL query that can itself be queried as if it were a table. The reason you want to store that query and pretend it is a table is partly the same reason you might assign anything to a variable while coding, but mostly to separate concerns in the app. The view does a bunch of stuff to format the data, then the next thing consumes that view. If the view needs to be updated because something upstream changed or was wrong, the rest of the system doesn't need to care. The views in a pipeline like this can be really extensive. And complicated, like over 100 lines of SQL. They are key to the QA jobs as well.

**Everything is a table.** With that in mind, you might be tempted to think there is something special about views, that you can query them just like they are a table. This is the opposite of true. Just like everything is an object in Smalltalk, or everything is a function in Haskell, or code is data in LISP, a handy way to think about SQL is "everything is a table." It's also not true. The accurate statement is "most queries in SQL return a result set, which itself can be queried." But the point is that SQL is super composable in this way, so there is nothing special about views being queryable, they just happen to be stored. Query results can be queried, and those results can be queried, and it's turtles all the way down. [Buffalo buffalo Buffalo buffalo buffalo.](https://en.wikipedia.org/wiki/Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo)

**CTEs.** Knowing this, [Common Table Expressions](https://www.postgresql.org/docs/current/queries-with.html) aren't at all mysterious. They are variables within a given SQL statement that hold the results of a query, which you can then reference by name later to do more stuff with it. You just create a "table" and give it a name and have access to that for the duration of the statement execution. They take the form `WITH some_descriptive_name AS (SELECT ... etc ... just a query here)`. Mostly CTEs are used to improve readability, and you can accomplish a similar thing by nesting subqueries. But it is easier to reason about CTEs, much the same way async/await is easier to reason about than a tangle of promise chains in JavaScript. There used to be some hubbub about CTEs being inefficient when compared to subqueries, but this is less true nowadays, depending on the engine and version, and anyway if you are having that conversation you aren't reading this tutorial for tips.

**Joins, unions, and such.** There's no need for me to write anything about joins and unions and intersections and so forth here. Every beginner SQL tutorial (like Stanford's [Databases: Relational Databases and SQL](https://online.stanford.edu/courses/soe-ydatabases0005-databases-relational-databases-and-sql)) will start by explaining joins, and the internet is full of examples, cheat sheets, and Venn diagrams. You use joins not only to create unified data sets, but also to cleverly replace bad identifiers and stuff.
