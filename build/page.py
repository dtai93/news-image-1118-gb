"""1024 newspaper page for Wednesday 18 November 2026."""
import json
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from geo import paint_land
from scenes import paint_scene

ROOT = Path(__file__).resolve().parent.parent
INK = (28, 20, 14)
HEAD = (12, 8, 6)
MUTED = (48, 38, 30)
PAPER = (244, 239, 230)
CREAM = (251, 247, 240)
RUST = (158, 42, 32)
WHITE = (255, 252, 246)
REG = {
    "Americas": (14, 118, 128),
    "Europe": (36, 74, 158),
    "Middle East": (196, 96, 24),
    "Asia": (104, 58, 164),
    "Africa": (22, 118, 70),
    "Oceania": (176, 64, 122),
}
FIELD = {
    "DIPLOMACY": (26, 79, 139), "IRAN WAR": (143, 29, 26), "TECH": (29, 107, 58),
    "POLITICS": (107, 63, 160), "HEALTH": (196, 92, 18), "CLIMATE": (14, 124, 107),
    "COURTS": (90, 64, 40), "ENERGY": (150, 112, 16), "SPORT": (150, 42, 52),
    "SCIENCE": (32, 78, 140), "CRIME": (120, 50, 40), "EDUCATION": (40, 80, 120),
    "ECONOMY": (20, 100, 80), "CULTURE": (120, 50, 90), "TRANSPORT": (40, 90, 110),
}
# caption, chip, headline, dek — facts match data/stories.json
CARD = {
    1: ("SHENZHEN · OPEN TRADE", "21 ECONOMIES", "Xi defends open trade\nat the APEC summit",
        "His Shenzhen speech backs the WTO and a 21-economy area. Putin is in the city."),
    2: ("KUWAIT · DRONES REPELLED", "18 NOV", "Kuwait says it is\nrepelling hostile drones",
        "Kuwait says it countered hostile drones over the country on 18 November."),
    3: ("NVIDIA · HUANG BLOCKED", "$116BN", "Nvidia's board rejects\nHuang's return as CEO",
        "Directors back interim CEO Colette Kress after revenue of $116 billion."),
    4: ("SHENZHEN · KOREA, CHIPS", "2 LEADERS", "Xi and Lee talk\nKorea and chips",
        "The two leaders met in Shenzhen: Lee asked Xi about peace and chips."),
    5: ("WASHINGTON · FDA NOMINEE", "1 NAME", "White House drops\none FDA nominee",
        "The White House withdrew Heidi Overton before a Senate vote."),
    6: ("ALASKA · SENATE 56–44", "56–44", "Peltola takes the\nAlaska Senate seat",
        "Peltola beat Sullivan. Democrats now hold the Senate 56–44."),
    7: ("PAHO · MEASLES STATUS", "3 COUNTRIES", "US loses its\nmeasles-free status",
        "PAHO says endemic measles is back in the US, Mexico and Bolivia."),
    8: ("ANTALYA · NET ZERO 2030", "2030", "Australia presses\n2030 net zero",
        "In Antalya, Canberra's draft asks rich countries for net zero by 2030."),
    9: ("TRUMP · OUTAGES 'FINE'", "NSA", "Trump says the\noutage wave is fine",
        "Trump says the 18 November outage wave is fine; the NSA cites maintenance."),
    10: ("LONDON · SANCTIONS", "1,200+", "UK sanctions\nsettler-linked firms",
        "Britain sanctioned settlement-linked firms; Europe condemned over 1,200 homes."),
    11: ("COURT · 330 MONTHS", "330 MO", "Merchant gets a\n330-month term",
        "The Justice Department says Asif Merchant received 330 months."),
    12: ("ISLAMABAD · TWO PACTS", "2 PACTS", "Dar and Meredov\nsign two pacts",
        "Ishaq Dar and Rashid Meredov signed a TAPI protocol and a tourism pact."),
    35: ("ACCRA · FANS CLASH", "GHANA", "Ghana fans clash\nafter the Libya loss",
         "GhanaWeb: fans fought police after Ghana lost to Libya."),
}
ALSO = {
    13: "Shenzhen: Anwar says open-trade talk is one-sided",
    14: "Manila: Rubio says Trump is ready to meet Kim",
    15: "Taipei: Shih says Taiwan goes to APEC smiling",
    16: "Manila: Trump to see Marcos, then fly to China",
    17: "Antalya: 33 faith groups pledge fossil divestment",
    18: "London: Red Wednesday fund at £964,003 of £1m",
    19: "Truro: ex-Methodist leader guilty on 11 counts",
    20: "London: UK pay settlements edge up to 3.2%",
    21: "Oslo: Haaland penalty sends Norway through",
    22: "Lisbon: Portugal wins first game of a new era",
    23: "Turin: Zverev reaches the ATP Finals last four",
    24: "Nassau: Woods, 50, to return in the Bahamas",
    25: "California: Waymo suspends freeway robotaxis",
    26: "Seoul: exam rules sticker every clothing button",
    27: "Sangju: magnitude 3.6, biggest inland in 2y 5m",
    28: "Karachi: Bilawal says Sindh split risks bloodshed",
    29: "Islamabad: ADB lends $500m for pension reform",
    30: "Islamabad: 8 bar members back Imran care plea",
    31: "Peshawar: 3 PTI leaders held despite court bail",
    32: "Rawalpindi: Munir discusses defence ties with UK",
    33: "Ilocos: fake-FBI raid arrests 3 Malaysians",
    34: "Manila: protest greets Trump over Pax Silica",
    36: "Durham: Stojakovic scores 46 on Duke's floor",
    37: "Gulf: Formula 1 keeps two season finales on",
    38: "Frankfurt: leak probe traces Deutsche Bank clients",
    39: "Rome: Pope Leo says his tumour is contained",
    41: "Flores: magnitude 5.9 quake at 10 km, GFZ says",
    42: "Abuja: Tinubu hails rescue of 308 kidnap victims",
    43: "Guinea: court jails 224 over illegal gold mining",
    40: "Boston: Harvard ties phone bans to small gains",
}


