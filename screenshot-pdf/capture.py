"""Full-page screenshot (PNG) and PDF of a page, downloaded to ./output.

Actor: https://apify.com/thriving_adder/website-screenshot-pdf
Cost: $0.002 per screenshot and $0.0025 per PDF; failed pages are free.
The dataset rows contain signed download links (pngUrl, jpegUrl, pdfUrl): treat them like private links.
"""
import os
import urllib.request
from decimal import Decimal

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("thriving_adder/website-screenshot-pdf").call(
    run_input={"urls": [{"url": "https://www.python.org/"}], "outputFormats": ["png", "pdf"], "viewport": "desktop"},
    max_total_charge_usd=Decimal("0.02"),
)
os.makedirs("output", exist_ok=True)
for item in client.dataset(run.default_dataset_id).iterate_items():
    if item.get("error"):
        print(item.get("url"), "->", item["error"])
        continue
    for field, ext in (("pngUrl", "png"), ("jpegUrl", "jpg"), ("pdfUrl", "pdf")):
        if item.get(field):
            path = f"output/{item[field.replace('Url', 'Key')]}.{ext}"
            urllib.request.urlretrieve(item[field], path)
            print("Saved", path, os.path.getsize(path), "bytes")
