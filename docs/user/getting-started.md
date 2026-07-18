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

Current Stable package: **1.11.1** ([PyPI](https://pypi.org/project/ourui/) or editable install from this repo). Dump schema **30** (additive); language/IR breaking changes remain Frozen at schema **25** until `2.0`.

Style layout/type props: [Style intents](reference/style-intents.md) (foundation). Theme roles: [Theme](reference/theme.md) (thin sheet).

## Run the sample app

Tutorial counter demo:

```bash
ourui serve examples/tutorial/06_counter_app.py
```

Open [http://127.0.0.1:8765/](http://127.0.0.1:8765/). You should see a welcome hero, feature cards, and a counter.

## More samples

```bash
ourui serve examples/landing/app.py          # marketing dogfood (primitives + intents)
ourui serve examples/tutorial/05_theme.py    # theme roles
```

Auth in front of prod host (app-layer): [`examples/gateway/`](../../examples/gateway/).

## Optional: emit static HTML

```bash
ourui emit examples/tutorial/06_counter_app.py
```

Prints HTML (embedded CSS + JS shim) to stdout. Interactive `@server` actions require `ourui serve`.

## What you have now

- OurUI installed
- A dev server on port **8765** with hot reload
- Access to Stable APIs through Phase **S6** (forms, Nav, theme roles, layout, motion, Canvas, polish) plus style intents (ADR-013) L3 (`1.11.1`) and `Theme(page=)` / `Theme(css=)`

## See also

- [Tutorial 01 — Your first page](tutorial/01-your-first-page.md)
- [UI components reference](reference/ui-components.md)
- [What Stable includes](concepts/what-p0-includes.md)
