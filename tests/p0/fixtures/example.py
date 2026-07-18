from ourui import State, server, ui

count = State(0)


@server
def get_started() -> dict[str, str]:
    return {"message": "Welcome from OurUI server"}


@server
def increment() -> int:
    count.set(count.get() + 1)
    return count.get()


page = ui.Page(
    ui.Hero(
        title="Welcome",
        subtitle="Build SaaS in Python",
        cta=ui.Button("Get Started", variant="primary", on_click=get_started),
    ),
    ui.Section(
        title="Features",
        children=[
            ui.Card("Analysis"),
            ui.Card("Realtime"),
            ui.Text(count),
            ui.Button("+1", on_click=increment),
        ],
    ),
)
