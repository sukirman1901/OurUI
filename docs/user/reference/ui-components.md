# UI components

Built-in `ui.*` nodes for layout and presentation. The compiler parses these calls at compile time; see the [Language Spec](../../../LANGUAGE_SPEC.md) for the normative kind list.

```python
from ourui import ui

page = ui.Page(
    ui.Hero(title="Welcome", subtitle="Build in Python"),
    ui.Section(
        title="Features",
        children=[
            ui.Grid(
                ui.Card("Analysis"),
                ui.Card("Realtime"),
            ),
            ui.Button("Continue", color="primary"),
        ],
    ),
)
```

## Overview

| Component | Domain | Role |
|-----------|--------|------|
| `ui.Page` | Intent | Root container for a routable page |
| `ui.Hero` | Intent | Prominent header (`pad=`, `motion=family.pattern`) |
| `ui.Section` | Intent | Grouped content (`layout=`, `gap=`, `pad=`, `align=`, `motion=`) |
| `ui.Shell` | Intent | Layout region (`layout=…` + style intents: `width=`, `gap=`, `grow=`, …) |
| `ui.Nav` | Intent | Chrome bar (`placement=`, `tone=`, `menu=drawer`) |
| `ui.Footer` | Intent | Page footer (`brand=` / `links=` / `meta=`) |
| `ui.Meta` | Intent | Document head (`title`, `description`, `og=`) |
| `ui.Button` | Presentation | Clickable control (`motion=press.scale`, disabled/loading) |
| `ui.Text` | Presentation | Inline text (or bound `State`) |
| `ui.Card` | Presentation | Card container |
| `ui.Grid` | Presentation | Responsive grid layout |
| `ui.Link` | Presentation | In-app or external navigation (`href=`) |
| `ui.Input` | Presentation | Form field (`name=` → `@server`; `type=` incl. `textarea`) |
| `ui.Select` | Presentation | Dropdown (`options=`) |
| `ui.Toggle` | Presentation | Checkbox (boolean payload) |
| `ui.Slider` | Presentation | Range (`min=` / `max=` / `step=`) |
| `ui.ThemeToggle` | Presentation | Toggle `.dark` on `<html>` |
| `ui.Canvas` | Presentation | WebGL escape (`mode=gradient\|dither\|raymarch`) |
| `ui.Frame` | Presentation | Host escape iframe preview (`bind=` / `srcdoc=`) |
| `ui.Image` | Presentation | `src=` / `alt=` / `fit=` |
| `ui.Icon` | Presentation | Reicon-style `name=` |
| `ui.Code` | Presentation | Code block |
| `ui.CopyButton` | Presentation | Clipboard (`copy=`) |
| `ui.Menu` | Presentation | Dropdown menu (`items=`) |
| `ui.Form` | Presentation | Form shell (`on_submit=`) |
| `ui.Dialog` | Presentation | Modal (`open=` / `title=` / `actions=`) |
| `ui.Toast` | Presentation | Toast (`open=` / `text=`) |
| `ui.List` / `ui.Table` | Presentation | List / table; `items=`/`rows=` may be `State` (dynamic) |
| `ui.Empty` / `ui.Spinner` / `ui.Alert` | Presentation | Status primitives |
| `ui.Show` / `ui.When` | Presentation | Conditional visibility (`show=`; When has `then=` / `else_=`) |
| `ui.Theme` | Tokens | Design token overrides (module-level) |

## `ui.Page`

Root container. Assign to a module-level variable (commonly `page`) or define several pages with `route=` for multi-page apps.

```python
page = ui.Page(
    ui.Hero(title="Hello"),
    ui.Section(title="Content", children=[ui.Text("Body text")]),
)

# Multiple pages — see routing reference
home = ui.Page(ui.Hero(title="Home"), route="/")
about = ui.Page(ui.Section(title="About"), route="/about")
```

| Prop | Type | Description |
|------|------|-------------|
| `children` | nodes | Child UI nodes (positional args or `children=[...]`) |
| `route` | `str` | URL path when the module defines more than one page (required for each page in that case) |

A single `ui.Page` without `route=` is served at `/`.

## `ui.Hero`

Prominent header at the top of a page.

```python
ui.Hero(
    title="Welcome",
    subtitle="Build SaaS in Python",
    cta=ui.Button("Get Started", color="primary", on_click=get_started),
)
```

