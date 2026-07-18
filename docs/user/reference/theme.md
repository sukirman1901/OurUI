# Theme and tokens

OurUI emits semantic CSS variables under the `--ourui-*` namespace. Override defaults once with `ui.Theme`, then reference token names on components.

```python
from ourui import ui

theme = ui.Theme(primary="#1a5f4a", primary_fg="#f5faf8")

page = ui.Page(
    ui.Hero(title="Themed"),
    ui.Button("Primary", color="primary"),
)
```

Normative rules: [Language Spec — Design tokens](../../../LANGUAGE_SPEC.md#design-tokens-phase-p).

## `ui.Theme`

Assign at **module level** (same pattern as `page = ui.Page(...)`). The compiler merges overrides into the Semantic Graph `tokens` and the HTML emitter writes `:root { … }` and `.dark { … }` blocks.

```python
theme = ui.Theme(
    primary="#1a5f4a",
    primary_fg="#f5faf8",
    dark={"primary": "#2dd4a8", "primary_fg": "#042f2e"},
)
```

| Kwarg | CSS variable | Typical use |
|-------|--------------|-------------|
| `bg` | `--ourui-bg` | Page background |
| `fg` | `--ourui-fg` | Body text |
| `primary` | `--ourui-primary` | Primary buttons, links |
| `primary_fg` | `--ourui-primary-fg` | Text on primary surfaces |
| `muted` | `--ourui-muted` | Subtle fills |
| `muted_fg` | `--ourui-muted-fg` | Text on muted surfaces |
| `border` | `--ourui-border` | Borders and dividers |
| `card` | `--ourui-card` | Card background |
| `card_fg` | `--ourui-card-fg` | Text on cards |
| `accent` | `--ourui-accent` | Highlights |
| `accent_fg` | `--ourui-accent-fg` | Text on accent surfaces |
| `danger` | `--ourui-danger` | Destructive actions |
| `danger_fg` | `--ourui-danger-fg` | Text on danger surfaces |
| `radius` | `--ourui-radius` | Border radius |
| `space_sm` | `--ourui-space-sm` | Small spacing |
| `space_md` | `--ourui-space-md` | Medium spacing |

Underscores in kwarg names become hyphens in CSS: `primary_fg` → `--ourui-primary-fg`.

## Light and dark

Built-in light and dark palettes ship with the compiler. Top-level kwargs override **light** tokens. Pass a **`dark={...}`** dict to override dark-mode tokens separately:

```python
theme = ui.Theme(
    primary="#1a5f4a",
    dark={"primary": "#2dd4a8"},
)
```

Light defaults apply on `:root`. Dark defaults apply under a `.dark` class on an ancestor element.

## Using tokens on components

Reference semantic color roles with `color=`, `variant=`, or `bg=` on nodes that support tone styling (for example `ui.Button`):

```python
ui.Button("Save", color="primary")
ui.Button("Delete", color="danger")
ui.Button("Later", color="muted")
```

Accepted color role names:

`primary`, `muted`, `accent`, `danger`, `card`, `bg`, `fg`

Matching values add tone classes (for example `ourui-tone-primary`) that map to `var(--ourui-primary)` and related variables.

## Inspecting output

Run the app and view page source, or emit static HTML:

```bash
ourui serve examples/tutorial/05_theme.py
ourui emit examples/tutorial/05_theme.py | grep ourui-primary
```

Dump also includes tokens at schema version 9:

```bash
ourui dump examples/tutorial/05_theme.py | python3 -c "
import json, sys
print(json.dumps(json.load(sys.stdin)['semantic_graph'].get('tokens', {}), indent=2))
"
```

## See also

- [Tutorial 05 — Theme and tokens](../tutorial/05-theme-tokens.md)
- [UI components — ui.Theme](ui-components.md#uitheme)
- [Debugging with dump](../guides/debugging-with-dump.md)
