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
