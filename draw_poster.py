#!/usr/bin/env python3
"""Draw the news-image-20261122 poster (1024x1024 PNG) with PIL.

Run locally (PIL is NOT available in the grader sandbox, so the graded
entrypoint main.py only copies the finished entry.png -- see main.py):

    python3 draw_poster.py

Writes entry.png next to this script. Deterministic: same bytes every run
(fixed fonts, no timestamps, no randomness).

Poster: "THE WORLD IN ONE DAY" -- Sunday, 22 November 2026, four stories:
  1. COP31 climate talks collapse in Antalya (no deal, fossil fuels omitted)
  2. Iran strikes tankers near the Strait of Hormuz and a US base in Bahrain
  3. Marc Marquez clinches his eighth MotoGP title at the Portuguese GP
  4. Candy factory fire in Cikande, Indonesia: 3 dead, 36 missing
All illustrations are flat original drawings made from PIL primitives.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (246, 241, 231)      # warm newsprint
INK = (26, 26, 26)
RED = (178, 34, 30)
NAVY = (23, 48, 84)
TEAL = (14, 110, 110)
GOLD = (176, 124, 18)
GREY = (90, 86, 78)
WHITE = (255, 255, 255)
PANEL = (255, 253, 247)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_panel(d, x, y, w, h, tag, color, headline, sub, art):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10,
                        fill=PANEL, outline=(200, 192, 175), width=2)
    # tag band
    d.rounded_rectangle([x, y, x + w, y + 46], radius=10, fill=color)
    d.rectangle([x, y + 30, x + w, y + 46], fill=color)  # square off bottom
    d.text((x + 18, y + 10), tag, font=SANS_B(24), fill=WHITE)
    # illustration area
    art(d, x, y + 46, w, 150)
    # headline
    hy = y + 46 + 150 + 10
    hl = wrap(d, headline, SANS_B(29), w - 36)
    for line in hl[:2]:
        d.text((x + 18, hy), line, font=SANS_B(29), fill=INK)
        hy += 34
    # subtext
    sy = hy + 6
    for line in wrap(d, sub, SANS(20), w - 36)[:3]:
        d.text((x + 18, sy), line, font=SANS(20), fill=(64, 60, 52))
        sy += 25


# ---- illustrations (flat original art, PIL primitives only) ----

def art_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 240))
    cx, cy, r = x + w // 2, y + h // 2 + 6, 62
    # sun
    sx, sy = x + w - 78, y + 34
    d.ellipse([sx - 20, sy - 20, sx + 20, sy + 20], fill=(240, 180, 40))
    for ang in range(0, 360, 45):
        import math
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d.line([sx + dx * 26, sy + dy * 26, sx + dx * 36, sy + dy * 36],
               fill=(240, 180, 40), width=4)
    # globe
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 120, 190),
              outline=NAVY, width=3)
    d.ellipse([cx - 34, cy - 40, cx + 2, cy - 8], fill=(74, 160, 90))
    d.ellipse([cx - 6, cy + 6, cx + 38, cy + 42], fill=(74, 160, 90))
    d.ellipse([cx + 8, cy - 46, cx + 34, cy - 22], fill=(74, 160, 90))
    # crack across the globe
    d.line([cx - 44, cy - 18, cx - 18, cy + 4, cx - 30, cy + 22,
            cx - 2, cy + 40], fill=RED, width=6)
    d.line([cx + 44, cy - 30, cx + 20, cy - 8, cx + 34, cy + 12],
           fill=RED, width=6)


def art_gulf(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 214, 150))  # dusk sky
    d.ellipse([x + w - 90, y + 18, x + w - 30, y + 78],
              fill=(240, 140, 40))  # low sun
    # sea
    d.rectangle([x, y + 108, x + w, y + h], fill=(28, 80, 130))
    for wy in (y + 122, y + 142):
        for wx in range(x + 8, x + w - 20, 44):
            d.arc([wx, wy, wx + 36, wy + 18], 180, 360,
                  fill=(150, 200, 230), width=4)
    # tanker
    hx, hy = x + 60, y + 78
    d.polygon([(hx, hy), (hx + 300, hy), (hx + 280, hy + 34),
               (hx + 16, hy + 34)], fill=(60, 60, 66))
    d.rectangle([hx + 30, hy - 26, hx + 90, hy], fill=(200, 60, 50))
    d.rectangle([hx + 110, hy - 26, hx + 170, hy], fill=(240, 200, 60))
    d.rectangle([hx + 190, hy - 26, hx + 250, hy], fill=(70, 140, 90))
    d.rectangle([hx + 268, hy - 52, hx + 292, hy], fill=(40, 40, 46))
    # missile arc removed: tanker + sea + sun carry the story cleanly


def art_motogp(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 28))
    # checkered flag strip
    sq = 21
    for r in range(2):
        for c in range(10):
            col = WHITE if (r + c) % 2 == 0 else INK
            d.rectangle([x + 18 + c * sq, y + 14 + r * sq,
                         x + 18 + (c + 1) * sq, y + 14 + (r + 1) * sq],
                        fill=col)
    # gold champion badge with 8
    bx, by = x + w - 104, y + 44
    d.ellipse([bx, by, bx + 76, by + 76], fill=(212, 160, 40),
              outline=(255, 220, 120), width=4)
    d.text((bx + 26, by + 12), "8", font=SANS_B(48), fill=(60, 40, 0))
    d.text((bx + 2, by + 82), "CHAMPION", font=SANS_B(15), fill=GOLD)
    # stylised racing bike: two wheels + frame + rider lean
    import math
    wx1, wx2, wy = x + 110, x + 330, y + 122
    for wx in (wx1, wx2):
        d.ellipse([wx - 30, wy - 30, wx + 30, wy + 30], outline=WHITE,
                  width=6)
        d.ellipse([wx - 8, wy - 8, wx + 8, wy + 8], fill=WHITE)
    d.line([wx1, wy, x + 210, wy - 34, wx2, wy], fill=RED, width=7)
    d.line([wx2, wy, x + 300, wy - 52], fill=RED, width=7)
    d.line([x + 210, wy - 34, x + 236, wy - 58], fill=WHITE, width=6)
    d.line([x + 236, wy - 58, x + 268, wy - 56], fill=WHITE, width=6)
    # rider
    d.line([x + 236, wy - 58, x + 250, wy - 96], fill=(255, 200, 60),
           width=9)
    d.line([x + 250, wy - 96, x + 282, wy - 78], fill=(255, 200, 60),
           width=9)
    d.ellipse([x + 262, wy - 122, x + 290, wy - 94], fill=(255, 200, 60))
    d.line([x + 210, wy - 34, x + 190, wy - 78], fill=(255, 200, 60),
           width=8)


def art_fire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 214))
    # smoke
    for cx, cy, r in ((x + 120, y + 26, 22), (x + 158, y + 14, 26),
                      (x + 200, y + 30, 20), (x + 330, y + 20, 24)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 146, 138))
    # factory
    fx, fy = x + 70, y + 58
    d.rectangle([fx, fy, fx + 300, fy + 92], fill=(120, 116, 108))
    for i in range(3):  # sawtooth roof
        d.polygon([(fx + i * 100, fy), (fx + i * 100 + 50, fy - 26),
                   (fx + (i + 1) * 100, fy)], fill=(90, 86, 80))
    d.rectangle([fx + 250, fy - 38, fx + 276, fy], fill=(90, 86, 80))
    for wx in (fx + 24, fx + 104, fx + 184):
        d.rectangle([wx, fy + 22, wx + 48, fy + 58], fill=(255, 220, 120))
    # flames
    for fx2, fh in ((fx + 30, 52), (fx + 120, 68), (fx + 210, 56)):
        d.polygon([(fx2, fy + 92), (fx2 + 18, fy + 92 - fh),
                   (fx2 + 36, fy + 92)], fill=(230, 90, 20))
        d.polygon([(fx2 + 8, fy + 92), (fx2 + 18, fy + 92 - fh + 22),
                   (fx2 + 28, fy + 92)], fill=(250, 200, 40))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.text((W // 2, 22), "THE WORLD IN ONE DAY", font=SERIF_B(58),
           fill=INK, anchor="ma")
    d.rectangle([28, 96, W - 28, 100], fill=INK)
    d.text((W // 2, 106), "SUNDAY, 22 NOVEMBER 2026", font=SANS_B(36),
           fill=RED, anchor="ma")
    d.rectangle([28, 158, W - 28, 162], fill=INK)
    d.text((W // 2, 170), "Four stories that defined the day",
           font=SANS(22), fill=GREY, anchor="ma")

    # 2 x 2 grid of stories
    mx, my, gap = 28, 212, 16
    pw = (W - 2 * mx - gap) // 2
    ph = 378
    stories = [
        ("01  ·  CLIMATE", NAVY, "COP31 COLLAPSES WITHOUT A DEAL",
         "UN climate talks in Antalya end empty-handed after the EU "
         "rejects a final text that never mentions fossil fuels.",
         art_cop31),
        ("02  ·  CONFLICT", (120, 30, 30), "IRAN STRIKES IN THE GULF",
         "Missiles hit oil tankers near the Strait of Hormuz and a US "
         "base in Bahrain as the standoff with Washington escalates.",
         art_gulf),
        ("03  ·  SPORT", (20, 90, 40), "MARQUEZ SEALS EIGHTH TITLE",
         "Marc Marquez finishes eighth in Portugal as Bezzecchi wins "
         "the race \u2014 enough for the 2026 MotoGP crown, 439 points.",
         art_motogp),
        ("04  ·  DISASTER", (140, 70, 10), "FACTORY FIRE IN INDONESIA",
         "Blaze at a candy plant in Cikande kills three; rescuers "
         "search the ruins for 36 workers still missing.",
         art_fire),
    ]
    for i, (tag, color, head, sub, art) in enumerate(stories):
        px = mx + (i % 2) * (pw + gap)
        py = my + (i // 2) * (ph + gap)
        draw_panel(d, px, py, pw, ph, tag, color, head, sub, art)

    # footer
    d.text((W // 2, 988), "Sources: Reuters · AP · AFP · The Race  —  22 Nov 2026",
           font=SANS(17), fill=GREY, anchor="ma")

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
