# Language Spec

Normative surface for the current compiler (`ourui` **1.0.0**, dump schema **25** — **Frozen** for `1.0.x`). Breaking language/dump changes require `2.0` + ADR/RFC.

## Status

See [SPEC_STATUS.md](SPEC_STATUS.md). Language surface: **Frozen** at 1.0 (P0 + Phase S + Phase T–V). `Derived` remains **Draft**.

## Authoring model

OurUI programs are Python modules that build UI intent using the `ourui.ui` surface (and related helpers). The compiler parses Python, analyzes calls, and lowers them to IIR — it does not execute the module as a browser app.

## Grammar (allowed)

- Module-level assignments and expressions that construct UI nodes
- Calls of the form `ui.Name(...)` or user components
- Keyword arguments for attributes (`title=`, `variant=`, `color=`, `on_click=`, …)
- Nested calls as children / nested props
- String and numeric literals; simple dict/list literals for structured props
- `State(...)`, `@server` handlers, function/class components
- `ui.Theme(...)` for design token overrides

### Not yet

- Full Python execution semantics for arbitrary side effects in UI construction
- Client-only `State` (browser-local)

## Design tokens

OurUI emits semantic CSS variables under the `--ourui-*` namespace. Emit consumes **Resolved Design** (Host Contract); `ui.Theme` / `DEFAULT_*` seed the Design System pack only.

```python
theme = ui.Theme(primary="#1a5f4a", primary_fg="#f5faf8", dark={"primary": "#2dd4a8"})
ui.Button("Go", color="primary")
ui.ThemeToggle("Theme")  # toggles .dark on <html>
```

Token families (override via `ui.Theme`):

| Family | Keys (examples) |
|--------|-----------------|
| Color | `bg`, `fg`, `primary`, `primary_fg`, `muted`, `accent`, `danger`, `card`, `border`, … |
| Shape | `radius` |
| Space | `space_xs` … `space_2xl` |
| Type | `font_sans`, `font_display`, `text_xs` … `text_2xl`, `leading_*` |
| Elevation | `elev_0` … `elev_3` |

- HTML emit writes `:root { … }` and `.dark { … }`
- `color=` / `variant=` / `bg=` matching roles add tone classes
- Dump includes `semantic_graph.tokens` (schema **21**)

## Routing

Multiple pages via `route=` on `ui.Page`. Prefer `ui.Link(..., href=...)` for navigation.

## Built-in kinds

| Kind | Domain | Notes |
|---|---|---|
| `Page` | Intent | Root; optional `layout=` / `route=` |
| `Hero` | Intent | Hero; `pad=` / `motion=` |
| `Section` | Intent | Section; `layout=` / `gap=` / `pad=` / `align=` / `motion=` |
| `Shell` | Intent | Layout region; `layout=` + gap/pad/align/justify |
| `Nav` | Intent | Chrome; `placement=` / `tone=` / `menu=` + brand/items/actions |
| `Footer` | Intent | Footer; brand/links/meta slots |
| `Meta` | Intent | Document head title/description/og |
| `Button` | Presentation | May carry `on_click`, `motion=press`, disabled/loading |
| `Text` | Presentation | Text content |
| `Card` | Presentation | Card; optional `motion=` |
| `Grid` | Presentation | Grid concept |
| `Link` | Presentation | `href=` required |
| `Input` / `Select` / `Toggle` / `Slider` | Presentation | Form controls → `@server` payload |
| `ThemeToggle` | Presentation | Client `.dark` toggle |
| `Canvas` | Presentation | WebGL escape; `mode=gradient\|dither\|raymarch` |
| `Image` | Presentation | `src=` / `alt=` / `fit=` |
| `Icon` | Presentation | Reicon-style `name=` |
| `Code` | Presentation | Code block |
| `CopyButton` | Presentation | Clipboard; `copy=` |
| `Menu` | Presentation | Dropdown; `items=` |

### Layout intents (`layout=`)

`stack` \| `row` \| `grid` \| `split-2` \| `split-3` \| `split-sidebar`

Spacing / alignment (semantic enums — not raw CSS): `gap=` / `pad=` = `none|xs|sm|md|lg|xl|2xl`; `align=` = `start|center|end|stretch`; `justify=` = `start|center|end|between`.

### Motion (`motion=`)

`none` \| `enter` \| `press` \| `reveal` — host CSS + `prefers-reduced-motion`.

### Nav

```python
ui.Nav(
    brand=ui.Link("OurUI", href="/"),
    items=[ui.Link("Features", href="#features")],
    actions=[ui.ThemeToggle("Theme"), ui.Link("App", href="/app", color="primary")],
    placement="sticky-top",
    tone="glass",
    menu="drawer",
)
```

### Forms (S2)

```python
ui.Input(name="email", type="email", bind=email)
ui.Select(name="theme", options=["light", "dark"], bind=theme)
ui.Toggle(name="enabled", label="On", bind=on)
ui.Slider(name="volume", min=0, max=100, step=5, bind=level)
ui.Button("Save", on_click=save)  # posts [data-ourui-field] values
```

### Canvas escape (S5)

```python
ui.Canvas(mode="gradient", config={"pace": 40}, reduced_motion="static")
```

Explicit host escape — not the default styling path (ADR-005).

## Components / Behavior

Function and class components expand at Analyze. `State` + `@server` + `on_click` as in Phase F–H.

## Example

See [examples/example.py](examples/example.py) and [demo/app.py](demo/app.py).

## Errors

- Syntax errors from Python parse
- Unknown `ui.*` callee / failed component expand
- Non-literal arguments where literals are required (limited)

Spans are attached to nodes (I5).

## Evolution

Extensions require updates here and, if they add vocabulary, an [RFC](RFC_PROCESS.md). Dump schema bumps with Stable surface changes.
