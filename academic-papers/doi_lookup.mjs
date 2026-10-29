// Look up a list of DOIs and print a short citation for each. Unknown or invalid DOIs are free rows.
// Actor: https://apify.com/thriving_adder/academic-research-papers  ($0.001 per paper)
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('thriving_adder/academic-research-papers').call(
    { dois: ['10.1038/nature14539', '10.1145/3065386'], includeAbstract: false },
    { maxTotalChargeUsd: 0.01 },
);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const p of items) {
    if (p.error) { console.log(`${p.lookup}: ${p.errorCode} (not charged)`); continue; }
    const authors = p.authors.length > 2 ? `${p.authors[0]} et al.` : p.authors.join(' & ');
    console.log(`${authors} (${p.publicationYear}). ${p.title}. ${p.venue ?? ''}. https://doi.org/${p.doi}`);
}
