# Runtime

**Status:** Draft shim (Phase F); real RPC Experimental.

## Phase F shim

Emitted JS (`packages/ourui/ourui/emit/js.py`):

- Binds `click` on `[data-ourui-on-click]`
- Calls `OurUI.invoke(handlerName)`
- Dispatches `ourui:call` CustomEvent
- Logs server vs client stubs (`console.info`)

Handlers come from RTR (`@server` / plain `def` + `on_click=`). No Python AST in the browser (I1).

## Next

Replace stub with HTTP/WebSocket call to a real OurUI server runtime.
