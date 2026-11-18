"""Flat scenes for the 13 illustrated cards. Coordinates are 0–100."""
import math
from PIL import Image, ImageDraw, ImageFont

INK = (28, 20, 14)
RED = (176, 32, 36)
GOLD = (240, 196, 0)
WHITE = (255, 252, 246)
NAVY = (18, 52, 118)
GREEN = (16, 122, 70)
SKY = (196, 220, 234)
SAND = (232, 210, 170)
SEA = (120, 176, 204)


class R:
    def __init__(self, d, w, h):
        self.d, self.w, self.h = d, w, h

    def p(self, x, y):
        return (x / 100 * self.w, y / 100 * self.h)

    def box(self, x, y, w, h):
        a, b = self.p(x, y)
        c, e = self.p(x + w, y + h)
        return (a, b, c, e)

    def rect(self, x, y, w, h, fill, outline=None):
        self.d.rectangle(self.box(x, y, w, h), fill=fill, outline=outline)

    def poly(self, pts, fill, outline=None):
        self.d.polygon([self.p(x, y) for x, y in pts], fill=fill, outline=outline)

    def oval(self, x, y, w, h, fill, outline=None):
        self.d.ellipse(self.box(x, y, w, h), fill=fill, outline=outline)

    def line(self, pts, fill, width):
        self.d.line([self.p(x, y) for x, y in pts], fill=fill, width=max(1, int(width)))

    def text(self, x, y, s, font, fill):
        self.d.text(self.p(x, y), s, font=font, fill=fill)

    def px(self, fonts, rel, bold=True):
        path = fonts["sansb"] if bold else fonts["sans"]
        return _font(path, max(8, int(self.h * rel)), 700 if bold else 400)


def _sky(r):
    r.rect(0, 0, 100, 100, SKY)
    r.rect(0, 68, 100, 32, SAND)


def _star(r, cx, cy, rad, fill):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = rad if i % 2 == 0 else rad * 0.4
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    r.poly(pts, fill)


def _flag_cn(r, x, y, w, h):
    r.rect(x, y, w, h, RED, INK)
    _star(r, x + w * 0.28, y + h * 0.32, min(w, h) * 0.22, GOLD)


def _flag_kw(r, x, y, w, h):
    r.rect(x, y, w, h / 3, GREEN)
    r.rect(x, y + h / 3, w, h / 3, WHITE)
    r.rect(x, y + 2 * h / 3, w, h / 3, RED)
    r.poly([(x, y), (x + w * 0.32, y + h / 2), (x, y + h)], INK)


def _flag_kr(r, x, y, w, h):
    r.rect(x, y, w, h, WHITE, INK)
    r.oval(x + w * 0.28, y + h * 0.18, w * 0.44, h * 0.64, RED)
    r.d.pieslice(r.box(x + w * 0.28, y + h * 0.18, w * 0.44, h * 0.64), 200, 20, fill=(26, 86, 196))


def _flag_uk(r, x, y, w, h):
    r.rect(x, y, w, h, NAVY)
    r.rect(x, y + h * 0.38, w, h * 0.24, WHITE)
    r.rect(x + w * 0.38, y, w * 0.24, h, WHITE)
    r.rect(x, y + h * 0.44, w, h * 0.12, RED)
    r.rect(x + w * 0.44, y, w * 0.12, h, RED)


def _font(path, size, weight=700):
    font = ImageFont.truetype(path, max(8, int(size)))
    try:
        font.set_variation_by_axes([int(weight)])
    except OSError:
        pass
    return font


def _centered(d, r, text, cx, cy, rel, fill, fonts):
    size = max(8, int(r.h * rel))
    font = _font(fonts["sansb"], size, 700)
    tw = d.textlength(text, font=font)
    d.text((cx / 100 * r.w - tw / 2, cy / 100 * r.h), text, font=font, fill=fill)


