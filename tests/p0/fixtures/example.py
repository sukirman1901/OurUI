from ourui import server, ui


@server
def get_started() -> dict[str, str]:
    return {"message": "Welcome from OurUI server"}


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
        ],
    ),
)
