from ourui import State, server, ui

email = State("")
theme = State("light")
enabled = State(True)
volume = State(40)
summary = State("")

tokens = ui.Theme(primary="#1a5f4a", primary_fg="#f5faf8")


@server
def save_form(**payload: object) -> str:
    email.set(str(payload.get("email", "")))
    theme.set(str(payload.get("theme", "")))
    enabled.set(bool(payload.get("enabled")))
    raw_vol = payload.get("volume", 0)
    try:
        volume.set(int(raw_vol))  # type: ignore[arg-type]
    except (TypeError, ValueError):
        volume.set(0)
    text = f"{email.get()}|{theme.get()}|{enabled.get()}|{volume.get()}"
    summary.set(text)
    return text


page = ui.Page(
    ui.Section(
        ui.Input(
            name="email",
            type="email",
            placeholder="you@example.com",
            label="Email",
            bind=email,
        ),
        ui.Select(
            name="theme",
            options=["light", "dark"],
            label="Theme",
            bind=theme,
        ),
        ui.Toggle(name="enabled", label="Enabled", bind=enabled),
        ui.Slider(name="volume", min=0, max=100, step=5, label="Volume", bind=volume),
        ui.Button("Save", color="primary", on_click=save_form),
        ui.Text(summary),
        layout="stack",
    ),
)
