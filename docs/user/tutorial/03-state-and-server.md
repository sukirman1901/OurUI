# Tutorial 03 — State and server

## Goal

Keep reactive data in **`State`**, mutate it from a **`@server`** handler, and wire a button click to that handler.

## Code

**`examples/tutorial/03_state_server.py`**

```python
from ourui import State, server, ui

count = State(0)


@server
def increment() -> int:
    count.set(count.get() + 1)
    return count.get()


page = ui.Page(
    ui.Hero(title="State"),
    ui.Text(count),
    ui.Button("+1", color="primary", on_click=increment),
)
```

Run:

```bash
ourui serve examples/tutorial/03_state_server.py
```

Click **+1**. The displayed count updates without writing JavaScript yourself.

## What you learned

- **`State(initial)`** holds a value the UI can bind to. Pass a `State` instance to **`ui.Text`** to show it.
- Read with **`count.get()`**, write with **`count.set(value)`**.
- Decorate Python functions with **`@server`** so the runtime can call them over HTTP when the user interacts with the page.
- **`ui.Button(..., on_click=handler)`** connects a click to a server handler. Use **`color="primary"`** for the themed primary style (tokens come in tutorial 05).
- Server handlers can return a value; the runtime uses it to refresh bound UI.

In dev mode (`ourui serve` without `--prod`), `State` is process-global and shared across browser tabs — fine for learning, not for production multi-user apps. Production sessions are covered in tutorial 06.

## Next

- [Tutorial 04 — Routing](04-routing.md)