def face(query):
    return subprocess.check_output(["fc-match", "-f", "%{file}", query], text=True).strip()


def rcol(region):
    if region in ("NORTH AMERICA", "AMERICAS", "SOUTH AMERICA"):
        return REG["Americas"]
    return REG[{"EUROPE": "Europe", "MIDDLE EAST": "Middle East", "ASIA": "Asia",
                "AFRICA": "Africa", "OCEANIA": "Oceania"}[region]]


def wrap(d, text, font, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def font(path, size, weight=700):
    face_font = ImageFont.truetype(path, size)
    try:
        face_font.set_variation_by_axes([int(weight)])
    except OSError:
        pass
    return face_font


def fit(path, text, max_w, start, minimum, draw, weight=700):
    size = start
    while size > minimum:
        chosen = font(path, size, weight)
        if all(draw.textlength(line, font=chosen) <= max_w for line in text.split("\n")):
            return chosen
        size -= 1
    return font(path, minimum, weight)


def load():
    stories = json.loads((ROOT / "data" / "stories.json").read_text())["stories"]
    illustrated = [s for s in stories if s["tier"] in ("lead", "main")]
    also = [s for s in stories if s["tier"] == "also"]
    # Keep also in a readable order: file order, with Boston before the three new wires.
    also.sort(key=lambda s: s["n"] if s["n"] != 40 else 40.5)
    for i, s in enumerate(illustrated, 1):
        s["num"] = i
    for i, s in enumerate(also, len(illustrated) + 1):
        s["num"] = i
    return illustrated, also


def caption(d, box, label, font):
    x, y, w, h = box
    bar = 15 if h > 90 else 13
    d.rectangle((x, y + h - bar, x + w, y + h), fill=INK)
    tw = d.textlength(label, font=font)
    d.text((x + max(2, (w - tw) / 2), y + h - bar + 1), label, font=font, fill=WHITE)


def chip(d, right, top, label, font):
    tw = d.textlength(label, font=font)
    w, h = tw + 8, font.size + 3
    x = right - w - 5
    d.rounded_rectangle((x, top + 4, x + w, top + 4 + h), radius=2, fill=RUST)
    d.text((x + 4, top + 4), label, font=font, fill=WHITE)


def line_step(size):
    """Line height is at least 1.15 times the font size."""
    return max(1, math.ceil(size * 1.15))


def place_lines(d, x, y, lines, fnt):
    """Tops are a full line-step apart, and each line's ink clears the one above by 2px."""
    step = line_step(fnt.size)
    ys = []
    for i, line in enumerate(lines):
        cursor = y if not ys else ys[-1] + step
        if ys:
            prev_bottom = d.textbbox((x, ys[-1]), lines[i - 1], font=fnt)[3]
            ink_off = d.textbbox((0, 0), line, font=fnt)[1]
            cursor = max(cursor, prev_bottom + 2 - ink_off)
        ys.append(cursor)
    last = d.textbbox((x, ys[-1]), lines[-1], font=fnt)[3] if lines else y
    return ys, last


def tag(d, x, y, story, path, max_w, start):
    region = {"NORTH AMERICA": "N. AMERICA", "MIDDLE EAST": "M. EAST"}.get(story["region"], story["region"])
    label = f"{story['num']}  {region} · {story['field']}"
    font = fit(path, label, max_w, start, 8, d, 700)
    n = f"{story['num']}  "
    d.text((x, y), n, font=font, fill=rcol(story["region"]))
    x += d.textlength(n, font=font)
    reg = region + " · "
    d.text((x, y), reg, font=font, fill=rcol(story["region"]))
    x += d.textlength(reg, font=font)
    d.text((x, y), story["field"], font=font, fill=FIELD.get(story["field"], INK))
    return font


def card(base, _d, box, story, fonts, lead):
    x, y, w, h = (int(v) for v in box)
    layer = Image.new("RGB", (w, h), CREAM)
    d = ImageDraw.Draw(layer)
    col = rcol(story["region"])
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=4, fill=CREAM, outline=col, width=2)
    cap, chip_l, hl, dek = CARD[story["n"]]
    # Room for a 1.15em headline, a 3px gap, and the dek, inside the card.
    text_h = 104 if lead else 94
    art_h = max(44, h - text_h)
    art = (3, 3, w - 6, art_h)
    # Scene stops above the caption strip so picture text cannot be clipped by it.
    bar = 15 if art_h > 90 else 13
    paint_scene(layer, (art[0], art[1], art[2], max(24, art_h - bar)), story["n"], fonts)
    cfont = fit(fonts["sansb"], cap, art[2], 13 if lead else 10, 8, d)
    caption(d, art, cap, cfont)
    chip(d, w - 3, 3, chip_l, fonts["chip"])
    ty = 3 + art_h
    tf = tag(d, 6, ty, story, fonts["sansb"], w - 14, 13 if lead else 11)
    top = ty + tf.size
    max_w = w - 14
    hlines = hl.split("\n")[:2]
    df = fonts["dek"] if lead else fonts["dek_s"]
    full = wrap(d, dek, df, max_w) or [dek]
    start = 22 if lead else 15
    # Keep every dek line. Shrink the headline by 1px, then 2px, before trimming the dek.
    picked = None
    for limit in (len(full), min(len(full), 2)):
        for shrink in (0, 1, 2):
            hf = fit(fonts["serif"], "\n".join(hlines), max_w, start - shrink, 11, d, 900)
            hys, hbot = place_lines(d, 6, top, hlines, hf)
            dlines = full[:limit]
            dys, dbot = place_lines(d, 6, hbot + 3, dlines, df)
            if dbot <= h - 4:
                picked = (hf, hys, dys, dlines)
                break
        if picked:
            break
    if picked is None:
        hf = fit(fonts["serif"], "\n".join(hlines), max_w, max(11, start - 2), 11, d, 900)
        hys, hbot = place_lines(d, 6, top, hlines, hf)
        dlines = full[:2]
        dys, _dbot = place_lines(d, 6, hbot + 3, dlines, df)
        picked = (hf, hys, dys, dlines)
    hf, hys, dys, dlines = picked
    for yy, line in zip(hys, hlines):
        d.text((6, yy), line, font=hf, fill=HEAD)
    for yy, line in zip(dys, dlines):
        d.text((6, yy), line, font=df, fill=(22, 14, 10))
    base.paste(layer, (x, y))


