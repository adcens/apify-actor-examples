"""Lighthouse scores and Core Web Vitals for a list of URLs, saved as a Google Sheets-ready CSV.

Actor: https://apify.com/thriving_adder/bulk-lighthouse-auditor
Cost: $0.012 per audit (one URL on one device); failed audits are free.
Import the CSV in Google Sheets with File > Import > Upload.
"""
import csv
import os
from decimal import Decimal

from apify_client import ApifyClient

URLS = ["https://www.python.org/"]  # add your own pages here

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("thriving_adder/bulk-lighthouse-auditor").call(
    run_input={"urls": [{"url": u} for u in URLS], "devices": ["mobile"]},
    max_total_charge_usd=Decimal("0.05"),
)

columns = ["url", "device", "performance", "accessibility", "bestPractices", "seo",
           "lcpMs", "cls", "tbtMs", "fcpMs", "coreWebVitalsPass", "reportUrl", "error"]
os.makedirs("output", exist_ok=True)
with open("output/lighthouse.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    for item in client.dataset(run.default_dataset_id).iterate_items():
        scores = item.get("scores") or {}
        row = {c: item.get(c) for c in columns}
        row.update({k: scores.get(k) for k in ("performance", "accessibility", "bestPractices", "seo")})
        writer.writerow(row)
        print(row["url"], row["device"], "performance", row["performance"], "LCP", row["lcpMs"], "ms", row["error"] or "")
print("Saved output/lighthouse.csv")
