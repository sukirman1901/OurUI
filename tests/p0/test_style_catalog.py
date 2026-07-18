"""Style Intent Catalog (ADR-013) — scales, utilities, passthrough."""

from __future__ import annotations

from pathlib import Path

import pytest

from ourui.design.scales import emit_scale_css_vars
from ourui.design.style_catalog import assert_catalog_complete, catalog_summary
from ourui.design.style_intents import emit_utility_css, style_intent_classes
from ourui.pipeline import compile_dump, emit_html

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def _emit(tmp_path: Path, source: str) -> str:
    src = tmp_path / "app.py"
    src.write_text(source, encoding="utf-8")
    return emit_html(src, title="style")


def test_catalog_matrix_complete() -> None:
    assert_catalog_complete()
    summary = catalog_summary()
    assert summary["entries"] >= 80
    assert summary["by_status"].get("A", 0) > 0
    assert summary["version"] == "1.11.0"
    by_tw = {r["tw"]: r for r in summary["items"]}
    assert by_tw["responsive"]["status"] == "A"
    assert by_tw["hover-focus-states"]["status"] == "A"
    assert by_tw["transition-animation"]["status"] == "AB"
    assert by_tw["ring"]["status"] == "A"
    assert by_tw["divide-x-y"]["status"] == "A"
    assert by_tw["space-x-y"]["status"] == "A"
    assert by_tw["bg-gradient"]["status"] == "A"
    assert by_tw["background-image"]["status"] == "A"
    assert by_tw["mix-blend"]["status"] == "A"
    assert by_tw["mask"]["status"] == "A"
    assert by_tw["content"]["status"] == "A"
    assert by_tw["container-queries"]["status"] == "A"
    assert by_tw["scroll-margin-padding"]["status"] == "A"
    assert by_tw["caret-color"]["status"] == "A"
    assert by_tw["sr-only"]["status"] == "A"
    assert by_tw["placeholder-selection"]["status"] == "A"
    assert by_tw["outline"]["status"] == "A"
    assert by_tw["accent-color"]["status"] == "A"
    assert by_tw["font-variant-numeric"]["status"] == "A"
    assert by_tw["font-stretch"]["status"] == "A"
    assert by_tw["font-feature-settings"]["status"] == "A"
    assert by_tw["appearance"]["status"] == "A"
    assert by_tw["text-indent"]["status"] == "A"
    assert by_tw["zoom"]["status"] == "A"
    assert summary["by_status"].get("C", 0) == 0


def test_responsive_dict_intents_and_emit(tmp_path: Path) -> None:
    classes = style_intent_classes(
        {
            "pad": {"base": "4", "md": "8", "lg": "12"},
            "width": {"md": "lg"},
            "gap": {"md": "6"},
            "grid_cols": {"base": 1, "md": 3},
            "direction": {"base": "col", "md": "row"},
            "grow": {"md": True},
            "text": {"base": "sm", "md": "lg"},
        }
    )
    assert "ourui-pad-4" in classes
    assert "ourui-md-pad-8" in classes
    assert "ourui-lg-pad-12" in classes
    assert "ourui-md-w-lg" in classes
    assert "ourui-md-gap-6" in classes
    assert "ourui-grid-cols-1" in classes
    assert "ourui-md-grid-cols-3" in classes
    assert "ourui-direction-col" in classes
    assert "ourui-md-direction-row" in classes
    assert "ourui-md-grow-1" in classes
    assert "ourui-text-sm" in classes
    assert "ourui-md-text-lg" in classes

    utils = emit_utility_css()
    assert "@media (min-width: 768px)" in utils
    assert ".ourui-md-pad-8 {" in utils
    assert ".ourui-lg-pad-12 {" in utils
    assert ".ourui-md-w-lg {" in utils
    assert ".ourui-md-direction-row {" in utils

    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(
    ui.Shell(
        ui.Text("R"),
        pad={"base": "4", "md": "8"},
        width={"md": "full"},
        grid_cols={"base": 1, "md": 2},
    )
)
""",
    )
    assert "ourui-pad-4" in html
    assert "ourui-md-pad-8" in html
    assert "ourui-md-w-full" in html
    assert "ourui-md-grid-cols-2" in html
    assert ".ourui-md-pad-8 {" in html


def test_ring_intent_classes_and_emit(tmp_path: Path) -> None:
    classes = style_intent_classes(
        {"ring": "2", "ring_color": "primary", "shadow": "md"}
    )
    assert "ourui-ring-2" in classes
    assert "ourui-ring-color-primary" in classes
    assert "ourui-shadow-md" in classes

    inset = style_intent_classes({"ring": True, "ring_inset": True})
    assert "ourui-ring-inset" in inset

    utils = emit_utility_css()
    assert ".ourui-ring-2 {" in utils
    assert "--ourui-ring-shadow:" in utils
    assert ".ourui-ring-color-primary {" in utils

    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(ui.Button("Go", ring="2", ring_color="accent"))
""",
    )
    assert "ourui-ring-2" in html
    assert "ourui-ring-color-accent" in html
    assert ".ourui-ring-2 {" in html


