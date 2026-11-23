#!/usr/bin/env python3
"""news-image-20261122 entry (Python 3.13, standard library only).

Copies the poster (entry.png, drawn from scratch by draw_poster.py with
PIL) to /output/entry.png.

The poster is "THE WORLD IN ONE DAY": one image summing up Sunday
22 November 2026's world news in four panels -- COP31 climate talks
collapse in Antalya with no deal, Iran strikes tankers near the Strait
of Hormuz and a US base in Bahrain, Marc Marquez clinches his eighth
MotoGP title at the Portuguese GP, and a candy factory fire in Cikande,
Indonesia kills three with 36 workers missing. The date is printed in
the poster's masthead so the image names the day it sums up.

The drawing program runs locally only: the grader sandbox has no PIL
installed (standard library only), so main.py copies the finished
image instead of drawing it. Re-draw it with:

    python3 draw_poster.py

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

The copy is byte-for-byte, so two runs write identical bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
DST = os.path.join(OUT_DIR, "entry.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)


if __name__ == "__main__":
    main()
