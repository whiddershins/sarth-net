import assert from "node:assert/strict";
import test from "node:test";
import { canonicalRedirect } from "../src/canonical.js";
import { feedRewrite } from "../src/feeds.js";
import worker from "../src/index.js";

function req(url, headers = {}) {
  return new Request(url, { headers });
}

test("loopback is served, not redirected", () => {
  assert.equal(canonicalRedirect(req("http://127.0.0.1:8787/about/?q=1")), null);
  assert.equal(canonicalRedirect(req("http://localhost:8787/work/")), null);
  assert.equal(canonicalRedirect(req("http://[::1]:8787/")), null);
});

test("apex and http and workers.dev keep the path and query", () => {
  assert.equal(
    canonicalRedirect(req("https://sarth.net/about/?q=1", { host: "sarth.net" })),
    "https://www.sarth.net/about/?q=1",
  );
  assert.equal(
    canonicalRedirect(req("http://sarth.net/llms.txt", { host: "sarth.net" })),
    "https://www.sarth.net/llms.txt",
  );
  assert.equal(
    canonicalRedirect(req("https://www.sarth.net/about/", {
      host: "www.sarth.net",
      "cf-visitor": '{"scheme":"http"}',
    })),
    "https://www.sarth.net/about/",
  );
  assert.equal(
    canonicalRedirect(req("https://sarth-net.sarth.workers.dev/work/?x=1", {
      host: "sarth-net.sarth.workers.dev",
    })),
    "https://www.sarth.net/work/?x=1",
  );
  assert.equal(
    canonicalRedirect(req("https://sarth-net.marshy-runner.workers.dev/llms.txt", {
      host: "sarth-net.marshy-runner.workers.dev",
    })),
    "https://www.sarth.net/llms.txt",
  );
  assert.equal(
    canonicalRedirect(req("https://www.sarth.net/booking", {
      host: "WWW.SARTH.NET",
      "x-forwarded-proto": "http",
    })),
    "https://www.sarth.net/booking",
  );
});

test("the canonical origin is not redirected", () => {
  assert.equal(
    canonicalRedirect(req("https://www.sarth.net/about/?q=1", {
      host: "www.sarth.net",
      "cf-visitor": '{"scheme":"https"}',
    })),
    null,
  );
});

test("a Host header overrides the wrangler dev URL", () => {
  assert.equal(
    canonicalRedirect(req("http://127.0.0.1:8787/words/2026/7/31/visual-reference-prompting?x=1", {
      host: "sarth.net",
    })),
    "https://www.sarth.net/words/2026/7/31/visual-reference-prompting?x=1",
  );
});

test("format=rss on the old Squarespace feed paths is a feed file", () => {
  assert.deepEqual(feedRewrite("https://www.sarth.net/beautiful-tornado?format=rss"), {
    path: "/transmissions/beautiful-tornado/podcast.xml",
    contentType: "application/rss+xml; charset=utf-8",
  });
  assert.deepEqual(feedRewrite(new URL("https://www.sarth.net/beautiful-tornado/?format=rss")), {
    path: "/transmissions/beautiful-tornado/podcast.xml",
    contentType: "application/rss+xml; charset=utf-8",
  });
  assert.deepEqual(feedRewrite("https://www.sarth.net/words?format=rss"), {
    path: "/feed.xml",
    contentType: "application/atom+xml; charset=utf-8",
  });
  assert.deepEqual(feedRewrite("https://www.sarth.net/words/?format=rss"), {
    path: "/feed.xml",
    contentType: "application/atom+xml; charset=utf-8",
  });
});

test("format=RSS is a feed in any case", () => {
  for (const value of ["RSS", "Rss", "rSs"]) {
    assert.deepEqual(feedRewrite(`https://www.sarth.net/words?format=${value}`), {
      path: "/feed.xml",
      contentType: "application/atom+xml; charset=utf-8",
    });
    assert.deepEqual(feedRewrite(`https://www.sarth.net/beautiful-tornado?format=${value}`), {
      path: "/transmissions/beautiful-tornado/podcast.xml",
      contentType: "application/rss+xml; charset=utf-8",
    });
  }
});

