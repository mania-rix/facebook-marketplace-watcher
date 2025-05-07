# Facebook‑Marketplace Watcher 🚗📦

Headless Playwright + BeautifulSoup scraper that logs into Facebook Marketplace, filters for
your search URL, and emails **only the listings posted in the last _N_ minutes** (default 20).

> ⚠️ **Use responsibly:** scraping Marketplace violates Facebook ToS.  
> You can be rate‑limited, shadow‑banned, or forced onto reCAPTCHA after a few days.
> See “Hardening against detection” below.

---

## Features
* **Any category** – just drop in the Marketplace URL with your filters.
* **Fresh‑only** – checks timestamps and ignores anything older than X minutes.
* **De‑dupe** – MD5 of each listing URL prevents duplicate emails.
* **HTML mail** – price, kilometres, link and posted‑ago time.
* **Pluggable alerts** – default Gmail SMTP; swap in Slack, Discord, etc.

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export FB_EMAIL=you@example.com
export FB_PASSWORD=s3cret1
export GMAIL_USER=notifybot@gmail.com
export GMAIL_PASS=app‑password
python watcher.py        # runs forever, 30‑s poll
