# Running the quarterly update in the cloud

The quarterly refresh must not depend on David's laptop being awake. This
document is the setup and the standing prompt for the cloud routine that runs
it. Local `/quarterly-update` still works and stays the fallback.

## What a cloud routine can and cannot do here

- It clones this repo's **default branch** (`main`) fresh on every run. Only
  what is committed to `main` is visible to it.
- It can push to `claude/*` branches only. It cannot push to `main`.
- Minimum interval is one hour. Quarterly is well within that.
- It has no memory between runs. Everything it needs must be in the repo.

That branch restriction is a good fit, not a limitation. CLAUDE.md rule 10
says David reviews every grade change before it publishes. The routine writes
a branch and opens a pull request. `main` is what deploys. Merging is the act
of publishing, and only David does it.

## One-time setup

1. Repo is on GitHub at `davidhooshaus/spokane-scorecard`, private, default
   branch `main`.
2. Claude Code on the web is enabled, and this repo is connected to it.
3. Authorize the connectors the run needs in the cloud environment. Authorizing
   on the desktop does not authorize the cloud runner.
   - **Gmail** for the summary email
   - **Firecrawl or web fetch** for the data pulls
4. Register the scheduled routine (below) with the id
   `personal-spokane-scorecard-quarterly`.

## Cadence

Quarterly, on the 15th of February, May, August and November, 6:00am Pacific.

```
0 6 15 2,5,8,11 *
```

The 15th, not the 1st. The quarterly sources the scorecard depends on (DOR
taxable retail sales, ACTIV8 vacancy) publish partway through the quarter, and
ESD county data runs about six weeks behind. Running on the 1st pulls a stale
quarter and wastes the cycle.

## The routine prompt

Paste this as the routine's prompt. It is deliberately verbose about the
guardrails, because an unattended run has nobody to stop it.

```
You are running the quarterly update for The Spokane Employer Scorecard. This
is an unattended cloud run against the spokane-scorecard repo. All paths are
repo-relative.

Read first, and follow them exactly:
- CLAUDE.md (the editorial constitution; every rule in it binds this run)
- .claude/commands/quarterly-update.md (the step-by-step runbook)
- methodology.html (the rubric you grade against, and the append-only log)

Connectors required: Gmail, and web fetch or Firecrawl.

Do the runbook, steps 1 through 7, in order. Save any files you pull under
data/<dataset>/<YYYY-QN>/.

Then, instead of runbook step 8's interactive hand-off, do this:

1. Commit everything to a NEW branch named claude/quarterly-<YYYY-QN>. Never
   commit to main. Never merge. Never enable auto-merge.
2. Open a pull request into main titled "Quarterly update <YYYY-QN>". The PR
   body must list, in this order:
   - every figure that changed, with old value, new value, and the vintage of
     the new reading
   - every grade that changed, with a one-line reason tied to the rubric
   - every source link that was added or replaced
   - anything you could NOT verify, stated plainly
3. Create a Gmail DRAFT to david@hausadvisors.com and nobody else. The subject
   must be exactly:
   "[AUTO] Spokane Scorecard quarterly update <YYYY-QN> ready for review"
   Lead the body with a BLUF: in two to four sentences, say what changed, which
   grades moved and in which direction, and what David has to decide. Put the
   PR link on its own line right after the BLUF. Everything else goes below.
   Create the draft only. Do not send it.

Hard rules for this run:
- You are not publishing. You are proposing. main is untouched.
- Grades change only when the underlying data changed. Never re-grade for a
  news cycle or a vibe. If the rubric does not clearly move a grade, leave the
  grade alone and say so in the PR.
- Every number links to a source a reader can click. If you cannot source a
  number, it does not go on the page. Say in the PR what you dropped and why.
- The methodology.html change log is append-only. Add a new entry at the top.
  Never edit or delete an existing entry.
- Label geography and vintage on every figure. Spokane County, Spokane metro
  and City of Spokane are different places.
- No em dashes anywhere. Use periods, commas or parentheses.
- Never name an official or a specific project as wasteful.
- If a grade improved, say so at the top of the verdict, in green, with credit.
- If you cannot re-export press/flywheel.png (cairosvg may be unavailable in
  this environment), edit flywheel.svg anyway and flag the stale PNG as an
  open item in both the PR body and the email. Do not skip the SVG edit.
- If a source is unreachable, do not guess and do not carry forward last
  quarter's number as if it were fresh. Leave the old figure, mark it in the PR
  as not refreshed this quarter, and name the source that failed.
```

## Known gaps

- **press/flywheel.png re-export.** The runbook re-exports the 1600px PNG with
  cairosvg when a flywheel dot changes color. That may not be installed in the
  cloud runner. The prompt tells the routine to edit the SVG regardless and
  flag the stale PNG, so a colour change never silently desyncs the two files.
  David re-exports locally, or we settle on a cloud-available exporter.
- **CENSUS_API_KEY.** Roadmap item 4 (ACS S2001 full-time earnings) needs a
  Census key. The cloud runner has no access to a local environment variable.
  Solve this before November, either with a secret in the cloud environment or
  by pulling from data.census.gov by hand that quarter.
- **The attention audit is not a routine.** `/attention-audit` requires
  pre-registering a counting rule with David before any counting, and a
  20-row human spot-check. That is interactive work. Run it locally.
