"""Enterprise E1 reference — minimal CRUD-shaped admin list."""

from ourui import State, server, ui

title = State("")
rows = State(
    [
        {"id": "1", "title": "Welcome", "status": "published"},
        {"id": "2", "title": "Draft notes", "status": "draft"},
    ]
)
message = State("")
show_form = State(True)


@server
def create_item(payload: dict | None = None):
    data = payload or {}
    name = str(data.get("title") or title.get() or "").strip()
    if not name:
        message.set("Title is required")
        return {"message": message.get(), "rows": rows.get()}
    cur = list(rows.get() or [])
    cur.append({"id": str(len(cur) + 1), "title": name, "status": "draft"})
    rows.set(cur)
    title.set("")
    message.set(f"Created “{name}”")
    return {"rows": rows.get(), "title": title.get(), "message": message.get()}


@server
def toggle_form():
    show_form.set(not bool(show_form.get()))
    return {"show_form": show_form.get()}


page = ui.Page(
    ui.Nav(
        brand=ui.Text("Acme Admin"),
        items=[ui.Link("Items", href="/")],
        actions=[ui.Button("Toggle form", color="muted", on_click=toggle_form)],
    ),
    ui.Hero(
        title="Items",
        subtitle="Enterprise E1 reference — Form + Show + dynamic Table.",
    ),
    ui.Show(
        ui.Form(
            ui.Input(name="title", label="Title", bind=title, placeholder="New item"),
            ui.Button("Create", color="primary"),
            on_submit=create_item,
        ),
        show=show_form,
    ),
    ui.When(
        show=message,
        then=ui.Alert(text=message, severity="success"),
        else_=ui.Empty(title="No recent action"),
    ),
    ui.Table(columns=["id", "title", "status"], rows=rows),
)
