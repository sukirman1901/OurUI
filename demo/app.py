"""Plasma-shaped SaaS dogfood — Phase S1: ui.Link + ui.Shell.

Uses the **local editable** OurUI package (S1 not on PyPI 0.1.1 yet).
Remaining gaps: WebGL, sliders, forms — see GAPS.md.
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
)

pace = State(40)
texture = State(55)
lens = State(30)
mode = State("gradient")
preset = State("ember")
share_id = State("")
export_snippet = State("// GAP: no code editor / clipboard UI yet")


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
        f"// would be WebGL export · mode={mode.get()} · "
        f"pace={pace.get()} texture={texture.get()} lens={lens.get()} preset={preset.get()}"
    )
    return share_id.get()


@server
def fake_copy() -> str:
    return export_snippet.get()


def FeatureCard(title: str, body: str):
    return ui.Card(title, children=[ui.Text(body)])


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
            children=[
                ui.Text(self.value),
                ui.Button("−", color="muted", on_click=self.down),
                ui.Button("+", color="muted", on_click=self.up),
                ui.Text("GAP S2: real Slider control"),
            ],
        )


class StudioFilters(Component):
    def build(self):
        return ui.Section(
            title="Filters",
            layout="stack",
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
            children=[
                ui.Card(
                    "WebGL placeholder",
                    children=[
                        ui.Text("GAP S5: ui.Canvas / Plasma engine"),
                        ui.Text("Mode: "),
                        ui.Text(mode),
                        ui.Text(" · Preset: "),
                        ui.Text(preset),
                    ],
                ),
                ui.Button("Randomize", color="accent", on_click=randomize),
                ui.Button("Reset", color="muted", on_click=reset_filters),
            ],
        )


class StudioStyle(Component):
    def build(self):
        return ui.Section(
            title="Style",
            layout="stack",
            children=[
                ui.Button("Ember", color="primary", on_click=pick_ember),
                ui.Button("Ocean", color="primary", on_click=pick_ocean),
                ui.Button("Noir", color="primary", on_click=pick_noir),
                ui.Button("Fake save", color="accent", on_click=fake_save),
                ui.Button("Show export", color="muted", on_click=fake_copy),
                ui.Text("Share id: "),
                ui.Text(share_id),
                ui.Text(export_snippet),
            ],
        )


landing = ui.Page(
    ui.Hero(
        title="Plasma",
        subtitle="OurUI reconstruction — S1 adds real Link + Shell layout.",
        cta=ui.Link("Open Studio", href="/app", color="primary"),
    ),
    ui.Section(
        title="Navigate",
        layout="stack",
        children=[
            ui.Link("Studio", href="/app"),
            ui.Link("Embed stub", href="/embed"),
            ui.Link("Plasma (real product)", href="https://plasma.nusaiba.dev/"),
        ],
    ),
    ui.Section(
        title="Why Plasma",
        children=[
            ui.Grid(
                children=[
                    FeatureCard("Live tune", "GAP S5: mini WebGL canvases"),
                    FeatureCard("Copy shader", "GAP S6: code / clipboard"),
                    FeatureCard("Share", "GAP: Redis API"),
                    FeatureCard("Shell", "S1: ui.Shell layout=split-3 on /app"),
                ],
            ),
        ],
    ),
    ui.Section(
        title="Playground",
        layout="stack",
        children=[
            FilterRow("Pace", pace, pace_down, pace_up),
            FilterRow("Texture", texture, texture_down, texture_up),
            ui.Text("GAP S2: color inputs + continuous sliders"),
        ],
    ),
    ui.Section(
        title="FAQ",
        children=[
            FaqItem("Can I click to Studio now?", "Yes — ui.Link href=/app (Phase S1)."),
            FaqItem("Where is WebGL?", "Still GAP S5 — Canvas escape not shipped."),
        ],
    ),
    ui.Section(
        title="CTA",
        children=[
            ui.Card(
                "Try Studio",
                children=[
                    ui.Link("Open Studio", href="/app", color="primary"),
                    ui.Text("Footer links still thin — Image/Icon/Meta = S6."),
                ],
            ),
        ],
    ),
    route="/",
)

studio = ui.Page(
    ui.Section(
        title="Plasma Studio",
        layout="stack",
        children=[
            ui.Link("← Landing", href="/"),
            ui.Button("Gradient", color="primary", on_click=set_mode_gradient),
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
    ),
    route="/app",
)

embed = ui.Page(
    ui.Hero(title="Embed", subtitle="Stub — query ?id= and Canvas still missing."),
    ui.Section(
        layout="stack",
        children=[
            ui.Link("← Studio", href="/app"),
            ui.Link("← Landing", href="/"),
            ui.Text("Share id: "),
            ui.Text(share_id),
        ],
    ),
    route="/embed",
)
