# CLAUDE.md — The Spokane Prosperity Scorecard

Resident-run civic accountability site. One question, graded quarterly from
public data: is Spokane attracting employers that raise wages? The site's
entire value is credibility. Every rule below exists to protect it.

## What this repo is

Static HTML, no build step, no framework, no dependencies beyond Google Fonts.
Deployed via GitHub Pages. Updated by hand each quarter using the
`/quarterly-update` command. Keep it this way. If a change requires npm,
a bundler, or a database, it is the wrong change.

Files:
- `index.html` — the scorecard: verdict, narrative, flywheel, 8 graded cards,
  lever map, case studies, asks, methodology links, Tally form link
- `methodology.html` — rubric, sources, limitations, change log (append-only)
- `calculator.html` — employer impact tool (illustration, never a forecast)
- `flywheel.svg` — the compounding diagram, embedded by index.html
- `press/flywheel.png` — 1600px social/press export of the SVG
- `data/` — pulled datasets (DOR files, Census pulls, city-lever data obtained by request)
- `.claude/commands/` — the `/quarterly-update` runbook

## Non-negotiable editorial rules

1. **Every number links to its source.** No claim ships without a citation a
   reader can click. If a number can't be sourced, it doesn't go on the page.
2. **Grades change only when data changes.** Never re-grade for news cycles,
   politics, or vibes. Rubric lives in methodology.html.
3. **The change log is append-only.** Every grade change, number revision, and
   methodology tweak gets a versioned entry with a one-line reason. Never edit
   or delete past entries. Errors get corrected in a NEW entry.
4. **Lever-map status lines are only ever:** (a) tied to a graded card,
   (b) tied to a linked source, or (c) an open data request. Never an
   unsourced assertion about an institution or person.
5. **The calculator shows ranges, never point estimates**, cites its
   multipliers (Moretti, capped per Bartik/Upjohn), and keeps its
   "What this is not" section. It illustrates a mechanism. It never forecasts.
6. **Geography and vintage on every figure.** Spokane County vs. Spokane metro
   (includes Stevens County) vs. City of Spokane. Label it. Date it.
7. **Generous to people, ruthless with numbers.** Never name an official or a
   specific project as wasteful. The data does the damning.
8. **The commitment back is binding.** When a grade improves, say so at the
   top of the page, in green, with credit. This is what separates
   accountability from hostility.
9. **Honesty over comfort.** If honest review makes the ledger look worse
   (see change log v1.1), ship it and log it. Never the reverse.
10. **David reviews every grade change before it publishes.** Present diffs;
    do not push re-grades autonomously.

## Voice

**Reading level: 6th grade.** Run `python3 tools/readability.py` before publishing. The
exception is terminology where simplifying would change the meaning: taxable retail sales,
labor force participation, local multiplier, per-person income, and the proper names of
agencies and schools. Keep those exact. Everything around them gets short sentences and
plain words. The lever is almost always sentence length, not vocabulary. Never trade away a
number, a geography label, or a caveat to hit a score. Clarity, not simplification.


Plain words, short sentences, resident-to-resident. No corporate register, no
academic hedging beyond what honesty requires. Never use em dashes (periods,
commas, or parentheses instead). No exclamation points. Bench lines argue the
grade in one breath; "why it matters" lines connect the number to a storefront,
a paycheck, or a neighbor.

## Data sources (cadence in parentheses)

- WA ESD Spokane County profile — jobs, unemployment (monthly, ~6wk lag):
  https://esd.wa.gov/jobs-and-training/labor-market-information/reports-and-research/labor-market-county-profiles/spokane-county-profile
- USAFacts Spokane metro jobs (monthly):
  https://usafacts.org/answers/how-many-jobs-were-added-in-the-us-last-month/metro-area/spokane-wa/
- Spokane Workforce Council targeted industries — sector jobs/wages (periodic):
  https://spokaneworkforce.org/targeted-industries/
- BLS OEWS Spokane — occupational wages (annual, spring release):
  https://www.bls.gov/regions/west/news-release/occupationalemploymentandwages_spokane.htm
- WA Dept. of Revenue — taxable retail sales (quarterly; Journal of Business
  covers each release): https://dor.wa.gov/
- ACTIV8 Real Estate — CoStar retail vacancy + construction (quarterly):
  https://www.activ8re.com/
- Census ACS — incomes, earnings (annual; API now requires a key, set
  CENSUS_API_KEY; else use data.census.gov or censusreporter.org)
- Spokane Trends (EWU) — working-age employment 2.4.2, STEM degrees 3.5.7:
  https://www.spokanetrends.org/
- WA OFM — population (annual)
- BLS QCEW open CSV API — county jobs and pay history for the trend charts
  (annual averages, 2014 forward, no key; pulled by `tools/pull_trends.py` into `data/qcew/`)

## Roadmap (November first, in this order)

1. Pre-registered numeric grade thresholds published BEFORE re-grading.
2. City-controlled output measures, where the data can be obtained: permit turnaround
   time, employment-land readiness, business fees, major expansions retained or won.
   Retired 2026-08-31: the council attention audit. Counting agenda mentions is a weak
   proxy for results, gameable, and it pushed the project toward political watchdog and
   away from scorekeeper. Measure the scoreboard, not how often the coach talks about winning.
3. Swap unemployment card for working-age employment (Spokane Trends 2.4.2).
4. Add full-time worker median earnings (ACS S2001, needs Census key).
5. Peer-metro comparison column (Boise, Chattanooga, Huntsville).
6. Graduate-retention request log: emails to Gonzaga, Whitworth, EWU,
   WSU Spokane, CCS. Log responses. First publisher gets celebrated.
7. Migration data for the leak (Census flows, IRS SOI).

## Never do

- Add analytics/tracking without discussing with David first.
- Auto-update the site from live feeds. Hand-updated is the design.
- Soften, reword, or delete anything a past change log entry says.
- Put unsourced institutional claims in the lever map.
- Turn the quarterly essay into a press release. It explains; it doesn't sell.
