#!/usr/bin/env python3
"""Regenerate the hero watermark in index.html from data/qcew/spokane_county_annual.csv.

Run after tools/pull_trends.py each quarter. The watermark is the real QCEW
jobs line for Spokane County, drawn as a quiet background shape behind the
hero: no axes, no numbers, no claim on its face. The sourced version of the
same line lives in the Job growth card. It shows data, never a grade
(methodology, Trend charts rule): if the line turns, the shape turns.
"""
import csv, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, "data", "qcew", "spokane_county_annual.csv")
HTML = os.path.join(ROOT, "index.html")
START, END = "<!-- hero-chart:start -->", "<!-- hero-chart:end -->"

rows = [(int(r["year"]), int(r["annual_avg_emplvl"]))
        for r in csv.DictReader(open(CSV))]
rows.sort()
y0, y1 = rows[0][0], rows[-1][0]

# Fixed value range so the silhouette stays comparable across editions.
VMIN, VMAX = 195000, 250000
lo, hi = min(v for _, v in rows), max(v for _, v in rows)
if lo < VMIN or hi > VMAX:
    sys.exit(f"data {lo}..{hi} outside {VMIN}..{VMAX}; widen the range")

W, H, TOP, BOT = 1600, 520, 60, 500
def px(year): return (year - y0) / (y1 - y0) * W
def py(val):  return BOT - (val - VMIN) / (VMAX - VMIN) * (BOT - TOP)

pts = " ".join(f"{px(yr):.1f},{py(v):.1f}" for yr, v in rows)
area = f"{pts} {W},{H} 0,{H}"

svg = (f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="none" aria-hidden="true">'
       f'<polygon points="{area}" fill="#2a6b73" opacity="0.07"/>'
       f'<polyline points="{pts}" fill="none" stroke="#2a6b73" stroke-width="3" '
       f'opacity="0.18" stroke-linejoin="round" stroke-linecap="round" '
       f'vector-effect="non-scaling-stroke"/></svg>')

s = open(HTML).read()
a, z = s.index(START), s.index(END)
s = s[:a + len(START)] + "\n      " + svg + "\n      " + s[z:]
open(HTML, "w").write(s)
print(f"hero watermark: QCEW line {y0}-{y1}")
