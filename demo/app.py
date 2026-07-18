"""OurUI Playground — editable compiler REPL.

Write OurUI intent in the left textarea → Run → Result (iframe) + HTML / JS / CSS / AST.
"""

from __future__ import annotations

import sys
import tempfile
import traceback
from pathlib import Path

# Serve loads this file via importlib; ensure sibling artifacts import resolves.
_DEMO_DIR = Path(__file__).resolve().parent
if str(_DEMO_DIR) not in sys.path:
    sys.path.insert(0, str(_DEMO_DIR))

from ourui import Component, State, server, ui
from ourui.pipeline import dump_json, emit_all
from playground_artifacts import AST_OUT, CSS_OUT, HTML_OUT, JS_OUT, SAMPLE_SOURCE

# CUSTOM — light IDE chrome (zinc / ink / teal Run)
theme = ui.Theme(
    bg="#f4f4f5",
    fg="#18181b",
    primary="#18181b",
    primary_fg="#fafafa",
    muted="#e4e4e7",
    muted_fg="#71717a",
    border="#e4e4e7",
    card="#ffffff",
    card_fg="#18181b",
    accent="#0f766e",
    accent_fg="#f0fdfa",
    danger="#b91c1c",
    danger_fg="#fef2f2",
    radius="0.375rem",
    space_xs="0.25rem",
    space_sm="0.5rem",
    space_md="0.75rem",
    space_lg="1rem",
    space_xl="1.5rem",
    font_sans='"DM Sans", "Segoe UI", system-ui, sans-serif',
    font_display='"DM Sans", "Segoe UI", system-ui, sans-serif',
    elev_0="none",
    elev_1="none",
    elev_2="0 4px 12px color-mix(in srgb, #18181b 8%, transparent)",
    dark={
        "bg": "#09090b",
        "fg": "#fafafa",
        "primary": "#fafafa",
        "primary_fg": "#18181b",
        "muted": "#27272a",
        "muted_fg": "#a1a1aa",
        "border": "#27272a",
        "card": "#0c0c0e",
        "card_fg": "#fafafa",
        "accent": "#2dd4bf",
        "accent_fg": "#042f2e",
    },
)

# Editable source + live compile artifacts (seeded from baked hello_sample)
source_code = State(SAMPLE_SOURCE)
preview_html = State(HTML_OUT)
html_art = State(HTML_OUT)
js_art = State(JS_OUT)
css_art = State(CSS_OUT)
ast_art = State(AST_OUT)
console_log = State("Ready · edit source → Run to compile")


def _compile_source(src: str) -> tuple[dict[str, str], str]:
    path = Path(tempfile.mkdtemp(prefix="ourui_pg_")) / "user.py"
    path.write_text(src, encoding="utf-8")
    bundle = emit_all(path, title="Result")
    return bundle, dump_json(path)


@server
def run_playground(**payload: object) -> str:
    raw = payload.get("source", source_code.get())
    src = "" if raw is None else str(raw)
    source_code.set(src)
    if not src.strip():
        console_log.set("error · empty source")
        return console_log.get()
    try:
        bundle, dump = _compile_source(src)
        preview_html.set(bundle["html"])
        html_art.set(bundle["html"])
        js_art.set(bundle["js"])
        css_art.set(bundle["css"])
        ast_art.set(dump)
        console_log.set(f"ok · compiled {len(src)} chars → HTML/JS/CSS/AST")
    except Exception as exc:  # noqa: BLE001 — surface compile errors in console
        console_log.set(f"error · {exc}\n{traceback.format_exc(limit=3)}")
    return console_log.get()


@server
def clear_console() -> str:
    console_log.set("")
    return console_log.get()


@server
def reset_sample() -> str:
    source_code.set(SAMPLE_SOURCE)
    preview_html.set(HTML_OUT)
    html_art.set(HTML_OUT)
    js_art.set(JS_OUT)
    css_art.set(CSS_OUT)
    ast_art.set(AST_OUT)
    console_log.set("reset · hello_sample seed")
    return console_log.get()


