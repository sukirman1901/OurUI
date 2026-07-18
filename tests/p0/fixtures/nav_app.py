from ourui import ui

theme = ui.Theme(primary="#1a5f4a", primary_fg="#f5faf8")

page = ui.Page(
    ui.Nav(
        brand=ui.Link("OurUI", href="/"),
        items=[
            ui.Link("Features", href="#features"),
            ui.Link("Docs", href="#docs"),
        ],
        actions=[
            ui.Link("Open Studio", href="/app", color="primary"),
        ],
        placement="sticky-top",
        tone="glass",
    ),
    ui.Hero(title="Chrome", subtitle="S3a Nav"),
    ui.Section(title="Features", children=[ui.Text("Body")]),
)
