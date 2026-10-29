"""List a site's sitemap URLs, check them, and print a short SEO health report (and save a CSV).

Actor: https://apify.com/thriving_adder/sitemap-url-health
Cost: $0.0008 per URL checked ($0.0002 per URL if you only list them with checkUrls=false).
Use it on your own sites or sites you are allowed to audit.
"""
import collections
import csv
import os
from decimal import Decimal

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("thriving_adder/sitemap-url-health").call(
    run_input={"startUrls": [{"url": "https://crawlee.dev"}], "maxUrlsPerSite": 10},
    max_total_charge_usd=Decimal("0.02"),
)
rows = list(client.dataset(run.default_dataset_id).iterate_items())

status = collections.Counter(r.get("statusCode") for r in rows)
issues = collections.Counter(i for r in rows for i in (r.get("issues") or []))
print(f"{len(rows)} URLs checked. Status codes: {dict(status)}")
print("Issues:", dict(issues) or "none")
for r in rows:
    if (r.get("statusCode") or 0) >= 300 or not r.get("isIndexable", True):
        print("  check:", r["url"], r.get("statusCode"), r.get("finalUrl"))

os.makedirs("output", exist_ok=True)
with open("output/sitemap_health.csv", "w", newline="", encoding="utf-8") as f:
    cols = ["url", "statusCode", "finalUrl", "isIndexable", "title", "metaDescription", "canonical", "issues", "lastmod"]
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for r in rows:
        w.writerow({**r, "issues": ";".join(r.get("issues") or [])})
print("Saved output/sitemap_health.csv")
