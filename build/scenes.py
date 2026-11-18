"""Flat scenes for the 13 illustrated cards. Coordinates are 0–100."""
import math
from PIL import Image, ImageDraw, ImageFont

INK = (28, 20, 14)
RED = (176, 32, 36)
GOLD = (228, 176, 32)
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
        return ImageFont.truetype(path, max(8, int(self.h * rel)))


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
    r.d.pieslice(r.box(x + w * 0.28, y + h * 0.18, w * 0.44, h * 0.64), 200, 20, fill=(20, 70, 170))


def _flag_uk(r, x, y, w, h):
    r.rect(x, y, w, h, NAVY)
    r.rect(x, y + h * 0.38, w, h * 0.24, WHITE)
    r.rect(x + w * 0.38, y, w * 0.24, h, WHITE)
    r.rect(x, y + h * 0.44, w, h * 0.12, RED)
    r.rect(x + w * 0.44, y, w * 0.12, h, RED)


def _person(r, x, y, s=1):
    r.oval(x, y, 7 * s, 8 * s, INK)
    r.rect(x - 1.5 * s, y + 8 * s, 10 * s, 14 * s, (40, 60, 110))


def _drone(r, x, y):
    r.poly([(x, y + 4), (x + 16, y + 2), (x + 18, y + 6), (x + 2, y + 8)], (70, 74, 80))
    r.line([(x + 4, y), (x + 14, y + 10)], RED, r.h * 0.06)
    r.line([(x + 14, y), (x + 4, y + 10)], RED, r.h * 0.06)


def _houses(r, x, y):
    for i in range(4):
        r.poly([(x + i * 9, y + 8), (x + 4 + i * 9, y), (x + 8 + i * 9, y + 8)], RED)
        r.rect(x + 1 + i * 9, y + 8, 6, 8, SAND, INK)


def scene1(d, w, h, fonts):
    r = R(d, w, h)
    _sky(r)
    _flag_cn(r, 4, 16, 16, 42)
    _person(r, 30, 28)
    r.rect(26, 50, 16, 18, (120, 72, 48))
    r.rect(24, 66, 20, 4, (90, 54, 36))
    r.rect(70, 28, 3, 40, (90, 70, 48))
    r.rect(90, 28, 3, 40, (90, 70, 48))
    r.rect(68, 20, 26, 5, GOLD)
    for i in range(7):
        a = math.radians(200 + i * 20)
        x, y = 48 + 28 * math.cos(a), 18 + 16 * math.sin(a) * -1
        r.poly([(x, y), (x + 3, y + 5), (x - 2, y + 4)], RED)


def scene2(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, SKY)
    r.rect(0, 58, 100, 42, SEA)
    r.poly([(0, 62), (28, 48), (58, 60), (100, 46), (100, 70), (0, 78)], SAND)
    _flag_kw(r, 4, 8, 20, 32)
    _drone(r, 36, 14)
    _drone(r, 56, 28)
    r.line([(78, 70), (78, 48)], INK, r.h * 0.04)
    r.poly([(70, 48), (86, 48), (78, 38)], (70, 78, 90))
    r.oval(62, 28, 22, 16, None, RED)


def scene3(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, (232, 240, 232))
    r.rect(6, 22, 46, 56, (24, 120, 64), INK)
    for i in range(5):
        r.rect(10, 28 + i * 9, 38, 4, (180, 220, 180))
    r.oval(58, 18, 34, 50, None)
    r.line([(64, 28), (86, 56)], RED, r.h * 0.07)
    r.line([(86, 28), (64, 56)], RED, r.h * 0.07)
    r.text(60, 68, "$116BN", r.px(fonts, 0.28), INK)


def scene4(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, SKY)
    _flag_cn(r, 3, 10, 18, 36)
    _flag_kr(r, 24, 10, 18, 36)
    r.poly([(58, 18), (70, 16), (74, 40), (78, 78), (64, 80), (60, 48)], (150, 170, 140))
    for i, col in enumerate(((40, 90, 160), (40, 140, 80), (200, 140, 40))):
        r.rect(8 + i * 16, 62, 12, 16, col, INK)
        if i:
            r.line([(8 + i * 16 - 4, 70), (8 + i * 16, 70)], INK, 2)


