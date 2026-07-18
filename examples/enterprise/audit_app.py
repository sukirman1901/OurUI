"""Enterprise Kit — audit log table driven by State."""

from ourui import State, server, ui

rows = State(
    [
        {"id": "a1", "actor": "ada", "action": "login", "at": "2026-07-18T10:00:00Z"},
        {"id": "a2", "actor": "grace", "action": "update_settings", "at": "2026-07-18T11:30:00Z"},
        {"id": "a3", "actor": "ada", "action": "create_item", "at": "2026-07-18T12:15:00Z"},
    ]
)
filter_actor = State("")


@server
def refresh_audit(payload: dict | None = None):
    data = payload or {}
    actor = str(data.get("filter_actor") or filter_actor.get() or "").strip()
    filter_actor.set(actor)
    # Template: filter in-memory; real apps query an audit store outside OurUI.
    all_rows = [
        {"id": "a1", "actor": "ada", "action": "login", "at": "2026-07-18T10:00:00Z"},
        {"id": "a2", "actor": "grace", "action": "update_settings", "at": "2026-07-18T11:30:00Z"},
        {"id": "a3", "actor": "ada", "action": "create_item", "at": "2026-07-18T12:15:00Z"},
    ]
    if actor:
        rows.set([r for r in all_rows if r["actor"] == actor])
    else:
        rows.set(all_rows)
    return {"rows": rows.get(), "filter_actor": filter_actor.get()}


page = ui.Page(
    ui.Nav(
        brand=ui.Text("Acme Audit"),
        items=[ui.Link("Events", href="/")],
    ),
    ui.Hero(
        title="Audit log",
        subtitle="Enterprise Kit — Table of audit-ish rows from State.",
    ),
    ui.Form(
        ui.Input(name="filter_actor", label="Filter actor", bind=filter_actor, placeholder="ada"),
        ui.Button("Refresh", color="primary"),
        on_submit=refresh_audit,
    ),
    ui.Table(columns=["id", "actor", "action", "at"], rows=rows),
)
