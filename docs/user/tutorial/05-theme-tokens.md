# Tutorial 05 — Theme and style intents

> Filename kept for link stability.

## Goal

Know the split:

| Layer | API | Role |
|---|---|---|
| **Craft (foundation)** | Style intents (`aspect=`, `pad_x=`, …) | Tailwind-depth utilities |
| **Brand (thin sheet)** | `ui.Theme(...)` | Color/type/space roles, density, page measure |

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

Inspect page source for `--ourui-primary`. Style-intents gallery: `examples/landing/`.

## What you learned

- Assign **`theme = ui.Theme(...)`** at module level. Overrides merge into Resolved Design; emit writes `:root` / `.dark` CSS vars.
- Common color keys: `primary`, `primary_fg`, `bg`, `fg`, `muted`, `accent`, `danger`, plus `radius` and space/type/elevation keys.
- Pass **`color="primary"`** (or `muted`, `accent`, `danger`, …) on buttons and links.
- **`dark={...}`** overrides the dark palette. **`ui.ThemeToggle`** flips `.dark` on `<html>` (icon-only).
- Optional **`density=`** and **`page={...}`** — see [Page measure](../concepts/page-measure.md).
- Layout utilities (`aspect=`, `width=`, `gap=`, …) are **style intents**, not Theme color roles — see [Style intents](../reference/style-intents.md).

| Theme kwarg | CSS variable | Typical use |
|-------------|--------------|-------------|
| `primary` | `--ourui-primary` | Primary buttons, links |
| `primary_fg` | `--ourui-primary-fg` | Text on primary surfaces |
| `bg` / `fg` | `--ourui-bg`, `--ourui-fg` | Page background and body text |
| `space_md` | `--ourui-space-md` | Default gaps/padding (legacy keys) |
| `elev_1` | `--ourui-elev-1` | Light shadow |
| `font_display` | `--ourui-font-display` | Hero / section titles |

## Next

- [Tutorial 06 — Serve: dev and prod](06-serve-dev-and-prod.md)
- [Page measure](../concepts/page-measure.md)
- [Theme reference](../reference/theme.md)
- [Style intents](../reference/style-intents.md)
