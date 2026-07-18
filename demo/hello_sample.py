"""Minimal OurUI hello — the playground Source pane + Result mirror this file."""

from ourui import State, server, ui

name = State("world")
count = State(0)


@server
def bump():
    count.set(count.get() + 1)
    return {"count": count.get()}


page = ui.Page(
    ui.Text("Hello "),
    ui.Text(name),
    ui.Text("!"),
    ui.Input(name="name", bind=name),
    ui.Button("clicks", on_click=bump),
    ui.Text("clicks: "),
    ui.Text(count),
)