def pins(d, origin, mw, mh, illustrated, also, font):
    ox, oy = origin

    def loc(s):
        return (ox + (s["lon"] + 180) / 360 * (mw - 1), oy + (75 - s["lat"]) / 131 * (mh - 1))

    for s in also:
        x, y = loc(s)
        if ox <= x <= ox + mw and oy <= y <= oy + mh:
            c = rcol(s["region"])
            d.ellipse((x - 2.4, y - 2.4, x + 2.4, y + 2.4), fill=c, outline=WHITE)
    placed = []
    for s in illustrated:
        x, y = loc(s)
        d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=INK)
        nudge = {1: (-16, -14), 4: (16, 12), 5: (-12, -10), 7: (20, -8),
                 9: (22, -2), 11: (6, -18)}.get(s["num"], (0, -12))
        bx, by = x + nudge[0], y + nudge[1]
        bx = min(ox + mw - 10, max(ox + 10, bx))
        by = min(oy + mh - 10, max(oy + 10, by))
        for k in range(12):
            if all((bx - px) ** 2 + (by - py) ** 2 >= 19 ** 2 for px, py in placed):
                break
            ang = -math.pi / 2 + k * 0.9
            bx = min(ox + mw - 10, max(ox + 10, x + math.cos(ang) * (12 + k * 2)))
            by = min(oy + mh - 10, max(oy + 10, y + math.sin(ang) * (12 + k * 2)))
        placed.append((bx, by))
        if abs(bx - x) + abs(by - y) > 6:
            d.line((x, y, bx, by), fill=INK, width=1)
        c = rcol(s["region"])
        d.ellipse((bx - 8, by - 8, bx + 8, by + 8), fill=c, outline=WHITE)
        label = str(s["num"])
        tw = d.textlength(label, font=font)
        d.text((bx - tw / 2, by - 6), label, font=font, fill=WHITE)


