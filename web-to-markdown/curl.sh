#!/usr/bin/env bash
# One page to Markdown with a single synchronous API call. Needs APIFY_TOKEN in the environment.
# This Actor requires a cost cap (maxTotalChargeUsd) of at least $0.03; you are billed only for events that happen.
# Actor: https://apify.com/thriving_adder/web-to-markdown-llms-txt  ($0.001 per page)
set -euo pipefail
mkdir -p output
curl -sS -X POST "https://api.apify.com/v2/acts/thriving_adder~web-to-markdown-llms-txt/run-sync-get-dataset-items?maxTotalChargeUsd=0.03" \
  -H "Authorization: Bearer ${APIFY_TOKEN}" -H "Content-Type: application/json" \
  -d '{"urls":[{"url":"https://www.python.org/about/"}]}' \
  -o output/page.json
python3 -c "import json; print(json.load(open('output/page.json'))[0]['markdown'][:600])"
