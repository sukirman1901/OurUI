# Getting started

Run a complete OurUI app in your browser in a few minutes.

## Prerequisites

- **Python 3.11+**
- A terminal and a web browser

## Install

Create a virtual environment and install OurUI in editable mode from this repository:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e packages/ourui
```

## Run the sample app

Use the bundled counter demo as your starting point:

```bash
ourui serve examples/tutorial/06_counter_app.py
```

Open [http://127.0.0.1:8765/](http://127.0.0.1:8765/) in your browser. You should see a welcome hero, feature cards, and a counter. Click **Get Started** or **+1** to exercise server handlers.

The sample defines a `page` variable with `ui.Page`, `State`, `@server` functions, and reusable components — the same patterns you will learn step by step in the tutorial.

## Optional: emit static HTML

To inspect the generated document without a server:

```bash
ourui emit examples/tutorial/06_counter_app.py
```

This prints HTML (with embedded CSS and a small JS shim) to stdout. Redirect to a file and open it in a browser if you want a static snapshot. Interactive `@server` actions require `ourui serve`.

## What you have now

- OurUI installed locally
- A dev server on port **8765** with hot reload
- A working app that combines layout, state, and server RPC

## See also

- [Tutorial 01 — Your first page](tutorial/01-your-first-page.md) — start from a minimal page and build up
