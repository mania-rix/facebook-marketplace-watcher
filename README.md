# Facebook‑Marketplace Watcher 🚗📦

Headless **Playwright** + **BeautifulSoup** scraper that logs into Facebook
Marketplace, applies your custom search URL, and emails **only the listings
posted in the last _N_ minutes** (default 20).

> ⚠️ **Use responsibly:** scraping Marketplace violates Facebook ToS.  
> You may be rate‑limited, shadow‑banned, or forced onto reCAPTCHA.  
> See [Hardening against detection](#hardening-against-detection).

📄 **License:** MIT + Commons Clause – free for personal / academic use,  
_no commercial resale or hosted SaaS without permission._  

---

## ✨ Features
* **Any category** – paste any Marketplace URL with your filters.
* **Fresh‑only** – skips anything older than *X* minutes.
* **De‑dupe** – MD5 hash prevents repeat emails.
* **HTML alerts** – price, kilometres, link, “posted ago”.
* **Pluggable outputs** – Gmail SMTP by default; swap in Slack, Discord…

---

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium                    # 1‑time browser install

export FB_EMAIL=you@example.com
export FB_PASSWORD=s3cret1
export GMAIL_USER=notifybot@gmail.com
export GMAIL_PASS=app‑password

python watcher.py                              # runs forever, 30‑s poll
