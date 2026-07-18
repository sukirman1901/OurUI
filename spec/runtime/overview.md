# Runtime

**Status:** Draft (Phase G–J).

## Dev server

```bash
ourui serve examples/example.py
# http://127.0.0.1:8765/
```

| Route | Behavior |
|---|---|
| `GET /` | Recompile → HTML with live `State` + HMR client |
| `POST /__ourui/call/<handler>` | Run handler; JSON `{ok, result, state}` |
| `GET /__ourui/hmr` | SSE stream; `event: reload` when source mtime changes |
| `GET /__ourui/hmr/status` | `{generation, mtime_ns}` |

Module cache keeps `State` values across requests. On HMR reload, the module is re-imported so code edits apply (in-memory State resets).

## JS shim

- Server handlers `fetch` RPC endpoint
- `applyState(state)` updates `[data-ourui-bind="…"]`
- When served with `hmr=True`: `EventSource("/__ourui/hmr")` → `location.reload()` on `reload`

## Invariants

Browser never receives Python AST (I1). Emitter consumes HostNode only (I2). Handler + State mutation run on the **dev server**.
