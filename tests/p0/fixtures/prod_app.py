from ourui import State, server, ui

count = State(0)


@server
def increment() -> int:
    count.set(count.get() + 1)
    return count.get()


@server
def boom() -> None:
    raise RuntimeError("intentional failure")


page = ui.Page(
    ui.Hero(title="Prod", subtitle="session"),
    ui.Text(count),
    ui.Button("+1", on_click=increment),
)
