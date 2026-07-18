"""Plasma-shaped SaaS dogfood — Phase S1–S6 complete.

Language surface: Nav, tokens/theme, Footer, layout, motion, Canvas, Image/Icon/Meta/Code.
"""

from ourui import Component, State, server, ui

theme = ui.Theme(
    primary="#6C5CE7",
    primary_fg="#f5f3ff",
    accent="#9AD013",
    accent_fg="#0D0D0F",
    bg="#09090b",
    fg="#f4f4f5",
    muted="#27272a",
    muted_fg="#a1a1aa",
    card="#18181b",
    card_fg="#f4f4f5",
    border="#3f3f46",
    dark={
        "bg": "#09090b",
        "fg": "#f4f4f5",
        "primary": "#8b7cf7",
        "primary_fg": "#0b0a12",
        "accent": "#9AD013",
        "accent_fg": "#0D0D0F",
        "muted": "#27272a",
        "muted_fg": "#a1a1aa",
        "card": "#18181b",
        "card_fg": "#f4f4f5",
        "border": "#3f3f46",
    },
)

pace = State(40)
texture = State(55)
lens = State(30)
mode = State("gradient")
preset = State("ember")
share_id = State("")
export_snippet = State("Plasma.init('#canvas', { mode: 'gradient', pace: 40 })")


@server
def apply_playground(**payload: object) -> dict[str, int | str]:
    if "mode" in payload:
        mode.set(str(payload.get("mode", mode.get())))
    if "lens" in payload:
        try:
            lens.set(int(payload.get("lens", lens.get())))  # type: ignore[arg-type]
        except (TypeError, ValueError):
            pass
    return {"mode": mode.get(), "lens": lens.get(), "pace": pace.get()}


@server
def set_mode_gradient() -> str:
    mode.set("gradient")
    return mode.get()


@server
def set_mode_dither() -> str:
    mode.set("dither")
    return mode.get()


@server
def set_mode_raymarch() -> str:
    mode.set("raymarch")
    return mode.get()


@server
def pace_down() -> int:
    pace.set(max(0, pace.get() - 5))
    return pace.get()


@server
def pace_up() -> int:
    pace.set(min(100, pace.get() + 5))
    return pace.get()


@server
def texture_down() -> int:
    texture.set(max(0, texture.get() - 5))
    return texture.get()


@server
def texture_up() -> int:
    texture.set(min(100, texture.get() + 5))
    return texture.get()


@server
def lens_down() -> int:
    lens.set(max(0, lens.get() - 5))
    return lens.get()


@server
def lens_up() -> int:
    lens.set(min(100, lens.get() + 5))
    return lens.get()


@server
def pick_ember() -> str:
    preset.set("ember")
    return preset.get()


@server
def pick_ocean() -> str:
    preset.set("ocean")
    return preset.get()


@server
def pick_noir() -> str:
    preset.set("noir")
    return preset.get()


@server
def randomize() -> dict[str, int | str]:
    pace.set((pace.get() + 17) % 101)
    texture.set((texture.get() + 23) % 101)
    lens.set((lens.get() + 11) % 101)
    return {"pace": pace.get(), "texture": texture.get(), "lens": lens.get(), "mode": mode.get()}


@server
def reset_filters() -> dict[str, int | str]:
    pace.set(40)
    texture.set(55)
    lens.set(30)
    mode.set("gradient")
    preset.set("ember")
    return {
        "pace": pace.get(),
        "texture": texture.get(),
        "lens": lens.get(),
        "mode": mode.get(),
        "preset": preset.get(),
    }


@server
def fake_save() -> str:
    share_id.set("demo-local-only")
    export_snippet.set(
        f"Plasma.init('#canvas', {{ mode: '{mode.get()}', "
        f"pace: {pace.get()}, texture: {texture.get()}, lens: {lens.get()}, preset: '{preset.get()}' }})"
    )
    return share_id.get()


@server
def fake_copy() -> str:
    return export_snippet.get()


def FeatureCard(title: str, body: str):
    return ui.Card(title, children=[ui.Text(body)], motion="enter")


def FaqItem(q: str, a: str):
    return ui.Card(q, children=[ui.Text(a)])


class FilterRow(Component):
    def __init__(self, label: str, value: State, down, up):
        self.label = label
        self.value = value
        self.down = down
        self.up = up

    def build(self):
        return ui.Section(
            title=self.label,
            layout="stack",
            gap="sm",
            children=[
                ui.Text(self.value),
                ui.Button("−", color="muted", on_click=self.down, motion="press"),
                ui.Button("+", color="muted", on_click=self.up, motion="press"),
            ],
        )


class StudioFilters(Component):
    def build(self):
        return ui.Section(
            title="Filters",
            layout="stack",
            gap="md",
            pad="md",
            children=[
                FilterRow("Pace", pace, pace_down, pace_up),
                FilterRow("Texture", texture, texture_down, texture_up),
                FilterRow("Lens", lens, lens_down, lens_up),
            ],
        )


class StudioPreview(Component):
    def build(self):
        return ui.Section(
            title="Preview canvas",
            layout="stack",
            gap="md",
            pad="md",
            children=[
                ui.Canvas(mode="gradient", config={"pace": 40, "lens": 30, "texture": 55}),
                ui.Text("Mode: "),
                ui.Text(mode),
                ui.Text(" · Preset: "),
                ui.Text(preset),
                ui.Button("Randomize", color="accent", on_click=randomize, motion="press"),
                ui.Button("Reset", color="muted", on_click=reset_filters),
            ],
        )


