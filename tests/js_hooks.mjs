const WRAPPER = new URL('./apify_client_proxy.mjs', import.meta.url).href;
export async function resolve(specifier, context, next) {
    if (specifier === 'apify-client' && context.parentURL !== WRAPPER) return { url: WRAPPER, shortCircuit: true };
    return next(specifier, context);
}
