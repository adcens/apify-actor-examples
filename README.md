# Apify Actor examples (thriving_adder)

Short, copy-paste examples for calling eight pay-per-event Actors on the [Apify Store](https://apify.com/thriving_adder) from Python, JavaScript and curl.

> **Disclosure:** I built and publish these Actors (Apify username `thriving_adder`) and I earn money when they are used. The examples are MIT-licensed. You can copy them freely, including for other Actors.

## The Actors

Prices are per event as listed on the Store on 29 Oct 2026. Every run also has Apify's Actor start fee of $0.00005 per GB of memory. Rows that fail or are skipped are free. Check each Store page for current prices.

| Folder | Actor (Store page) | What it does | Price per event |
|---|---|---|---|
| [`sec-edgar-xbrl/`](sec-edgar-xbrl/) | [SEC EDGAR Filings & XBRL Financials](https://apify.com/thriving_adder/sec-edgar-filings-xbrl) | Gets filing lists and XBRL financial facts (revenue, net income…) for US-listed companies from SEC's public EDGAR APIs. | $0.001 per filing, $0.0003 per XBRL fact |
| [`bulk-lighthouse/`](bulk-lighthouse/) | [Bulk Lighthouse & Core Web Vitals Auditor](https://apify.com/thriving_adder/bulk-lighthouse-auditor) | Runs Google Lighthouse on a list of URLs and returns scores, Core Web Vitals and an HTML report link. | $0.012 per audit, $0.010 per second-device audit |
| [`web-to-markdown/`](web-to-markdown/) | [Web to Markdown & llms.txt Generator for LLMs](https://apify.com/thriving_adder/web-to-markdown-llms-txt) | Converts public web pages into clean Markdown with RAG-ready chunks, and generates `llms.txt` for a site. | $0.001 per page, $0.02 per llms.txt file |
| [`sea-open-data/`](sea-open-data/) | [Malaysia & Singapore Open Data API](https://apify.com/thriving_adder/sea-open-data) | Reads official open data from data.gov.my / OpenDOSM, Bank Negara Malaysia and data.gov.sg, with licence and attribution on every row. | $0.0005 per record |
| [`academic-papers/`](academic-papers/) | [Academic Paper Search: OpenAlex, Crossref & arXiv](https://apify.com/thriving_adder/academic-research-papers) | Searches papers by query or looks them up by DOI/arXiv id across OpenAlex and Crossref (arXiv is optional), with duplicates merged. | $0.001 per unique paper |
| [`sitemap-url-health/`](sitemap-url-health/) | [Sitemap URL Extractor & SEO Health Checker](https://apify.com/thriving_adder/sitemap-url-health) | Reads a site's sitemaps and checks each URL's status, redirects, indexability and basic SEO tags. | $0.0008 per URL checked, $0.0002 per URL listed only |
| [`page-metadata/`](page-metadata/) | [Page Metadata, OpenGraph & JSON-LD Extractor](https://apify.com/thriving_adder/page-metadata-extractor) | Pulls title, meta description, Open Graph/Twitter tags, JSON-LD, canonical and detected tech from a list of pages. | $0.0006 per page |
| [`screenshot-pdf/`](screenshot-pdf/) | [Website Screenshot & PDF Generator](https://apify.com/thriving_adder/website-screenshot-pdf) | Captures full-page PNG/JPEG screenshots and PDFs of public pages, on desktop or mobile. | $0.002 per screenshot, $0.0025 per PDF |

### Examples

| Folder | File | What it shows |
|---|---|---|
| sec-edgar-xbrl | `sec_financials_to_pandas.py` | AAPL and MSFT annual revenue, net income and net margin as a pandas table and CSV |
| | `latest_filings.mjs` | The latest 10-K/10-Q/8-K filings for NVDA and TSLA, with links |
| bulk-lighthouse | `lighthouse_to_csv.py` | Lighthouse scores and Core Web Vitals as a CSV you can import into Google Sheets |
| web-to-markdown | `markdown_chunks_for_rag.py` | Turns pages into Markdown chunks in a JSONL file, ready for embeddings |
| | `llms_txt_for_docs.mjs` | Generates `llms.txt` for a docs site (docs.python.org/3, 10 pages) |
| | `curl.sh` | Converts one page with a single synchronous API call |
| sea-open-data | `sea_open_data_to_pandas.py` | Malaysian CPI (OpenDOSM) and BNM exchange rates as pandas DataFrames, printed with the required attribution |
| | `curl.sh` | Latest Singapore HDB resale transactions (data.gov.sg) as CSV |
| academic-papers | `papers_to_csv.py` | Searches papers on a topic and saves a CSV for screening |
| | `doi_lookup.mjs` | Looks up DOIs and prints short citations |
| sitemap-url-health | `sitemap_health_report.py` | Checks sitemap URLs and prints a short report, with a CSV |
| | `curl.sh` | Lists and checks sitemap URLs as CSV in one call |
| page-metadata | `metadata_extract.py` | Shows titles, descriptions, OG image, JSON-LD types, tech and SEO issues for 3 sites |
| | `curl.sh` | Returns the same fields as CSV in one call |
| screenshot-pdf | `capture.py` | Desktop PNG and PDF of a page, downloaded to `output/` |
| | `capture_mobile.mjs` | A mobile JPEG screenshot |

## Setup

You need a free Apify account and its API token from **Console → Settings → API & Integrations**. Apify's Free plan currently includes a monthly platform credit (US$5 per month as of October 2026; see [apify.com/pricing](https://apify.com/pricing) for current terms). Every example here uses a few cents at most.

```bash
export APIFY_TOKEN="your-token-here"   # never commit it; the examples only read it from the environment

# Python 3.10+
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
cd sec-edgar-xbrl && python sec_financials_to_pandas.py

# Node.js 18+
npm install
cd academic-papers && node doi_lookup.mjs

# curl
cd page-metadata && ./curl.sh
```

Results are written to an `output/` folder next to each script. That folder is ignored by git.

### Cost caps

Every example sets a maximum cost per run. In Python that is `max_total_charge_usd`, in JS `maxTotalChargeUsd`, and in curl the `maxTotalChargeUsd` query parameter. The Actor stops starting new paid work when the cap is reached and keeps the results it already has. Some Actors require a minimum cap (for example, $0.03 for Web to Markdown, because one llms.txt file costs $0.02). You only pay for events that actually happen, not the cap.

### Data and responsible use

- These Actors only read public data. They never log in anywhere, they identify themselves with an honest User-Agent, and the ones that fetch web pages respect robots.txt. The data Actors use official public APIs.
- Run the URL-based Actors on sites you own or are allowed to audit.
- Open-data rows include their licence and attribution text. Keep them when you share the data (CC BY 4.0 for OpenDOSM, the Singapore Open Data Licence for data.gov.sg, and BNM's terms of use).
- This repository contains no scraped data and no tokens.

## Test log

On **29 Oct 2026** I ran every example once against the live Actors with the tiny inputs shown in the code. That was 21 runs in total, including reruns after fixes, and every run SUCCEEDED. The test harness in `tests/` sends the calls through the logged-in Apify CLI, so no token was used or stored.

| Example | Result |
|---|---|
| sec_financials_to_pandas.py | ✅ 18 XBRL facts, 9 fiscal years (AAPL FY2022–25, MSFT FY2022–26) |
| latest_filings.mjs | ✅ 6 filings with links |
| lighthouse_to_csv.py | ✅ 1 mobile audit (python.org) |
| markdown_chunks_for_rag.py | ✅ 2 pages, 20 chunks |
| llms_txt_for_docs.mjs | ✅ llms.txt for docs.python.org/3 |
| web-to-markdown/curl.sh | ⚠️ Not run in its final form, because the test account hit its monthly usage limit. The first attempt had a cap below the Actor's $0.03 minimum and was rejected, which led to the cap note above. The same call works from Python. |
| sea_open_data_to_pandas.py | ✅ 12 CPI months and 5 exchange rates, with attribution |
| sea-open-data/curl.sh | ✅ 5 HDB resale rows as CSV |
| papers_to_csv.py | ✅ 10 unique papers |
| doi_lookup.mjs | ✅ 2 DOIs resolved |
| sitemap_health_report.py | ✅ 10 URLs checked on crawlee.dev |
| sitemap-url-health/curl.sh | ✅ 5 URLs as CSV |
| metadata_extract.py | ✅ 3 pages |
| page-metadata/curl.sh | ✅ 2 pages as CSV |
| capture.py | ✅ 1 PNG and 1 PDF downloaded |
| capture_mobile.mjs | ✅ 1 mobile JPEG downloaded |

**Cost of the test round:**
- About **$0.014** of Apify platform usage.
- About **$0.12** of events at list prices. These did not show up as paid-Actor usage on the account, because the runs were made by the Actors' owner.
- A normal user running every example once would pay roughly $0.10–0.15 in total.

To rerun the tests yourself, you need the Apify CLI logged in, the venv and `npm install`. Then run `PYTHON=.venv/bin/python tests/run_all.sh`. The harness routes calls through `apify api` so your token never appears in the code or in logs.

## License

MIT. See [LICENSE](LICENSE). "Apify" is a trademark of Apify Technologies s.r.o. This project is not affiliated with or endorsed by Apify, the SEC, DOSM, BNM, GovTech Singapore, OpenAlex or Crossref.
