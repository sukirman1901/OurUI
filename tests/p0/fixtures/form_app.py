from ourui import State, server, ui

email = State("")
saved = State("")

theme = ui.Theme(primary="#1a5f4a", primary_fg="#f5faf8")


@server
def save_email(**payload: object) -> str:
    value = str(payload.get("email", ""))
    email.set(value)
    saved.set(value)
    return value


page = ui.Page(
    ui.Section(
        ui.Input(
            name="email",
            type="email",
            placeholder="you@example.com",
            label="Email",
            bind=email,
        ),
        ui.Button("Save", color="primary", on_click=save_email),
        ui.Text(saved),
        layout="stack",
    ),
)