def test_l3_batch_intents_and_emit(tmp_path: Path) -> None:
    classes = style_intent_classes(
        {
            "scroll_m": "4",
            "scroll_pt": "8",
            "space_x": "4",
            "space_y": "2",
            "divide": "x",
            "divide_w": "2",
            "divide_color": "border",
            "sr_only": True,
            "caret": "primary",
            "bg_gradient": "to-r",
            "gradient_from": "primary",
            "gradient_to": "accent",
        }
    )
    assert "ourui-scroll-m-4" in classes
    assert "ourui-scroll-pt-8" in classes
    assert "ourui-space-x-4" in classes
    assert "ourui-space-y-2" in classes
    assert "ourui-divide-x" in classes
    assert "ourui-divide-w-2" in classes
    assert "ourui-divide-color-border" in classes
    assert "ourui-sr-only" in classes
    assert "ourui-caret-primary" in classes
    assert "ourui-bg-gradient-to-r" in classes
    assert "ourui-gradient-from-primary" in classes
    assert "ourui-gradient-to-accent" in classes

    utils = emit_utility_css()
    assert ".ourui-scroll-m-4 {" in utils
    assert "scroll-margin:" in utils
    assert ".ourui-space-x-4 >" in utils
    assert ".ourui-divide-x >" in utils
    assert ".ourui-sr-only {" in utils
    assert ".ourui-caret-primary {" in utils
    assert ".ourui-bg-gradient-to-r {" in utils
    assert "linear-gradient(to right," in utils

    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(
    ui.Shell(
        ui.Text("a"),
        ui.Text("b"),
        divide="y",
        divide_w="1",
        space_y="4",
        scroll_m="4",
        bg_gradient="to-b",
        gradient_from="primary",
        gradient_to="muted",
    ),
    ui.Label("Hidden", sr_only=True),
    ui.Input(placeholder="Name", caret_color="accent"),
)
""",
    )
    assert "ourui-divide-y" in html
    assert "ourui-space-y-4" in html
    assert "ourui-scroll-m-4" in html
    assert "ourui-bg-gradient-to-b" in html
    assert "ourui-sr-only" in html
    assert "ourui-caret-accent" in html
    assert ".ourui-divide-y >" in html


def test_l3_longtail_intents_and_emit(tmp_path: Path) -> None:
    classes = style_intent_classes(
        {
            "appearance": "none",
            "color_scheme": "dark",
            "field_sizing": "content",
            "scrollbar_width": "thin",
            "scrollbar_gutter": "stable",
            "scrollbar_color": "primary",
            "tab_size": "4",
            "text_indent": "4",
            "zoom": "110",
            "backface": "hidden",
        }
    )
    assert "ourui-appearance-none" in classes
    assert "ourui-color-scheme-dark" in classes
    assert "ourui-field-sizing-content" in classes
    assert "ourui-scrollbar-width-thin" in classes
    assert "ourui-scrollbar-gutter-stable" in classes
    assert "ourui-scrollbar-color-primary" in classes
    assert "ourui-tab-size-4" in classes
    assert "ourui-text-indent-4" in classes
    assert "ourui-zoom-110" in classes
    assert "ourui-backface-hidden" in classes

    utils = emit_utility_css()
    assert ".ourui-appearance-none {" in utils
    assert ".ourui-tab-size-4 {" in utils
    assert ".ourui-text-indent-4 {" in utils
    assert ".ourui-zoom-110 {" in utils

    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(
    ui.Input(placeholder="x", appearance="none", field_sizing="content"),
    ui.Code("print(1)", tab_size="4", scrollbar_width="thin"),
)
""",
    )
    assert "ourui-appearance-none" in html
    assert "ourui-tab-size-4" in html
    assert ".ourui-appearance-none {" in html


