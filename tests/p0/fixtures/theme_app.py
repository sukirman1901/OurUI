from ourui import ui

theme = ui.Theme(
    primary="#112233",
    dark={"primary": "#aabbcc"},
)

page = ui.Page(
    ui.Hero(title="Themed"),
    ui.Button("Go", color="primary"),
)
