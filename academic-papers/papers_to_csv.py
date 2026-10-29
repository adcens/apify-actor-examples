"""Search OpenAlex + Crossref for papers on a topic and save a CSV for screening.

Actor: https://apify.com/thriving_adder/academic-research-papers
Cost: $0.001 per unique paper (duplicates across sources are merged and charged once).
"""
import csv
import os
from decimal import Decimal

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("thriving_adder/academic-research-papers").call(
    run_input={"queries": ["retrieval augmented generation evaluation"], "maxResultsPerQuery": 5, "yearFrom": 2023, "sort": "relevance"},
    max_total_charge_usd=Decimal("0.03"),
)

columns = ["title", "publicationYear", "venue", "citedByCount", "doi", "isOpenAccess", "pdfUrl", "url", "sources"]
os.makedirs("output", exist_ok=True)
with open("output/papers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
    writer.writeheader()
    for p in client.dataset(run.default_dataset_id).iterate_items():
        if p.get("error"):
            print("no result (free):", p["error"])
            continue
        writer.writerow({**p, "sources": "+".join(p.get("sources") or [])})
        print(f"{p.get('citedByCount') or 0:>6}  {p.get('publicationYear')}  {p['title'][:80]}")
print("Saved output/papers.csv")
