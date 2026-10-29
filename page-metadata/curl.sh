#!/usr/bin/env bash
# Meta tags of a few pages as CSV. Needs APIFY_TOKEN.
# Actor: https://apify.com/thriving_adder/page-metadata-extractor  ($0.0006 per page)
set -euo pipefail
mkdir -p output
curl -sS -X POST "https://api.apify.com/v2/acts/thriving_adder~page-metadata-extractor/run-sync-get-dataset-items?format=csv&fields=url,statusCode,title,metaDescription,canonical,lang,issues&maxTotalChargeUsd=0.01" \
  -H "Authorization: Bearer ${APIFY_TOKEN}" -H "Content-Type: application/json" \
  -d '{"urls":[{"url":"https://www.python.org"},{"url":"https://example.com"}]}' \
  -o output/metadata.csv
cat output/metadata.csv
