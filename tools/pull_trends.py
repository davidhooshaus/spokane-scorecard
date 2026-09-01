#!/usr/bin/env python3
"""Pull verified history for the trend charts. No API keys.

Outputs (rerun each quarter, runbook step 2):
  data/qcew/spokane_county_annual.csv   year, annual_avg_emplvl, avg_annual_pay
  data/qcew/healthcare_share.csv        year, healthcare_emplvl, total_emplvl, share_pct
  data/laus/june_unemployment.csv       year, rate

Sources:
  BLS QCEW open CSV API (annual averages, Spokane County 53063, 2014 forward,
  which is the API's floor). Health care = NAICS 62 summed across ownerships.
  BLS API v1 (no key) for LAUS county unemployment, series
  LAUCN530630000000003, June of each year, not seasonally adjusted.
"""
import csv, io, json, os, time, urllib.request

FIPS = "53063"
START = 2014

def fetch(url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or {})
    return urllib.request.urlopen(req, timeout=30).read().decode()

def qcew():
    rows, shares = [], []
    y = START
    while True:
        try:
            raw = fetch(f"https://data.bls.gov/cew/data/api/{y}/a/area/{FIPS}.csv")
        except Exception:
            break
        total = hc = None
        hc_sum = 0
        for x in csv.DictReader(io.StringIO(raw)):
            if x["own_code"] == "0" and x["industry_code"] == "10":
                total = x
            if x["industry_code"] == "62" and x["agglvl_code"] == "74":
                hc_sum += int(x["annual_avg_emplvl"])
        if not total:
            break
        t = int(total["annual_avg_emplvl"])
        rows.append({"year": y, "annual_avg_emplvl": t,
                     "avg_annual_pay": int(total["avg_annual_pay"])})
        shares.append({"year": y, "healthcare_emplvl": hc_sum, "total_emplvl": t,
                       "share_pct": round(100 * hc_sum / t, 1)})
        time.sleep(0.35); y += 1
    return rows, shares

def laus():
    out = {}
    for a, b in [("2015", "2016"), ("2017", "2026")]:
        body = json.dumps({"seriesid": ["LAUCN530630000000003"],
                           "startyear": a, "endyear": b}).encode()
        d = json.loads(fetch("https://api.bls.gov/publicAPI/v1/timeseries/data/",
                             data=body, headers={"Content-Type": "application/json"}))
        for x in d["Results"]["series"][0]["data"]:
            if x["period"] == "M06":
                out[int(x["year"])] = float(x["value"])
        time.sleep(0.5)
    return [{"year": y, "rate": out[y]} for y in sorted(out)]

def write(path, rows, fields):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)
    print(f"wrote {path}: {len(rows)} rows ({rows[0]['year']}..{rows[-1]['year']})")

def main():
    rows, shares = qcew()
    write("data/qcew/spokane_county_annual.csv", rows,
          ["year", "annual_avg_emplvl", "avg_annual_pay"])
    write("data/qcew/healthcare_share.csv", shares,
          ["year", "healthcare_emplvl", "total_emplvl", "share_pct"])
    write("data/laus/june_unemployment.csv", laus(), ["year", "rate"])

if __name__ == "__main__":
    main()
