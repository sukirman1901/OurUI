"""Minimal red (danger) button demo."""

from ourui import ui

page = ui.Page(
    ui.Hero(
        title="Button demo",
        subtitle="color=\"danger\" — semantic red tone from ourui-default.",
    ),
    ui.Button("Hello World", color="danger"),
)
