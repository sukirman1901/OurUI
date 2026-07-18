"""Enterprise Kit — settings shell (ThemeToggle + form + Show/When)."""

from ourui import State, server, ui

theme = ui.Theme(density="comfortable")

display_name = State("Ada Lovelace")
notify = State(True)
message = State("")
show_saved = State(False)


@server
def save_settings(payload: dict | None = None):
    data = payload or {}
    name = str(data.get("display_name") or display_name.get() or "").strip()
    if name:
        display_name.set(name)
    if "notify" in data:
        notify.set(bool(data.get("notify")))
    message.set("Settings saved")
    show_saved.set(True)
    return {
        "display_name": display_name.get(),
        "notify": notify.get(),
        "message": message.get(),
        "show_saved": show_saved.get(),
    }


@server
def dismiss_banner():
    show_saved.set(False)
    return {"show_saved": show_saved.get()}


page = ui.Page(
    ui.Nav(
        brand=ui.Text("Acme Settings"),
        items=[ui.Link("General", href="/")],
        actions=[ui.ThemeToggle(), ui.Button("Dismiss", color="muted", on_click=dismiss_banner)],
    ),
    ui.Hero(
        title="General",
        subtitle="Enterprise Kit — ThemeToggle, fields, Show/When.",
    ),
    ui.Show(
        ui.Alert(text=message, severity="success"),
        show=show_saved,
    ),
    ui.Form(
        ui.Input(name="display_name", label="Display name", bind=display_name),
        ui.Toggle(name="notify", label="Email notifications", bind=notify),
        ui.Button("Save", color="primary"),
        on_submit=save_settings,
    ),
    ui.When(
        show=notify,
        then=ui.Text("Notifications are on."),
        else_=ui.Text("Notifications are off."),
    ),
)
