# Language Spec (P0+ subset)

Normative surface for the current compiler. Later phases extend this document via RFC when needed.

## Status

See [SPEC_STATUS.md](SPEC_STATUS.md). Language surface: **Stable** (P0 subset).

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

## Design tokens (Phase P)

OurUI emits semantic CSS variables under the `--ourui-*` namespace (hex/px defaults — not a third-party theme dump).

```python
theme = ui.Theme(primary="#1a5f4a", primary_fg="#f5faf8", dark={"primary": "#2dd4a8"})
ui.Button("Go", color="primary")
```

- Builtin light + dark maps live in the compiler; `ui.Theme` merges overrides into Semantic Graph `tokens`
- HTML emit writes `:root { … }` and `.dark { … }`; components use `var(--ourui-…)`
- `color=` / `variant=` / `bg=` values that match token roles (`primary`, `accent`, `danger`, `muted`, …) add tone classes
- Dump schema version **9** includes `semantic_graph.tokens`

## Routing (Phase K)

Multiple pages in one module via `route=` on `ui.Page`:

```python
home = ui.Page(route="/", ui.Hero(title="Home"))
about = ui.Page(route="/about", ui.Section(title="About"))
```

- Analyze registers `routes: {"/": node_id, …}` in the Semantic Graph
- A single `ui.Page` without `route=` defaults to `/`
- Multiple pages require an explicit `route=` on each
- `ourui serve` compiles the matching page per `GET` path; unknown paths → 404
- Prefer `ui.Link("About", href="/about")` for in-app navigation (emits `<a href>`)

## Built-in kinds

| Kind | Domain | Notes |
|---|---|---|
| `Page` | Intent | Root container; optional `layout=` |
| `Hero` | Intent | Hero intent |
| `Section` | Intent | Section intent; optional `layout=` |
| `Shell` | Intent | Layout region; `layout=` = `stack` \| `row` \| `split-3` \| `grid` |
| `Button` | Presentation | Button-as-concept (not HTML); may carry `on_click` |
| `Text` | Presentation | Text content |
| `Card` | Presentation | Card concept |
| `Grid` | Presentation | Grid concept (pre-layout) |
| `Link` | Presentation | Navigation anchor; requires `href=` |
| `Input` | Presentation | Form field; `name=` collected into `@server` payload on button click |

### Layout intents (`layout=`)

Authoring values (not CSS utilities): `stack`, `row`, `split-3`, `grid`.  
Emit maps them to host classes (e.g. `.ourui-shell-split-3`) — see ADR-005.

### Links

```python
ui.Link("Studio", href="/app")
ui.Link("Docs", href="https://example.com", color="primary")  # external → target=_blank
```

### Inputs (Phase S2)

```python
email = State("")

@server
def save(**payload):
    email.set(str(payload.get("email", "")))

ui.Input(name="email", type="email", placeholder="you@example.com", label="Email", bind=email)
ui.Button("Save", on_click=save)  # JS posts collected [data-ourui-field] values
```

## Components (Phase I)

```python
def FeatureCard(title: str):
    return ui.Card(title)

class CounterPanel(Component):
    def __init__(self, label: str):
        self.label = label
    def build(self):
        return ui.Section(title=self.label, children=[...])

FeatureCard("Analysis")
CounterPanel("Counter")
```

Expanded at **Analyze** (before IIR). Provenance includes `expand:FeatureCard`. Body must return a single `ui.*` or nested component call.

## Behavior (Phase F–H)

```python
from ourui import ui, server, State

count = State(0)

@server
def increment():
    count.set(count.get() + 1)
    return count.get()

ui.Text(count)
ui.Button("+1", on_click=increment)
```

- `on_click` — function name or string → RTR events → `data-ourui-on-click`
- `@server` — handler kind in the handler table; executed by `ourui serve`
- `State` — server-side value; binds become `data-ourui-bind`; RPC returns `state` for JS `applyState`

Theme references may appear as string tokens (e.g. `variant="primary"`).

## Example

See [examples/example.py](examples/example.py).

## Errors

- Syntax errors from Python parse
- Unknown `ui.*` callee / failed component expand
- Non-literal arguments where literals are required (limited)

Spans are attached to nodes (I5).

## Evolution

Extensions require updates here and, if they add vocabulary, an [RFC](RFC_PROCESS.md).
