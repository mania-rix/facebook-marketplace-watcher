# Contributing to Facebook‑Marketplace‑Watcher

Thanks for taking time to improve the project! Marketplace changes fast, so extra eyes and pull requests are always welcome. 🚀

## Quick start
```bash
git clone https://github.com/<your‑fork>/facebook‑marketplace‑watcher
cd facebook‑marketplace‑watcher
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
# create .env with FB_EMAIL=… etc.
pytest -v          # tests should pass
```

---

## Issue labels

| Label            | Meaning                                                 |
| ---------------- | ------------------------------------------------------- |
| **help‑wanted**  | Good starting point for newcomers                       |
| **bug**          | Reproducible defect, needs a fix                        |
| **enhancement**  | New feature or improvement                              |
| **hardening**    | Ideas to avoid bot detection / reCAPTCHA                |

---

## Open *help‑wanted* tasks

- **Cookie reuse** – save & reload session cookies instead of logging in each run.  
- **Randomised delays** – jitter sleep interval / user‑agent to mimic humans.  
- **Better secret handling** – switch to `.env` + `python‑dotenv` (no creds in code).  
- **Dockerfile** – self‑contained runner with Mailhog for email testing.  
- **Unit tests** – isolate `process_listing()` logic with static HTML fixtures.  

Feel free to suggest more!

---

## Coding guidelines

* **Black** + **isort** for styling (`black . && isort .` before commit).  
* Python 3.11+ typing syntax (`list[int]`, `dict[str, str]`, etc.).  
* One feature / bug‑fix per pull request; add or update tests in **`tests/`**.

---

## Pull‑request checklist

- [ ] New code is formatted with **black** and imports ordered with **isort**.  
- [ ] `pytest -v` passes locally.  
- [ ] Docs / README updated if behaviour changes.  
- [ ] Commit(s) signed‑off (`Signed‑off‑by: Your Name <email>`).

---

## Code of conduct

Be kind and patient; reviewers are volunteers.  
No spam, scraping account details, or credential requests in public issues.

Happy hacking! 🔧
