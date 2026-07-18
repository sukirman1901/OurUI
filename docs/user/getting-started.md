# Getting started

Run a complete OurUI app in your browser in a few minutes.

## Prerequisites

- **Python 3.11+**
- A terminal and a web browser

## Install

**From PyPI:**

```bash
pip install ourui
```

**From this repository (editable):**

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e packages/ourui
```

Current Stable package: **1.0.0** ([PyPI](https://pypi.org/project/ourui/)). Dump schema **25** is Frozen for 1.0.x.

## Run the sample app

Tutorial counter demo:

```bash
ourui serve examples/tutorial/06_counter_app.py
```

Open [http://127.0.0.1:8765/](http://127.0.0.1:8765/). You should see a welcome hero, feature cards, and a counter.

## Run the Plasma demo (full Phase S surface)

```bash
ourui serve demo/app.py
```

| URL | What you see |
|-----|----------------|
| http://127.0.0.1:8765/ | Landing — Nav, Canvas, tokens, motion, Footer |
| http://127.0.0.1:8765/app | Studio shell (`split-3`) + WebGL preview |
| http://127.0.0.1:8765/embed | Embed stub |

## Optional: emit static HTML

```bash
ourui emit examples/tutorial/06_counter_app.py
```

Prints HTML (embedded CSS + JS shim) to stdout. Interactive `@server` actions require `ourui serve`.

## What you have now

- OurUI installed
- A dev server on port **8765** with hot reload
- Access to Stable APIs through Phase **S6** (forms, Nav, tokens, layout, motion, Canvas, polish)

## See also

- [Tutorial 01 — Your first page](tutorial/01-your-first-page.md)
- [UI components reference](reference/ui-components.md)
- [What Stable includes](concepts/what-p0-includes.md)
