"""Turn web pages into Markdown chunks (JSONL) ready for an embeddings / RAG pipeline.

Actor: https://apify.com/thriving_adder/web-to-markdown-llms-txt
Cost: $0.001 per page converted; failed or skipped pages are free.
Only convert pages you are allowed to use; the publisher's copyright still applies.
"""
import json
import os
from decimal import Decimal

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("thriving_adder/web-to-markdown-llms-txt").call(
    run_input={
        "urls": [{"url": "https://www.python.org/about/"}, {"url": "https://docs.python.org/3/tutorial/index.html"}],
        "chunkTokens": 400,
        "chunkOverlapTokens": 40,
    },
    max_total_charge_usd=Decimal("0.03"),
)

os.makedirs("output", exist_ok=True)
n = 0
with open("output/chunks.jsonl", "w", encoding="utf-8") as f:
    for page in client.dataset(run.default_dataset_id).iterate_items():
        if page.get("error"):
            print("skipped (free):", page["url"], page["errorCode"])
            continue
        for i, chunk in enumerate(page.get("chunks") or [page["markdown"]]):
            text = chunk["text"] if isinstance(chunk, dict) else chunk
            f.write(json.dumps({"id": f"{page['url']}#{i}", "url": page["url"], "title": page["title"], "text": text}) + "\n")
            n += 1
        print(f"{page['url']}: {page['wordCount']} words")
print(f"Saved {n} chunks to output/chunks.jsonl")
