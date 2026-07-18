# Tutorial 05 — Theme and tokens

## Goal

Set brand colors once with **`ui.Theme`**, then reference token names like **`color="primary"`** on components instead of hard-coded hex values.

## Code

**`examples/tutorial/05_theme.py`**

```python
from ourui import ui

theme = ui.Theme(primary="#1a5f4a", primary_fg="#f5faf8")

page = ui.Page(
    ui.Hero(title="Themed"),
    ui.Button("Primary", color="primary"),
)
```

Run:

```bash
ourui serve examples/tutorial/05_theme.py
```

The primary button uses your theme colors. Inspect the page source to see `--ourui-primary` and `--ourui-primary-fg` CSS variables in the emitted stylesheet.

## What you learned

- Assign **`theme = ui.Theme(...)`** at module level (same pattern as `page = ui.Page(...)`). OurUI picks it up at compile time and injects token CSS into the document.
- **`ui.Theme`** kwargs override the built-in light palette. Common keys: `primary`, `primary_fg`, `bg`, `fg`, `muted`, `accent`, `danger`, and spacing/radius tokens (`radius`, `space_sm`, `space_md`).
- Pass **`color="primary"`** (or `muted`, `accent`, `danger`, `card`, `bg`, `fg`) on **`ui.Button`** and other nodes that accept a color role. The runtime maps the name to the matching CSS variable.
- Tokens become **`--ourui-*` variables** in generated CSS (underscores become hyphens, e.g. `primary_fg` → `--ourui-primary-fg`). Light defaults apply on `:root`; built-in dark defaults live under `.dark` if you add a dark-mode class later.
- You can pass a **`dark={...}`** dict to `ui.Theme` to override dark-mode tokens separately. Omit it to keep the default dark palette.

| Token kwarg | CSS variable | Typical use |
|-------------|--------------|-------------|
| `primary` | `--ourui-primary` | Primary buttons, links |
| `primary_fg` | `--ourui-primary-fg` | Text on primary surfaces |
| `bg` / `fg` | `--ourui-bg`, `--ourui-fg` | Page background and body text |
| `muted` | `--ourui-muted` | Subtle fills and secondary UI |
| `accent` | `--ourui-accent` | Highlights |
| `danger` | `--ourui-danger` | Destructive actions |

## Next

- [Tutorial 06 — Serve: dev and prod](06-serve-dev-and-prod.md)
