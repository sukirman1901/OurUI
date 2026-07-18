"""Enterprise E1 — conditional Show/When + dynamic List/Table."""

from ourui import State, server, ui

visible = State(True)
items = State(["Alpha", "Beta", "Gamma"])
rows = State(
    [
        {"name": "Ada", "role": "Admin"},
        {"name": "Lin", "role": "Editor"},
    ]
)


@server
def toggle():
    visible.set(not bool(visible.get()))
    return {"visible": visible.get()}


@server
def add_item():
    cur = list(items.get() or [])
    cur.append(f"Item {len(cur) + 1}")
    items.set(cur)
    return {"items": items.get()}


@server
def add_row():
    cur = list(rows.get() or [])
    cur.append({"name": f"User {len(cur) + 1}", "role": "Viewer"})
    rows.set(cur)
    return {"rows": rows.get()}


page = ui.Page(
    ui.Hero(title="E1 completeness", subtitle="Show / When / dynamic list & table"),
    ui.Button("Toggle panel", color="primary", on_click=toggle),
    ui.Show(
        ui.Alert("Panel visible via ui.Show(show=State)", severity="info"),
        show=visible,
    ),
    ui.When(
        show=visible,
        then=ui.Text("When: then-branch"),
        else_=ui.Text("When: else-branch"),
    ),
    ui.Button("Add list item", color="muted", on_click=add_item),
    ui.List(items=items),
    ui.Button("Add table row", color="muted", on_click=add_row),
    ui.Table(columns=["name", "role"], rows=rows),
)
