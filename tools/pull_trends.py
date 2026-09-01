#!/usr/bin/env python3
"""Pull the Spokane County long-run series from BLS QCEW open data (no key).

Writes one CSV per run to data/qcew/spokane_county_annual.csv:
  year, annual_avg_emplvl, avg_annual_pay
Total covered employment, all ownerships (own_code 0, industry 10), The open CSV API serves 2014
onward; deeper history exists in BLS annual archive files if ever needed. Used by the trend charts on index.html. Re-run
each quarter (runbook step 2); the newest complete year appears each spring.
"""
import csv, io, sys, time, urllib.request

FIPS = "53063"
START = 2014

def year_row(year):
    url = f"https://data.bls.gov/cew/data/api/{year}/a/area/{FIPS}.csv"
    try:
        raw = urllib.request.urlopen(url, timeout=30).read().decode()
    except Exception as e:
        return None
    for x in csv.DictReader(io.StringIO(raw)):
        if x["own_code"] == "0" and x["industry_code"] == "10":
            return {"year": year,
                    "annual_avg_emplvl": int(x["annual_avg_emplvl"]),
                    "avg_annual_pay": int(x["avg_annual_pay"])}
    return None

def main():
    rows = []
    y = START
    while True:
        r = year_row(y)
        if r is None:
            break
        rows.append(r); time.sleep(0.35); y += 1
    with open("data/qcew/spokane_county_annual.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["year", "annual_avg_emplvl", "avg_annual_pay"])
        w.writeheader(); w.writerows(rows)
    print(f"wrote {len(rows)} years: {rows[0]['year']}..{rows[-1]['year']}")
    for r in rows[-4:]:
        print(" ", r["year"], r["annual_avg_emplvl"], r["avg_annual_pay"])

if __name__ == "__main__":
    main()