| Prop | Type | Description |
|------|------|-------------|
| `title` | `str` | Main heading (positional string also accepted) |
| `subtitle` | `str` | Optional subheading |
| `cta` | node | Optional call-to-action (commonly a `ui.Button` or `ui.Link`) |
| `pad` | intent | `none` \| `xs` \| `sm` \| `md` \| `lg` \| `xl` \| `2xl` |
| `motion` | intent | `none` \| `enter` \| `reveal` |
| `children` | nodes | Additional child nodes (e.g. `ui.Canvas`) |

## `ui.Section`

Groups related content under a heading.

```python
ui.Section(
    title="Features",
    children=[
        ui.Text("First item"),
        ui.Text("Second item"),
    ],
)
```

| Prop | Type | Description |
|------|------|-------------|
| `title` | `str` | Section heading (positional string also accepted) |
| `subtitle` | `str` | Optional subheading |
| `layout` | intent | Same values as `ui.Shell` `layout=` |
| `gap` / `pad` | intent | `none` \| `xs` \| `sm` \| `md` \| `lg` \| `xl` \| `2xl` |
| `align` / `justify` | intent | Alignment intents (see Layout intents below) |
| `motion` | intent | `none` \| `enter` \| `reveal` |
| `children` | nodes | Child nodes inside the section |

## `ui.Button`

Clickable control. Wire clicks to server handlers with `on_click=`.

```python
ui.Button("+1", color="primary", on_click=increment)
ui.Button("Cancel", color="muted")
```

| Prop | Type | Description |
|------|------|-------------|
| `text` | `str` | Button label (first positional string also accepted) |
| `color` | token name | Semantic tone: `primary`, `muted`, `accent`, `danger`, `card`, `bg`, `fg` |
| `variant` | token name | Alias for tone styling (same token names as `color`) |
| `on_click` | handler | Function name or `@server` function reference |

## `ui.Text`

Displays text. Pass a string or a `State` instance to show live values.

```python
ui.Text("Static label")
ui.Text(count)  # count = State(0)
```

| Prop | Type | Description |
|------|------|-------------|
| `text` | `str` or `State` | Content to display (positional `State` or string also accepted) |

## `ui.Card`

Card container, often used inside grids or sections.

```python
ui.Card("Analysis")
ui.Card(title="Realtime", children=[ui.Text("Details here")])
```

| Prop | Type | Description |
|------|------|-------------|
| `title` / `text` | `str` | Card heading (first positional string maps to `text` or `title`) |
| `children` | nodes | Nested content |

## `ui.Grid`

Responsive grid layout for cards or other nodes.

```python
ui.Grid(
    ui.Card("One"),
    ui.Card("Two"),
    ui.Card("Three"),
)
```

| Prop | Type | Description |
|------|------|-------------|
| `children` | nodes | Grid items (positional args or `children=[...]`) |

The emitter renders a CSS grid with `repeat(auto-fit, minmax(12rem, 1fr))`.

## `ui.Input`

Form field (Phase S2). On button click, JS collects all `[data-ourui-field]` values and posts them as the `@server` payload.

```python
email = State("")

@server
def save(**payload):
    email.set(str(payload.get("email", "")))

ui.Input(
    name="email",
    type="email",
    placeholder="you@example.com",
    label="Email",
    bind=email,
)
ui.Button("Save", on_click=save)
```

| Prop | Type | Description |
|------|------|-------------|
| `name` | `str` | Field key in the RPC payload (required for form collection) |
| `type` | `str` | `text` \| `email` \| `password` \| `number` \| `search` \| `url` \| `tel` \| `textarea` |
| `placeholder` | `str` | Placeholder text |
| `label` | `str` | Optional visible label |
| `bind` / `value` | `State` or `str` | Initial value; `bind=` syncs from server State after RPC |

## `ui.Select`

Dropdown form control.

```python
ui.Select(name="theme", options=["light", "dark"], label="Theme", bind=theme)
```

| Prop | Description |
|------|-------------|
| `name` | Payload key |
| `options` | List of strings or `{value, label}` dicts |
| `label` | Optional visible label |
| `bind` / `value` | Selected value |

## `ui.Toggle`

Checkbox form control (payload boolean).

```python
ui.Toggle(name="enabled", label="Enabled", bind=enabled)
```

## `ui.Slider`

Range form control.

```python
ui.Slider(name="volume", min=0, max=100, step=5, label="Volume", bind=volume)
```

## `ui.Theme`

Module-level design token overrides. Not a visual node — assign at module scope like `page`.

```python
theme = ui.Theme(primary="#1a5f4a", primary_fg="#f5faf8")
```

See [Theme reference](theme.md) for all token keys and CSS variable mapping.

