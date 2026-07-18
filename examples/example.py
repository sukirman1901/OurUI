from ourui import server, ui


@server
def get_started() -> None:
    """Server handler stub — wired via JS shim in Phase F."""
    return None


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