def render():
    illustrated, also = load()
    if len(illustrated) != 13 or len(also) != 30:
        raise SystemExit(f"counts illustrated={len(illustrated)} also={len(also)}")
    sans = face("Arimo")
    serif = face("Playfair Display")
    paths = {"sans": sans, "sansb": sans, "serif": serif}
    im = Image.new("RGB", (1024, 1024), PAPER)
    d = ImageDraw.Draw(im)
    kicker = font(sans, 13, 700)
    d.text((10, 5), "THE WORLD'S NEWS IN ONE PICTURE", font=kicker, fill=RUST)
    right = f"{len(illustrated) + len(also)} STORIES · 6 CONTINENTS · ALL FROM WEDNESDAY"
    d.text((1014 - d.textlength(right, font=kicker), 5), right, font=kicker, fill=HEAD)
    date = "Wednesday 18 November 2026"
    date_font = fit(serif, date, 1004, 52, 36, d, 900)
    dx = (1024 - d.textlength(date, font=date_font)) / 2
    dy = 20
    d.text((dx, dy), date, font=date_font, fill=HEAD)
    # Key sits under the date's real ink, not under font.size (descenders overlap that).
    rule_y = d.textbbox((dx, dy), date, font=date_font)[3] + 5
    d.line((20, rule_y, 1004, rule_y), fill=INK, width=2)
    key_font = font(sans, 12, 700)
    keys = [("Diplomacy", "DIPLOMACY"), ("War", "IRAN WAR"), ("Politics", "POLITICS"),
            ("Tech", "TECH"), ("Health", "HEALTH"), ("Climate", "CLIMATE"),
            ("Courts", "COURTS"), ("Energy", "ENERGY"), ("Sport", "SPORT")]
    widths = [16 + d.textlength(label, font=key_font) for label, _ in keys]
    kx = (1024 - (sum(widths) + 10 * (len(keys) - 1))) / 2
    ky = rule_y + 6
    for (label, fk), wlabel in zip(keys, widths):
        d.rectangle((kx, ky + 2, kx + 10, ky + 12), fill=FIELD[fk])
        d.text((kx + 13, ky), label, font=key_font, fill=HEAD)
        kx += wlabel + 10
    fonts = {"sans": sans, "sansb": sans, "serif": serif,
             "chip": font(sans, 11, 700),
             "dek": font(sans, 13, 700), "dek_s": font(sans, 11, 700)}
    footer_h, bottom_h = 44, 300
    bottom_y = 1024 - 6 - footer_h - bottom_h
    lead_y = ky + key_font.size + 8
    avail = bottom_y - 8 - lead_y
    lead_h = 208
    small_gap = 5
    small_h = (avail - lead_h - 6 - small_gap) // 2
    gap = 6
    lw = (1024 - 16 - 2 * gap) // 3
    for i, s in enumerate(illustrated[:3]):
        card(im, d, (8 + i * (lw + gap), lead_y, lw, lead_h), s, fonts, True)
    sy = lead_y + lead_h + 6
    sw = (1024 - 16 - 4 * gap) // 5
    for i, s in enumerate(illustrated[3:]):
        row, col = divmod(i, 5)
        card(im, d, (8 + col * (sw + gap), sy + row * (small_h + small_gap), sw, small_h), s, fonts, False)
    map_right = 408
    d.rounded_rectangle((8, bottom_y, map_right, bottom_y + bottom_h), radius=4, outline=(176, 164, 146), width=1)
    hfont = font(sans, 13, 700)
    d.text((16, bottom_y + 3), "WHERE IT HAPPENED", font=hfont, fill=HEAD)
    map_h = 172
    map_box = (16, bottom_y + 19, map_right - 28, map_h)
    paint_land(im, map_box)
    pins(d, (map_box[0], map_box[1]), map_box[2], map_box[3], illustrated, also,
         font(sans, 10, 700))
    # Legend sits directly under the map. Figures sit under the legend, inside the box.
    box_bottom = bottom_y + bottom_h - 6
    leg_top = map_box[1] + map_h + 4
    lf_size, title_size, num_size, cap_size = 12, 11, 16, 9
    while True:
        lstep = line_step(lf_size)
        title_y = leg_top + 2 * lstep + 4
        num_y = title_y + line_step(title_size) + 2
        cap_y = num_y + line_step(num_size) + 2
        end = cap_y + line_step(cap_size)
        if end <= box_bottom or num_size <= 13:
            break
        num_size -= 1
    lf = font(sans, lf_size, 700)
    tf = font(sans, title_size, 700)
    nf = font(serif, num_size, 900)
    cf = font(sans, cap_size, 700)
    for i, (name, col) in enumerate(REG.items()):
        lx = 16 + (i % 3) * 128
        ly = leg_top + (i // 3) * lstep
        d.ellipse((lx, ly + 2, lx + 9, ly + 11), fill=col)
        d.text((lx + 13, ly), name, font=lf, fill=HEAD)
    d.text((16, title_y), "THE DAY IN FIGURES", font=tf, fill=RUST)
    figures = [("21", "ECONOMIES"), ("$116BN", "REVENUE"), ("56–44", "SENATE"), ("330", "MONTHS")]
    title_bot = d.textbbox((16, title_y), "THE DAY IN FIGURES", font=tf)[3]
    num_off = min(d.textbbox((0, 0), num, font=nf)[1] for num, _cap in figures)
    num_y = max(num_y, title_bot + 3 - num_off)
    slot = (map_right - 24) / 4
    for i, (num, _cap) in enumerate(figures):
        cx = 16 + i * slot + slot / 2
        tw = d.textlength(num, font=nf)
        d.text((cx - tw / 2, num_y), num, font=nf, fill=HEAD)
    num_bot = max(d.textbbox((0, num_y), num, font=nf)[3] for num, _cap in figures)
    cap_off = d.textbbox((0, 0), "ECONOMIES", font=cf)[1]
    cap_y = max(cap_y, num_bot + 3 - cap_off)
    for i, (_num, cap) in enumerate(figures):
        cx = 16 + i * slot + slot / 2
        tw = d.textlength(cap, font=cf)
        d.text((cx - tw / 2, cap_y), cap, font=cf, fill=HEAD)
    ax = 414
    d.rounded_rectangle((ax, bottom_y, 1016, bottom_y + bottom_h), radius=4, outline=(176, 164, 146), width=1)
    d.text((ax + 8, bottom_y + 3), "ALSO ON WEDNESDAY 18 NOVEMBER", font=hfont, fill=HEAD)
    af = font(sans, 12, 700)
    col_w = (1016 - ax - 16) / 2
    longest = max(ALSO.values(), key=len)
    while af.size > 10 and d.textlength("43  " + longest, font=af) > col_w - 4:
        af = font(sans, af.size - 1, 700)
    top = bottom_y + 22
    row_h = (bottom_h - 28) / 15
    for i, s in enumerate(also):
        col, row = divmod(i, 15)
        xx = ax + 8 + col * (col_w + 6)
        yy = top + row * row_h
        num = str(s["num"])
        d.text((xx, yy), num, font=af, fill=rcol(s["region"]))
        d.text((xx + d.textlength(num, font=af) + 3, yy), ALSO[s["n"]], font=af, fill=HEAD)
    src = ("Sources: AP, BNN Bloomberg, Dawn, GhanaWeb, Inquirer, NBC News, The Nation, "
           "New York Times, Nikkei Asia, PBS, Philstar, Religion Media Centre, Reuters, "
           "SBS, TechCrunch, allAfrica. Original drawings.")
    sf = font(sans, 11, 600)
    fy = bottom_y + bottom_h + 3
    for i, line in enumerate(wrap(d, src, sf, 1004)[:2]):
        d.text((10, fy + i * 13), line, font=sf, fill=MUTED)
    jy = fy + 27
    d.rounded_rectangle((8, jy, 1016, min(1022, jy + 16)), radius=2, outline=RUST, width=1)
    note = ("JUDGE NOTE   Every story happened or was first reported on Wednesday 18 November 2026. "
            "Disputed claims are attributed.")
    nf = fit(sans, note, 996, 11, 9, d, 700)
    d.text((14, jy + 2), note, font=nf, fill=INK)
    raw = ROOT / "build" / "raw.png"
    im.save(raw)
    keep = [(240, 196, 0), (26, 86, 196), (176, 32, 36)] + list(REG.values()) + list(FIELD.values())
    base = im.quantize(colors=128 - len(keep), method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal = base.getpalette()
    colors = [(pal[i * 3], pal[i * 3 + 1], pal[i * 3 + 2]) for i in range(128 - len(keep))]
    for pin in keep:
        if pin not in colors:
            colors.append(pin)
    flat = [c for rgb in colors for c in rgb]
    flat.extend([0, 0, 0] * (256 - len(colors)))
    palette = Image.new("P", (1, 1))
    palette.putpalette(flat)
    q = im.quantize(palette=palette, dither=Image.Dither.NONE)
    out = ROOT / "entry.png"
    q.save(out, format="PNG", optimize=True)
    small = im.resize((300, 300), Image.Resampling.LANCZOS)
    small.save(ROOT / "build" / "at300.png")
    check = Image.open(out)
    size = out.stat().st_size
    print(f"entry.png {check.size} {check.mode} {size} bytes colors={len(check.getcolors(256) or [])}")
    if check.size != (1024, 1024) or size >= 1_000_000:
        raise SystemExit("gate failed")


if __name__ == "__main__":
    render()