def test_hover_focus_intents_and_emit(tmp_path: Path) -> None:
    classes = style_intent_classes(
        {
            "opacity": {"base": "100", "hover": "80"},
            "shadow": {"hover": "lg"},
            "scale": {"hover": "105"},
            "decorate": {"hover": "underline"},
            "hover": {"bg": "muted", "ring": "2"},
            "focus": {"ring": True, "outline": "2"},
        }
    )
    assert "ourui-opacity-100" in classes
    assert "ourui-hover-opacity-80" in classes
    assert "ourui-hover-shadow-lg" in classes
    assert "ourui-hover-scale-105" in classes
    assert "ourui-hover-underline" in classes
    assert "ourui-hover-bg-muted" in classes
    assert "ourui-hover-ring-2" in classes
    assert "ourui-focus-ring" in classes
    assert "ourui-focus-outline-2" in classes

    utils = emit_utility_css()
    assert ".ourui-hover-opacity-80:hover {" in utils
    assert ".ourui-focus-ring:focus-visible {" in utils
    assert ".ourui-hover-bg-muted:hover {" in utils
    assert ".ourui-focus-outline-2:focus-visible {" in utils

    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(
    ui.Button("Go", opacity={"hover": "80"}, hover={"shadow": "md"}, focus={"ring": "2"})
)
""",
    )
    assert "ourui-hover-opacity-80" in html
    assert "ourui-hover-shadow-md" in html
    assert "ourui-focus-ring-2" in html
    assert ".ourui-hover-opacity-80:hover {" in html


def test_outline_accent_font_numeric(tmp_path: Path) -> None:
    classes = style_intent_classes(
        {
            "outline": "2",
            "outline_color": "primary",
            "outline_offset": "2",
            "accent_color": "accent",
            "font_numeric": "tabular",
        }
    )
    assert "ourui-outline-2" in classes
    assert "ourui-outline-color-primary" in classes
    assert "ourui-outline-offset-2" in classes
    assert "ourui-accent-color-accent" in classes
    assert "ourui-font-numeric-tabular" in classes

    none_cls = style_intent_classes({"outline": "none", "accent": "primary", "font_numeric": "slashed-zero"})
    assert "ourui-outline-none" in none_cls
    assert "ourui-accent-color-primary" in none_cls
    assert "ourui-font-numeric-slashed-zero" in none_cls

    utils = emit_utility_css()
    assert ".ourui-outline-2 {" in utils
    assert ".ourui-accent-color-accent {" in utils
    assert ".ourui-font-numeric-tabular {" in utils

    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(
    ui.Button("Go", outline="2", outline_color="primary", outline_offset="2", focus={"outline": "2"}),
    ui.Input(placeholder="x", accent_color="accent"),
    ui.Text("42", font_numeric="tabular"),
)
""",
    )
    assert "ourui-outline-2" in html
    assert "ourui-outline-color-primary" in html
    assert "ourui-accent-color-accent" in html
    assert "ourui-font-numeric-tabular" in html
    assert "ourui-focus-outline-2" in html
    assert ".ourui-outline-2 {" in html