def scene5(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, SKY)
    r.poly([(6, 42), (28, 16), (50, 42)], WHITE)
    r.rect(10, 42, 36, 36, WHITE, INK)
    for i in range(4):
        r.rect(14 + i * 8, 48, 3, 24, (200, 206, 214))
    r.rect(58, 36, 34, 14, (244, 236, 214), INK)
    r.text(60, 38, "OVERTON", r.px(fonts, 0.16), INK)
    r.poly([(78, 58), (96, 58), (96, 78), (74, 78)], (90, 70, 56))
    r.line([(74, 48), (80, 60)], RED, r.h * 0.05)


def scene6(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, (226, 236, 242))
    r.poly([(4, 28), (22, 16), (40, 26), (34, 48), (46, 64), (28, 80), (6, 70), (2, 46)], (70, 120, 150))
    label = "56–44"
    size = max(11, int(h * 0.36))
    f = ImageFont.truetype(fonts["sansb"], size)
    while size > 10 and d.textlength(label, font=f) > w * 0.48:
        size -= 1
        f = ImageFont.truetype(fonts["sansb"], size)
    tw = d.textlength(label, font=f)
    d.text((w * 0.50, h * 0.32), label, font=f, fill=INK)


def scene7(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, (236, 228, 220))
    r.rect(4, 28, 6, 28, (180, 190, 200), INK)
    r.poly([(2, 28), (12, 28), (7, 18)], (200, 60, 60))
    blobs = [(22, (70, 110, 160), "US"), (48, (40, 130, 80), "MEX"), (74, (190, 150, 40), "BOL")]
    f = r.px(fonts, 0.2)
    for x, col, name in blobs:
        r.oval(x, 22, 20, 28, col, INK)
        r.oval(x + 6, 30, 5, 5, RED)
        r.text(x + 2, 56, name, f, INK)


def scene8(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, SKY)
    r.oval(4, 8, 22, 36, GOLD)
    r.poly([(28, 30), (40, 22), (58, 26), (62, 48), (48, 62), (32, 58), (26, 44)], (40, 140, 90))
    r.rect(66, 18, 28, 48, WHITE, INK)
    r.text(68, 28, "2030", r.px(fonts, 0.28), RED)


def scene9(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, (220, 226, 230))
    for i, lamp in enumerate((GREEN, GOLD, GREEN)):
        r.rect(8 + i * 20, 16, 16, 58, (36, 44, 56), INK)
        r.oval(12 + i * 20, 24, 8, 12, lamp)
    r.line([(74, 30), (90, 48), (78, 48), (94, 68)], GREEN, r.h * 0.07)


def scene10(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, (236, 230, 214))
    _flag_uk(r, 4, 12, 22, 36)
    r.poly([(32, 18), (52, 8), (56, 16), (36, 26)], (110, 72, 40))
    r.rect(48, 24, 16, 4, (110, 72, 40))
    _houses(r, 4, 58)
    r.text(62, 48, "1,200", r.px(fonts, 0.3), RED)


def scene11(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, (228, 224, 216))
    r.rect(4, 28, 46, 28, (92, 64, 42), INK)
    r.rect(8, 18, 6, 14, (70, 48, 32))
    r.rect(40, 18, 6, 14, (70, 48, 32))
    r.rect(58, 16, 36, 50, WHITE, INK)
    r.text(60, 28, "330", r.px(fonts, 0.38), INK)


def scene12(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, SKY)
    r.poly([(2, 30), (24, 22), (28, 70), (4, 74)], SAND)
    r.poly([(70, 26), (96, 20), (98, 72), (68, 68)], (170, 196, 140))
    r.line([(26, 48), (72, 44)], (40, 90, 160), r.h * 0.06)
    r.poly([(68, 38), (80, 44), (68, 50)], RED)
    r.oval(44, 38, 10, 16, (200, 80, 40), INK)
    r.text(36, 62, "2 PACTS", r.px(fonts, 0.22), INK)


def scene13(d, w, h, fonts):
    r = R(d, w, h)
    r.rect(0, 0, 100, 100, (226, 232, 220))
    r.line([(8, 70), (50, 16), (92, 70)], INK, max(2, r.h * 0.045))
    r.line([(8, 70), (92, 70)], INK, r.h * 0.05)
    r.rect(6, 8, 16, 12, RED)
    r.rect(6, 12, 16, 4, GOLD)
    r.rect(6, 16, 16, 4, GREEN)
    for i, x in enumerate((30, 42, 62, 74)):
        r.oval(x, 40, 8, 10, INK)
        r.line([(x + 4, 50), (x + 4, 68)], INK, 2)
    r.line([(38, 56), (64, 52)], RED, r.h * 0.05)


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
