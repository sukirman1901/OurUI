# State

`State` holds reactive server-side values that the UI can bind to. Mutate it inside `@server` handlers; the runtime pushes updates back to the browser.

```python
from ourui import State, server, ui

count = State(0)

@server
def increment() -> int:
    count.set(count.get() + 1)
    return count.get()

page = ui.Page(
    ui.Text(count),
    ui.Button("+1", color="primary", on_click=increment),
)
```

Normative behavior: [Language Spec — Behavior](../../../LANGUAGE_SPEC.md#behavior-phase-fh).

## Creating state

```python
count = State(0)
message = State("hello")
items = State([1, 2, 3])
```

Assign at **module level** so the compiler registers the binding and `ourui serve` can snapshot it.

## Reading and writing

| Method | Description |
|--------|-------------|
| `state.get()` | Return the current value |
| `state.set(value)` | Replace the value |
| `state.value` | Property alias for the current value |

Prefer `get()` / `set()` in `@server` handlers for clarity.

## Binding to UI

Pass a `State` instance where text content is expected:

```python
ui.Text(count)
ui.Button(str(count))  # for labels, convert explicitly if needed
```

The compiler records a `reads_state` edge. Emitted HTML includes `data-ourui-bind` attributes; the bundled JS applies RPC `state` payloads after handler calls.

## Dev vs production scoping

| Mode | `State` scope |
|------|---------------|
| Dev (`ourui serve`) | **Process-global** — all browser tabs share the same in-memory values |
| Production (`ourui serve --prod`) | **Per-session** — isolated via the `ourui_sid` cookie |

In production, each session starts from the module's initial `State(...)` values, then overlays session storage on each request. Empty sessions do not leak another user's in-memory state.

Use `--prod` (and optionally `--workers` / `--session-dir`) before deploying multi-user apps. See [Serve: dev and prod](../tutorial/06-serve-dev-and-prod.md).

## Handler return values

`@server` functions may return a value. The runtime always includes a live **`state`** snapshot in the JSON response:

```json
{
  "ok": true,
  "handler": "increment",
  "result": 3,
  "state": {"count": 3}
}
```

Returning a value is optional — the `state` object is what refreshes bound UI.

## Limitations (P0)

- **Server-side only** — no browser-local `State` without a server round-trip
- State must be constructed with a module-level `State(...)` call the analyzer can see
- Arbitrary Python side effects during UI construction are not part of the stable surface

## See also

- [Server handlers](server.md)
- [Tutorial 03 — State and server](../tutorial/03-state-and-server.md)
- [CLI — serve](cli.md)
