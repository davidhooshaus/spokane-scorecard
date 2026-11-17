# BLS QCEW annual averages. spokane_county_annual.csv and healthcare_share.csv
are pulled by tools/pull_trends.py (county 53063, 2014 forward, no key).
us_annual.csv is the matching US total (area US000, own_code 0, industry 10)
from the same open CSV API, pulled 2026-11-16:
https://data.bls.gov/cew/data/api/{year}/a/area/US000.csv
Used for the pay-versus-US share in the Paychecks card. industry_pay_2025.csv
and sector_change_2019_2025.csv feed the calculator presets and the hiring chart.