class StudioStyle(Component):
    def build(self):
        return ui.Section(
            title="Style",
            layout="stack",
            gap="sm",
            pad="md",
            children=[
                ui.Button("Ember", color="primary", on_click=pick_ember),
                ui.Button("Ocean", color="primary", on_click=pick_ocean),
                ui.Button("Noir", color="primary", on_click=pick_noir),
                ui.Button("Fake save", color="accent", on_click=fake_save),
                ui.Code(export_snippet, language="javascript"),
                ui.CopyButton("Copy export", copy="Plasma.init('#canvas', { mode: 'gradient' })", color="muted"),
                ui.Text("Share id: "),
                ui.Text(share_id),
            ],
        )


landing = ui.Page(
    ui.Meta(
        title="Plasma — OurUI",
        description="Developer writes intent. Compiler writes implementation.",
        og={"title": "Plasma", "description": "OurUI Plasma-shaped demo"},
    ),
    ui.Nav(
        brand=ui.Link("Plasma", href="/"),
        items=[
            ui.Link("Features", href="#features"),
            ui.Link("Playground", href="#playground"),
            ui.Link("FAQ", href="#faq"),
        ],
        actions=[
            ui.ThemeToggle(ui.Icon("moon")),
            ui.Menu(
                "More",
                items=[
                    ui.Link("Embed", href="/embed"),
                    ui.Link("Studio", href="/app"),
                ],
            ),
            ui.Link("Open Studio", href="/app", color="primary"),
        ],
        placement="sticky-top",
        tone="glass",
        menu="drawer",
    ),
    ui.Hero(
        title="Plasma",
        subtitle="Developer writes intent. Compiler writes implementation. Host receives primitives.",
        pad="2xl",
        motion="enter",
        children=[
            ui.Canvas(mode="gradient", reduced_motion="static", config={"pace": 40, "lens": 30}),
            ui.Link("Open Studio", href="/app", color="primary"),
        ],
    ),
    ui.Section(
        title="Why Plasma",
        pad="xl",
        motion="reveal",
        gap="lg",
        children=[
            ui.Grid(
                children=[
                    FeatureCard("Live tune", "ui.Canvas WebGL escape — Gradient / Dither / Raymarch"),
                    FeatureCard("Copy shader", "ui.Code + ui.CopyButton clipboard"),
                    FeatureCard("Theme", "Type / space / elevation tokens + ThemeToggle"),
                    FeatureCard("Shell", "gap / pad / align + split-sidebar / split-3"),
                ],
            ),
        ],
    ),
    ui.Section(
        title="Playground",
        layout="stack",
        pad="xl",
        gap="md",
        children=[
            FilterRow("Pace", pace, pace_down, pace_up),
            FilterRow("Texture", texture, texture_down, texture_up),
            ui.Slider(name="lens", min=0, max=100, step=5, label="Lens", bind=lens),
            ui.Select(
                name="mode",
                options=["gradient", "dither", "raymarch"],
                label="Mode",
                bind=mode,
            ),
            ui.Button("Apply", color="primary", on_click=apply_playground, motion="press"),
        ],
    ),
    ui.Section(
        title="FAQ",
        pad="xl",
        children=[
            FaqItem("Can I click to Studio now?", "Yes — ui.Link href=/app (Phase S1)."),
            FaqItem("Where is WebGL?", "Shipped — ui.Canvas Plasma escape (S5)."),
        ],
    ),
    ui.Footer(
        brand=ui.Text("Plasma"),
        links=[
            ui.Link("Studio", href="/app"),
            ui.Link("Embed", href="/embed"),
        ],
        meta=[ui.Text("Built with OurUI 0.4")],
    ),
    route="/",
)

studio = ui.Page(
    ui.Meta(title="Plasma Studio", description="Tune shaders with OurUI intent"),
    ui.Nav(
        brand=ui.Link("Plasma Studio", href="/app"),
        items=[ui.Link("Landing", href="/")],
        actions=[ui.ThemeToggle("Theme")],
        placement="sticky-top",
        tone="solid",
        menu="drawer",
    ),
    ui.Section(
        title="Plasma Studio",
        layout="stack",
        gap="md",
        pad="md",
        children=[
            ui.Button("Gradient", color="primary", on_click=set_mode_gradient, motion="press"),
            ui.Button("Dither", color="muted", on_click=set_mode_dither),
            ui.Button("Raymarch", color="muted", on_click=set_mode_raymarch),
            ui.Text("Mode: "),
            ui.Text(mode),
        ],
    ),
    ui.Shell(
        StudioFilters(),
        StudioPreview(),
        StudioStyle(),
        layout="split-3",
        gap="lg",
        align="start",
    ),
    route="/app",
)

embed = ui.Page(
    ui.Meta(title="Embed", description="Shared Plasma view"),
    ui.Hero(
        title="Embed",
        subtitle="Canvas host escape for shared views.",
        pad="xl",
        children=[
            ui.Canvas(mode="dither", config={"pace": 55, "texture": 70}),
        ],
    ),
    ui.Section(
        layout="stack",
        gap="md",
        children=[
            ui.Link("← Studio", href="/app"),
            ui.Link("← Landing", href="/"),
            ui.Text("Share id: "),
            ui.Text(share_id),
        ],
    ),
    route="/embed",
)
