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
