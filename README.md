# URL-Shortener
Smart URL Shortener (with Analytics)
A tiny Flask app that shortens URLs and tracks basic analytics:

Total clicks

Last clicked timestamp

User-agent breakdown (mobile/tablet/pc/bot)

Great for showcasing full-stack fundamentals, simple persistence, and lightweight analytics.

Features
Shorten any http/https URL to a 6-character slug.

Redirect to the original URL.

Track clicks by device type and last_clicked timestamp.

JSON API and minimal HTML UI.

Tech
Python, Flask

JSON file for storage (urls.json)

user-agents for parsing device type

Quick start
Install:

pip install flask user-agents

Run:

python app.py

Use:

Open http://127.0.0.1:5000/

Submit a long URL to get a short slug, e.g. /Ab12Cd

Visit /<slug> to redirect and increment analytics

Get stats: GET /stats?slug=<slug>

API
POST /shorten

JSON: {"url":"https://example.com"}

Returns: {"short":"Ab12Cd","stats":{...}}

GET /<slug>

Redirects to the long URL if slug exists.

GET /stats?slug=<slug>

Returns analytics for the slug.

Data model
urls.json

{
"Ab12Cd
https://example.com",
"created": "2025-08-17T10:00
00Z", "
licks": 12, "last_clicked": "2025
08-17T12:22:35Z", "ua_stats": { "mobile": 7, "tablet"


Notes
Demo-grade; for production, replace JSON with a database and add auth/rate-limiting.

If the JSON gets corrupted, delete urls.json and restart.

Next ideas
Custom slugs

Expiration dates

Admin dashboard with charts
