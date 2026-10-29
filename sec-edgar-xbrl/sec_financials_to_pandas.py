"""Annual revenue and net income from SEC XBRL data, as a pandas table.

Actor: https://apify.com/thriving_adder/sec-edgar-filings-xbrl
Cost: about $0.01 for this input ($0.0003 per XBRL fact, plus Apify's tiny start fee).
"""
import os
from decimal import Decimal

import pandas as pd
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("thriving_adder/sec-edgar-filings-xbrl").call(
    run_input={
        "companies": ["AAPL", "MSFT"],
        "includeFilings": False,
        "includeXbrlFacts": True,
        "xbrlConcepts": ["RevenueFromContractWithCustomerExcludingAssessedTax", "NetIncomeLoss"],
        "xbrlForms": ["10-K"],
        "factsPeriodFrom": "2022-01-01",
    },
    max_total_charge_usd=Decimal("0.05"),  # hard cap for this run
)
items = list(client.dataset(run.default_dataset_id).iterate_items())
facts = pd.DataFrame([i for i in items if i.get("type") == "xbrl-fact"])

# Keep full fiscal years (10-Ks also report quarterly figures) and pivot to one row per company and fiscal-year end.
# (Each 10-K repeats prior years as comparatives; pivoting on periodEnd keeps one value per year, from the latest filing.)
annual = facts[facts["durationDays"] > 300].sort_values("filed")
table = annual.pivot_table(index=["ticker", "periodEnd"], columns="concept", values="value", aggfunc="last")
table = table.rename(columns={"RevenueFromContractWithCustomerExcludingAssessedTax": "revenue", "NetIncomeLoss": "netIncome"})
table["netMargin"] = (table["netIncome"] / table["revenue"]).round(3)

pd.set_option("display.width", 120)
print(table)
os.makedirs("output", exist_ok=True)
table.to_csv("output/sec_annual_financials.csv")
print("Saved output/sec_annual_financials.csv")
