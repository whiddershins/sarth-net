// Old feed addresses. The HTML paths stay pages; only format=rss (any case:
// Squarespace wrote format=RSS) is a feed. The WordPress site's /feed/,
// /feed/rss/ and /feed/atom/ are the site feed. _redirects cannot see the
// query string, so the Worker does this.

const SITE_FEED = {
  path: "/feed.xml",
  contentType: "application/atom+xml; charset=utf-8",
};

const FEED_PATHS = new Set(["/feed", "/feed/", "/feed/rss", "/feed/rss/", "/feed/atom", "/feed/atom/"]);

export function feedRewrite(url) {
  const parsed = typeof url === "string" ? new URL(url) : url;
  const path = parsed.pathname;
  if (FEED_PATHS.has(path)) return { ...SITE_FEED };
  if ((parsed.searchParams.get("format") || "").toLowerCase() !== "rss") return null;
  if (path === "/beautiful-tornado" || path === "/beautiful-tornado/") {
    return {
      path: "/transmissions/beautiful-tornado/podcast.xml",
      contentType: "application/rss+xml; charset=utf-8",
    };
  }
  if (path === "/words" || path === "/words/") return { ...SITE_FEED };
  return null;
}
