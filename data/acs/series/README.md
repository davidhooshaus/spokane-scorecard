# Census ACS 1-year series for Spokane County vs the US, 2014 to 2025. Pulled 2026-11-16.

Columns: per-capita income (B19301_001E), county share of the US figure,
median household income (B19013_001E), and the share of adults 20 to 64
who are working (table S2301, employment/population ratio).

Source: Census Bureau Data API, one query per year, for example
https://api.census.gov/data/2025/acs/acs1?get=group(B19301)&ucgid=0500000US53063
and the matching acs/acs1/subject S2301 queries. Each year's variable
label was checked in the API response.

Notes that must travel with any use of this file:
- No 2020 row. The Census Bureau did not release standard 1-year ACS
  estimates for 2020 because pandemic disruption broke the survey.
- 2014 uses the older S2301 layout, variable S2301_C03_019E, labeled
  "Employed, population 20 to 64 years." It measures the same thing as
  the modern S2301_C03_021E employment/population ratio.
- Dollars are in each year's own dollars, not adjusted to one base year.
  The county-vs-US shares are the comparable series.
- One-year county estimates carry margins of error of roughly one to two
  points on the employment ratio; single-year wiggles are mostly noise.
