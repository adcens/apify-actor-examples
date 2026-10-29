#!/usr/bin/env bash
# Latest Singapore HDB resale transactions (data.gov.sg) as CSV. Needs APIFY_TOKEN.
# Actor: https://apify.com/thriving_adder/sea-open-data  ($0.0005 per record)
# Licence: Singapore Open Data Licence v1.0; keep the "attribution" column when you share the data.
set -euo pipefail
mkdir -p output
curl -sS -X POST "https://api.apify.com/v2/acts/thriving_adder~sea-open-data/run-sync-get-dataset-items?format=csv&maxTotalChargeUsd=0.01" \
  -H "Authorization: Bearer ${APIFY_TOKEN}" -H "Content-Type: application/json" \
  -d '{"datasets":[{"source":"data.gov.sg","id":"d_8b84c4ee58e3cfc0ece0d773c8ca6abc","sort":"month desc","limit":5}]}' \
  -o output/hdb_resale.csv
head -c 700 output/hdb_resale.csv; echo
