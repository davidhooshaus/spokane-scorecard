#!/usr/bin/env python3
"""Generate the trend-chart <figure> blocks for the measure cards.

Reads the pulled series under data/ and prints one block per chart to
stdout, separated by === markers, in the same SVG style as the jobs and
pay charts. Paste each block into its card in index.html (the runbook's
step 3 covers regenerating these each quarter).

Series read:
  data/acs/series/acs1_series_2014_2025.csv       incomes + working-age
  data/qcew/spokane_county_annual.csv             county pay
  data/qcew/us_annual.csv                         US pay
  data/dor/series/spokane_city_trs_annual_2014_2025.csv  city spending
  data/ofm/history/spokane_state_april1_2010_2026.csv    population
"""
import csv, os

os.chdir(os.path.join(os.path.dirname(__file__), '..'))

X0, X1 = 56.0, 610.0
TOP, BOT = 18.0, 208.0
TEAL, INK, GRAY, GRID, AMBER = '#2a6b73', '#211d18', '#4a5654', '#e3ebe9', '#a06e0a'
FONT = 'font-family="Public Sans, sans-serif" style="font-variant-numeric:tabular-nums"'


def read(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def xpos(years):
    n = len(years)
    return {y: X0 + (X1 - X0) * i / (n - 1) for i, y in enumerate(years)}


def ypos(v, vmin, vmax):
    return BOT - (v - vmin) / (vmax - vmin) * (BOT - TOP)


def gridlines(vals, vmin, vmax, fmt):
    out = []
    for v in vals:
        y = ypos(v, vmin, vmax)
        out.append(f'<line x1="56" y1="{y:.1f}" x2="610" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>'
                   f'<text x="48" y="{y + 4:.1f}" text-anchor="end" font-size="11" fill="{GRAY}">{fmt(v)}</text>')
    return ''.join(out)


def polyline(pts, color=TEAL, width=2.5, dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    p = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    return (f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{width}"{d}'
            ' stroke-linejoin="round" stroke-linecap="round"/>')


def xticks(xs, years, show):
    return ''.join(f'<text x="{xs[y]:.1f}" y="230" text-anchor="middle" font-size="11" fill="{GRAY}">{y}</text>'
                   for y in show if y in xs)


def marker(x, label, y_label=29):
    return (f'<line x1="{x:.1f}" y1="18" x2="{x:.1f}" y2="208" stroke="{AMBER}" stroke-width="1" stroke-dasharray="3 3"/>'
            f'<text x="{x + 5:.1f}" y="{y_label}" font-size="10.5" fill="{AMBER}">{label}</text>')


def enddot(x, y, label, dy=4.0):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{TEAL}"/>'
            f'<text x="{x + 7:.1f}" y="{y + dy:.1f}" font-size="11.5" font-weight="700" fill="{INK}">{label}</text>')


def table(caption, head, rows):
    body = ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in rows)
    return (f'<details class="astable"><summary>Show these numbers as a table</summary><table>'
            f'<caption>{caption}</caption><thead><tr><th scope="col">{head[0]}</th>'
            f'<th scope="col">{head[1]}</th></tr></thead><tbody>{body}</tbody></table></details>')


acs = read('data/acs/series/acs1_series_2014_2025.csv')
acs_years = [int(r['year']) for r in acs]
all_years = list(range(2014, 2026))
xs = xpos(all_years)

blocks = []

