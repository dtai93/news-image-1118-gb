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
