# Theme (`ui.Theme`)

**What it is:** a thin **brand sheet** — CSS variables for color, type, space, elevation, optional density, optional page measure.

**What it is not:** the craft foundation. Layout/spacing/sizing craft is [Style intents](style-intents.md) (`aspect=`, `pad_x=`, `width=`, …).

```text
Craft depth  →  style intents  (ADR-013)     ← focus now
Brand roles  →  ui.Theme       (this page)   ← supporting
```

Defaults come from `ourui.theme` (zinc/ink + IBM Plex Sans). Override with module-level `ui.Theme(...)`. Emit writes `--ourui-*` on `:root` / `.dark` from **Resolved Design** (Host Contract).

```python
from ourui import ui

# Optional — omit Theme to use defaults
theme = ui.Theme(
    primary="#18181b",
    primary_fg="#fafafa",
    density="comfortable",           # or "compact"
    page={"max_width": "42rem"},     # measure; "none" → full-bleed
)

page = ui.Page(
    ui.Hero(title="Themed"),
    ui.Button("Primary"),            # untoned → primary
    ui.Button("Quiet", color="muted"),
    ui.ThemeToggle(),                # icon-only .dark toggle
)
```

Normative rules: [Language Spec — Design tokens](../../../LANGUAGE_SPEC.md#design-tokens).

## `ui.Theme` kwargs

Assign at **module level**. Compiler merges into Semantic Graph `tokens` and Resolved Design.

```python
theme = ui.Theme(
    density="comfortable",
    primary="#18181b",
    primary_fg="#fafafa",
    accent="#2563eb",
    font_sans='"IBM Plex Sans", system-ui, sans-serif',
    space_lg="1.25rem",
    sizes={"lg": "36rem"},           # optional ADR-013 scale overrides
    space={"4": "1.25rem"},
    type={"display": "clamp(2rem, 5vw, 4rem)"},
    page={"max_width": "42rem"},
    dark={"primary": "#fafafa", "primary_fg": "#09090b"},
)
```

### Density

| Value | Effect |
|-------|--------|
| `comfortable` (default) | Space tokens as-is |
| `compact` | `ourui-density-compact` on `<html>` / `.ourui-root`; tighten `--ourui-space-sm/md/lg` |

### Page measure

| Key | Effect |
|-----|--------|
| `max_width` | Page content max width; `"none"` → full-bleed (`data-page-bleed="1"`) |
| `pad_block` / `pad_inline` | Page padding |

See [Page measure](../concepts/page-measure.md).

### Color roles

| Kwarg | CSS variable | Typical use |
|-------|--------------|-------------|
| `bg` / `fg` | `--ourui-bg` / `--ourui-fg` | Page background / body text |
| `primary` / `primary_fg` | `--ourui-primary` / `--ourui-primary-fg` | Primary actions |
| `muted` / `muted_fg` | `--ourui-muted` / `--ourui-muted-fg` | Subtle fills |
| `border` | `--ourui-border` | Borders |
| `card` / `card_fg` | `--ourui-card` / `--ourui-card-fg` | Cards |
| `accent` / `accent_fg` | `--ourui-accent` / … | Highlights |
| `danger` / `danger_fg` | `--ourui-danger` / … | Destructive |

### Shape, space, type, elevation

| Family | Kwargs (examples) | CSS |
|--------|-------------------|-----|
| Shape | `radius` | `--ourui-radius` |
| Space | `space_xs` … `space_2xl` | `--ourui-space-*` |
| Type | `font_sans`, `font_display`, `text_xs` … `text_2xl`, `leading_*` | `--ourui-font-*`, `--ourui-text-*` |
| Elevation | `elev_0` … `elev_3` | `--ourui-elev-*` |

### Scale table overrides (ADR-013)

| Kwarg | Effect |
|-------|--------|
| `space={...}` | Override `--ourui-space-*` keys used by `pad=` / `gap=` / … |
| `sizes={...}` | Override size scale for `width=` / `height=` / … |
| `type={...}` | Override type scale keys |

### Author CSS (`css=`) — app escape without editing the package

Append raw CSS after host utilities (Tailwind’s “using custom CSS” analogue). Prefer Theme roles + style intents first; use `css=` for one-offs the catalog does not cover yet.

```python
CUSTOM = """
.hero-glow {
  box-shadow: 0 0 40px color-mix(in srgb, var(--ourui-accent) 35%, transparent);
}
"""

theme = ui.Theme(
    primary="#18181b",
    css=CUSTOM,  # or css=\"\"\".hero-glow { … }\"\"\"
)
```

Emitted inside the page `<style>` block after utilities / motion. Prefer `--ourui-*` vars so light/dark still track Theme. Not a substitute for intent props — promote repeated patterns into the style catalog when they stabilize.

Underscores become hyphens: `primary_fg` → `--ourui-primary-fg`.

## Light and dark

Top-level kwargs override **light**. Pass **`dark={...}`** for dark-mode overrides. Light applies on `:root`; dark under `.dark` (typically `<html>`).

### `ui.ThemeToggle`

Icon-only control that toggles `.dark` on `<html>` (persists via `localStorage`):

```python
ui.ThemeToggle()
```

## Using roles on components

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
ourui dump examples/tutorial/05_theme.py   # schema 30; semantic_graph.tokens
```

## See also

- [Tutorial 05 — Theme and style intents](../tutorial/05-theme-tokens.md)
- [Page measure](../concepts/page-measure.md)
- [Style intents](style-intents.md) — **craft foundation**
- [UI components](ui-components.md)
- [Debugging with dump](../guides/debugging-with-dump.md)
