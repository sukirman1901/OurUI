# Server handlers

Decorate Python functions with `@server` to run them over HTTP when users interact with the page. Handlers mutate `State`, return optional results, and drive UI updates without writing JavaScript.

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

Run with `ourui serve app.py`. Normative behavior: [Language Spec — Behavior](../../../LANGUAGE_SPEC.md#behavior-phase-fh).

## Defining handlers

```python
from ourui import server

@server
def get_started() -> dict[str, str]:
    return {"message": "Welcome from OurUI server"}

@server
def increment() -> int:
    count.set(count.get() + 1)
    return count.get()
```

The `@server` decorator marks the function in the handler table. Only `@server` functions are invoked by the runtime RPC endpoint.

## Wiring clicks

Connect a button (or other control) to a handler with `on_click=`:

```python
ui.Button("Get Started", color="primary", on_click=get_started)
ui.Button("+1", on_click=increment)
ui.Button("Legacy", on_click="increment")  # string name also accepted
```

The compiler lowers `on_click` to RTR events and emits `data-ourui-on-click` in HTML.

## HTTP API

When `ourui serve` is running:

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/` and registered routes | Emit HTML for the matching `ui.Page` |
| `POST` | `/__ourui/call/<handler>` | Execute a `@server` function |
| `GET` | `/__ourui/health` | Health check (**`--prod` only**) |
| `GET` | `/__ourui/hmr` | SSE hot reload (**dev only**) |

### Calling a handler

```bash
curl -s -X POST http://127.0.0.1:8765/__ourui/call/increment \
  -H 'Content-Type: application/json' \
  -d '{}'
```

Success response:

```json
{
  "ok": true,
  "handler": "increment",
  "result": 1,
  "state": {"count": 1}
}
```

- **`result`** — the handler's return value (may be `null`)
- **`state`** — snapshot of all module-level `State` objects after the call

The request body is optional JSON. If the handler accepts keyword arguments, keys from the payload are passed through; otherwise the handler is called with no arguments.

### Errors

| Status | When |
|--------|------|
| `404` | Unknown handler name |
| `400` | Invalid JSON or malformed handler path |
| `500` | Handler raised an exception |

In **dev mode**, `500` responses include a **`traceback`** field. In **`--prod`**, only a generic error message is returned to the client (full trace is written to stderr on the server).

## Sessions and concurrency

| Mode | Behavior |
|------|----------|
| Dev | Handlers run against process-global `State`; requests are serialized with a lock |
| `--prod` | Session state is loaded before the call and saved after; cookie `ourui_sid` identifies the session |

With multiple workers (`--prod --workers N`), use the file session store so all workers see the same session data. See [CLI — serve](cli.md).

## Static HTML limitation

`ourui emit` produces HTML with the client shim, but **`@server` handlers require `ourui serve`** — there is no backend to execute Python when opening static files alone.

## See also

- [State](state.md)
- [Tutorial 03 — State and server](../tutorial/03-state-and-server.md)
- [Serve: dev and prod](../tutorial/06-serve-dev-and-prod.md)
