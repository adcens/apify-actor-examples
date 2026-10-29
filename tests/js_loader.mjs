// Tests only: `node --import ./tests/js_loader.mjs example.mjs` makes `apify-client` point at the local CLI proxy.
import { register } from 'node:module';
register('./js_hooks.mjs', import.meta.url);
