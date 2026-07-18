"""Site header — Quiet compiler chrome (svelte.dev-style).

OurUI analyzes the serve entry (``app.py``) only. Keep ``site_header`` in
``app.py`` in sync with this module when editing the nav.
"""

from ourui import ui


def site_header():
    return ui.Nav(
        brand=ui.Link("OurUI", href="/"),
        items=[
            ui.Link(
                "Docs",
                href="https://github.com/sukirman1901/OurUI/tree/main/docs/user",
            ),
            ui.Link(
                "Tutorial",
                href="https://github.com/sukirman1901/OurUI/tree/main/docs/user/tutorial",
            ),
            ui.Link(
                "Examples",
                href="https://github.com/sukirman1901/OurUI/tree/main/examples",
            ),
        ],
        actions=[
            ui.ThemeToggle("Theme"),
            ui.Link("GitHub", href="https://github.com/sukirman1901/OurUI"),
            ui.Link(
                "Get started",
                href="https://github.com/sukirman1901/OurUI/blob/main/docs/user/getting-started.md",
                color="primary",
            ),
        ],
        placement="sticky-top",
        tone="glass",
        menu="drawer",
    )
