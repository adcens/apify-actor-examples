// Mobile JPEG screenshot of a page, downloaded to ./output.
// Actor: https://apify.com/thriving_adder/website-screenshot-pdf  ($0.002 per screenshot)
// The jpegUrl in the results is a signed download link: treat it like a private link.
import { writeFile, mkdir } from 'node:fs/promises';
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('thriving_adder/website-screenshot-pdf').call(
    { urls: [{ url: 'https://example.com/' }], viewport: 'mobile', outputFormats: ['jpeg'], jpegQuality: 70 },
    { maxTotalChargeUsd: 0.01 },
);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
await mkdir('output', { recursive: true });
for (const i of items) {
    if (i.error) { console.log(`${i.url}: ${i.error}`); continue; }
    const res = await fetch(i.jpegUrl);
    const file = `output/${i.jpegKey}.jpg`;
    await writeFile(file, Buffer.from(await res.arrayBuffer()));
    console.log(`${i.url} -> ${file} (${i.jpegBytes} bytes, ${i.pageHeightPx}px tall)`);
}
