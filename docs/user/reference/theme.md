# Theme and tokens

OurUI emits semantic CSS variables under the `--ourui-*` namespace. Defaults (1.0.1+) are a **zinc / ink** product palette with IBM Plex Sans — not cream/serif brochure tokens. Override with `ui.Theme`, then reference token names on components. Emit consumes **Resolved Design** (Host Contract); theme overrides seed the Design System pack.

```python
from ourui import ui

# Optional — omit Theme to use ourui-default zinc/ink pack
theme = ui.Theme(primary="#18181b", primary_fg="#fafafa", accent="#2563eb")

page = ui.Page(
    ui.Hero(title="Themed"),
    ui.Button("Primary"),  # untoned buttons resolve to primary
    ui.Button("Quiet", color="muted"),
    ui.ThemeToggle("Theme"),
)
```

Normative rules: [Language Spec — Design tokens](../../../LANGUAGE_SPEC.md#design-tokens).

## `ui.Theme`

Assign at **module level**. The compiler merges overrides into Semantic Graph `tokens` and Resolved Design; emit writes `:root { … }` and `.dark { … }`.

```python
theme = ui.Theme(
    primary="#18181b",
    primary_fg="#fafafa",
    accent="#2563eb",
    font_sans='"IBM Plex Sans", system-ui, sans-serif',
    space_lg="1.25rem",
    dark={"primary": "#fafafa", "primary_fg": "#09090b"},
)
```

### Color

| Kwarg | CSS variable | Typical use |
|-------|--------------|-------------|
| `bg` / `fg` | `--ourui-bg` / `--ourui-fg` | Page background / body text |
| `primary` / `primary_fg` | `--ourui-primary` / `--ourui-primary-fg` | Primary actions |
| `muted` / `muted_fg` | `--ourui-muted` / `--ourui-muted-fg` | Subtle fills |
| `border` | `--ourui-border` | Borders |
| `card` / `card_fg` | `--ourui-card` / `--ourui-card-fg` | Cards |
| `accent` / `accent_fg` | `--ourui-accent` / … | Highlights |
| `danger` / `danger_fg` | `--ourui-danger` / … | Destructive |

### Shape, space, type, elevation (Phase S3)

| Family | Kwargs (examples) | CSS |
|--------|-------------------|-----|
| Shape | `radius` | `--ourui-radius` |
| Space | `space_xs` … `space_2xl` | `--ourui-space-*` |
| Type | `font_sans`, `font_display`, `text_xs` … `text_2xl`, `leading_*` | `--ourui-font-*`, `--ourui-text-*` |
| Elevation | `elev_0` … `elev_3` | `--ourui-elev-*` (shadow presets) |

Underscores become hyphens: `primary_fg` → `--ourui-primary-fg`.

## Light and dark

Top-level kwargs override **light**. Pass **`dark={...}`** for dark-mode overrides. Light applies on `:root`; dark under `.dark` on an ancestor (typically `<html>`).

### `ui.ThemeToggle`

Client control that toggles the `.dark` class on `<html>` (persists via `localStorage`):

```python
ui.ThemeToggle("Theme")
ui.ThemeToggle(ui.Icon("moon"))
```

## Using tokens on components

```python
ui.Button("Save", color="primary")
ui.Button("Delete", color="danger")
ui.Link("Docs", href="/docs", color="accent")
```

Accepted color roles: `primary`, `muted`, `accent`, `danger`, `card`, `bg`, `fg`.

## Inspecting output

```bash
ourui serve examples/tutorial/05_theme.py
ourui emit examples/tutorial/05_theme.py | grep ourui-primary
ourui dump examples/tutorial/05_theme.py   # schema version 21; semantic_graph.tokens
```

## See also

- [Tutorial 05 — Theme and tokens](../tutorial/05-theme-tokens.md)
- [UI components](ui-components.md)
- [Debugging with dump](../guides/debugging-with-dump.md)