# 1. Working-age employment: Spokane vs US, 20 to 64, gap at 2020
spk = {int(r['year']): float(r['emp_pop_20_64_spokane']) for r in acs}
usv = {int(r['year']): float(r['emp_pop_20_64_us']) for r in acs}
vmin, vmax = 64.0, 78.0
seg_a = [y for y in all_years if y in spk and y < 2020]
seg_b = [y for y in all_years if y in spk and y > 2020]
svg = (f'<svg viewBox="0 0 680 240" role="img" aria-label="Line chart of the share of adults 20 to 64 '
       f'with a job, 2014 to 2025, Spokane County against the United States. Spokane starts about four '
       f'points below the nation, falls behind to 2019, then closes the whole gap by 2025. No line is '
       f'drawn for 2020 because that survey was not released." {FONT}><rect width="680" height="240" fill="#ffffff"/>'
       + gridlines([66, 70, 74, 78], vmin, vmax, lambda v: f'{v:.0f}%')
       + marker(xs[2020], 'no 2020 survey')
       + polyline([(xs[y], ypos(usv[y], vmin, vmax)) for y in seg_a], color=GRAY, width=2)
       + polyline([(xs[y], ypos(usv[y], vmin, vmax)) for y in seg_b], color=GRAY, width=2)
       + polyline([(xs[y], ypos(spk[y], vmin, vmax)) for y in seg_a])
       + polyline([(xs[y], ypos(spk[y], vmin, vmax)) for y in seg_b])
       + f'<text x="{xs[2014] + 6:.1f}" y="{ypos(71.2, vmin, vmax) - 8:.1f}" font-size="11" fill="{GRAY}">U.S.</text>'
       + f'<text x="{xs[2014] + 6:.1f}" y="{ypos(67.4, vmin, vmax) + 16:.1f}" font-size="11" font-weight="700" fill="{TEAL}">Spokane</text>'
       + f'<text x="{xs[2025] + 7:.1f}" y="{ypos(76.0, vmin, vmax) - 6:.1f}" font-size="11" fill="{GRAY}">U.S. 76.0%</text>'
       + enddot(xs[2025], ypos(75.9, vmin, vmax), '75.9%', dy=14.0)
       + xticks(xs, all_years, [2014, 2017, 2020, 2023, 2025]) + '</svg>')
rows = [(str(y), f'{spk[y]:.1f}% / {usv[y]:.1f}%') for y in acs_years]
blocks.append(('WORKINGAGE', f'''<figure class="trend" id="watrend">
    {svg}
    <figcaption><b>Spokane closed a four-point gap in a decade.</b> Share of adults 20 to 64 with a job, Spokane County (teal) and the U.S. (gray), 2014 to 2025. In 2019 Spokane sat 3.7 points behind the nation. By 2025 the two lines meet. The Census Bureau released no 2020 figures because the pandemic broke that year&rsquo;s survey. County one-year figures carry a margin of error near 2 points, so single-year wiggles are mostly noise; the decade-long climb is not.
    {table('Share of adults 20 to 64 with a job, Spokane / U.S.', ('Year', 'Spokane / U.S.'), rows)}
    <span class="src" style="display:block;margin-top:8px;">Source: <a href="https://data.census.gov/table/ACSST1Y2025.S2301?g=050XX00US53063">Census ACS 1-year, table S2301</a>, one query per year. <a href="data/acs/series/acs1_series_2014_2025.csv">Download this data (CSV)</a>.</span></figcaption>
  </figure>'''))

# 2. Paychecks: county pay as share of US pay
cty = {int(r['year']): int(r['avg_annual_pay']) for r in read('data/qcew/spokane_county_annual.csv')}
usp = {int(r['year']): int(r['avg_annual_pay']) for r in read('data/qcew/us_annual.csv')}
share = {y: 100 * cty[y] / usp[y] for y in all_years}
vmin, vmax = 82.0, 89.0
svg = (f'<svg viewBox="0 0 680 240" role="img" aria-label="Line chart of Spokane County average pay as a '
       f'share of United States average pay, 2014 to 2025. The share climbs from about 83 percent to '
       f'about 88 percent, with a small dip in 2020." {FONT}><rect width="680" height="240" fill="#ffffff"/>'
       + gridlines([83, 85, 87, 89], vmin, vmax, lambda v: f'{v:.0f}%')
       + marker(xs[2020], 'pandemic')
       + polyline([(xs[y], ypos(share[y], vmin, vmax)) for y in all_years])
       + enddot(xs[2025], ypos(share[2025], vmin, vmax), f'{share[2025]:.1f}%')
       + xticks(xs, all_years, [2014, 2017, 2020, 2023, 2025]) + '</svg>')
