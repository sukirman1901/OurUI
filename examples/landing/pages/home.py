"""Home page shell — header + placeholder (phase 1).

OurUI analyzes the serve entry (``app.py``) only. Keep ``home_page`` in
``app.py`` in sync with this module when editing the page shell.
"""

from ourui import ui

from components.site_header import site_header


def home_page():
    return ui.Page(
        site_header(),
        ui.Section(
            title="Header preview",
            children=[
                ui.Text("Phase 1 — site header only. Hero comes next."),
            ],
        ),
    )
