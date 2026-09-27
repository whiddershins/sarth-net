import { canonicalRedirect } from "./canonical.js";
import { feedRewrite } from "./feeds.js";

export default {
  async fetch(request, env) {
    const target = canonicalRedirect(request);
    if (target) {
      return new Response(null, {
        status: 301,
        headers: {
          Location: target,
          "X-Robots-Tag": "noindex",
        },
      });
    }
    // Apple Podcasts and podcastrepublic subscribe to the old Squarespace
    // feed address, and the old blog feed was /words?format=rss.
    // _redirects cannot match a query string.
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
