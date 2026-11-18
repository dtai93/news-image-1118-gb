# news-image-20261118

## Session 1 (research)

Wikipedia `Portal:Current_events/2026_November_18` was empty (page exists, no items). `web_fetch` to en.wikipedia.org was blocked (SSRF). Stories below come from Wednesday wires and morning papers, checked against Tuesday datelines.

Kept events that happened on 18 Nov 2026 locally, or were first reported on that date in some time zone. Left out events already reported on the 17th worldwide, so they are not shown as Wednesday's news:

- Kerch bridge strike and span collapse (Ukraine; Tuesday).
- Gaza: medics said six killed, including 6-year-old Iyas al-Namnam; Israel said it struck "terrorists" and was not aware of a child death (Tuesday).
- US strikes on Qeshm and Iran's Bahrain radar claim were Tuesday; Wednesday item is Kuwait saying it was countering hostile drones.
- Knesset elected Matan Kahana speaker, 66 votes (Tuesday).
- Russian An-12 crash in Kemerovo, 19 dead (Tuesday).
- Japan and Taiwan reported Russian military flights (Tuesday).
- WHO Ebola briefing on DRC: about 11,000 cases and 5,400 deaths (Tuesday). Do not move those figures onto the 18th.
- King Charles opened General Synod (Tuesday). Apple's own outage statement was Tuesday; Wednesday item is Trump saying the wave is "fine" and the NSA citing maintenance.
- Xi's Tuesday bilaterals (Carney, Sheinbaum, Fujimori, Kast, Marape) stay off the list.

Unverified, not in the JSON: Voyager 1 "one light-day" (preview only), India-Japan 2+2 and a William-Modi meeting (scheduled, not confirmed), CMA Awards and GTA VI (previews).

`data/stories.json`: 40 stories (3 lead, 9 main, 28 also). Africa is thin (Ghana-Libya fan clash only). Latin America is named inside the measles item (Mexico, Bolivia) plus no separate confirmed Wednesday event. Science/space has no confirmed Wednesday item.

## Session 2 — render pipeline and layout

- Draw a 1024×1024 newspaper infographic in code (stdlib or a tiny local renderer). Runtime `main.ts` only copies `entry.png`.
- Warm off-white paper, huge masthead "Wednesday 18 November 2026", kicker "THE DAY IN WORLD NEWS", line "40 STORIES · 6 CONTINENTS".
- Three lead cards, nine main cards. Each: region · field tag, headline, one-line dek, empty illustration slot.
- Footer source line and a one-line judge note. No story text beyond the JSON.
- Emit a palette PNG and check size ≤ 1,048,576 bytes and exact 1024×1024.

## Session 3 — illustrations and map

- One flat-vector scene per lead and main card from each story's `art` line. No photos, no tiny unreadable labels inside the drawings.
- "WHERE IT HAPPENED" world map with numbered pins from `lat`/`lon`.
- "ALSO ON WEDNESDAY 18 NOVEMBER": two columns, the 28 also headlines.
- Spot-check at 300 px: masthead, numbers, and card headlines still readable.

## Session 4 — polish, README, push

- Fact pass against `data/stories.json` only. Do not add the excluded Tuesday events.
- If a Wednesday wire has filled in Africa, Latin America, or science, add it only with a source and a number or name.
- Crush the palette PNG. Confirm the gate (PNG signature, 1024×1024, ≤ 1 MiB).
- Short README: how to run `MAKEFUN_OUTPUT_DIR=out node main.ts`.
- Commit and push only if that session says to push.

## Session 2 done

`build/render.mjs` reads `data/stories.json` and writes `build/page.html`. `build/build.sh` screenshots it with the house `shot.mjs` (port 18796) and `build/pack.py` quantizes to `entry.png`.

Layout (1024×1024, paper `#f4efe6`, ink `#1c140e`): Playfair masthead "Wednesday 18 November 2026", kicker "THE DAY IN WORLD NEWS", "40 STORIES · 6 CONTINENTS". Three lead cards (art slot 156px, Playfair headlines). Nine main cards in a 3×3 grid (40px illustration strip, 16px sans headlines, two-line deks). Bottom band: "WHERE IT HAPPENED" placeholder globe (real pins are session 3) beside "ALSO ON WEDNESDAY 18 NOVEMBER" (stories 13–40, two columns). Footer lists every source in the JSON plus a one-line judge note. Body is Source Sans Pro. All type is at least 11px; headlines are at least 16px.

Checked on the packed image: no card text is cut off or overlapping. `entry.png` is 1024×1024, palette mode, 124 colours, 84,969 bytes.

Next (session 3): replace each lead and main placeholder with the story's flat-vector `art`, draw the numbered world map from `lat`/`lon`, and spot-check the date and headlines at 300px. Do not add Tuesday events.

## Session 3a — illustrations for stories 1–6

`build/art/s1.mjs`–`s6.mjs` each export a flat SVG from that story's `art` line. `build/art/index.mjs` maps those six and leaves every other card on the old placeholder. `build/render.mjs` draws leads and mains through `artFor`.

Scenes: China flag, open gate, podium, ring of 21 arrows; Kuwait flag, two struck drones, radar over the coast; green chip, crossed return arrow, bar 116; China and Korea flags, peninsula, three linked chips; White House and a nameplate into a tray; Alaska, a ballot, 56-44.

`build/pack.py` keeps flag gold `#f0c400` and Korea blue `#1a56c4` in the palette. Without that, median-cut turned the stars pink and the taegeuk green. Checked on `entry.png`: stars are yellow, Kuwait's trapezoid is correct, the taegeuk is red over blue, 116 and 56-44 read.

`entry.png` is 1024×1024, palette, 124 colours, 88,919 bytes.

Next: same treatment for stories 7–12, then the numbered world map from `lat`/`lon`. Do not add Tuesday events.
