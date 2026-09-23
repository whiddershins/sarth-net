---
title: Visual Reference Prompting
description: We’ve been doing hybrid production at Third Wall Studio since before anyone called it that. I made Burlap for this precise use case: Start from original art and use it to style more images, explore variations, and generate the in-betweens.
url: https://www.sarth.net/transmissions/visual-reference-prompting/
published: 2026-07-31
author: Sarth Calhoun
---
Jul 31, 2026

# Visual Reference Prompting

We’ve been doing hybrid production at [Third Wall Studio](https://thirdwallstudio.com) since before anyone called it that. I made [Burlap](https://burlap.app) for this precise use case: Start from original art and use it to style more images, explore variations, and most importantly generate all the “in betweens” that make animation so brutally manual and meticulous.

I call this *visual reference prompting* meaning you want to be using visual material as the input to creating visual material. This is axiomatic. There is a reason they say “a picture is worth a thousand words.”

There are two dimensions of this technique, broadly. One is using a subject reference (for example a character) and the other is a style reference. In both cases you are pushing the genAI into a different probability space. This is how to get a unique style, and also how you chase consistency.

In the general case this is context management. Actively choosing the elements that are fed into the model with each generation step. And in Burlap you do this in the most intuitive way I could imagine: just select stuff on the canvas and send it to be generated.

Because the default Burlap interface isn’t a chat mode, to implement chat you would need to manually reselect all the context after each round of generation. Which is pointlessly manual for chat. But it also exposes to the end user what chat is. Resending the entire convo over and over and over. Instead, we are trying to give the model the precise context it needs, for each generation we call. For a concrete example: Frogs and Goblins (below).

[Download Burlap](https://burlap.app/download) · [Third Wall Studio](https://thirdwallstudio.com)
