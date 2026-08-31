---
description: Run the full quarterly data refresh for the Spokane Employer Scorecard
---

Run the quarterly update. Follow CLAUDE.md rules throughout, especially:
grades change only on data, David signs off on every grade change before
push, and the change log is append-only.

## 0. Freeze the outgoing edition FIRST
Before touching a single figure, copy the current edition into the archive. This is the
step that makes the whole project credible, so it happens before any edit, not after.

- `mkdir -p archive/<YYYY-MM>` using the OUTGOING edition's month (the one on the masthead
  right now, not the one you are about to publish).
- Copy `index.html`, `methodology.html`, `calculator.html` and `flywheel.svg` into it.
- In each copied HTML file: add `<meta name="robots" content="noindex">` before `<title>`,
  drop the `og:url` tag, insert the amber archived-edition banner directly after `<body>`
  (copy the exact markup from `archive/2026-08/index.html`), and rewrite `href="archive/"`
  to `href="/archive/"`. Links between the three archived pages stay relative so the
  snapshot is self-contained.
- Add the edition to `archive/index.html`: month, verdict, tally, one line on the headline
  finding, and links to its three pages.
- Verify the snapshot opens and its internal links resolve before you edit anything live.

Never edit a file inside `archive/`. If an archived edition contains an error, the
correction goes in a NEW change log entry on the live methodology page. The archive is the
receipt; it does not get revised.

## 1. Dates
Update the masthead in index.html: "Updated <Month Year>" and
"Next update <Month Year>" (one quarter out).

## 2. Pull fresh figures (sources and cadences in CLAUDE.md)
For each card, fetch the newest reading and note its vintage:
- Job growth: ESD county YoY change; USAFacts avg monthly jobs
- Who's hiring: Workforce Council sector 5-yr changes
- Unemployment / working-age employment: ESD; Spokane Trends 2.4.2
- Incomes: ACS per-capita (and S2001 full-time earnings once keyed)
- Spending: newest DOR quarter for city, county, state
- Storefronts: newest ACTIV8/CoStar quarter (vacancy + construction pipeline)
- People: OFM/ESD population and growth vs. state and US
Save any downloaded files under data/<dataset>/<YYYY-QN>/.

## 3. Update each card
Figure, the <small> geography+vintage label, bench text, source dates, and
the chart: recompute every bar width as value/max*100 (for lower-is-better
charts like unemployment, keep the "shorter bar is better" note). Add a new
source link when a new release is cited; keep old links only if still load-bearing.

## 4. Re-grade
Apply the rubric strictly. If a grade changes:
- card class (row g/y/r) and the grade chip text
- the tally chips ("N green / N yellow / N red")
- if the card maps to a flywheel dot (Talent, Employers, Spending,
  Storefronts): edit the dot fill in flywheel.svg, update the diagram caption
  in index.html if the sentence no longer holds, and re-export
  press/flywheel.png at 1600px (cairosvg works).
- if anything turned green: honor the commitment. Add a green banner line to
  the top of the verdict with credit to whoever moved it.

## 5. Rewrite the narrative
Refresh the two paragraphs under "Why the city looks the way it does" so every
sentence matches a current graded number. Same voice: plain, short, no em dashes.
This text doubles as the quarterly email; draft that email as a separate
markdown file in data/emails/ for David to send.

## 5b. Say what changed
Rewrite the `.changed` line above the measures so it names, in one sentence each: every
figure that moved, every grade that changed, and any measure that was added or replaced.
Link the word "past editions" to `archive/`. If a grade changed, say which way and why in
half a clause. This is the first thing a returning reader looks for.

## 6. Log it
methodology.html change log: new version entry at the top listing every
changed figure's new vintage and every grade change with a one-line reason.
Never touch old entries.

## 6b. Check the reading level
Run `python3 tools/readability.py`. The standard: prose at or below 6th grade,
except where a term is load-bearing and simplifying it would change the meaning
(taxable retail sales, labor force participation, local multiplier, the names of
agencies and schools). Rewrite anything new that lands high, usually by splitting
long sentences rather than by swapping words. Never simplify a number, a
geography label, or a caveat into something less precise. Clarity is the goal,
not a lower score.

## 7. Verify before showing David
- every link resolves
- every new claim has a source
- geography + vintage labeled on every figure
- no em dashes introduced
- chart widths match the numbers

## 8. Hand off
Never publish without David. How you hand off depends on where this is running.

**Local, with David present.** Present a summary: numbers changed, grades
changed (with diffs), the draft email. Only after his sign-off: commit as
"quarterly update YYYY-QN" and push. Then remind him: send the email, note the
update to press contacts, and if anything went green, say it louder than the reds.

**Unattended cloud run.** There is nobody to sign off, so do not try to get
sign-off and do not proceed as if you had it. Commit to a new branch
`claude/quarterly-YYYY-QN`, open a pull request into `main`, and draft the
review email. Full instructions in CLOUD.md. `main` is what deploys, so merging
is publishing, and only David merges.
