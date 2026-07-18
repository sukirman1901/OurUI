from ourui import Derived, State, server, ui

email = State("")
dialog_open = State(False)
toast_open = State(False)
label = Derived(lambda: f"Hi {email.get() or 'friend'}")


@server
def save(**payload: object) -> dict:
    if "email" in payload:
        email.set(str(payload["email"]))
    toast_open.set(True)
    return {"email": email.get(), "toast_open": True}


@server
def open_dialog() -> dict:
    dialog_open.set(True)
    return {"dialog_open": True}


page = ui.Page(
    ui.Form(
        ui.Input("email", type="email", label="Email", bind=email, helper="Work email"),
        ui.Button("Save", on_click=save),
        on_submit=save,
    ),
    ui.Button("Open dialog", on_click=open_dialog),
    ui.Dialog(
        ui.Text("Confirm action"),
        title="Confirm",
        open=dialog_open,
        actions=[ui.Button("OK", on_click=save)],
    ),
    ui.Toast("Saved", open=toast_open),
    ui.List(items=["Alpha", "Beta"]),
    ui.Table(columns=["name", "role"], rows=[{"name": "Ada", "role": "Eng"}, {"name": "Lin", "role": "Design"}]),
    ui.Empty(title="No results", subtitle="Try another filter"),
    ui.Spinner(text="Loading…"),
    ui.Alert("Heads up", severity="info"),
    ui.Text(label),
)
