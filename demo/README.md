# OurUI demo — Plasma-shaped dogfood (Phase S1–S6)

Dogfoods the full language surface on **ourui ≥ 0.4.0** (editable install from this repo, or `pip install ourui`).

```bash
cd /Users/aaa/Documents/Developer/ourui   # or your clone
source .venv/bin/activate
pip install -e packages/ourui            # if needed
ourui serve demo/app.py
```

Open:

| URL | Page |
|-----|------|
| http://127.0.0.1:8765/ | Landing — Nav, Hero + Canvas, tokens, motion, Footer, Meta |
| http://127.0.0.1:8765/app | Studio — Shell `split-3`, Canvas preview, forms |
| http://127.0.0.1:8765/embed | Embed stub with Canvas |

See [GAPS.md](GAPS.md) for what is closed vs still app-scope (Redis/auth).