rows = [(str(y), f'{share[y]:.1f}%') for y in all_years]
blocks.append(('PAYSHARE', f'''<figure class="trend" id="paytrend">
        {svg}
        <figcaption><b>The pay gap with the nation is closing, slowly.</b> Spokane County average annual pay as a share of the U.S. figure, 2014 to 2025. About half a point of catch-up a year, from 83 cents on the national dollar to almost 88. At this pace, parity is a decade away.
        {table('Spokane County pay as a share of U.S. pay (QCEW)', ('Year', 'Share'), rows)}
        <span class="src" style="display:block;margin-top:8px;">Source: <a href="https://www.bls.gov/cew/">BLS QCEW</a> annual averages, Spokane County and U.S. total. <a href="data/qcew/spokane_county_annual.csv">County CSV</a>, <a href="data/qcew/us_annual.csv">U.S. CSV</a>.</span></figcaption>
      </figure>'''))

# 3. Incomes: per-capita income as share of US, gap at 2020
pci = {int(r['year']): float(r['pci_pct_of_us']) for r in acs}
vmin, vmax = 84.0, 101.0
svg = (f'<svg viewBox="0 0 680 240" role="img" aria-label="Line chart of Spokane County income per person '
       f'as a share of the United States figure, 2014 to 2025. The line wobbles between 87 and 98 percent '
       f'and never reaches 100. A 2024 high of 97.5 percent falls back to 93.5 in 2025. No point is drawn '
       f'for 2020 because that survey was not released." {FONT}><rect width="680" height="240" fill="#ffffff"/>'
       + gridlines([85, 90, 95], vmin, vmax, lambda v: f'{v:.0f}%')
       + f'<line x1="56" y1="{ypos(100, vmin, vmax):.1f}" x2="610" y2="{ypos(100, vmin, vmax):.1f}" stroke="#2b3134" stroke-width="1" stroke-dasharray="5 3"/>'
       + f'<text x="48" y="{ypos(100, vmin, vmax) + 4:.1f}" text-anchor="end" font-size="11" font-weight="700" fill="#2b3134">100%</text>'
       + f'<text x="{xs[2016]:.1f}" y="{ypos(100, vmin, vmax) - 6:.1f}" font-size="10.5" fill="{GRAY}">U.S. level</text>'
       + marker(xs[2020], 'no 2020 survey', y_label=200)
       + polyline([(xs[y], ypos(pci[y], vmin, vmax)) for y in seg_a])
       + polyline([(xs[y], ypos(pci[y], vmin, vmax)) for y in seg_b])
       + enddot(xs[2025], ypos(pci[2025], vmin, vmax), '93.5%')
       + xticks(xs, all_years, [2014, 2017, 2020, 2023, 2025]) + '</svg>')
rows = [(str(y), f'{pci[y]:.1f}%') for y in acs_years]
blocks.append(('INCSHARE', f'''<figure class="trend" id="inctrend">
      {svg}
      <figcaption><b>A decade below the line.</b> Spokane County income per person as a share of the U.S. figure, 2014 to 2025. The line has wobbled between 87% and 98% for twelve years and never touched the nation. The 2024 reading looked like a breakthrough. 2025 took most of it back. One-year county readings carry real margins of error, which is why the grade rule uses the level, not single-year moves.
      {table('Spokane County income per person as a share of the U.S.', ('Year', 'Share'), rows)}
      <span class="src" style="display:block;margin-top:8px;">Source: <a href="https://data.census.gov/table/ACSDT1Y2025.B19301?g=050XX00US53063">Census ACS 1-year, table B19301</a>, one query per year. <a href="data/acs/series/acs1_series_2014_2025.csv">Download this data (CSV)</a>.</span></figcaption>
    </figure>'''))

# 4. Spending: city TRS annual growth
trs = {int(r['year']): float(r['yoy_pct']) for r in read('data/dor/series/spokane_city_trs_annual_2014_2025.csv') if r['yoy_pct']}
yrs = sorted(trs)
xs2 = xpos(yrs)
vmin, vmax = -5.0, 23.0
svg = (f'<svg viewBox="0 0 680 240" role="img" aria-label="Line chart of yearly growth in City of Spokane '
       f'taxable retail sales, 2015 to 2025. Growth runs four to seven percent through 2019, dips below '
       f'zero in 2020, spikes to 21 percent in 2021, then cools every year to 0.1 percent in 2025." {FONT}>'
       '<rect width="680" height="240" fill="#ffffff"/>'
       + gridlines([10, 20], vmin, vmax, lambda v: f'+{v:.0f}%')
       + f'<line x1="56" y1="{ypos(0, vmin, vmax):.1f}" x2="610" y2="{ypos(0, vmin, vmax):.1f}" stroke="#2b3134" stroke-width="1"/>'
       + f'<text x="48" y="{ypos(0, vmin, vmax) + 4:.1f}" text-anchor="end" font-size="11" fill="{GRAY}">0%</text>'
       + marker(xs2[2020], 'pandemic')
       + f'<text x="{xs2[2021] + 5:.1f}" y="{ypos(21.1, vmin, vmax) - 8:.1f}" font-size="10.5" fill="{GRAY}">stimulus rebound</text>'
       + polyline([(xs2[y], ypos(trs[y], vmin, vmax)) for y in yrs])
       + enddot(xs2[2025], ypos(trs[2025], vmin, vmax), '+0.1%')
       + xticks(xs2, yrs, [2015, 2018, 2021, 2023, 2025]) + '</svg>')
