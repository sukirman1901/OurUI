"""Minimal OurUI hello — the playground Source pane + Result mirror this file."""

from ourui import State, server, ui

name = State("world")
count = State(0)


@server
def bump():
    count.set(count.get() + 1)
    return {"count": count.get()}


page = ui.Page(
    ui.Hero(
        title="Hello",
        subtitle="Say hi, then count clicks — emitted host UI, not markup soup.",
        cta=ui.Button("Click me", on_click=bump),
    ),
    ui.Input(name="name", label="Your name", bind=name),
    ui.Text("Greeting: Hello "),
    ui.Text(name),
    ui.Text(" — clicks: "),
    ui.Text(count),
)
