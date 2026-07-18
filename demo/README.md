# OurUI demo — Plasma-shaped dogfood (Phase S1)

Uses **editable** OurUI from this repo (Link/Shell are newer than PyPI 0.1.1).

```bash
cd /Users/aaa/Documents/Developer/ourui
source .venv/bin/activate   # monorepo venv with pip install -e packages/ourui
ourui serve demo/app.py
```

- http://127.0.0.1:8765/ — landing with **ui.Link**
- http://127.0.0.1:8765/app — **ui.Shell(layout="split-3")**
- http://127.0.0.1:8765/embed — stub

See [GAPS.md](GAPS.md) for remaining S2–S6 items.
