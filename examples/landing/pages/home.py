"""Home page — marketing section stack (mirror of ``app.py`` helpers).

OurUI analyzes the serve entry (``app.py``) only. Keep this module aligned when
editing the landing composition.
"""

from ourui import ui

from components.site_header import site_header

GET_STARTED = (
    "https://github.com/sukirman1901/OurUI/blob/main/docs/user/getting-started.md"
)
DOCS = "https://github.com/sukirman1901/OurUI/tree/main/docs/user"
TUTORIAL = "https://github.com/sukirman1901/OurUI/tree/main/docs/user/tutorial"
GITHUB = "https://github.com/sukirman1901/OurUI"
PYPI = "https://pypi.org/project/ourui/"

HERO_SNIPPET = """from ourui import ui

theme = ui.Theme(page={"max_width": "none", "pad_block": "0", "pad_inline": "0", "gap": "space_xl"})

page = ui.Page(
    ui.Nav(brand=ui.Link("OurUI", href="/"), ...),
    ui.Hero(
        title="OurUI",
        subtitle="Developer writes intent.",
    ),
)
"""


def home_page():
    return ui.Page(
        ui.Meta(
            title="OurUI — intent in Python, primitives in the host",
            description=(
                "Python-first UI language: write intent, compile to HTML/CSS/JS. "
                "pip install ourui."
            ),
            og={
                "title": "OurUI",
                "description": "Developer writes intent. Compiler writes implementation.",
            },
        ),
        site_header(),
        ui.Hero(
            title="OurUI",
            subtitle=(
                "Developer writes intent. Compiler writes implementation. "
                "Host receives primitives."
            ),
            pad="xl",
            motion="hero.stagger-copy",
            cta=ui.Shell(
                ui.Link("Get started", href=GET_STARTED, color="primary"),
                ui.Link("pip install ourui", href=PYPI),
                layout="row",
                gap="4",
                wrap="wrap",
            ),
            children=[ui.Code(HERO_SNIPPET, language="python")],
        ),
        ui.Section(
            title="Ships where Python already is",
            subtitle="Install from PyPI. Author in one file. Inspect every IR stage.",
            pad="xl",
            gap="6",
            align="center",
            motion="reveal.fade-up",
            children=[
                ui.Shell(
                    ui.Link("PyPI · ourui", href=PYPI),
                    ui.Link("GitHub", href=GITHUB),
                    ui.Text("Python 3.11+"),
                    ui.Text("MIT"),
                    layout="row",
                    gap="8",
                    wrap="wrap",
                    justify="center",
                    align="center",
                ),
            ],
        ),
        ui.Section(
            title="One vocabulary from source to host",
            subtitle="Not a React clone in Python — intent props, finite emit, explicit escape.",
            pad="xl",
            gap="8",
            motion="reveal.fade-up",
            children=[
                ui.Shell(
                    ui.Section(
                        title="Intent",
                        children=[
                            ui.Text(
                                "Page, Nav, Hero, width=, gap=, color=, motion= — "
                                "say what you mean in Python."
                            ),
                        ],
                        pad="6",
                        grow="1",
                    ),
                    ui.Section(
                        title="Compiler",
                        children=[
                            ui.Text(
                                "AST → semantic graph → Resolved Design → HTML/CSS/JS. "
                                "Dump every stage; no hidden runtime UI framework."
                            ),
                        ],
                        pad="6",
                        grow="1",
                    ),
                    ui.Section(
                        title="Host",
                        children=[
                            ui.Text(
                                "Browser gets primitives and tokens. Canvas and Frame "
                                "stay escape hatches — not the default authoring path."
                            ),
                        ],
                        pad="6",
                        grow="1",
                    ),
                    layout="row",
                    gap="4",
                    wrap="wrap",
                    align="stretch",
                ),
            ],
        ),
        ui.Section(
            title="Compose with style intents",
            subtitle="Intent props → compiled CSS — width=, pad_x=, grid_cols=, grow=.",
            pad="xl",
            gap="6",
            motion="reveal.fade-up",
            children=[
                ui.Code(
                    """ui.Shell(
    ui.Section(title="Filters", width="xs"),
    ui.Section(title="Preview", grow="1"),
    ui.Section(title="Style", width="sm"),
    layout="split-3",
    gap="4",
    pad_x="6",
)""",
                    language="python",
                ),
                ui.Shell(
                    ui.Link("Style intents", href=f"{DOCS}/reference/style-intents.md"),
                    ui.Link(
                        "Language vs kit",
                        href=f"{GITHUB}/blob/main/docs/decisions/ADR-014-language-primitives-vs-kit.md",
                    ),
                    layout="row",
                    gap="4",
                    wrap="wrap",
                ),
            ],
        ),
        ui.Section(
            title="Start with intent",
            subtitle="pip install ourui — then serve a single Python module.",
            pad="xl",
            gap="6",
            align="center",
            motion="reveal.fade-up",
            children=[
                ui.Shell(
                    ui.Link("Get started", href=GET_STARTED, color="primary"),
                    ui.Link("Read the tutorial", href=TUTORIAL),
                    layout="row",
                    gap="4",
                    wrap="wrap",
                    justify="center",
                ),
                ui.Code("pip install ourui\nourui serve app.py", language="bash"),
            ],
        ),
        ui.Footer(
            brand=ui.Link("OurUI", href="/"),
            links=[
                ui.Link("Docs", href=DOCS),
                ui.Link("PyPI", href=PYPI),
                ui.Link("GitHub", href=GITHUB),
            ],
            meta=[ui.Text("Language primitives. Kit stays out.")],
        ),
    )