def _person(r, x, y, s=1):
    r.oval(x, y, 9 * s, 10 * s, (214, 176, 140))
    r.rect(x + 0.5 * s, y, 8 * s, 3.8 * s, INK)
    r.poly([(x - 3 * s, y + 22 * s), (x + 4.5 * s, y + 9.4 * s), (x + 12 * s, y + 22 * s)], (28, 40, 84))
    r.poly([(x + 3.2 * s, y + 10 * s), (x + 5.8 * s, y + 10 * s),
            (x + 5.2 * s, y + 17 * s), (x + 3.8 * s, y + 17 * s)], WHITE)


def _drone(r, x, y):
    r.poly([(x, y + 4), (x + 16, y + 2), (x + 18, y + 6), (x + 2, y + 8)], (70, 74, 80))
    r.line([(x + 4, y), (x + 14, y + 10)], RED, r.h * 0.06)
    r.line([(x + 14, y), (x + 4, y + 10)], RED, r.h * 0.06)


def _houses(r, x, y):
    for i in range(4):
        r.poly([(x + i * 9, y + 8), (x + 4 + i * 9, y), (x + 8 + i * 9, y + 8)], RED)
        r.rect(x + 1 + i * 9, y + 8, 6, 8, SAND, INK)


def _flags21(r, x, y):
    cols = [(176, 32, 36), (26, 86, 196), (16, 122, 70), GOLD, NAVY,
            (14, 118, 128), (196, 96, 24), (104, 58, 164), (22, 118, 70)]
    n = 0
    for row in range(3):
        for col in range(7):
            c = cols[n % len(cols)]
            fx, fy = x + col * 5.2, y + row * 9
            r.rect(fx, fy, 4.2, 6.4, c, INK)
            r.rect(fx, fy, 1.3, 6.4, WHITE if c != WHITE else RED)
            n += 1


def scene1(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, SKY)
    r.rect(0, 74, 100, 26, (176, 158, 130))
    _flag_cn(r, 2, 8, 14, 34)
    _person(r, 30, 16, 1.15)
    r.line([(48, 36), (48, 24)], (50, 52, 56), max(2, r.h * 0.035))
    r.oval(46.2, 20, 3.6, 5.5, (50, 52, 56))
    r.poly([(22, 76), (28, 44), (50, 44), (56, 76)], (122, 74, 46))
    r.rect(26, 40, 26, 6, (92, 56, 34))
    r.rect(23, 50, 34, 24, (148, 28, 32), INK)
    _centered(d, r, "APEC 2026", 40, 52, 0.11, WHITE, fonts)
    _centered(d, r, "SHENZHEN", 40, 64, 0.10, WHITE, fonts)
    _flags21(r, 63, 26)


def _kw_tower(r, x, top, tall):
    r.rect(x + 2.4, top, 1.5, 70 - top, (236, 238, 240))
    r.oval(x, top + 16, 6.2, 14, (64, 138, 176), INK)
    if tall:
        r.oval(x + 1.1, top + 6, 4, 9, (150, 196, 214), INK)
        r.line([(x + 3.1, top + 6), (x + 3.1, top - 6)], (236, 238, 240), max(2, r.h * 0.03))


def scene2(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 58, SKY)
    r.rect(0, 56, 100, 44, SEA)
    r.poly([(0, 64), (22, 52), (48, 60), (78, 50), (100, 58), (100, 78), (0, 82)], SAND)
    _flag_kw(r, 3, 6, 16, 26)
    _kw_tower(r, 24, 18, True)
    _kw_tower(r, 34, 26, False)
    r.rect(46, 36, 7, 28, (168, 176, 182), INK)
    r.rect(47.2, 40, 1.6, 3, (90, 150, 180))
    r.rect(50.2, 40, 1.6, 3, (90, 150, 180))
    r.rect(47.2, 46, 1.6, 3, (90, 150, 180))
    r.rect(55, 42, 6, 22, (140, 148, 154), INK)
    r.rect(70, 66, 12, 5, (60, 68, 62), INK)
    r.poly([(80, 66), (92, 60), (92, 66)], (48, 52, 48))
    r.line([(84, 63), (48, 16)], GOLD, max(2, r.h * 0.04))
    r.line([(86, 64), (68, 24)], (255, 214, 64), max(2, r.h * 0.035))
    _drone(r, 40, 8)
    r.oval(38, 4, 18, 16, None, RED)
    _drone(r, 60, 16)
    r.line([(62, 18), (76, 30)], RED, max(2, r.h * 0.045))
    r.line([(76, 18), (62, 30)], RED, max(2, r.h * 0.045))


