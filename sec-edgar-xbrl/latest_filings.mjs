// Latest 10-K / 10-Q / 8-K filings for a few tickers, with direct document links.
// Actor: https://apify.com/thriving_adder/sec-edgar-filings-xbrl  (about $0.001 per filing)
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('thriving_adder/sec-edgar-filings-xbrl').call(
    { companies: ['NVDA', 'TSLA'], formTypes: ['10-K', '10-Q', '8-K'], maxFilingsPerCompany: 3 },
    { maxTotalChargeUsd: 0.02 },
);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const f of items.filter((i) => i.type === 'filing')) {
    console.log(`${f.ticker}  ${f.form.padEnd(5)} filed ${f.filingDate}  ${f.documentUrl}`);
}
for (const e of items.filter((i) => i.error)) console.log(`(not charged) ${e.input}: ${e.errorCode}`);
