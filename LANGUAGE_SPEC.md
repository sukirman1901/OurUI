# Language Spec

Normative surface for the current compiler (`ourui` **1.11.0**, dump schema **30** additive). Language/IR breaking changes remain **Frozen** at schema **25** for `1.x` — a major bump (`2.0`) + ADR/RFC is required to break them.

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
- `ui.Theme(...)` for theme role / scale overrides
- Style intent props on layout kinds (`aspect=`, `pad_x=`, `width=`, …) — see ADR-013

### Not in language scope

- Full Python execution semantics for arbitrary side effects in UI construction
- Client-only `State` (browser-local)
- Composed section patterns inside Stable `ui.*` while the utility catalog is incomplete ([ADR-014](docs/decisions/ADR-014-language-primitives-vs-kit.md))

## Theme roles and style intents

**Style intents** are the craft foundation (ADR-013). **`ui.Theme`** is a thin brand sheet (roles, density, `page=`). OurUI emits `--ourui-*` variables plus finite `.ourui-*` utilities. Emit consumes **Resolved Design** (Host Contract). User docs: [style intents](docs/user/reference/style-intents.md) · [theme](docs/user/reference/theme.md).

```python
theme = ui.Theme(primary="#1a5f4a", primary_fg="#f5faf8", dark={"primary": "#2dd4a8"})
ui.Button("Go", color="primary")
ui.ThemeToggle()  # icon-only; toggles .dark on <html>
ui.Shell(…, aspect="video", width="full")
```

Theme role families (override via `ui.Theme`):

| Family | Keys (examples) |
|--------|-----------------|
| Color | `bg`, `fg`, `primary`, `primary_fg`, `muted`, `accent`, `danger`, `card`, `border`, … |
| Shape | `radius` |
| Space | `space_xs` … `space_2xl` |
| Type | `font_sans`, `font_display`, `text_xs` … `text_2xl`, `leading_*` |
| Elevation | `elev_0` … `elev_3` |
| Scale tables (ADR-013) | `space={...}`, `sizes={...}`, `type={...}` dict overrides for `--ourui-space-*` / `--ourui-size-*` / `--ourui-text-*` |

- HTML emit writes `:root { … }` and `.dark { … }` plus generated style-intent utilities (`.ourui-w-lg`, …)
- `color=` / `variant=` / `bg=` matching roles add tone classes
- Layout/presentation props such as `width=`, `pad_x=`, `grow=`, `grid_cols=` — see [style-intents.md](docs/user/reference/style-intents.md) ([ADR-013](docs/decisions/ADR-013-style-intent-catalog.md))
- Dump includes `semantic_graph.tokens` (since schema **21**; current dump schema **30**) and `style_catalog`

## Style intents

Authoring uses **intent props** (not utility class strings). Emit generates finite `.ourui-*` utilities from Tailwind-derived scales. Kit/pattern libraries compose these props outside the language.

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
| `Form` / `Dialog` / `Toast` | Presentation | Phase T surfaces |
| `List` / `Table` / `Empty` / `Spinner` / `Alert` | Presentation | Phase U; List/Table may bind `items=`/`rows=` State |
| `Show` / `When` | Presentation | Conditional visibility |
| `Frame` | Presentation | Host escape iframe (`srcdoc=` / `bind=`); `SEC001` under `--profile a11y` |
| `Theme` | Analysis | Thin brand overrides; `density=`; optional `page=` measure |

### Layout intents (`layout=`)

`stack` \| `row` \| `grid` \| `split-2` \| `split-3` \| `split-sidebar`

Spacing / alignment (semantic enums — not raw CSS): `gap=` / `pad=` = `none|xs|sm|md|lg|xl|2xl`; `align=` = `start|center|end|stretch`; `justify=` = `start|center|end|between`.

### Motion (`motion=`)

`family.pattern` vocabulary ([ADR-012](docs/decisions/ADR-012-motion-vocabulary.md)) — e.g. `reveal.fade-up`, `text.word-reveal`, `press.scale`.  
Legacy aliases: `enter` → `reveal.fade-up`, `reveal` → `reveal.mask-wipe`, `press` → `press.scale`.  
Host CSS/JS + `prefers-reduced-motion`. Full catalog registered; M1 ships Stable emit.

### Nav

```python
ui.Nav(
    brand=ui.Link("OurUI", href="/"),
    items=[ui.Link("Features", href="#features")],
    actions=[ui.ThemeToggle(), ui.Link("App", href="/app", color="primary")],
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

See [examples/example.py](examples/example.py) and [examples/tutorial/](examples/tutorial/).

## Errors

- Syntax errors from Python parse
- Unknown `ui.*` callee / failed component expand
- Non-literal arguments where literals are required (limited)

Spans are attached to nodes (I5).

## Evolution

Extensions require updates here and, if they add vocabulary, an [RFC](RFC_PROCESS.md). Dump schema bumps with Stable surface changes. Additive schemas **26–30** do not break the Frozen **25** baseline.
