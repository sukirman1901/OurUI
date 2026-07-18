# Language Spec (P0 subset)

Normative surface for **P0**. Later phases extend this document via RFC when needed.

## Status

See [SPEC_STATUS.md](SPEC_STATUS.md). P0 DSL: **Draft**.

## Authoring model

OurUI programs are Python modules that build UI intent using the `ourui.ui` surface (and related helpers). The compiler parses Python, analyzes calls, and lowers them to IIR — it does not execute the module as a browser app.

## P0 grammar (allowed)

- Module-level assignments and expressions that construct UI nodes
- Calls of the form `ui.Name(...)` or `Name(...)` where `Name` is a known intent/presentation kind
- Keyword arguments for attributes (`title=`, `variant=`, `color=`, …)
- Nested calls as children / nested props
- String and numeric literals; simple dict/list literals for structured props

### Not in P0

- Full Python execution semantics for arbitrary side effects
- User-defined `Component` classes (planned)
- Reactive `State` beyond server-side get/set + DOM bind (client-only State planned)
- Routing (planned)
- Real production multi-worker state store (dev serve uses in-process module cache)

## Built-in kinds (P0+)

| Kind | Domain | Notes |
|---|---|---|
| `Page` | Intent | Root container |
| `Hero` | Intent | Hero intent |
| `Section` | Intent | Section intent |
| `Button` | Presentation | Button-as-concept (not HTML); may carry `on_click` |
| `Text` | Presentation | Text content |
| `Card` | Presentation | Card concept |
| `Grid` | Presentation | Grid concept (pre-layout) |

### Behavior (Phase F–H)

```python
from ourui import ui, server, State

count = State(0)

@server
def increment():
    count.set(count.get() + 1)
    return count.get()

ui.Text(count)                 # bind
ui.Button("+1", on_click=increment)
```

- `State(initial)` — server-side reactive value (persists in `ourui serve` module cache).
- `ui.Text(count)` / `bind=` — lowers to RTR Text with `data-ourui-bind`.
- After `@server` RPC, JS `applyState` updates bound nodes from `response.state`.

Theme references may appear as string tokens in attributes (e.g. `variant="primary"`).

## Example

```python
from ourui import ui

page = ui.Page(
    ui.Hero(
        title="Welcome",
        subtitle="Build SaaS in Python",
        cta=ui.Button("Get Started", variant="primary"),
    ),
    ui.Section(
        title="Features",
        children=[
            ui.Card("Analysis"),
            ui.Card("Realtime"),
        ],
    ),
)
```

## Errors

P0 reports:

- Syntax errors from Python parse
- Unknown `ui.*` callee
- Non-literal arguments where literals are required (limited)

Spans are attached to nodes (I5).

## Evolution

Extensions require updates here and, if they add vocabulary, an [RFC](RFC_PROCESS.md).