rows = [(str(y), f'{trs[y]:+.1f}%') for y in yrs]
blocks.append(('SPENDTREND', f'''<figure class="trend" id="spendtrend">
      {svg}
      <figcaption><b>Four years of cooling, to a stop.</b> Yearly growth in City of Spokane taxable retail sales, 2015 to 2025. The 2010s ran at 4&ndash;7% a year. The 2021 spike is the stimulus-era rebound. Since then every year has been cooler than the last, down to 0.1% in 2025. These are dollars as spent, not adjusted for inflation, which makes a flat 2025 worse than it looks. The 2025 figure carries the tax-base caution below.
      {table('Yearly growth, City of Spokane taxable retail sales', ('Year', 'Growth'), rows)}
      <span class="src" style="display:block;margin-top:8px;">Source: <a href="https://apps.dor.wa.gov/ResearchStats/Content/TaxableRetailSalesLocal/Report.aspx">WA Dept. of Revenue local query tool</a>, annual figures, Spokane (City), all NAICS. <a href="data/dor/series/spokane_city_trs_annual_2014_2025.csv">Download this data (CSV)</a>.</span></figcaption>
    </figure>'''))

# 5. People: county population 2010 to 2026
pop = {int(r['year']): int(r['spokane_county']) for r in read('data/ofm/history/spokane_state_april1_2010_2026.csv')}
yrs = sorted(pop)
xs3 = xpos(yrs)
vmin, vmax = 460000.0, 585000.0
svg = (f'<svg viewBox="0 0 680 240" role="img" aria-label="Line chart of Spokane County population each '
       f'April, 2010 to 2026, rising steadily from about 471 thousand to about 571 thousand with no down '
       f'year." {FONT}><rect width="680" height="240" fill="#ffffff"/>'
       + gridlines([480000, 520000, 560000], vmin, vmax, lambda v: f'{v / 1000:.0f}k')
       + marker(xs3[2020], '2020 census')
       + polyline([(xs3[y], ypos(pop[y], vmin, vmax)) for y in yrs])
       + enddot(xs3[2026], ypos(pop[2026], vmin, vmax), '570,600')
       + xticks(xs3, yrs, [2010, 2014, 2018, 2022, 2026]) + '</svg>')
rows = [(str(y), f'{pop[y]:,}') for y in yrs]
blocks.append(('POPTREND', f'''<figure class="trend" id="poptrend">
      {svg}
      <figcaption><b>About 99,000 more neighbors since 2010.</b> Spokane County population each April 1, 2010 to 2026, the state&rsquo;s official count. Sixteen years, no down year. Growth has slowed since 2022 but never stopped. Figures before 2020 are OFM&rsquo;s estimates as revised after the 2020 census; 2020 is the census count itself; later years are the current estimates.
      {table('Spokane County population, April 1 (OFM)', ('Year', 'People'), rows)}
      <span class="src" style="display:block;margin-top:8px;">Source: <a href="https://ofm.wa.gov/data-research/population-demographics/estimates/april-1-official/">WA OFM April 1 estimates</a> and the <a href="https://ofm.wa.gov/data-research/population-demographics/estimates/archive/">historical series</a>. <a href="data/ofm/history/spokane_state_april1_2010_2026.csv">Download this data (CSV)</a>.</span></figcaption>
    </figure>'''))

for name, block in blocks:
    print(f'===== {name} =====')
    print(block)
    print()
