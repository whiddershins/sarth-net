// Host and scheme redirects for sarth.net. Canonical is https://www.sarth.net.
// Loopback is left alone so `wrangler dev` can serve the pages.

export const CANONICAL_ORIGIN = "https://www.sarth.net";

const LOCAL_HOSTS = new Set(["localhost", "127.0.0.1", "::1"]);

export function hostnameOf(request) {
  const raw = request.headers.get("host") || new URL(request.url).host;
  const withoutPort = raw.replace(/:\d+$/, "");
  return withoutPort.replace(/^\[/, "").replace(/\]$/, "").toLowerCase();
}

export function requestScheme(request) {
  const visitor = request.headers.get("cf-visitor");
  if (visitor) {
    try {
      const parsed = JSON.parse(visitor);
      if (parsed && parsed.scheme) return String(parsed.scheme).toLowerCase();
    } catch {
      // Fall through to the forwarded protocol.
    }
  }
  const forwarded = request.headers.get("x-forwarded-proto");
  if (forwarded) return forwarded.split(",")[0].trim().toLowerCase();
  return new URL(request.url).protocol.replace(":", "").toLowerCase();
}

// Null when the request is already on the canonical origin, or is local dev.
// Otherwise the https://www.sarth.net URL with the same path and query.
export function canonicalRedirect(request) {
  const host = hostnameOf(request);
  if (LOCAL_HOSTS.has(host)) return null;
  const scheme = requestScheme(request);
  if (host === "www.sarth.net" && scheme === "https") return null;
  const url = new URL(request.url);
  return CANONICAL_ORIGIN + url.pathname + url.search;
}
