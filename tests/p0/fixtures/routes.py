from ourui import ui

home = ui.Page(
    ui.Hero(title="Home", subtitle="Welcome home"),
    route="/",
)

about = ui.Page(
    ui.Section(title="About", subtitle="Learn more about OurUI"),
    route="/about",
)
