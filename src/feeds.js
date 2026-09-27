// Old Squarespace feed addresses. The HTML paths stay pages; only format=rss
// is a feed. _redirects cannot see the query string, so the Worker does this.

export function feedRewrite(url) {
  const parsed = typeof url === "string" ? new URL(url) : url;
  if (parsed.searchParams.get("format") !== "rss") return null;
  const path = parsed.pathname;
  if (path === "/beautiful-tornado" || path === "/beautiful-tornado/") {
    return {
      path: "/transmissions/beautiful-tornado/podcast.xml",
      contentType: "application/rss+xml; charset=utf-8",
    };
  }
  if (path === "/words" || path === "/words/") {
    return {
      path: "/feed.xml",
      contentType: "application/atom+xml; charset=utf-8",
    };
  }
  return null;
}
