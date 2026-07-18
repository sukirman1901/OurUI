"""Site header — Quiet compiler chrome.

OurUI analyzes the serve entry (``app.py``) only. Keep ``site_header`` in
``app.py`` in sync with this module when editing the nav.
"""

from ourui import ui

GET_STARTED = (
    "https://github.com/sukirman1901/OurUI/blob/main/docs/user/getting-started.md"
)
DOCS = "https://github.com/sukirman1901/OurUI/tree/main/docs/user"
TUTORIAL = "https://github.com/sukirman1901/OurUI/tree/main/docs/user/tutorial"
EXAMPLES = "https://github.com/sukirman1901/OurUI/tree/main/examples"
GITHUB = "https://github.com/sukirman1901/OurUI"


def site_header():
    return ui.Nav(
        brand=ui.Link("OurUI", href="/"),
        items=[
            ui.Link("Docs", href=DOCS),
            ui.Link("Tutorial", href=TUTORIAL),
            ui.Link("Examples", href=EXAMPLES),
        ],
        actions=[
            ui.ThemeToggle(),
            ui.Link("GitHub", href=GITHUB),
            ui.Link("Get started", href=GET_STARTED, color="primary"),
        ],
        placement="sticky-top",
        tone="glass",
        menu="drawer",
    )
