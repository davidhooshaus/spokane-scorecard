---
description: Run the full quarterly data refresh for the Spokane Employer Scorecard
---

Run the quarterly update. Follow CLAUDE.md rules throughout, especially:
grades change only on data, David signs off on every grade change before
push, and the change log is append-only.

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

## 6. Log it
methodology.html change log: new version entry at the top listing every
changed figure's new vintage and every grade change with a one-line reason.
Never touch old entries.

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
