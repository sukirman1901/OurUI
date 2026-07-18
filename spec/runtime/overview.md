# Runtime

**Status:** Draft (Phase G — `ourui serve` + RPC).

## Dev server

```bash
ourui serve examples/example.py
# http://127.0.0.1:8765/
```

| Route | Behavior |
|---|---|
| `GET /` | Recompile source → emit HTML (RTR → HTML/CSS/JS) |
| `POST /__ourui/call/<handler>` | Load authoring module; call named `@server` / handler; JSON `{ok, result}` |

## JS shim

Server-kind handlers `fetch` `POST /__ourui/call/<name>`. Client-kind handlers stay local. Events: `ourui:call`, `ourui:result`.

Implementation: `packages/ourui/ourui/runtime/`, `packages/ourui/ourui/emit/js.py`.

## Invariants

Browser still never receives Python AST (I1). Emitter still consumes HostNode only (I2). Handler execution happens on the **dev server**, not in the browser.
