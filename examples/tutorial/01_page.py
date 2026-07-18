from ourui import ui

page = ui.Page(
    ui.Hero(title="Hello OurUI", subtitle="Your first page"),
    ui.Section(title="Next", children=[ui.Text("Open docs/user/tutorial/02-components.md")]),
)
