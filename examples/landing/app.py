"""OurUI marketing landing — phase 1 (site header).

Entry for ``ourui serve`` / ``dump`` / ``emit``. OurUI compiles this file's AST
only, so ``site_header`` / ``home_page`` are defined here. Mirror modules live
under ``components/`` and ``pages/`` for folder structure (keep in sync).
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


theme = ui.Theme(recipe="marketing")
page = home_page()