def scene3(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, (214, 220, 226))
    r.rect(3, 4, 58, 50, (232, 236, 238), INK)
    heights = (22, 30, 38, 46)
    for i, bh in enumerate(heights):
        r.rect(7 + i * 9, 50 - bh, 7, bh, (20, 118, 64) if i < 3 else (12, 86, 48), INK)
    _centered(d, r, "$116BN", 24, 6, 0.18, INK, fonts)
    r.rect(66, 10, 24, 26, (20, 122, 68), INK)
    for i in range(4):
        r.rect(69, 14 + i * 5, 18, 2.2, (186, 224, 186))
    for i in range(5):
        r.rect(63.5, 12 + i * 5, 2.8, 1.8, GOLD)
        r.rect(89.5, 12 + i * 5, 2.8, 1.8, GOLD)
    r.poly([(4, 86), (96, 86), (88, 60), (12, 60)], (124, 78, 48))
    r.line([(12, 60), (88, 60)], (90, 56, 32), max(2, r.h * 0.04))
    r.rect(40, 64, 22, 14, WHITE, INK)
    _centered(d, r, "CEO", 51, 66, 0.16, INK, fonts)
    r.line([(42, 66), (60, 76)], RED, max(2, r.h * 0.045))
    r.line([(60, 66), (42, 76)], RED, max(2, r.h * 0.045))


def scene4(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, SKY)
    r.rect(0, 70, 100, 30, (186, 170, 146))
    _flag_cn(r, 2, 6, 16, 28)
    _flag_kr(r, 20, 6, 16, 28)
    r.poly([(62, 14), (74, 12), (78, 36), (82, 72), (68, 74), (64, 40)], (120, 158, 120), INK)
    _person(r, 4, 30, 1.05)
    _person(r, 32, 30, 1.05)
    r.poly([(6, 84), (54, 84), (48, 66), (12, 66)], (110, 70, 44))
    for i, col in enumerate(((32, 96, 170), (28, 140, 78), (190, 140, 36))):
        r.rect(16 + i * 11, 68, 8, 9, col, INK)
        if i:
            r.line([(16 + i * 11 - 3, 72), (16 + i * 11, 72)], INK, 2)


def scene5(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, SKY)
    r.rect(0, 78, 100, 22, (168, 186, 150))
    r.rect(4, 46, 18, 32, WHITE, INK)
    r.rect(40, 46, 18, 32, WHITE, INK)
    r.poly([(16, 46), (31, 22), (46, 46)], WHITE, INK)
    r.rect(22, 40, 18, 38, WHITE, INK)
    for i in range(4):
        r.rect(24 + i * 4, 48, 2.2, 22, (186, 196, 206))
    r.rect(48, 18, 4, 10, (40, 70, 140))
    r.rect(46, 16, 8, 3, RED)
    r.rect(54, 28, 40, 22, (250, 244, 226), INK)
    _centered(d, r, "OVERTON", 74, 32, 0.16, INK, fonts)
    r.poly([(62, 64), (94, 64), (98, 84), (58, 84)], (96, 74, 52), INK)
    r.line([(78, 68), (90, 80)], RED, max(2, r.h * 0.045))
    r.line([(90, 68), (78, 80)], RED, max(2, r.h * 0.045))


