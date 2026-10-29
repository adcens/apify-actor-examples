"""Malaysian CPI (OpenDOSM) and Bank Negara Malaysia exchange rates as pandas DataFrames.

Actor: https://apify.com/thriving_adder/sea-open-data
Cost: $0.0005 per record. Every row carries the licence and the attribution text you must show.
"""
import os
from decimal import Decimal

import pandas as pd
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("thriving_adder/sea-open-data").call(
    run_input={
        "datasets": [
            {"source": "opendosm", "id": "cpi_headline", "filter": "overall@division", "sort": "-date", "limit": 12},
            {"source": "bnm", "id": "exchange-rate", "limit": 5},
        ]
    },
    max_total_charge_usd=Decimal("0.03"),
)
rows = [r for r in client.dataset(run.default_dataset_id).iterate_items() if not r.get("error")]

cpi = pd.json_normalize([r for r in rows if r["datasetId"] == "cpi_headline"], sep="_")
cpi = cpi[["record_date", "record_index"]].rename(columns=lambda c: c.replace("record_", "")).sort_values("date")
fx = pd.json_normalize([r for r in rows if r["datasetId"] == "exchange-rate"], sep="_")
fx = fx[[c for c in fx.columns if c.startswith("record_")]].rename(columns=lambda c: c.replace("record_", ""))

print("Malaysia CPI (overall):\n", cpi.to_string(index=False))
print("\nBNM exchange rates:\n", fx.to_string(index=False))
print("\nAttribution to show with these figures:")
for text in sorted({r["attribution"] for r in rows}):
    print("-", text)
os.makedirs("output", exist_ok=True)
cpi.to_csv("output/my_cpi.csv", index=False)
fx.to_csv("output/bnm_fx.csv", index=False)
