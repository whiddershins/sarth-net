---
title: Why Python is the default for data work
description: Python is the default for data work because it is what people know, plus an ecosystem (Pandas, PyTorch) written in C, C++ and CUDA. What that does and does not tell you about building pipelines.
url: https://www.sarth.net/transmissions/why-python-is-the-default-for-data-work/
published: 2026-09-22
author: Sarth Calhoun
---
Essay

# Why Python is the default for data work

*Adapted from a piece I wrote in April 2024.*

Arguably the biggest reason Python is the defacto language for data work is that it is what people know. Lots of people know Python because it is easy to learn, and it is taught in introductory computer classes at most major Universities. MIT taught 6.001, [Structure and Interpretation of Computer Programs](https://mitpress.mit.edu/9780262510875/structure-and-interpretation-of-computer-programs/), in Scheme from 1980 until [January of 2008](https://mitadmissions.org/blogs/entry/the_end_of_an_era_1/), when Gerry Sussman taught it one last time and the introductory sequence became 6.00 and 6.01, in Python. The world hasn't looked back since. Many data scientists and researchers have a limited engineering background, and anyway the first language you learn is often the one you will always feel most comfortable with. This is how Python started to push out more specialized tools such as R and MatLab for data stuff ….

Another side effect of this is the typical nature of an existing Python LLM repo on GitHub. The community is amazingly generous, examples of cutting edge stuff is shared daily. If you've written production code in a modern environment, you might be puzzled when diving into the source of these apps. Many of the decisions (objects, global variables, etc.) work just fine for what the contributor wanted to accomplish, but are a bit jarring if you showed up expecting the conventions you use at work.

But the "killer app" for Python is the ecosystem, most dramatically Pandas and PyTorch. Pandas is used for data analysis and manipulation, and PyTorch for machine learning and AI. Both of these libraries are incredible for what they do, and don't have easy analogues in other languages. And what's more, although Python is famously slow, these libraries are written in lower level languages (C, C++, and CUDA) so they match or outperform all other options in the places where it matters most (large scale data analysis and manipulation in the case of Pandas, and machine learning in the case of PyTorch).

So this is not an essay called "how to have a career as a data scientist without ever touching Python" … that essay would be short, tortured, and professional malpractice.
