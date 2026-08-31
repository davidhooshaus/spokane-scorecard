---
description: Build the council attention audit (November feature) with a pre-registered counting rule
---

Build the attention audit: what share of Spokane City Council's public agenda
over the past 12 months touched employer attraction at all. This is the
scorecard's conversion of "majoring on the minors" from opinion into
measurement, so the counting rule must be pre-registered before counting.

## 1. Pre-register the rule (with David, before touching data)
Draft the inclusion rule, e.g.: an agenda item counts if it concerns
attracting, retaining, or expanding private employers, employment-land
readiness, permitting reform for commercial/industrial uses, or economic
development strategy. Routine items (proclamations, consent-calendar
contracts, personnel) count toward the denominator, not the numerator.
Decide edge cases in writing. Publish the rule in methodology.html BEFORE
publishing any result. The rule cannot change after counting without a
logged reason.

## 2. Gather
Collect 12 months of City Council agendas and minutes from the city's public
meeting portal (my.spokanecity.org). Save raw copies under
data/attention-audit/raw/.

## 3. Classify
One row per agenda item in data/attention-audit/items.csv:
date, meeting, item title, category, counts_toward_numerator (y/n), note.
Classify conservatively; when in doubt, count it as employer-related
(bias against our own thesis, which strengthens the result).

## 4. Verify
Have David spot-check 20 random rows. Log the spot-check result in the CSV
folder. If disagreement exceeds 2 of 20, revisit the rule together.

## 5. Publish
Add the ninth card to index.html: the share, the denominator, the rule in one
sentence, a link to the full CSV, and the honest caveat (attention is an
input, not an outcome; a low share is a choice, not a crime). Grade per
thresholds agreed with David in advance. Update tally chips, log the new
measure in the change log, and prepare the accompanying quarterly email angle.
