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

Current Stable package: **1.8.3** ([PyPI](https://pypi.org/project/ourui/)). Dump schema **30** (additive); language/IR breaking changes remain Frozen at schema **25** until `2.0`.

## Run the sample app

Tutorial counter demo:

```bash
ourui serve examples/tutorial/06_counter_app.py
```

Open [http://127.0.0.1:8765/](http://127.0.0.1:8765/). You should see a welcome hero, feature cards, and a counter.

## Run more samples

```bash
ourui serve examples/enterprise/crud_app.py
ourui serve examples/enterprise/settings_app.py --port 8766
```

Enterprise kit and OIDC/gateway stubs live under [`examples/enterprise/`](../../examples/enterprise/).

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
