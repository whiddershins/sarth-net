---
title: Recursive functions in teapots
description: Recursive functions in teapots, a post by Sarth Calhoun first published at this address on sarth.net on February 12, 2013, on learning recursion in MIT OpenCourseWare’s CS 6.00.
url: https://www.sarth.net/recursive-functions-in-teapots/
published: 2013-02-12
facet: machine
author: Sarth Calhoun
---
Feb 12, 2013 · Machine

# Recursive functions in teapots

I’ve been really in to MIT Opencourseware CS 6.00 “Introduction to Computer Science” … it is taught in python and focuses on how to use computers to solve problems.

One of the coolest concepts so far, and one of the most difficult for me to get my mind around, is the idea of recursive functions. These are functions which call themselves.

The example in the lecture is a function for deciding if a word is a palindrome, and I’m sure this is an old classic for all of you with a CS background. [ I wonder if, having seen this lecture I would have done [Project Euler problem 4](http://projecteuler.net/) differently. ]

The recursive method they give for deciding whether a word is a [palindrome](http://en.wikipedia.org/wiki/Palindrome) goes like this:

Is this word a palindrome? Well,

Does it have zero, or one letters? Yes? It is a palindrome.

If not, are the first and last letters the same?

They are? Oh, ok, discard the first and last letters then, and ask, Is this word a palindrome …

There is even a whole category of programming languages called [functional programming languages](http://www.haskell.org/haskellwiki/Haskell) and they LOVE recursion.

Which makes it even nicer that I saw this on the Book of Sarth tumblr today, and just had to do a [repost](http://thebookofsarth.tumblr.com/post/42906472855/emailing-ramses3000-fuckk-no-this-is-not):

I think I love this because it is a useful version of

> “We met at dawn at the gates of paris
> 
> and I, being the better man, quickly overcame my adversary
> 
> after which I retired to a bar
> 
> whereupon I met a man
> 
> what have you been doing? He asked …
> 
> What have I been doing?
> 
> Yes, what have you been doing?
> 
> I’ve been dueling.
> 
> You’ve been dueling?
> 
> Yes, I’ve been dueling
> 
> With whom have you been dueling?
> 
> With whom have I been dueling?
> 
> Yes, with whom have you been dueling
> 
> Lieutenant Greene of the Queens Marines
> 
> Lieutenant Greene of the Queens Marines!
> 
> Yes, Lieutenant Greene of the Queens Marines
> 
> But, he was my brother!
> 
> He was your brother?
> 
> Yes, he was my brother, we must duel!
> 
> We must duel?
> 
> Yes, we must duel
> 
> We met at dawn at the gates of Paris, and I …

Filed under: [Musings](/category/musings/).

Tags: [cs 6.00](/tag/cs-6-00/), [opencourseware](/tag/opencourseware/), [recursion](/tag/recursion/).

Originally published on sarth.net, February 12, 2013.