def scene6(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, (214, 228, 234))
    r.poly([(2, 58), (14, 40), (28, 34), (40, 40), (48, 30), (54, 46),
            (46, 58), (52, 78), (40, 68), (26, 74), (12, 62), (4, 70)], (64, 124, 156), INK)
    r.oval(6, 66, 4, 3, (64, 124, 156), INK)
    r.oval(12, 70, 3.4, 2.6, (64, 124, 156), INK)
    r.rect(60, 40, 22, 32, (24, 52, 104), INK)
    r.rect(58, 34, 26, 8, (16, 36, 78))
    r.rect(66, 36, 10, 2.4, (8, 14, 28))
    r.rect(66, 16, 10, 20, WHITE, INK)
    r.line([(68, 22), (74, 22)], INK, max(1, int(r.h * 0.025)))
    r.line([(68, 26), (74, 26)], INK, max(1, int(r.h * 0.025)))
    _centered(d, r, "56-44", 78, 78, 0.22, INK, fonts)


def scene7(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, (236, 228, 218))
    r.rect(5, 28, 7, 32, (214, 220, 224), INK)
    r.rect(6.4, 16, 4.2, 14, (70, 76, 82))
    r.poly([(7.2, 60), (9.8, 60), (8.5, 78)], (150, 160, 168), INK)
    r.rect(6.6, 22, 3.8, 3, RED)
    # US with a Florida point, Mexico with Baja, Bolivia
    r.poly([(24, 22), (40, 20), (42, 34), (38, 36), (40, 48), (30, 46), (22, 36)], (70, 116, 164), INK)
    r.poly([(46, 28), (52, 24), (58, 30), (62, 48), (50, 52), (44, 40)], (36, 130, 78), INK)
    r.poly([(44, 34), (46, 30), (48, 40)], (36, 130, 78))
    r.poly([(74, 24), (86, 28), (84, 52), (72, 48)], (190, 148, 40), INK)
    for x, y in ((32, 30), (54, 36), (78, 36)):
        r.oval(x, y, 5, 5, RED)
    f = r.px(fonts, 0.16)
    r.text(28, 58, "US", f, INK)
    r.text(48, 58, "MEX", f, INK)
    r.text(74, 58, "BOL", f, INK)


def scene8(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, SKY)
    r.oval(2, 6, 16, 26, GOLD)
    # Cape York, gulf bite, southern coast, Tasmania
    r.poly([(28, 18), (36, 14), (40, 28), (52, 26), (62, 36), (66, 52),
            (54, 64), (40, 60), (30, 66), (22, 52), (24, 36)], (36, 140, 88), INK)
    r.oval(48, 64, 8, 6, (36, 140, 88), INK)
    r.rect(70, 22, 26, 52, WHITE, INK)
    r.rect(73, 28, 20, 2, (180, 176, 160))
    r.rect(73, 34, 16, 2, (180, 176, 160))
    _centered(d, r, "2030", 83, 44, 0.24, RED, fonts)
    _centered(d, r, "NET ZERO", 83, 64, 0.12, INK, fonts)


def scene9(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, (214, 220, 224))
    lamps = (GREEN, GOLD, GREEN)
    for i, lamp in enumerate(lamps):
        x = 6 + i * 22
        r.rect(x, 14, 16, 62, (32, 40, 50), INK)
        for row in range(5):
            for col in range(3):
                r.rect(x + 2 + col * 4, 28 + row * 8, 2.6, 4, (70, 150, 90) if lamp == GREEN else (90, 96, 70))
        r.oval(x + 4, 16, 8, 8, lamp, INK)
    r.line([(74, 28), (88, 44), (76, 44), (92, 64)], GREEN, max(3, r.h * 0.07))


