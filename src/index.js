import { CANONICAL_ORIGIN, canonicalRedirect } from "./canonical.js";
import { feedRewrite } from "./feeds.js";

const REDIRECT_STATUSES = new Set([301, 302, 307, 308]);

// The asset layer answers a directory URL without its trailing slash with a
// 307 to the slashed path. When the host hop would land on such a path, ask
// the assets first and put the slash into the same 301, so an apex or http
// visitor takes one hop instead of two. Anything the assets serve directly
// (files, 200 rewrites in _redirects, the feed paths) keeps its path as is.
export async function directoryTarget(target, request, env) {
  const url = new URL(target);
  const path = url.pathname;
  if (path.endsWith("/")) return target;
  if (path.slice(path.lastIndexOf("/") + 1).includes(".")) return target;
  if (request.method !== "GET" && request.method !== "HEAD") return target;
  if (feedRewrite(url)) return target;
  if (!env || !env.ASSETS) return target;
  let probe;
  try {
    probe = await env.ASSETS.fetch(new Request(CANONICAL_ORIGIN + path, { method: "HEAD" }));
  } catch {
    return target;
  }
  if (!REDIRECT_STATUSES.has(probe.status)) return target;
  const location = probe.headers.get("location");
  if (!location) return target;
  const next = new URL(location, CANONICAL_ORIGIN + path);
  if (next.pathname !== path + "/") return target;
  return CANONICAL_ORIGIN + next.pathname + url.search;
}

export default {
  async fetch(request, env) {
    const target = canonicalRedirect(request);
    if (target) {
      // A plain 301. No X-Robots-Tag: the redirect alone tells crawlers which
      // URL to index, and a noindex here put the http and apex addresses under
      // "Excluded by 'noindex' tag" in Search Console.
      return new Response(null, {
        status: 301,
        headers: { Location: await directoryTarget(target, request, env) },
      });
    }
    // Apple Podcasts and podcastrepublic subscribe to the old Squarespace
    // feed address, and the old blog feeds were /words?format=rss and the
    // WordPress /feed/. _redirects cannot match a query string.
    const feed = feedRewrite(request.url);
    if (feed) {
      const assetUrl = new URL(feed.path, request.url);
      const asset = await env.ASSETS.fetch(new Request(assetUrl, {
        method: request.method,
        headers: request.headers,
      }));
      if (!asset.ok) return asset;
      const headers = new Headers(asset.headers);
      headers.set("Content-Type", feed.contentType);
      headers.set("X-Content-Type-Options", "nosniff");
      return new Response(asset.body, { status: asset.status, headers });
    }
    // Canonical requests go through the asset pipeline, which still applies
    // public/_redirects, html_handling, and not_found_handling.
    return env.ASSETS.fetch(request);
  },
};
