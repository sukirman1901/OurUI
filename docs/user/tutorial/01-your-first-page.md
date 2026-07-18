# Tutorial 01 — Your first page

## Goal

Create a minimal OurUI page with a hero and a content section. No server logic yet — just layout.

## Code

Save or open:

**`examples/tutorial/01_page.py`**

```python
from ourui import ui

page = ui.Page(
    ui.Hero(title="Hello OurUI", subtitle="Your first page"),
    ui.Section(title="Next", children=[ui.Text("Open docs/user/tutorial/02-components.md")]),
)
```

Every tutorial module exposes a top-level `page` (or multiple pages with routes in later steps). The compiler finds that variable and renders it.

Run it:

```bash
ourui serve examples/tutorial/01_page.py
```

Open [http://127.0.0.1:8765/](http://127.0.0.1:8765/).

## What you learned

- Import `ui` from `ourui` and build a tree of UI nodes.
- **`ui.Page`** wraps the root content shown at `/`.
- **`ui.Hero`** is a prominent header block with `title` and optional `subtitle`.
- **`ui.Section`** groups content; pass child nodes in `children`.
- **`ui.Text`** displays plain text.
- **`ourui serve`** compiles your Python file and serves the page over HTTP.

## Next

- [Tutorial 02 — Components](02-components.md)
