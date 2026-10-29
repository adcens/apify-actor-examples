import { createRequire } from 'node:module';
const require = createRequire(new URL('../package.json', import.meta.url));
const real = require('apify-client');
export class ApifyClient extends real.ApifyClient {
    constructor(options = {}) { super({ ...options, baseUrl: process.env.EXAMPLES_PROXY_URL ?? 'http://127.0.0.1:8765' }); }
}
export default { ...real, ApifyClient };
