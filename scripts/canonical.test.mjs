import assert from "node:assert/strict";
import test from "node:test";
import { canonicalRedirect } from "../src/canonical.js";

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
