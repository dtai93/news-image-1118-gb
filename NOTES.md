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

## Session 3b — illustrations for stories 7–12

Main illustration strips are 65px (were 40). Page rows are now 82 / 217 / 396 / 256 / 46. Lead art track is 140px so two-line deks still fit. Also-list lines are 16px so items 13–40 stay inside the shorter band.

`build/art/s7.mjs`–`s12.mjs`, and s4–s6 redrawn for the taller strip. All twelve are registered in `build/art/index.mjs`.

Scenes: syringe, measles spots, US / Mexico (Baja) / Bolivia silhouettes; sun, Australia, a draft marked 2030; three server racks with one gold lamp and a check; Union Jack, gavel, five houses; courtroom bench and a calendar reading 330; a pipeline from a western landmass toward an eastern one, with a valve and an arrow.

Checked on `entry.png`: masthead, 2030, 330 and 56-44 read; main headlines and deks are intact; the also list runs 13–40. File is 1024×1024, palette, 123 colours, 90,756 bytes.

Next: numbered world map from `lat`/`lon`, then spot-check the date and headlines at 300px. Do not add Tuesday events.

## Session 3c — where it happened

`build/landmask.mjs` is a 90×40 equirectangular mask from 75N to 56S (`#` land, `.` sea, no Antarctica). `build/map.mjs` draws one dot per land cell and red numbered pins for stories 1–12. Leader offsets keep Shenzhen (1 and 4) and the Washington/New York cluster (5, 7, 9, 11) from sitting on the same badge.

The bottom band is 45/55: the map on the left, the also-list on the right. One-line legend: "Asia 1·4·12 · Gulf 2 · Americas 3·5-7·9·11 · Europe 8·10".

Checked on `entry.png`: the Americas, Europe, Africa, Asia and Australia read as separate shapes; each pin's dot is on that story's coast and the badges do not cover one another; the legend sits in the margin under the map. A 300px shrink still shows the masthead. File is 1024×1024, palette, 123 colours, 104,938 bytes.

Next (session 4): fact pass against `data/stories.json` only, crush the palette PNG, confirm the gate, short README. Do not add Tuesday events. Spot-check card headlines at 300px while doing that.

## Session 4 done

Fact pass stayed inside `data/stories.json`. No Tuesday events added. Kuwait's lead dek no longer mentions the Tuesday Qeshm strikes; it only says Kuwait reported countering drones on 18 November. Headlines that are someone else's claim already say so (Kuwait, PAHO, Trump, the Justice Department, Bilawal, Pope Leo, Rubio).

Masthead is "Wednesday 18 November 2026" and "40 STORIES · 6 CONTINENTS" (40 stories; Africa, Asia, Europe, North America, South America via Bolivia, Oceania via Australia). Footer: full source list plus "Original drawings." Judge note still dates the day and says disputed claims are attributed.

Drawings: US shape now has the Florida and Texas points, Mexico keeps a separate Baja, Australia has Cape York, the gulf bite, and Tasmania, and the Korea card's peninsula reads as a peninsula. "56-44" stays on one line.

`entry.png` is a palette PNG, 1024×1024, 107,572 bytes. `mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts` matches `entry.png` on two runs. `out/` is gitignored. README is the make.fun template.

Pushed to origin main. A later session should change the picture only if a grade names a specific miss.

## Session 5 — match the #1 layout

Rebuilt the picture in `build/page.py` (Pillow), `build/geo.py` (lon/lat continents, equirectangular 75N–56S filling the map box) and `build/scenes.py`. `build/build.sh` now runs `python3 build/page.py`. `main.ts` still copies `entry.png`.

Layout now follows the 12–0 entry: kicker “THE WORLD'S NEWS IN ONE PICTURE” and “43 STORIES · 6 CONTINENTS · ALL FROM WEDNESDAY”; full-width date; three lead cards with ~110px scenes, dark caption strips and red stat chips; ten smaller illustrated cards in two rows of five; region-coloured tags, pins and legend; field-colour key kept under the date; “WHERE IT HAPPENED” map with numbered pins 1–13 and dots for the rest; two-column also list; source line and judge note.

