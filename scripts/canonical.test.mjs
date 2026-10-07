import assert from "node:assert/strict";
import test from "node:test";
import { readFileSync } from "node:fs";
import { canonicalRedirect } from "../src/canonical.js";
import { feedRewrite } from "../src/feeds.js";
import worker, { directoryTarget } from "../src/index.js";

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

// The asset layer as deployed: a directory URL without its slash is a 307 to
// the slashed path; files, slashed directories and 200 rewrites are a 200.
function slashingAssets(directories) {
  const seen = [];
  return {
    seen,
    env: {
      ASSETS: {
        fetch(request) {
          seen.push(request);
          const path = new URL(request.url).pathname;
          if (directories.includes(path)) {
            return new Response(null, { status: 307, headers: { location: path + "/" } });
          }
          return new Response("ok", { status: 200 });
        },
      },
    },
  };
}

test("the host redirect carries no X-Robots-Tag", async () => {
  const { env } = slashingAssets([]);
  for (const url of ["https://sarth.net/about/", "http://sarth.net/", "http://www.sarth.net/llms.txt"]) {
    const res = await worker.fetch(new Request(url, { headers: { host: new URL(url).host } }), env);
    assert.equal(res.status, 301);
    assert.equal(res.headers.get("x-robots-tag"), null);
  }
});

test("the host redirect adds a directory's trailing slash in the same hop", async () => {
  const { env } = slashingAssets(["/about", "/conspiracies/lulu"]);
  let res = await worker.fetch(new Request("https://sarth.net/about?x=1", { headers: { host: "sarth.net" } }), env);
  assert.equal(res.status, 301);
  assert.equal(res.headers.get("location"), "https://www.sarth.net/about/?x=1");
  res = await worker.fetch(new Request("http://www.sarth.net/conspiracies/lulu", { headers: { host: "www.sarth.net" } }), env);
  assert.equal(res.headers.get("location"), "https://www.sarth.net/conspiracies/lulu/");
});

test("the host redirect keeps the path when the assets serve it as is", async () => {
  const { seen, env } = slashingAssets(["/about"]);
  const cases = [
    ["https://sarth.net/sarth", "https://www.sarth.net/sarth"],              // a 200 rewrite
    ["https://sarth.net/llms.txt", "https://www.sarth.net/llms.txt"],        // a file: not probed
    ["https://sarth.net/about/", "https://www.sarth.net/about/"],            // already slashed: not probed
    ["https://sarth.net/words?format=RSS", "https://www.sarth.net/words?format=RSS"], // a feed: not probed
    ["https://sarth.net/feed", "https://www.sarth.net/feed"],                // a feed: not probed
  ];
  for (const [from, to] of cases) {
    const res = await worker.fetch(new Request(from, { headers: { host: "sarth.net" } }), env);
    assert.equal(res.headers.get("location"), to);
  }
  assert.deepEqual(seen.map((r) => new URL(r.url).pathname), ["/sarth"]);
});

test("a slash probe that fails or points elsewhere leaves the target alone", async () => {
  const broken = { ASSETS: { fetch() { throw new Error("down"); } } };
  assert.equal(
    await directoryTarget("https://www.sarth.net/about", new Request("https://sarth.net/about"), broken),
    "https://www.sarth.net/about",
  );
  const elsewhere = { ASSETS: { fetch() { return new Response(null, { status: 307, headers: { location: "/other/" } }); } } };
  assert.equal(
    await directoryTarget("https://www.sarth.net/about", new Request("https://sarth.net/about"), elsewhere),
    "https://www.sarth.net/about",
  );
  const post = new Request("https://sarth.net/about", { method: "POST" });
  assert.equal(await directoryTarget("https://www.sarth.net/about", post, elsewhere), "https://www.sarth.net/about");
});

test("every _redirects rule is a 200 rewrite to a page here, never a redirect", () => {
  const text = readFileSync(new URL("../public/_redirects", import.meta.url), "utf8");
  const rules = text
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith("#"))
    .map((line) => line.split(/\s+/));
  assert.ok(rules.length > 0);
  for (const [from, to, code] of rules) {
    assert.equal(code, "200", `${from} -> ${to} is a ${code}`);
    assert.ok(to.startsWith("/") && !to.startsWith("//"), `${from} -> ${to} leaves the site`);
    assert.ok(!from.includes("*") && !from.includes(":"), `${from} is a splat`);
  }
});