def test_placeholder_selection_intents(tmp_path: Path) -> None:
    classes = style_intent_classes(
        {
            "placeholder_color": "muted",
            "selection": {"bg": "primary", "color": "fg"},
        }
    )
    assert "ourui-placeholder-color-muted" in classes
    assert "ourui-selection-bg-primary" in classes
    assert "ourui-selection-color-fg" in classes

    flat = style_intent_classes({"selection_bg": "accent", "selection_color": "bg"})
    assert "ourui-selection-bg-accent" in flat
    assert "ourui-selection-color-bg" in flat

    utils = emit_utility_css()
    assert ".ourui-placeholder-color-muted::placeholder {" in utils
    assert ".ourui-selection-bg-primary::selection {" in utils

    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(
    ui.Input(placeholder="Name", placeholder_color="muted", selection={"bg": "primary", "color": "fg"}),
)
""",
    )
    assert 'placeholder="Name"' in html
    assert "ourui-placeholder-color-muted" in html
    assert "ourui-selection-bg-primary" in html
    assert ".ourui-placeholder-color-muted::placeholder {" in html


def test_font_stretch_and_feature(tmp_path: Path) -> None:
    classes = style_intent_classes(
        {"font_stretch": "condensed", "font_feature": "smcp", "font_numeric": "tabular"}
    )
    assert "ourui-font-stretch-condensed" in classes
    assert "ourui-font-feature-smcp" in classes
    assert "ourui-font-numeric-tabular" in classes
    utils = emit_utility_css()
    assert ".ourui-font-stretch-expanded {" in utils
    assert '.ourui-font-feature-liga { font-feature-settings: "liga" 1; }' in utils
    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(ui.Text("Hi", font_stretch="expanded", font_feature="liga"))
""",
    )
    assert "ourui-font-stretch-expanded" in html
    assert "ourui-font-feature-liga" in html


def test_mix_blend_mask_bg_image(tmp_path: Path) -> None:
    from ourui.design.style_intents import inline_literal_rules

    classes = style_intent_classes(
        {
            "mix_blend": "multiply",
            "backdrop_blend": "overlay",
            "mask": "fade-b",
            "bg_image": "none",
        }
    )
    assert "ourui-mix-blend-multiply" in classes
    assert "ourui-backdrop-blend-overlay" in classes
    assert "ourui-mask-fade-b" in classes
    assert "ourui-bg-image-none" in classes

    utils = emit_utility_css()
    assert ".ourui-mix-blend-multiply {" in utils
    assert ".ourui-mask-fade-b {" in utils
    assert ".ourui-bg-image-none {" in utils

    rule = inline_literal_rules("n1", {"bg_image": "/assets/hero.jpg"})
    assert 'background-image: url("/assets/hero.jpg");' in rule
    assert inline_literal_rules("n1", {"bg_image": 'javascript:alert(1)'}) == ""
    assert inline_literal_rules("n1", {"bg_image": 'url("x")'}) == ""

    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(
    ui.Shell(mix_blend="multiply", mask="fade-y", bg_image="/img/a.png", width="lg"),
)
""",
    )
    assert "ourui-mix-blend-multiply" in html
    assert "ourui-mask-fade-y" in html
    assert 'background-image: url("/img/a.png");' in html


def test_content_pseudo_and_container_queries(tmp_path: Path) -> None:
    from ourui.design.style_intents import inline_literal_rules

    classes = style_intent_classes(
        {
            "container": True,
            "direction": {"base": "col", "@md": "row"},
            "pad": {"base": "2", "cq_lg": "8"},
            "before": {"content": "none"},
            "after_content": "↗",
        }
    )
    assert "ourui-container" in classes
    assert "ourui-direction-col" in classes
    assert "ourui-cq-md-direction-row" in classes
    assert "ourui-pad-2" in classes
    assert "ourui-cq-lg-pad-8" in classes
    assert "ourui-before-content-none" in classes

    utils = emit_utility_css()
    assert ".ourui-container { container-type: inline-size; }" in utils
    assert "@container (min-width: 28rem) {" in utils
    assert ".ourui-cq-md-direction-row {" in utils
    assert ".ourui-before-content-none::before {" in utils

    rule = inline_literal_rules("n9", {"after_content": "↗", "container": "sidebar"})
    assert '[data-ourui-id="n9"]::after' in rule
    assert 'content: "↗";' in rule
    assert "container-name: sidebar;" in rule

    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(
    ui.Shell(
        ui.Link("Docs", href="/docs", after={"content": " ↗"}),
        container=True,
        direction={"base": "col", "@md": "row"},
        pad={"base": "4", "@lg": "8"},
    ),
)
""",
    )
    assert "ourui-container" in html
    assert "ourui-cq-md-direction-row" in html
    assert "ourui-cq-lg-pad-8" in html
    assert 'content: " ↗";' in html
    assert "@container (min-width: 28rem)" in html