test("the WordPress feed addresses are the site feed", () => {
  for (const path of ["/feed", "/feed/", "/feed/rss", "/feed/rss/", "/feed/atom", "/feed/atom/"]) {
    assert.deepEqual(feedRewrite(`https://www.sarth.net${path}`), {
      path: "/feed.xml",
      contentType: "application/atom+xml; charset=utf-8",
    });
  }
  assert.equal(feedRewrite("https://www.sarth.net/feed/other/"), null);
  assert.equal(feedRewrite("https://www.sarth.net/category/music/feed/"), null);
});

test("other paths and formats are not feeds", () => {
  for (const url of [
    "https://www.sarth.net/beautiful-tornado",
    "https://www.sarth.net/beautiful-tornado?format=json",
    "https://www.sarth.net/transmissions/beautiful-tornado/?format=rss",
    "https://www.sarth.net/words/2015/2/6/x?format=rss",
  ]) {
    assert.equal(feedRewrite(url), null);
  }
});

function assets(body, contentType) {
  const seen = [];
  return {
    seen,
    env: {
      ASSETS: {
        fetch(request) {
          seen.push(request);
          return new Response(body, { headers: { "content-type": contentType } });
        },
      },
    },
  };
}

test("the worker serves the podcast file for the old feed URL", async () => {
  const { seen, env } = assets("<rss/>", "application/xml");
  const res = await worker.fetch(new Request("https://www.sarth.net/beautiful-tornado?format=rss", {
    headers: { host: "www.sarth.net", "cf-visitor": '{"scheme":"https"}' },
  }), env);
  assert.equal(res.status, 200);
  assert.equal(res.headers.get("content-type"), "application/rss+xml; charset=utf-8");
  assert.equal(new URL(seen[0].url).pathname, "/transmissions/beautiful-tornado/podcast.xml");
  assert.equal(new URL(seen[0].url).search, "");
});

test("the worker serves the atom feed for the old blog feed URL", async () => {
  const { seen, env } = assets("<feed/>", "application/xml");
  const res = await worker.fetch(new Request("https://www.sarth.net/words?format=rss", {
    headers: { host: "www.sarth.net", "cf-visitor": '{"scheme":"https"}' },
  }), env);
  assert.equal(res.status, 200);
  assert.equal(res.headers.get("content-type"), "application/atom+xml; charset=utf-8");
  assert.equal(new URL(seen[0].url).pathname, "/feed.xml");
  assert.equal(new URL(seen[0].url).search, "");
});

test("the worker serves the site feed for /words?format=RSS and /feed/", async () => {
  for (const url of ["https://www.sarth.net/words?format=RSS", "https://www.sarth.net/feed/", "https://www.sarth.net/feed/rss/"]) {
    const { seen, env } = assets("<feed/>", "application/xml");
    const res = await worker.fetch(new Request(url, {
      headers: { host: "www.sarth.net", "cf-visitor": '{"scheme":"https"}' },
    }), env);
    assert.equal(res.status, 200);
    assert.equal(res.headers.get("content-type"), "application/atom+xml; charset=utf-8");
    assert.equal(new URL(seen[0].url).pathname, "/feed.xml");
  }
});

test("a beautiful-tornado page is passed to assets as requested", async () => {
  const request = new Request("https://www.sarth.net/beautiful-tornado", {
    headers: { host: "www.sarth.net", "cf-visitor": '{"scheme":"https"}' },
  });
  const { seen, env } = assets("page", "text/html");
  const res = await worker.fetch(request, env);
  assert.equal(res.status, 200);
  assert.equal(seen[0], request);
});

test("http on the podcast feed still redirects to https and keeps the query", async () => {
  const { seen, env } = assets("", "application/xml");
  const res = await worker.fetch(new Request("http://www.sarth.net/beautiful-tornado?format=rss", {
    headers: { host: "www.sarth.net" },
  }), env);
  assert.equal(res.status, 301);
  assert.equal(res.headers.get("location"), "https://www.sarth.net/beautiful-tornado?format=rss");
  assert.equal(seen.length, 0);
});

