#!/usr/bin/env python3
"""Regenerate the hero jobs chart in index.html from data/qcew/spokane_county_annual.csv.

Run after tools/pull_trends.py each quarter. The chart is an illustration of the
same QCEW series shown in the Job growth card, drawn in the calculator-chart
style. It always shows the data; it never shows a grade (methodology, Trend
charts rule). Review ANNOTATION each quarter: it must describe what the line
actually does, in plain words, and nothing else.
"""
import csv, os, sys

# Review this line every quarter against the fresh data.
ANNOTATION = "the climb stalls in 2024"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, "data", "qcew", "spokane_county_annual.csv")
HTML = os.path.join(ROOT, "index.html")
START, END = "<!-- hero-chart:start -->", "<!-- hero-chart:end -->"

rows = [(int(r["year"]), int(r["annual_avg_emplvl"]))
        for r in csv.DictReader(open(CSV))]
rows.sort()
y0, y1 = rows[0][0], rows[-1][0]
endyear, endval = rows[-1]

# Plot frame, viewBox 560x400
X0, X1, Y0, Y1 = 52, 540, 356, 40
VMIN, VMAX = 195000, 250000
lo, hi = min(v for _, v in rows), max(v for _, v in rows)
if lo < VMIN or hi > VMAX:
    sys.exit(f"data {lo}..{hi} outside axis range {VMIN}..{VMAX}; widen VMIN/VMAX")

def px(year): return X0 + (year - y0) / (y1 - y0) * (X1 - X0)
def py(val):  return Y0 - (val - VMIN) / (VMAX - VMIN) * (Y0 - Y1)

pts = " ".join(f"{px(yr):.1f},{py(v):.1f}" for yr, v in rows)
area = f"{pts} {px(y1):.1f},{Y0} {px(y0):.1f},{Y0}"
ex, ey = px(endyear), py(endval)
pandemic = f"{px(2020):.1f}" if y0 <= 2020 <= y1 else None

xticks = [yr for yr in (2014, 2017, 2020, 2023) if y0 <= yr <= y1]
if endyear not in xticks: xticks.append(endyear)

svg = []
svg.append('<svg viewBox="0 0 560 400" aria-hidden="true" '
           'font-family="Public Sans, sans-serif" style="font-variant-numeric:tabular-nums">')
svg.append('<rect width="560" height="400" fill="#ffffff"/>')
svg.append(f'<text x="{X0}" y="18" font-size="9.5" font-weight="700" letter-spacing="1.2" '
           f'fill="#4a5654">SPOKANE COUNTY JOBS SINCE {y0}</text>')
for val, lab in ((200000, "200k"), (220000, "220k"), (240000, "240k")):
    gy = py(val)
    svg.append(f'<line x1="{X0}" y1="{gy:.1f}" x2="{X1}" y2="{gy:.1f}" stroke="#e0e5e4" stroke-width="1"/>')
    svg.append(f'<text x="{X0-8}" y="{gy+3.5:.1f}" text-anchor="end" font-size="9.5" fill="#4a5654">{lab}</text>')
if pandemic:
    svg.append(f'<line x1="{pandemic}" y1="56" x2="{pandemic}" y2="{Y0}" '
               f'stroke="#a06e0a" stroke-width="1" stroke-dasharray="3 3"/>')
    svg.append(f'<text x="{float(pandemic)+5:.1f}" y="68" font-size="9.5" fill="#a06e0a">pandemic</text>')
svg.append(f'<polygon points="{area}" fill="#2a6b73" opacity="0.14"/>')
svg.append(f'<polyline points="{pts}" fill="none" stroke="#2a6b73" stroke-width="2.5" '
           'stroke-linejoin="round" stroke-linecap="round"/>')
svg.append(f'<line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="#4a5654" stroke-width="1.2"/>')
svg.append(f'<line x1="{ex:.1f}" y1="{Y0}" x2="{ex:.1f}" y2="{ey:.1f}" '
           'stroke="#2b3134" stroke-width="1.5" stroke-dasharray="3,3"/>')
svg.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="3.5" fill="#2a6b73"/>')
svg.append(f'<text x="{X1-8}" y="{max(ey-24, 34):.1f}" text-anchor="end" font-size="11.5" '
           f'font-weight="700" fill="#171d1c">{endval:,} jobs in {endyear}</text>')
svg.append(f'<text x="{X1-8}" y="{max(ey-8, 50):.1f}" text-anchor="end" font-size="10.5" '
           f'fill="#4a5654">{ANNOTATION}</text>')
for yr in xticks:
    svg.append(f'<text x="{px(yr):.1f}" y="376" text-anchor="middle" font-size="9.5" '
               f'fill="#4a5654">{yr}</text>')
svg.append('</svg>')
block = "\n      ".join(svg)

s = open(HTML).read()
a, z = s.index(START), s.index(END)
s = s[:a + len(START)] + "\n      " + block + "\n      " + s[z:]
open(HTML, "w").write(s)
print(f"hero chart: {y0}-{endyear}, endpoint {endval:,}, annotation: {ANNOTATION}")
