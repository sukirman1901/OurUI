# Runtime

**Status:** Draft (Phase G–H).

## Dev server

```bash
ourui serve examples/example.py
# http://127.0.0.1:8765/
```

| Route | Behavior |
|---|---|
| `GET /` | Recompile → HTML with live `State` snapshot |
| `POST /__ourui/call/<handler>` | Run handler; JSON `{ok, result, state}` |

Module cache keeps `State` values across requests in one `serve` process.

## JS shim

- Server handlers `fetch` RPC endpoint
- `applyState(state)` updates `[data-ourui-bind="…"]`
- Events: `ourui:call`, `ourui:result`

## Invariants

Browser never receives Python AST (I1). Emitter consumes HostNode only (I2). Handler + State mutation run on the **dev server**.
