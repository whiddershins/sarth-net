#!/usr/bin/env python3
"""Local preview with the holes editable in place.

  python3 scripts/dev.py [port]      default 8788, binds 127.0.0.1 only

Serves public/ like a static host. Into every HTML page it injects a small
script that makes each <div class="hole"> editable. Click a hole, type, click
away (or press Cmd+S): the text is written to content/holes/<id>.md,
scripts/build.py runs, and the page reloads showing the built HTML.

Nothing here touches the published site. The injection happens only in the
response this server sends; the files under public/ are what the build wrote.
Stdlib only.
"""
import json
import re
import subprocess
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
HOLES = ROOT / "content" / "holes"
BUILD = ROOT / "scripts" / "build.py"
ID_RE = re.compile(r"^[a-z0-9-]+/[a-z0-9-]+$")

CLIENT = r"""
<style>
  .hole { position: relative; outline: 1px dashed rgba(255,255,255,.35); outline-offset: 8px; border-radius: 2px; cursor: text; }
  .hole:focus-within { outline-color: rgba(255,255,255,.85); }
  .hole::after { content: attr(data-status); position: absolute; right: 0; top: -1.6em; font-size: .7rem; letter-spacing: .1em; text-transform: uppercase; opacity: .65; }
</style>
<script>
(() => {
  document.querySelectorAll('.hole[data-hole]').forEach(h => {
    const isPrompt = () => /^\[[\s\S]*\]$/.test(h.innerText.trim());
    let original = h.innerText.trim();
    h.dataset.status = 'click to write';
    h.setAttribute('contenteditable', 'plaintext-only');
    if (!h.isContentEditable) h.setAttribute('contenteditable', 'true');
    h.addEventListener('focus', () => {
      if (isPrompt()) h.innerText = '';
      h.dataset.status = 'editing · click away or ⌘S to save';
    });
    const save = async () => {
      const text = h.innerText.trim();
      if (text === original) { h.dataset.status = 'click to write'; return; }
      if (text === '' && /^\[/.test(original)) { location.reload(); return; }
      h.dataset.status = 'saving';
      try {
        const r = await fetch('/_hole', { method: 'POST', headers: { 'content-type': 'application/json' },
                                          body: JSON.stringify({ id: h.dataset.hole, text }) });
        const j = await r.json();
        if (j.ok) { h.dataset.status = 'saved'; setTimeout(() => location.reload(), 250); }
        else { h.dataset.status = 'not saved: ' + (j.error || r.status); }
      } catch (e) { h.dataset.status = 'not saved: ' + e; }
    };
    h.addEventListener('blur', save);
    h.addEventListener('keydown', e => {
      if ((e.metaKey || e.ctrlKey) && e.key === 's') { e.preventDefault(); h.blur(); }
    });
  });
})();
</script>
"""


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC), **kwargs)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s\n" % (fmt % args))

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        target = (PUBLIC / path.lstrip("/")).resolve()
        if path.endswith("/"):
            target = target / "index.html"
        if target.suffix == ".html" and target.is_file() and PUBLIC.resolve() in target.parents:
            body = target.read_text()
            body = body.replace("</body>", CLIENT + "</body>", 1).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def do_POST(self):
        if self.path != "/_hole":
            self.send_error(404)
            return
        n = int(self.headers.get("Content-Length") or 0)
        try:
            data = json.loads(self.rfile.read(n) or b"{}")
        except json.JSONDecodeError:
            return self._json(400, {"ok": False, "error": "bad json"})
        hid, text = str(data.get("id", "")), str(data.get("text", ""))
        if not ID_RE.match(hid):
            return self._json(400, {"ok": False, "error": "bad hole id"})
        target = HOLES / (hid.replace("/", "--") + ".md")
        paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
        HOLES.mkdir(parents=True, exist_ok=True)
        target.write_text("\n\n".join(paras) + ("\n" if paras else ""))
        r = subprocess.run([sys.executable, str(BUILD)], capture_output=True, text=True, cwd=ROOT)
        self._json(200, {"ok": r.returncode == 0, "error": (r.stdout + r.stderr).strip() if r.returncode else ""})

    def _json(self, code, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8788
    print(f"sarth.net with editable holes at http://127.0.0.1:{port}/  (Ctrl-C to stop)")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
