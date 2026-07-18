# Runtime

**Status:** Stable for single-process serve (Phase N). Multi-worker / shared store remains Experimental.

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
| `POST /__ourui/call/<handler>` | Run handler; JSON `{ok, result, state}` (may include `traceback` on 500) |
| `GET /__ourui/health` | `{"ok": true, "mode": "dev"}` |
| `GET /__ourui/hmr` | SSE stream; `event: reload` when source mtime changes |
| `GET /__ourui/hmr/status` | `{generation, mtime_ns}` |

Module cache keeps **process-global** `State` across requests (single-tenant). On HMR reload, the module is re-imported (in-memory State resets).

### Multi-page routing (Phase K)

```python
home = ui.Page(route="/", ui.Hero(title="Home"))
about = ui.Page(route="/about", ui.Section(title="About"))
```

Semantic Graph carries `routes: {"/": node_id, "/about": node_id}`. A single page without `route=` defaults to `/`. Plain anchor links trigger full page loads.

## Production mode (Phase N)

```bash
ourui serve examples/example.py --prod
```

| Behavior | Detail |
|---|---|
| HMR | Off (no file watcher, no SSE client in HTML) |
| State | Session-scoped via HttpOnly cookie `ourui_sid` (in-memory store) |
| Errors | 500 JSON without `traceback` (traceback logged to stderr) |
| Health | `GET /__ourui/health` → `{"ok": true, "mode": "prod"}` |
| Unknown pages | HTML 404 |
| Concurrency | Process lock around session hydrate → handler → persist |

Single-process only. Multi-worker / Redis / shared State store is out of scope (Experimental).

## JS shim

- Server handlers `fetch` RPC endpoint
- `applyState(state)` updates `[data-ourui-bind="…"]`
- When served with `hmr=True`: `EventSource("/__ourui/hmr")` → `location.reload()` on `reload`

## Invariants

Browser never receives Python AST (I1). Emitter consumes HostNode only (I2). Handler + State mutation run on the server process.
