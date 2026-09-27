import { canonicalRedirect } from "./canonical.js";

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
    // Canonical requests go through the asset pipeline, which still applies
    // public/_redirects, html_handling, and not_found_handling.
    return env.ASSETS.fetch(request);
  },
};
