---
title: Defending the boundary
description: Runtime type checking with io-ts codecs in Node streams: errors as values, async pipelines, and why validating at the boundary saves time, money, and heartache.
url: https://www.sarth.net/transmissions/external-tables/defending-the-boundary/
published: 2026-09-22
originally_written: 2024-07-13
author: Sarth Calhoun
---
Append-only pipelines · Part 4 of 5

# Defending the boundary

*Adapted from a piece I wrote in July 2024, about work I did starting in the fall of 2022.*

[io-ts](https://gcanti.github.io/io-ts/) is a TypeScript library by Giulio Canti built around the idea of a codec. A codec is one definition that does three jobs at once: it validates unknown data at runtime, it tells the compiler what the type is, and it encodes the value back out again. The thing it is for is the boundary, the place where data arrives from outside your program and you have no guarantee it is what you were promised. TypeScript's own types are gone by the time the program runs, so at that boundary they protect you from nothing. Newer libraries do the same job, Zod and Effect Schema being the ones people reach for now.

The pipeline uses [io-ts](https://gcanti.github.io/io-ts/) to do runtime type checking; most notably the transform step of the pipeline relies on it. For example, an .xls parser is used with [Node streams](https://nodejs.org/api/stream.html) (pipelines) and io-ts to go through each row of an Excel file provided by the partner and verify the cells provide data which can be encoded to the expected type. If it encounters a cell that doesn't meet expectations, you can either skip the row, fail the file, or fail the entire job, depending on the configuration.

This functional approach saved us tons of time, money, and heartache, and here's why.

With io-ts, one codec definition decodes whatever the partner sent into typed values, encodes those values back out to the CSV, and gives TypeScript the static type. So the validation, the type, and the serialization come from the same place and can't get out of sync with each other.

When a cell doesn't decode, io-ts doesn't throw an exception. It returns a Left, which is just a value, and it moves through the pipeline like any other value. That's why skipping the row, failing the file, or failing the job can be a configuration setting. And the decode errors include the path to the value that failed, so the QA reports can point at the exact row and column.

And because the pipelines are streams and the errors don't throw, the whole thing is completely async. An error doesn't have to crash your whole import, and you can effectively parallelize a bunch of the transformation.

**More explanation if the above doesn't make sense.** If you are wondering what and why, remember that TypeScript is largely an illusion. Everything TypeScript provides is for the purposes of writing code that has type safety at compile time, and is great when integrated well with your IDE. TypeScript won't let you compile code with mismatched types, but it then disappears entirely at the compile step. The code you run is *just* JavaScript. So whenever you are dealing with potentially arbitrary data at run time, TypeScript can't help.

This comes up anytime you read or write from the database, for example. You have to tell TypeScript "trust me, the data will conform to this type," but of course that's only true if you don't goof up your query results (or inserts) data structure and really match it with the TypeScript type. This is untenable in the scenario where you are getting data from a third party, especially a third party that has a history of changing the data format or sending bad data. It is one of the specified roles of this pipeline to handle the chaos of the data.

The bad, verbose, ugly, and laborious but effective way to deal with this would be falling back to a lot of old-school JavaScript type checking... a bunch of `if (typeof foo !== 'undefined')` and all that fun stuff.

The awesome, functional, and robust way to handle this is to use io-ts.

**Breaking apart the bits that might make this feel intimidating.** If this stuff looks intimidating, it might be because several different uncommon techniques are being used together, much the same as the [SQL in part 3](/transmissions/external-tables/current-truth-with-window-functions/). Each piece can be approachable taken one at a time.

- The TypeScript in this style is heavily oriented towards functional programming. It is formatted (by Prettier) with that in mind, and uses functional techniques like decorator functions and partial application, and advanced type concepts such as generics (stuff where what type is used is also variable). If this seems alien, there is more about this in [part 5](/transmissions/external-tables/living-with-the-code/).

- The parsing uses streams in the form of pipelines. Pipelines are a newer way of doing Node streams that makes them easier to understand and more readable. If you aren't familiar with streams, they aren't complicated and they are an important part of how Node fundamentally works. It's how you process little chunks of data successively until the whole file (or whatever) has been processed, so you don't have to have everything in memory at once. People usually get tripped up by streams because the words "writable" and "readable" sometimes feel like they mean the opposite of what you imagined. This is true of every similar technology in every language that supports it, and once you make peace with that the rest is pretty straightforward.

- io-ts is based on [fp-ts](https://gcanti.github.io/fp-ts/), which is a library that brings features common in functional programming languages into TypeScript. It's not necessary to learn everything about fp-ts to use io-ts, just look stuff up if you see something unfamiliar or incomprehensible.

- io-ts is for run-time type checking and conversion as indicated above. Its core type is `Type<A, O, I>`, where the `<A, O, I>` are type variables: the type you want to end up with, the type you want the output to be, and the type you expect the input to be, and so forth... if it can't do those operations because the data you are giving it doesn't conform, it will fail (actually go left instead of right, see [Either](https://gcanti.github.io/fp-ts/modules/Either.ts.html)).

io-ts is in maintenance mode now. If you're starting today, look at [Effect Schema](https://effect.website/docs/v3/schema/introduction), which is where the io-ts and fp-ts work continued and which keeps the functional pipeline style, or [Zod](https://zod.dev/), which is the most widely used and now also has [bidirectional codecs](https://zod.dev/codecs).

[← Part 3: Current truth with window functions](/transmissions/external-tables/current-truth-with-window-functions/) [Part 5: Living with the code →](/transmissions/external-tables/living-with-the-code/)
