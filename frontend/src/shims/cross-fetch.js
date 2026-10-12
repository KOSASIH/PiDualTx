// Safe browser shim for cross-fetch preventing read-only window.fetch property mutation errors
const _fetch = typeof globalThis !== 'undefined' && globalThis.fetch
  ? globalThis.fetch.bind(globalThis)
  : (typeof window !== 'undefined' && window.fetch ? window.fetch.bind(window) : () => Promise.reject(new Error('fetch not available')));

const _Headers = typeof globalThis !== 'undefined' ? globalThis.Headers : (typeof window !== 'undefined' ? window.Headers : undefined);
const _Request = typeof globalThis !== 'undefined' ? globalThis.Request : (typeof window !== 'undefined' ? window.Request : undefined);
const _Response = typeof globalThis !== 'undefined' ? globalThis.Response : (typeof window !== 'undefined' ? window.Response : undefined);

export default _fetch;
export { _fetch as fetch, _Headers as Headers, _Request as Request, _Response as Response };