def scene10(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, (236, 228, 210))
    _flag_uk(r, 3, 8, 20, 32)
    r.poly([(30, 28), (52, 10), (58, 20), (36, 38)], (122, 78, 42), INK)
    r.rect(46, 30, 18, 5, (92, 58, 32))
    _houses(r, 3, 52)
    _centered(d, r, "1,200+", 76, 48, 0.26, RED, fonts)


def scene11(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, (226, 220, 208))
    r.rect(2, 36, 48, 16, (118, 74, 44), INK)
    r.rect(0, 50, 52, 8, (82, 52, 30))
    r.poly([(6, 30), (34, 12), (40, 20), (12, 38)], (102, 68, 40), INK)
    r.line([(16, 32), (8, 70)], (72, 46, 28), max(3, r.h * 0.07))
    r.rect(56, 22, 40, 58, WHITE, INK)
    _centered(d, r, "330", 76, 28, 0.32, INK, fonts)
    _centered(d, r, "MONTHS", 76, 60, 0.15, RED, fonts)


def scene12(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, SKY)
    r.poly([(2, 28), (26, 18), (32, 72), (4, 78)], SAND, INK)
    r.poly([(68, 22), (98, 16), (99, 74), (66, 70)], (150, 186, 120), INK)
    r.line([(28, 48), (70, 42)], (36, 96, 168), max(4, r.h * 0.07))
    r.oval(40, 36, 14, 20, (196, 96, 36), INK)
    r.line([(44, 40), (50, 52)], (90, 50, 24), max(2, r.h * 0.04))
    r.poly([(64, 34), (76, 42), (64, 50)], RED)
    r.rect(78, 28, 12, 16, WHITE, INK)
    r.rect(78, 50, 12, 16, WHITE, INK)
    r.line([(80, 36), (88, 36)], INK, 1)
    r.line([(80, 58), (88, 58)], INK, 1)


def scene13(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, (206, 216, 200))
    r.rect(4, 8, 14, 16, RED, INK)
    r.rect(4, 13, 14, 5.2, GOLD)
    r.rect(4, 18.2, 14, 5.8, GREEN)
    r.rect(6, 18, 2, 28, (70, 74, 78))
    r.rect(2, 14, 10, 4, (250, 236, 170))
    r.rect(88, 18, 2, 28, (70, 74, 78))
    r.rect(84, 14, 10, 4, (250, 236, 170))
    r.poly([(8, 58), (50, 34), (92, 58), (92, 70), (8, 70)], (120, 130, 124), INK)
    for i, x in enumerate((16, 28, 40, 58, 70, 82)):
        r.oval(x, 42, 6, 6, RED if i % 2 == 0 else GOLD)
    r.oval(22, 62, 52, 28, (34, 130, 64), WHITE)
    r.line([(48, 64), (48, 88)], WHITE, max(2, r.h * 0.03))
    # fans in a scuffle, police with a shield between them
    r.oval(24, 66, 7, 7, (40, 36, 32))
    r.rect(25, 73, 5, 10, RED)
    r.oval(40, 62, 7, 7, (230, 236, 240))
    r.rect(41, 69, 5, 12, (24, 58, 140))
    r.rect(46, 70, 5, 8, (180, 190, 200), INK)
    r.oval(56, 66, 7, 7, (40, 36, 32))
    r.rect(57, 73, 5, 10, GOLD)
    r.line([(30, 76), (40, 74)], RED, max(2, r.h * 0.04))


SCENES = {
    1: scene1, 2: scene2, 3: scene3, 4: scene4, 5: scene5, 6: scene6,
    7: scene7, 8: scene8, 9: scene9, 10: scene10, 11: scene11, 12: scene12,
    35: scene13,
}


def paint_scene(base, box, n, fonts):
    x, y, w, h = (int(round(v)) for v in box)
    im = Image.new("RGB", (max(1, w), max(1, h)), (251, 247, 240))
    SCENES[n](ImageDraw.Draw(im), im.size[0], im.size[1], fonts)
    base.paste(im, (x, y))
