# Project layout

Organize an OurUI app so you can develop locally, run examples, and deploy without surprises.

## Suggested layout

For a small app or early prototype:

```text
my-app/
├── .venv/              # Python virtual environment (local only)
├── app.py              # Main OurUI module — exposes `page` or routed pages
├── examples/           # Optional smaller demos or experiments
│   └── draft_page.py
├── requirements.txt    # pip install -e ourui or pinned release
└── README.md
```

**`app.py`** is the entry point you pass to the CLI:

```bash
ourui serve app.py
ourui dump app.py
```

Every OurUI module must define at least one top-level **`page`** variable (or multiple **`ui.Page(..., route=...)`** assignments for routing). The compiler discovers those names at import time — keep them at module scope.

## Virtual environment

Create and activate a venv in the project root (same as [Getting started](../getting-started.md)):

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install ourui
# or editable from a clone:
pip install -e path/to/ourui/packages/ourui
```

Do not commit `.venv/` to version control. Document install steps in `README.md` instead.

## Examples folder

Use **`examples/`** for throwaway modules while learning or prototyping:

```text
examples/
├── landing.py
└── admin_preview.py
```

Run any file directly:

```bash
ourui serve examples/landing.py --port 8766
```

The bundled tutorial under this repository uses **`examples/tutorial/`** — follow those files in order if you are new to OurUI.

## Growing beyond one file

When the app grows, split by concern without changing the CLI contract:

```text
my-app/
├── app.py              # wires pages, theme, and imports
├── components/
│   └── counter.py
└── pages/
    ├── home.py
    └── settings.py
```

Import components and page fragments into **`app.py`**. OurUI still compiles the **single file** you pass to `ourui serve` — that file must assemble the final `page` (or routed pages) tree.

## What to run where

| Task | Command |
|------|---------|
| Local dev with hot reload | `ourui serve app.py` |
| Inspect compiler output | `ourui dump app.py` |
| Static HTML snapshot | `ourui emit app.py` |
| Production | `ourui serve app.py --prod` (see [Deploying](deploying.md)) |

## See also

- [Getting started](../getting-started.md) — install, first run, sample app
- [Tutorial 01 — Your first page](../tutorial/01-your-first-page.md) — minimal `ui.Page`
- [Tutorial 04 — Routing](../tutorial/04-routing.md) — multiple pages with `route=`
- [Deploying](deploying.md) — production flags and session storage