## `ui.Link`

Navigation control. Emits a real `<a href>` (full page load — no SPA router).

```python
ui.Link("Open Studio", href="/app")
ui.Link("Docs", href="https://example.com/docs")  # external → target=_blank
ui.Link("Home", href="/", color="primary")
```

| Prop | Notes |
|------|--------|
| `text` | Label (first positional string) |
| `href` | Required path or URL |
| `external` | Optional bool; default true for `http(s):` URLs |
| `color` | Optional tone token |

## `ui.Shell`

Intent layout region for product chrome (e.g. Studio three-column). Children are laid out by `layout=`.

```python
ui.Shell(
    ui.Section(title="Filters", width="xs"),
    ui.Section(title="Preview", grow="1"),
    ui.Section(title="Style", width="sm"),
    layout="split-3",
    gap="4",
)
```

| `layout=` | Emit |
|-----------|------|
| `stack` | `.ourui-shell-stack` (column) |
| `row` | `.ourui-row` |
| `split-3` | `.ourui-shell-split-3` (3 columns → 1 col under 768px) |
| `grid` | `.ourui-grid` |

`layout=` also works on `ui.Section` / `ui.Page`. Box/flex/grid size props (`width=`, `grow=`, `grid_cols=`, …): [Style intents](style-intents.md).

## `ui.Nav`

Product chrome bar (Phase S3a + S6 drawer). Placement is an intent enum — not raw CSS `position`.

```python
ui.Nav(
    brand=ui.Link("Plasma", href="/"),
    items=[
        ui.Link("Features", href="#features"),
        ui.Link("FAQ", href="#faq"),
    ],
    actions=[ui.Link("Open Studio", href="/app", color="primary")],
    placement="sticky-top",
    tone="glass",
)
```

| Prop | Description |
|------|-------------|
| `brand` | Leading node (usually `ui.Link`) |
| `items` | List of nav links |
| `actions` | Trailing actions (links/buttons) |
| `placement` | `flow` \| `sticky-top` (default) \| `fixed-top` \| `fixed-bottom` \| `overlay` \| `backdrop` |
| `tone` | `solid` (default) \| `glass` |
| `menu` | `none` (default) \| `drawer` (mobile collapse) |

## Layout intents (S4 + ADR-013)

On `Shell` / `Section` / `Hero` (and most layout nodes):

| Prop | Values |
|------|--------|
| `gap` / `pad` | Scale keys: `none` \| `xs`…`2xl` \| numeric space scale (`4`, `6`, …) |
| `pad_x` / `pad_y` / `margin_*` | Same space scale |
| `align` | `start` \| `center` \| `end` \| `stretch` |
| `justify` | `start` \| `center` \| `end` \| `between` |
| `layout` | `stack` \| `row` \| `grid` \| `split-2` \| `split-3` \| `split-sidebar` |
| `width` / `height` / `grow` / `grid_cols` / … | See [Style intents](style-intents.md) |
| `motion` | `none` \| `family.pattern` (see [Motion](../concepts/motion.md)); aliases `enter`/`reveal`/`press` |

## Phase S3–S6 surfaces

| Kind | Role |
|------|------|
| `ui.ThemeToggle` | Toggle `.dark` on `<html>` |
| `ui.Footer` | `brand=` / `links=` / `meta=` |
| `ui.Canvas` | WebGL escape; `mode=gradient\|dither\|raymarch` |
| `ui.Frame` | iframe preview escape; `bind=` / `srcdoc=` HTML string |
| `ui.Image` | `src=` / `alt=` / `fit=` |
| `ui.Icon` | Reicon-style `name=` |
| `ui.Meta` | Document `title` / `description` / `og=` |
| `ui.Code` | Code block |
| `ui.CopyButton` | Clipboard; `copy=` |
| `ui.Menu` | Dropdown; `items=` |

## Positional arguments

The `ui` namespace accepts shorthand positional args:

- First string on `Button`, `Text`, `Card`, `Link`, `CopyButton`, `Code`, `ThemeToggle`, `Menu` → `text`
- First string on `Icon` → `name`; on `Image` → `src`
- First string on `Input` / `Select` / `Toggle` / `Slider` → `name`
- First string on other kinds → `title` when `title` is not set
- UI node positional args → appended to `children`

## See also

- [Tutorial 01 — Your first page](../tutorial/01-your-first-page.md)
- [Routing](routing.md)
- [Theme](theme.md)
- [State](state.md)
- [Server handlers](server.md)
- [Component authoring](component-authoring.md)
