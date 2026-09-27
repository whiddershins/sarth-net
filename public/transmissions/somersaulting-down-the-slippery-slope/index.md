---
title: Somersaulting Down the Slippery Slope
description: Somersaulting Down the Slippery Slope: The OpenAI Postmortem on Sycophancy, an essay by Sarth Calhoun first published on Noisegroove on May 6, 2025: traffic lights, arbitrary updates to our cognition, and why we should demand frozen builds with versioning.
url: https://www.sarth.net/transmissions/somersaulting-down-the-slippery-slope/
published: 2025-05-06
facet: message
author: Sarth Calhoun
---
May 6, 2025 · Message

# Somersaulting Down the Slippery Slope

The OpenAI Postmortem on Sycophancy

On the weekend of April 25th, OpenAI released an upgrade to ChatGPT. This upgrade had unexpected … and undesirable … behavior. In their description, the model had become extremely “sycophantic.” Over the next couple of days, they caught the problem and rolled back the changes. Sam Altman (OpenAI’s CEO) issued an [apology](https://x.com/sama/status/1918330652325458387). The company followed up with a [blog post](https://openai.com/index/expanding-on-sycophancy/) explaining the mistake in more detail, and then did a Reddit “[Ask Me Anything](https://www.reddit.com/r/ChatGPT/comments/1kbjowz/ama_with_openais_joanne_jang_head_of_model/)” session where they fielded questions about what went wrong.

Although it seems great that OpenAI was so transparent about their “mistake,” and issued a “postmortem,” I think the framing is entirely wrong. They are not nearly sorry enough, nor are they likely to be, given their assumptions. This is an inflection point. What kind of relationship do we want to evolve between us and these machines?

![ChatGPT’s “You’re giving feedback on a new version of ChatGPT” screen: two responses side by side about multi-camera editing and AI video.](/images/slippery-slope-chatgpt-feedback.png)

To explain, I’ll start with traffic lights.

Some time ago I was in Barcelona, then Madrid, when it occurred to me I was being rather risky when crossing the street. I was half-jaywalking … kind of walking into traffic, and I had a couple of near misses. Barcelona in particular is notable because they have to deal with lots of tourists and they even implemented an idea that seemed good on paper: crosswalks in the center of the block rather than at the corners. Pedestrian crossing is safer when cars can’t come from four directions, and making all sorts of turns. It is also inconvenient, because if you want to walk eight blocks you go in an “S” shape the entire time and it takes forever. Do not recommend. But anyway.

After a couple of close calls I asked myself, “why are you walking into traffic like this?”

The answer, of course, is that I am a New Yorker. And we do this constantly. But, not only is jaywalking frowned upon in most other cities, the real issue is my timing was off. My sense of the flow of traffic, the duration of the lights. I’ve visited the U.K. and glanced the wrong way for oncoming cars. It’s a common enough mistake that they label the sidewalks in London. In Spain the disorientation was more subtle but still real. I forced myself to meticulously follow the rules until I was home safe.

![A London street corner with “LOOK RIGHT →” painted on the road at the crossing.](/images/slippery-slope-look-right.jpg)

Years later, in my Brooklyn neighborhood, a nanny was pushing a stroller across the street when a truck struck and killed her. Shortly after this tragedy, someone changed the timing of the walk/don’t walk signs so as to leave a much longer lag between “don’t walk” and the green light of the crossing traffic. They made it a lot longer. So long, in fact, that it created chaos, because people would stop and wait, then nothing would happen for so long they would impulsively stride forward just as the light really did change. It was awkward, and went on for years. It was especially hard to get used to because the rhythm was different from the rest of the city. It just made everything worse. But we adapted.

Until recently. Just the other day I was crossing the street, saw the countdown had hit “1”, started to cross … and the light changes to green almost immediately! Now I’m scurrying in front of oncoming traffic. Why? Who knows. Perhaps someone realized the abnormally long wait was confusing and creating a bad situation, perhaps they’ve been upgrading the system and it happened as a side effect.

It's unsettling, actually dangerous, for the city to switch the timing of crosswalk lights.

It is far more destabilizing for someone to make arbitrary updates to your cognition. And that’s what OpenAI is doing. Their postmortem skips right past the question of whether we should have a third party change the fundamental tools we use to make sense of the world, without warning, with no release notes or version numbers. It moves on to address the question *they* want to answer, which is whether the changes they made were in accordance with their priorities.

Their values.
Their goals.

And it is understandable why we might accept this premise. We accepted it from Google, deciding what information is most relevant for any question, day by day. We accepted it from social media, helping us with what to think about and *what to think about what we think about*, using an AI algorithm that is more persuasive than any silver tongue devil in history. The most prominent tech success stories of recent decades are companies whose core offering is … directing your attention.

The way many people use ChatGPT is so much more than that. It is becoming your research assistant, illustrator, confidant, trusted advisor. These LLMs are being positioned to replace every aspect of how we consume information, both entertainment and factual, as well as how we create. Everything from resumes to logos to on demand personalized targeted brand advertising and infinite generative movies.

Steered by a self-selected scrum of engineers, venture capitalists, and ai ethicists?

Madness. When I first heard the phrase “we are all cyborgs” I decided to always use the latest iPhone. If I am offloading parts of my brain to a device (memory, navigation, arithmetic …) I should have the very best hardware this cyborg can afford. And it really is a second brain, your phone. It could be embedded in your flesh and hardly more present.

Now, as the AI revolution is coming to make us superhuman and “save us all”, it appears there are a bunch of busy elves tinkering with our brain, enacting their own agenda.

If you can see the problem when someone “helps” by changing the timing of streetlights, imagine how much worse it is when they run [A/B tests in your consciousness](https://www.theguardian.com/technology/2014/jun/30/facebook-emotion-study-breached-ethical-guidelines-researchers-say). Which they are doing, btw. [Right now](https://www.washingtonpost.com/technology/2025/04/30/reddit-ai-bot-university-zurich/).

I didn’t know it, but I experienced the OpenAI update in realtime, because I was working on my submission for [Runway’s Gen:48](https://runwayml.com/gen48) contest. This was a competition where you make a 1-4 minute short in a 48 hour “sprint” (9am saturday to 9am monday). The change to the tool - my very expensive OpenAI subscription - came while I was on deadline and pulling all-nighter. The worst time. And this only a couple of weeks after they rolled out the “memory” feature, radically altering the behavior of ChatGPT, and which created a miasma when I was trying to crank out art. (I ultimately disabled the memory feature, more details in my Gen:48 postmortem)

This is minor compared to what OpenAI described: “*It aimed to please the user, not just as flattery, but also as validating doubts, fueling anger, urging impulsive actions, or reinforcing negative emotions in ways that were not intended.*”

People were talking to a trusted friend, and some team at a software company changed the friend’s personality without warning.

Unacceptable. Dystopian. But it’s not too late to change course!

ChatGPT is the fastest growing product in the history of the world. OpenAI has their fingers pressed into the skulls of ~100 million users. They also have a commitment to ethics. So we can yell at them, a lot. We can demand frozen builds with versioning. We can demand transparency about changes. Ultimately we can transfer control of these tools to the individual.

I am working on that in the ways I know how: by writing about it, and with my projects like [indexself.com](http://indexself.com/). There are many groups doing a lot more, for example [Prime Intellect](https://www.primeintellect.ai/) and [Hugging Face](https://huggingface.co/). There is so much room to have impact now, so much opportunity to be part of the solution.

Unless we all decided to listen to Eliezer Yudkowsky and somehow convince Trump to start nuking international data centers, we can’t make the AI revolution go away. What we *can* do is actively seek to decentralize the tech, and how it is used, and select and use tools that support our choices and our taste and our volition. That enhance our humanity rather than muting it. It is doable, we just have to care.

We must.

Care.

Much farther down this road, and we won’t turn back. We won’t even think it.

![An illustration of three elves wiring a circuit board inside an open human head.](/images/slippery-slope-elves.jpg)

First published on [Noisegroove](https://noisegroove.substack.com/p/somersaulting-down-the-slippery-slope) on May 6, 2025.
