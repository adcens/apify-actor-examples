#!/usr/bin/env bash
# Sitemap URL list + status check as CSV in one call. Needs APIFY_TOKEN.
# Actor: https://apify.com/thriving_adder/sitemap-url-health  ($0.0008 per URL checked)
set -euo pipefail
mkdir -p output
curl -sS -X POST "https://api.apify.com/v2/acts/thriving_adder~sitemap-url-health/run-sync-get-dataset-items?format=csv&fields=url,statusCode,isIndexable,title,issues&maxTotalChargeUsd=0.01" \
  -H "Authorization: Bearer ${APIFY_TOKEN}" -H "Content-Type: application/json" \
  -d '{"startUrls":[{"url":"https://crawlee.dev"}],"maxUrlsPerSite":5}' \
  -o output/sitemap.csv
cat output/sitemap.csv