def test_scale_and_utility_css_contain_core_tokens() -> None:
    scales = emit_scale_css_vars()
    assert "--ourui-size-lg:" in scales
    assert "--ourui-space-4:" in scales
    utils = emit_utility_css()
    assert ".ourui-w-lg {" in utils
    assert "width: var(--ourui-size-lg)" in utils
    assert ".ourui-pad-x-4 {" in utils
    assert ".ourui-grow-1 {" in utils
    assert ".ourui-grid-cols-3 {" in utils


def test_style_intent_classes_map_props() -> None:
    classes = style_intent_classes(
        {"width": "lg", "pad_x": "4", "grow": 1, "grid_cols": 3, "text": "Hello world"}
    )
    assert "ourui-w-lg" in classes
    assert "ourui-pad-x-4" in classes
    assert "ourui-grow-1" in classes
    assert "ourui-grid-cols-3" in classes
    # content text must not become font-size class
    assert "ourui-text-Hello-world" not in classes
    assert "ourui-text-Hello" not in classes

    type_classes = style_intent_classes({"text": "lg"})
    assert "ourui-text-lg" in type_classes


def test_emit_includes_scales_and_width_class(tmp_path: Path) -> None:
    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(
    ui.Shell(
        ui.Text("Box"),
        width="lg",
        pad_x="4",
        grow="1",
        gap="md",
    )
)
""",
    )
    assert "--ourui-size-lg:" in html
    assert ".ourui-w-lg {" in html
    assert "ourui-w-lg" in html
    assert "ourui-pad-x-4" in html
    assert "ourui-grow-1" in html


def test_literal_width_inline_rule(tmp_path: Path) -> None:
    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(ui.Shell(ui.Text("Lit"), width="12rem"))
""",
    )
    assert "width: 12rem;" in html
    assert "data-ourui-id=" in html


def test_aspect_ratio_intent_emits(tmp_path: Path) -> None:
    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(
    ui.Shell(ui.Text("Video"), aspect="video", width="full"),
    ui.Shell(ui.Text("Wide"), aspect="16/9", width="full"),
)
""",
    )
    assert "--ourui-aspect-video:" in html
    assert "--ourui-aspect-16-9:" in html
    assert ".ourui-aspect-video {" in html
    assert ".ourui-aspect-16-9 {" in html
    assert "ourui-aspect-video" in html
    assert "ourui-aspect-16-9" in html


def test_theme_scale_override(tmp_path: Path) -> None:
    html = _emit(
        tmp_path,
        """
from ourui import ui
theme = ui.Theme(sizes={"lg": "40rem"})
page = ui.Page(ui.Shell(ui.Text("T"), width="lg"))
""",
    )
    assert "--ourui-size-lg: 40rem;" in html


def test_table_columns_not_grid(tmp_path: Path) -> None:
    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(
    ui.Table(columns=["Name", "Age"], rows=[["Ada", "36"]])
)
""",
    )
    assert "ourui-table" in html or "<table" in html
    assert "ourui-grid-cols-Name" not in html


def test_promoted_c_row_intents() -> None:
    classes = style_intent_classes(
        {
            "object_position": "center",
            "grid_auto_cols": "fr",
            "bg_size": "cover",
            "filter": "grayscale",
            "skew_x": 3,
            "text_columns": 2,
        }
    )
    assert "ourui-object-position-center" in classes
    assert "ourui-grid-auto-cols-fr" in classes
    assert "ourui-bg-size-cover" in classes
    assert "ourui-filter-grayscale" in classes
    assert "ourui-skew-x-3" in classes
    assert "ourui-text-columns-2" in classes
    utils = emit_utility_css()
    assert ".ourui-object-position-center {" in utils
    assert ".ourui-filter-grayscale {" in utils


def test_dump_includes_style_catalog(tmp_path: Path) -> None:
    src = tmp_path / "app.py"
    src.write_text(
        """
from ourui import ui
page = ui.Page(ui.Text("Hi"))
""",
        encoding="utf-8",
    )
    dump = compile_dump(src)
    assert dump["emit"].get("style_intents") is True
    assert dump["style_catalog"]["entries"] >= 80
