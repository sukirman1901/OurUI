from ourui import ui

theme = ui.Theme(primary="#1a5f4a", primary_fg="#f5faf8")

page = ui.Page(
    ui.Hero(title="Themed"),
    ui.Button("Primary", color="primary"),
)