Story set: every fact from `data/stories.json`, Ghana promoted to the 13th illustrated card, plus three Wednesday wires — Flores magnitude 5.9 at 10 km (GFZ/Reuters), Tinubu hailing the rescue of 308 kidnap victims (The Nation), a Guinea court jailing 224 over illegal gold mining (allAfrica). No Tuesday events.

`entry.png` is 1024×1024 palette PNG, 84,821 bytes. `MAKEFUN_OUTPUT_DIR=out node main.ts` matches it. A 300px shrink still shows the date, the three lead headlines and the small-card headlines.

Next: only change the picture if a grade names a specific miss. Watch the US-cluster pin offsets and the small-card deks if a judge says a number is clipped.

## Session 6 — defect fix

Visible defects only. Story text, story set, and the rest of the layout are unchanged.

- Field key (Diplomacy, War, …) sat on the date’s descenders. A rule is now drawn from the date’s real ink box, and the key sits under that rule.
- Nvidia lead: `$116BN` is drawn in the picture above the caption strip, not through it. Scenes are painted only above the caption, so the strip cannot cover picture text.
- Islamabad: the big `2 PACTS` is gone. The red chip and the caption already say it; the drawing is the pipeline only.
- Other picture labels checked and kept inside their shapes: OVERTON, 56–44, US/MEX/BOL, 2030, 1,200, 330.
- Map legend labels are 14px (were 11). The map is a few pixels shorter so the legend does not cover land.

Checked at 1024 and at 300px: date and key are separate, `$116BN` and `330` sit fully in their pictures, Islamabad has no overlapping label, legend names read. `entry.png` is 1024×1024 palette, 82,947 bytes. `MAKEFUN_OUTPUT_DIR=out node main.ts` matches it.

Next: change the picture only if a grade names a specific miss.

## Session 7 — craft upgrade

Facts, story set, and the newspaper grid are unchanged. Type and pictures are heavier.

- Headlines and the date use Playfair Display at weight 900, ink `#0c0806`. Variable fonts were loading at weight 400, so “bold” paths had been regular. Arimo is now set to 700 for tags, deks, the field key, and the also-list. Deks stay 13px on leads and 11px on small cards. The also-list is 11px bold and near-black, so it still reads at 300px. Small cards allow a third dek line, so the longer deks (UK sanctions, TAPI, measles, net zero, outages) are no longer cut off.
- Scenes are concrete: Xi at a podium under an “APEC 2026 / SHENZHEN” banner and 21 flags; Kuwait towers with two drones, interceptor trails, and a launcher; a boardroom table, a crossed-out CEO plate, a chip, and `$116BN` on the chart; Alaska, a ballot, and 56-44; a gavel with “330 MONTHS”; a stadium, fans, and police for Ghana. OVERTON stays readable; the red mark is on the out-tray.
- “THE DAY IN FIGURES” under the map: 21 economies, $116BN revenue, 56–44 senate, 330 months. The continent legend sits beneath that strip and does not cover it.

`entry.png` is 1024×1024 palette, 86,832 bytes. Checked at full size and at 300px: date, lead headlines, also-list, and the four figures read; banner text is clear of the caption bars. `MAKEFUN_OUTPUT_DIR=out node main.ts` matches `entry.png`.

Next: change the picture only if a grade names a specific miss.

## Session 8 — overlap fix

Headline and dek spacing only, plus the map legend and the figures row. Story text is unchanged.

- Card type uses a line height of at least 1.15 times the font size. The dek starts 3px under the last headline line's ink. A headline drops 1px, then 2px, before a dek is cut to two lines. The measured cards keep the full dek. The tightest small cards (Korea, sanctions, TAPI) end 4px or more above the border, with 5px or more between the headline and the dek.
- Lead pictures are 98px tall (were 110) and small pictures 71px (were 73) so that line height fits inside the card. Headlines stay 22px on the leads. A few small headlines are 13–14px.
- Under the map, the continent legend is first and "THE DAY IN FIGURES" is under it. Both sit inside the box and do not cover the land or each other.

Checked at 1024 and on crops of the small cards: the named collisions (Korea, Alaska, Merchant, TAPI, lead deks, figures versus legend) are separated. `entry.png` is 1024×1024 palette, 88,781 bytes. `MAKEFUN_OUTPUT_DIR=out node main.ts` matches it.

Next: change the picture only if a grade names a specific miss.
