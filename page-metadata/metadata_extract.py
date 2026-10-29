"""Titles, meta descriptions, OpenGraph images, JSON-LD types and tech stack for a list of URLs.

Actor: https://apify.com/thriving_adder/page-metadata-extractor
Cost: $0.0006 per page extracted; failed pages are free.
"""
import os
from decimal import Decimal

from apify_client import ApifyClient

URLS = ["https://www.python.org", "https://www.djangoproject.com", "https://flask.palletsprojects.com/"]

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("thriving_adder/page-metadata-extractor").call(
    run_input={"urls": [{"url": u} for u in URLS]},
    max_total_charge_usd=Decimal("0.01"),
)
for page in client.dataset(run.default_dataset_id).iterate_items():
    if page.get("error"):
        print(page["url"], "->", page["errorCode"], "(not charged)")
        continue
    og = page.get("openGraph") or {}
    tech = ", ".join(t["name"] for t in page.get("technologies") or [])
    print(f"\n{page['url']}\n  title: {page.get('title')}\n  description: {page.get('metaDescription')}")
    print(f"  og:image: {og.get('image')}\n  JSON-LD: {page.get('jsonLdTypes')}\n  tech: {tech}\n  issues: {page.get('issues')}")
