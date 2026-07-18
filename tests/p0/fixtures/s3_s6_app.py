from ourui import ui

theme = ui.Theme(primary="#1a5f4a", primary_fg="#f5faf8")

page = ui.Page(
    ui.Meta(
        title="OurUI S3-S6",
        description="Phase S tokens through polish",
        og={"title": "OurUI", "description": "Semantic UI"},
    ),
    ui.Nav(
        brand=ui.Link("OurUI", href="/"),
        items=[
            ui.Link("Docs", href="#docs"),
            ui.Link("Studio", href="/app"),
        ],
        actions=[
            ui.ThemeToggle("Theme"),
            ui.Menu(
                "More",
                items=[
                    ui.Link("Embed", href="/embed"),
                ],
            ),
        ],
        placement="sticky-top",
        tone="glass",
        menu="drawer",
    ),
    ui.Hero(
        title="Tokens to Canvas",
        subtitle="S3–S6 surface",
        pad="xl",
        motion="enter",
        children=[
            ui.Canvas(mode="gradient", reduced_motion="static"),
        ],
    ),
    ui.Shell(
        ui.Section(
            title="Sidebar",
            pad="md",
            children=[ui.Text("Nav pane")],
        ),
        ui.Section(
            title="Main",
            gap="lg",
            align="center",
            motion="reveal",
            children=[
                ui.Image(src="/static/logo.svg", alt="Logo", fit="contain"),
                ui.Icon("sun"),
                ui.Code("print('ourui')", language="python"),
                ui.CopyButton("Copy", copy="print('ourui')", color="primary"),
                ui.Input(name="email", label="Email", invalid=True),
            ],
        ),
        layout="split-sidebar",
        gap="lg",
    ),
    ui.Footer(
        brand=ui.Text("OurUI"),
        links=[ui.Link("Docs", href="#docs")],
        meta=[ui.Text("© 2026")],
    ),
)