@server
def fake_save() -> str:
    console_log.set("saved · source (session State)")
    return console_log.get()


class TopChrome(Component):
    def build(self):
        return ui.Nav(
            brand=ui.Link("OurUI", href="/"),
            items=[ui.Text("Playground")],
            actions=[
                ui.Button("Run", color="accent", on_click=run_playground, motion="press"),
                ui.Button("Reset", color="muted", on_click=reset_sample, motion="press"),
                ui.ThemeToggle(ui.Icon("moon")),
                ui.Menu(
                    "Account",
                    items=[
                        ui.Link("About", href="/about"),
                        ui.Link(
                            "Docs",
                            href="https://github.com/sukirman1901/OurUI/tree/main/docs/user",
                        ),
                        ui.Button("Save", color="muted", on_click=fake_save),
                    ],
                ),
            ],
            placement="sticky-top",
            tone="solid",
            menu="drawer",
        )


class SourcePane(Component):
    def build(self):
        return ui.Section(
            layout="stack",
            gap="none",
            pad="none",
            children=[
                ui.Section(
                    layout="row",
                    gap="sm",
                    align="center",
                    chrome="file-tabs",
                    children=[
                        ui.Text("app.py", chrome="file-tab"),
                        ui.Text("+"),
                    ],
                ),
                ui.Input(
                    "source",
                    type="textarea",
                    bind=source_code,
                    placeholder="from ourui import State, server, ui\n...",
                ),
            ],
        )


def OutputTabsResult():
    return ui.Section(
        layout="row",
        gap="md",
        align="center",
        pad="sm",
        chrome="tabs",
        children=[
            ui.Link("Result", href="/", color="primary"),
            ui.Link("HTML", href="/html", color="muted"),
            ui.Link("JS", href="/js", color="muted"),
            ui.Link("CSS", href="/css", color="muted"),
            ui.Link("AST", href="/ast", color="muted"),
        ],
    )


def OutputTabsHtml():
    return ui.Section(
        layout="row",
        gap="md",
        align="center",
        pad="sm",
        chrome="tabs",
        children=[
            ui.Link("Result", href="/", color="muted"),
            ui.Link("HTML", href="/html", color="primary"),
            ui.Link("JS", href="/js", color="muted"),
            ui.Link("CSS", href="/css", color="muted"),
            ui.Link("AST", href="/ast", color="muted"),
        ],
    )


def OutputTabsJs():
    return ui.Section(
        layout="row",
        gap="md",
        align="center",
        pad="sm",
        chrome="tabs",
        children=[
            ui.Link("Result", href="/", color="muted"),
            ui.Link("HTML", href="/html", color="muted"),
            ui.Link("JS", href="/js", color="primary"),
            ui.Link("CSS", href="/css", color="muted"),
            ui.Link("AST", href="/ast", color="muted"),
        ],
    )


def OutputTabsCss():
    return ui.Section(
        layout="row",
        gap="md",
        align="center",
        pad="sm",
        chrome="tabs",
        children=[
            ui.Link("Result", href="/", color="muted"),
            ui.Link("HTML", href="/html", color="muted"),
            ui.Link("JS", href="/js", color="muted"),
            ui.Link("CSS", href="/css", color="primary"),
            ui.Link("AST", href="/ast", color="muted"),
        ],
    )


def OutputTabsAst():
    return ui.Section(
        layout="row",
        gap="md",
        align="center",
        pad="sm",
        chrome="tabs",
        children=[
            ui.Link("Result", href="/", color="muted"),
            ui.Link("HTML", href="/html", color="muted"),
            ui.Link("JS", href="/js", color="muted"),
            ui.Link("CSS", href="/css", color="muted"),
            ui.Link("AST", href="/ast", color="primary"),
        ],
    )


class ConsoleBar(Component):
    def build(self):
        return ui.Section(
            layout="stack",
            gap="xs",
            pad="sm",
            children=[
                ui.Section(
                    layout="row",
                    gap="sm",
                    justify="between",
                    align="center",
                    children=[
                        ui.Text("CONSOLE"),
                        ui.Button("Clear", color="muted", on_click=clear_console, motion="press"),
                    ],
                ),
                ui.Code(console_log, language="text"),
            ],
        )


