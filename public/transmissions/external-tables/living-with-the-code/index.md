---
title: Living with the code
description: Reading dense, strongly typed functional TypeScript: Prettier verticality, generics, and going one concept at a time.
url: https://www.sarth.net/transmissions/external-tables/living-with-the-code/
published: 2026-09-22
originally_written: 2024-07-13
author: Sarth Calhoun
---
Append-only pipelines · Part 5 of 5

# Living with the code

*Adapted from a piece I wrote in July 2024, about work I did starting in the fall of 2022.*

Code built this way is oriented towards strongly typed (TypeScript) functional code. This has an emphasis on safety, testing, reliability, and composability. It also follows the philosophy of self documenting code. Each function is a conceptual boundary, and the function and variable names should reflect exactly what they are. If you are comfortable in that world, you probably don't need to read this part. If anything feels complicated, here are some tips.

Make sure your IDE toolchain is set up right, with all the linting and [Prettier](https://prettier.io/) for formatting. Get set up with a TS REPL and the [JEST](https://jestjs.io/) runtime thing, and use the [TypeScript playground](https://www.typescriptlang.org/play) or the REPL to validate your understanding of how stuff works. One thing that might be off putting if you aren't used to it is how VERTICAL the code is. For example, when a function has numerous parameters, Prettier will put them each on their own line like:

```
const sendAlertAndRecordResult = async (
channel: string,
recipients: Recipient[],
message: string,
checkIds: string[],
dryRun: boolean
)
```

Or maybe it does this:

```
export async function runCheck<Result extends BaseResult = BaseResult>(
{
tableName,
checkName,
threshold = 0.05,
notify,
dryRun,
failOnWarning = false,
}: CheckConfig,
format: ResultFormatter<Result> = defaultFormatter
)
```

Which manages to combine parameter destructuring, default parameters, a generic/type variable...

And all starts to feel vaguely LISP-y.

You end up with lots of stuff before you get to your first curly brace and the actual function, because all these type annotations add a lot of cryptic information as well. If this style is new, your eye might size things up wrong, and literally get function declarations, type declarations, and function body all mixed up.

I know I don't have to say this but I will anyway: don't worry. None of these concepts are difficult if taken in isolation. It's just a bunch of them all at the same time. So if someone imported lodash and used partial application... it's not complicated. Just go one concept at a time and it will all come together in your mind, sooner than you think.

The conceptual gap here is similar to when you learned algebra in grade school. Some teacher might write x + 2 = 7 on the board and then teach you how to solve for x. (Remember, you are supposed to subtract the 2 from each side... blah blah.) The problem is, it's immediately evident that x is 5, so it can be hard to care about the steps you are supposed to take to derive x.

Then 2 years later you are doing trig or calculus or whatever and you can't just eyeball x anymore, but the procedure for solving for it didn't get wired into your brain because the algebra lessons were so stupid. OK, maybe that was just my experience, but whatever.

Reading the [TypeScript handbook](https://www.typescriptlang.org/docs/handbook/intro.html) can be similar. They present a concept with a trivial or contrived example, and it can be hard to see why you care, exactly. Or what it would look like in production code. Then you drop into a real repo and see some incomprehensible series of type annotations. There's a bunch of daylight between the examples and the real-world application. Also, types are more often inferred than not, so there's no consistency about when you see type annotations and when you don't... at least from the beginner's mind. But what that offers is a window into understanding the code. If you see type annotations, it is a signal the compiler can't infer the types, and that is itself information. In practice, all of this syntax is incredibly information dense. So you gotta force yourself to methodically understand each and every sigil. If you accept this, and go slowly for a moment, everything becomes accessible.

[← Part 4: Defending the boundary](/transmissions/external-tables/defending-the-boundary/) [Series overview →](/transmissions/external-tables/)
