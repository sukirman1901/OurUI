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
| `ui.Hero` | Intent | Prominent header block |
| `ui.Section` | Intent | Grouped content section (`layout=` optional) |
| `ui.Shell` | Intent | Layout region (`layout=stack\|row\|split-3\|grid`) |
| `ui.Button` | Presentation | Clickable control |
| `ui.Text` | Presentation | Inline text (or bound `State`) |
| `ui.Card` | Presentation | Card container |
| `ui.Grid` | Presentation | Responsive grid layout |
| `ui.Link` | Presentation | In-app or external navigation (`href=`) |
| `ui.Input` | Presentation | Form field (`name=` → `@server` payload on button click) |
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
| `cta` | node | Optional call-to-action (commonly a `ui.Button`) |
| `children` | nodes | Additional child nodes |

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
| `type` | `str` | `text` \| `email` \| `password` \| `number` \| `search` \| `url` \| `tel` |
| `placeholder` | `str` | Placeholder text |
| `label` | `str` | Optional visible label |
| `bind` / `value` | `State` or `str` | Initial value; `bind=` syncs from server State after RPC |

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
    ui.Section(title="Filters"),
    ui.Section(title="Preview"),
    ui.Section(title="Style"),
    layout="split-3",
)
```

| `layout=` | Emit |
|-----------|------|
| `stack` | `.ourui-shell-stack` (column) |
| `row` | `.ourui-row` |
| `split-3` | `.ourui-shell-split-3` (3 columns → 1 col under 768px) |
| `grid` | `.ourui-grid` |

`layout=` also works on `ui.Section` / `ui.Page`.

## Positional arguments

The `ui` namespace accepts shorthand positional args:

- First string on `Button`, `Text`, `Card`, `Link` → `text`
- First string on `Input` → `name`
- First string on other kinds → `title` when `title` is not set
- UI node positional args → appended to `children`

## See also

- [Tutorial 01 — Your first page](../tutorial/01-your-first-page.md)
- [Routing](routing.md)
- [Theme](theme.md)
- [State](state.md)
- [Server handlers](server.md)
- [Component authoring](component-authoring.md)
