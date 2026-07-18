"""Motion vocabulary demo — M1 + M2 patterns."""

from ourui import ui

theme = ui.Theme(recipe="product")

page = ui.Page(
    ui.Hero(
        title="Motion vocabulary",
        subtitle="ADR-012 M1 + M2",
        motion="hero.stagger-copy",
    ),
    ui.Section(
        title="Reveals",
        motion="reveal.split",
        children=[
            ui.Text("Word by word reveal", motion="text.word-reveal"),
            ui.Text("Marquee headline strip", motion="text.marquee"),
        ],
    ),
    ui.Section(
        title="Scroll",
        motion="scroll.fade-in-view",
        children=[ui.Text("Fades in when visible")],
    ),
    ui.Section(
        title="Partners",
        motion="flow.logo-marquee",
        children=[
            ui.Text("Alpha"),
            ui.Text("Beta"),
            ui.Text("Gamma"),
        ],
    ),
    ui.Button("Press me", color="primary", motion="press"),
)
