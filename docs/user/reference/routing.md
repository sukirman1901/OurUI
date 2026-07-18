# Routing

Serve multiple pages from one Python module by defining several `ui.Page` instances with `route=`. No separate router config file is required.

```python
from ourui import ui

home = ui.Page(ui.Hero(title="Home"), route="/")
about = ui.Page(ui.Section(title="About"), route="/about")
```

Normative rules: [Language Spec — Routing](../../../LANGUAGE_SPEC.md#routing-phase-k).

## Single page (default)

One module-level `ui.Page` without `route=` is served at **`/`**:

```python
page = ui.Page(ui.Hero(title="Hello"))
```

```bash
ourui serve app.py
# → http://127.0.0.1:8765/
```

The variable name can be `page` or anything else — the analyzer collects all top-level `ui.Page` calls.

## Multiple pages

When a module defines **more than one** `ui.Page`, each must include an explicit **`route=`**:

```python
home = ui.Page(ui.Hero(title="Home"), route="/")
about = ui.Page(ui.Section(title="About"), route="/about")
docs = ui.Page(ui.Section(title="Docs"), route="/docs")
```

Rules:

- Paths must be **unique** — duplicate routes raise a compile error
- Paths are ordinary URL paths (for example `/`, `/about`, `/settings/profile`)
- Omitting `route=` on any page when multiple pages exist raises an error

## How serve matches routes

`ourui serve` compiles the module, reads `semantic_graph.routes`, and emits HTML for the page whose `route=` matches the request path:

```bash
ourui serve examples/tutorial/04_routing.py
```

| URL | Page |
|-----|------|
| `http://127.0.0.1:8765/` | `home` (`route="/"`) |
| `http://127.0.0.1:8765/about` | `about` (`route="/about"`) |

On startup, the banner lists every registered route. Inspect routes in dump:

```bash
ourui dump examples/tutorial/04_routing.py | python3 -c "
import json, sys
sg = json.load(sys.stdin)['semantic_graph']
print(json.dumps(sg['routes'], indent=2))
"
```

Example output:

```json
{
  "/": "n_…",
  "/about": "n_…"
}
```

## Navigation

Each route is a full page load — no client-side SPA router is required. Open paths directly in the browser (for example `/about`) or link from outside the app. Standard `<a href="/about">` links work when present in emitted HTML; `ui.Text` escapes content, so use separate pages and browser navigation for P0 multi-page demos.

## Unknown paths

| Mode | Response |
|------|----------|
| Dev | JSON `404` — `{"error":"not found"}` |
| `--prod` | HTML `404` page |

`/index.html` is normalized to `/` when matching routes.

## Static emit per route

`ourui emit` compiles the default route (`/` when present). For multi-route static export, run emit once per route in tooling that supports the `route` parameter, or serve dynamically with `ourui serve`.

## See also

- [Tutorial 04 — Routing](../tutorial/04-routing.md)
- [UI components — ui.Page](ui-components.md#uipage)
- [Debugging with dump](../guides/debugging-with-dump.md)
