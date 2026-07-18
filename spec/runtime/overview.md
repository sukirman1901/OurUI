# Runtime

**Status:** Stable (Phase M — serve/RPC/HMR/routing). Production multi-worker hardening remains Experimental.

## Dev server

```bash
ourui serve examples/example.py
# http://127.0.0.1:8765/
```

| Route | Behavior |
|---|---|
| `GET /` (or registered paths) | Recompile matching `ui.Page` → HTML with live `State` + HMR client |
| `GET /about` … | Same for each `route=` registered at Analyze |
| Unknown path | `404` JSON `{"error":"not found"}` |
| `POST /__ourui/call/<handler>` | Run handler; JSON `{ok, result, state}` |
| `GET /__ourui/hmr` | SSE stream; `event: reload` when source mtime changes |
| `GET /__ourui/hmr/status` | `{generation, mtime_ns}` |

### Multi-page routing (Phase K)

```python
home = ui.Page(route="/", ui.Hero(title="Home"))
about = ui.Page(route="/about", ui.Section(title="About"))
```

Semantic Graph carries `routes: {"/": node_id, "/about": node_id}`. A single page without `route=` defaults to `/`. Plain anchor links trigger full page loads.

Module cache keeps `State` values across requests. On HMR reload, the module is re-imported so code edits apply (in-memory State resets).

## JS shim

- Server handlers `fetch` RPC endpoint
- `applyState(state)` updates `[data-ourui-bind="…"]`
- When served with `hmr=True`: `EventSource("/__ourui/hmr")` → `location.reload()` on `reload`

## Invariants

Browser never receives Python AST (I1). Emitter consumes HostNode only (I2). Handler + State mutation run on the **dev server**.
