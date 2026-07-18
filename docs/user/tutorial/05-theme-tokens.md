# Tutorial 05 — Theme and tokens

## Goal

Set brand colors (and type/space/elevation) once with **`ui.Theme`**, reference **`color="primary"`** on components, and optionally add **`ui.ThemeToggle`** for light/dark.

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

Inspect page source for `--ourui-primary` and related variables. For a denser branded screen, try `ourui serve examples/enterprise/settings_app.py`.

## What you learned

- Assign **`theme = ui.Theme(...)`** at module level. Overrides merge into Resolved Design; emit writes `:root` / `.dark` CSS vars.
- Common color keys: `primary`, `primary_fg`, `bg`, `fg`, `muted`, `accent`, `danger`, plus `radius` and space/type/elevation keys (`space_*`, `font_*`, `text_*`, `elev_*`).
- Pass **`color="primary"`** (or `muted`, `accent`, `danger`, …) on buttons and links.
- **`dark={...}`** overrides the dark palette. **`ui.ThemeToggle`** flips `.dark` on `<html>`.
- Dump schema **21** includes `semantic_graph.tokens` (still present; current dump schema is **28**).

| Token kwarg | CSS variable | Typical use |
|-------------|--------------|-------------|
| `primary` | `--ourui-primary` | Primary buttons, links |
| `primary_fg` | `--ourui-primary-fg` | Text on primary surfaces |
| `bg` / `fg` | `--ourui-bg`, `--ourui-fg` | Page background and body text |
| `space_md` | `--ourui-space-md` | Default gaps/padding |
| `elev_1` | `--ourui-elev-1` | Light shadow (cards/nav) |
| `font_display` | `--ourui-font-display` | Hero / section titles |

## Next

- [Tutorial 06 — Serve: dev and prod](06-serve-dev-and-prod.md)
- [Theme reference](../reference/theme.md)
