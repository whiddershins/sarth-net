---
title: Ingather
description: Ingather, the control system Sarth Calhoun built for a cannabis cultivation facility between August 2021 and March 2022. Rooms and zones, fertigation and lighting routines, dosing recipes and machines. Playable demo online.
url: https://www.sarth.net/conspiracies/ingather/
published: 2026-09-23
facet: machine
credit: Ingather, a T.E.C. Systems product. Sarth Calhoun led a nine-person team, six developers and two designers, as Director of Product, August 2021 to March 2022. It ran a 120,000 square foot indoor agriculture facility.
author: Sarth Calhoun
---
[Conspiracies](/conspiracies/) / Ingather

Conspiracy · Machine

# Ingather

Ingather is an integrated control system for a cannabis cultivation facility, built between August 2021 and March 2022. Rooms and zones, plant groups and strains, fertigation and lighting routines, dosing recipes and machines. A SvelteKit front end over a REST API, with its own server-side endpoints so the client never talks to the backend directly. Named for the archaic sense of the word: to gather in, to harvest.

The screens ran on monitors outside the rooms and on small touch panels, one per room, which is why the numbers are large and the controls are thumb-sized. A grower walking past a door could read the room without stopping.

The facility is gone and the API went with it. [The demo runs anyway](https://ingather-demo.marshy-runner.workers.dev).

![Ingather, a room overview: room phase, light level, zones and their fertigation programs, air handler readings.](/images/ingather.jpg)

A room overview. [Try it](https://ingather-demo.marshy-runner.workers.dev).

![Ingather, a zone: strain and batch, plant count and emitters, the lighting routine and the nutrient recipe with its numbered pumps.](/images/ingather-zone.jpg)

A zone. Its strain, its lighting routine, its recipe.

## What it controlled

A room holds zones; a zone holds a plant group of one strain. Each zone carries its own lighting routine, fertigation routine and nutrient recipe, so two zones in the same room can run differently.

- **Environment.** Temperature, humidity, vapour pressure deficit, CO2 and light level, each with a reading and a set point. VPD is the one a grower actually tunes, and it sits in the list beside the two measurements it is calculated from.
- **Fertigation.** Routines of timed cycles, expressed either as minutes of run time or as a share of the day’s target volume per plant, with the other derived from emitter flow rate and emitters per plant.
- **Dosing.** Machines of twelve pumps, each pump assigned a role and a mix group, dosing millilitres per gallon against a target pH and conductivity. A recipe is viable on a machine only if that machine carries every ingredient the recipe calls for.

## The demo

The system it controlled no longer exists, so the demo is the app with invented data behind it: four rooms, thirteen zones, nine strains, twelve plant groups, five recipes, four dosing machines. Everything runs in the browser and nothing is stored anywhere but the visitor’s own machine, so anything changed belongs to whoever changed it and is gone when they clear it.

Time runs at 1800 times real speed, a full light cycle every forty eight seconds, because a grow room only shows what it is doing across a day. The readings are generated rather than replayed, and generated the way a room behaves rather than as five unrelated waves: the lamps drive everything, temperature follows them late, humidity runs against temperature, CO2 is injected only under the lights, and vapour pressure deficit is calculated from the other two. The two flower rooms run opposite schedules, so they read as opposites at any moment you look.

[ingather-demo.marshy-runner.workers.dev](https://ingather-demo.marshy-runner.workers.dev)

## How it started

The credit: Ingather, a T.E.C. Systems product. Sarth Calhoun led a nine-person team, six developers and two designers, as Director of Product, August 2021 to March 2022. It ran a 120,000 square foot indoor agriculture facility.

## Conspiracies

It sits with the rest of the data and systems work on [Work](/work/). The pipeline writing is in [External tables](/transmissions/external-tables/) and [DuckDB, where have you been all my life](/transmissions/duckdb-where-have-you-been-all-my-life/).
