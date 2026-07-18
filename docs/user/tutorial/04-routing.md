# Tutorial 04 — Routing

## Goal

Serve **multiple pages from one Python module** by defining more than one `ui.Page` and giving each a `route=`.

## Code

**`examples/tutorial/04_routing.py`**

```python
from ourui import ui

home = ui.Page(ui.Hero(title="Home"), route="/")
about = ui.Page(ui.Section(title="About"), route="/about")
```

Run:

```bash
ourui serve examples/tutorial/04_routing.py
```

Open [http://127.0.0.1:8765/](http://127.0.0.1:8765/) for the home page, then [http://127.0.0.1:8765/about](http://127.0.0.1:8765/about) for the about page. The serve banner lists every registered route when you start the server.

## What you learned

- A module can expose **several `ui.Page` instances** instead of a single `page` variable. Each becomes a routable page.
- Pass **`route="/path"`** on every page when you define more than one. Paths must be unique (for example `/` and `/about`).
- If the module has **only one** `ui.Page` and you omit `route=`, OurUI serves it at **`/`** automatically.
- **`ourui serve`** matches the request path to a page and emits that page’s HTML. Unknown paths return 404 in production mode; in dev mode they return a JSON error.
- Route names are ordinary URL paths — no separate router config file is required.

## Next

- [Tutorial 05 — Theme and tokens](05-theme-tokens.md)