class ResultPreview(Component):
    def build(self):
        return ui.Frame(bind=preview_html, title="Result")


def ArtifactHtml():
    return ui.Section(
        layout="stack",
        gap="sm",
        pad="md",
        children=[ui.Code(html_art, language="html")],
    )


def ArtifactJs():
    return ui.Section(
        layout="stack",
        gap="sm",
        pad="md",
        children=[ui.Code(js_art, language="javascript")],
    )


def ArtifactCss():
    return ui.Section(
        layout="stack",
        gap="sm",
        pad="md",
        children=[ui.Code(css_art, language="css")],
    )


def ArtifactAst():
    return ui.Section(
        layout="stack",
        gap="sm",
        pad="md",
        children=[ui.Code(ast_art, language="json")],
    )


def ShellResult():
    return ui.Shell(
        SourcePane(),
        ui.Section(
            layout="stack",
            gap="none",
            pad="none",
            children=[OutputTabsResult(), ResultPreview(), ConsoleBar()],
        ),
        layout="split-2",
        gap="none",
        align="stretch",
    )


def ShellHtml():
    return ui.Shell(
        SourcePane(),
        ui.Section(
            layout="stack",
            gap="none",
            pad="none",
            children=[OutputTabsHtml(), ArtifactHtml(), ConsoleBar()],
        ),
        layout="split-2",
        gap="none",
        align="stretch",
    )


def ShellJs():
    return ui.Shell(
        SourcePane(),
        ui.Section(
            layout="stack",
            gap="none",
            pad="none",
            children=[OutputTabsJs(), ArtifactJs(), ConsoleBar()],
        ),
        layout="split-2",
        gap="none",
        align="stretch",
    )


def ShellCss():
    return ui.Shell(
        SourcePane(),
        ui.Section(
            layout="stack",
            gap="none",
            pad="none",
            children=[OutputTabsCss(), ArtifactCss(), ConsoleBar()],
        ),
        layout="split-2",
        gap="none",
        align="stretch",
    )


def ShellAst():
    return ui.Shell(
        SourcePane(),
        ui.Section(
            layout="stack",
            gap="none",
            pad="none",
            children=[OutputTabsAst(), ArtifactAst(), ConsoleBar()],
        ),
        layout="split-2",
        gap="none",
        align="stretch",
    )


playground = ui.Page(
    ui.Meta(
        title="OurUI Playground",
        description="Edit OurUI intent → Run → Result / HTML / JS / CSS / AST.",
        og={"title": "OurUI Playground"},
    ),
    TopChrome(),
    ShellResult(),
    route="/",
)

html_out = ui.Page(
    ui.Meta(title="HTML — OurUI Playground"),
    TopChrome(),
    ShellHtml(),
    route="/html",
)

js_out = ui.Page(
    ui.Meta(title="JS — OurUI Playground"),
    TopChrome(),
    ShellJs(),
    route="/js",
)

css_out = ui.Page(
    ui.Meta(title="CSS — OurUI Playground"),
    TopChrome(),
    ShellCss(),
    route="/css",
)

ast_out = ui.Page(
    ui.Meta(title="AST — OurUI Playground"),
    TopChrome(),
    ShellAst(),
    route="/ast",
)

about = ui.Page(
    ui.Meta(title="About — OurUI Playground"),
    ui.Nav(
        brand=ui.Link("OurUI", href="/"),
        items=[ui.Link("Playground", href="/")],
        actions=[ui.ThemeToggle(ui.Icon("sun"))],
        placement="sticky-top",
        tone="solid",
        menu="drawer",
    ),
    ui.Hero(
        title="OurUI Playground",
        subtitle="Editable compiler REPL: write intent → Run → Result iframe + HTML / JS / CSS / AST.",
        pad="xl",
        motion="enter",
    ),
    ui.Section(
        pad="lg",
        children=[
            ui.Link("Open playground", href="/", color="primary"),
        ],
    ),
    route="/about",
)
