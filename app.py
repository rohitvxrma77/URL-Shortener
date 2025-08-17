from __future__ import annotations
from flask import Flask, request, redirect, jsonify, render_template_string
import string, random, json, os, datetime
from typing import Dict, Any
from user_agents import parse as ua_parse

DB_FILE = "urls.json"
app = Flask(__name__)

HTML = """
<!doctype html>
<title>Smart URL Shortener</title>
<link rel="stylesheet" href="https://unpkg.com/mvp.css">
<main>
  <h1>Smart URL Shortener</h1>
  <form method="post" action="/shorten">
    <label>Long URL</label>
    <input name="url" placeholder="https://example.com" required>
    <button type="submit">Shorten</button>
  </form>
  {% if short %}
    <p><b>Short URL:</b> <a href="/{{ short }}">/{{ short }}</a></p>
    <pre>{{ stats }}</pre>
  {% endif %}
  <hr>
  <h3>Look up stats</h3>
  <form method="get" action="/stats">
    <input name="slug" placeholder="slug" required>
    <button type="submit">Get Stats</button>
  </form>
</main>
"""

def now_iso() -> str:
    return datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"

def load_db() -> Dict[str, Any]:
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except json.JSONDecodeError: return {}

def save_db(db: Dict[str, Any]) -> None:
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)

def gen_slug(n: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(n))

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML, short=None, stats="")

@app.route("/shorten", methods=["POST"])
def shorten():
    db = load_db()
    url = request.json["url"] if request.is_json else request.form.get("url", "")
    if not url.startswith(("http://", "https://")):
        return jsonify({"error": "URL must start with http:// or https://"}), 400

    slug = gen_slug()
    while slug in db:
        slug = gen_slug()

    db[slug] = {
        "long": url,
        "created": now_iso(),
        "clicks": 0,
        "last_clicked": None,
        "ua_stats": {"mobile": 0, "tablet": 0, "pc": 0, "bot": 0}
    }
    save_db(db)

    stats = json.dumps(db[slug], indent=2)
    if request.is_json:
        return jsonify({"short": slug, "stats": db[slug]})
    return render_template_string(HTML, short=slug, stats=stats)

@app.route("/<slug>", methods=["GET"])
def visit(slug: str):
    db = load_db()
    item = db.get(slug)
    if not item: return "Not found", 404

    ua = ua_parse(request.headers.get("User-Agent", ""))
    kind = "bot" if ua.is_bot else ("mobile" if ua.is_mobile else "tablet" if ua.is_tablet else "pc")
    item["clicks"] += 1
    item["last_clicked"] = now_iso()
    item["ua_stats"][kind] = item["ua_stats"].get(kind, 0) + 1
    save_db(db)
    return redirect(item["long"], code=302)

@app.route("/stats", methods=["GET"])
def stats():
    db = load_db()
    slug = request.args.get("slug", "")
    if slug in db:
        return jsonify({slug: db[slug]})
    return jsonify({"error": "not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
