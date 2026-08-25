const REDIRECTS = {
  "/sarthnet-in-transition": "/",
  "/sarth": "/",
  "/words": "/transmissions/",
  "/words/2026/7/31/visual-reference-prompting": "/transmissions/visual-reference-prompting/",
  "/rumors": "/transmissions/",
  "/rumors/2015/2/10/a-wonderful-write-up-of-the-book-of-sarth-on-the-verge": "/sightings/",
  "/rumors/2015/2/10/the-book-of-sarth-gizmodo-apps-of-the-week": "/sightings/",
  "/category/conspirators/rob-wasserman": "/conspirators/rob-wasserman/",
  "/category/conspirators/lou-reed": "/conspirators/lou-reed/",
  "/booking": "/contact/",
  "/happenings": "/",
  "/me-time-score": "/",
  "/new-blog": "/",
  "/intrigue": "/",
  "/category/press": "/sightings/",
  "/category/reviews": "/sightings/",
  "/category/conspiracies/metal-machine-trio": "/conspiracies/metal-machine-trio/",
  "/category/conspiracies/lou-reed-metallica-project": "/conspiracies/lulu/",
  "/metal-machine-trio-the-creation-of-the-universe": "/conspiracies/metal-machine-trio/",
  "/introspections": "/",
  "/introspections-collection": "/",
  "/introspections-about": "/",
};

const EXTERNAL = {
  "/book-of-sarth-in-the-app-store": "https://bookofsarth.com/",
};

function normalize(pathname) {
  if (pathname.length > 1 && pathname.endsWith("/")) {
    return pathname.slice(0, -1);
  }
  return pathname;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = normalize(url.pathname);

    const external = EXTERNAL[path];
    if (external) {
      return Response.redirect(external, 301);
    }

    const dest = REDIRECTS[path];
    if (dest) {
      return Response.redirect(new URL(dest, url.origin), 301);
    }

    return env.ASSETS.fetch(request);
  },
};
