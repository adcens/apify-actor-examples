// Generate an llms.txt for a documentation site (or a sub-path of it) and save it locally.
// Actor: https://apify.com/thriving_adder/web-to-markdown-llms-txt  ($0.02 per llms.txt)
// Meant for sites you run: review the file, then publish it as /llms.txt on your own site.
import { writeFile, mkdir } from 'node:fs/promises';
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('thriving_adder/web-to-markdown-llms-txt').call(
    { llmsTxtSites: [{ url: 'https://docs.python.org/3/' }], maxPagesPerSite: 10 },
    { maxTotalChargeUsd: 0.05 },
);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const site = items.find((i) => i.type === 'llms-txt');
if (!site || site.error) throw new Error(`No llms.txt: ${site?.error ?? 'no result'}`);
await mkdir('output', { recursive: true });
await writeFile('output/llms.txt', site.llmsTxt);
console.log(`${site.site}: ${site.pageCount} pages via ${site.discovery}; saved output/llms.txt`);
console.log(site.llmsTxt.split('\n').slice(0, 12).join('\n'));
