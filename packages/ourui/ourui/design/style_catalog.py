"""ADR-013 coverage matrix: every Tailwind TOC category → OurUI A/B/C.

A = author intent prop(s)
B = host-automatic / preflight
C = escape / limited subset / not yet authored
AC = author surface exists but incomplete vs Tailwind family depth
AB = author + host share the family

See docs/architecture/tailwind-gap.md for L3 priorities.
"""

from __future__ import annotations

from typing import Any

# status: A | B | C | AB | AC
CATALOG: list[dict[str, str]] = [
    # Core
    {"tw": "utility-classes-authoring", "ourui": "intent-props", "status": "A", "notes": "No class= API"},
    {
        "tw": "hover-focus-states",
        "ourui": "hover=/focus= + dict variants",
        "status": "A",
        "notes": "opacity/shadow/scale/decorate/ring/outline/bg; disabled/invalid still host",
    },
    {
        "tw": "responsive",
        "ourui": "hide_below/show_below + dict md/lg",
        "status": "A",
        "notes": "visibility + mobile-first pad/width/gap/text/grid_cols/direction/grow; pad={\"base\":\"4\",\"md\":\"8\"}",
    },
    {"tw": "dark-mode", "ourui": "ThemeToggle+.dark", "status": "AB", "notes": "existing"},
    {
        "tw": "theme-variables",
        "ourui": "--ourui-*+Theme",
        "status": "AB",
        "notes": "theme.py seed; density; page= measure",
    },
    {"tw": "colors", "ourui": "color=/Theme", "status": "A", "notes": "token roles — not full TW palette utils"},
    {"tw": "custom-styles", "ourui": "Theme+literals+css=", "status": "A", "notes": "Theme(css=) author sheet; allowlisted length literals"},
    {"tw": "class-detection", "ourui": "n/a", "status": "B", "notes": "compiler AST not class scan"},
    {"tw": "preflight", "ourui": "host-preflight", "status": "B", "notes": "html/body reset"},
    # Layout
    {"tw": "aspect-ratio", "ourui": "aspect=", "status": "A", "notes": "auto|square|video|photo|16/9|…"},
    {"tw": "columns-multicol", "ourui": "text_columns=", "status": "A", "notes": "not Table columns="},
    {"tw": "break-after-before-inside", "ourui": "host-print", "status": "B", "notes": "print defaults"},
    {"tw": "box-decoration-break", "ourui": "host", "status": "B"},
    {"tw": "box-sizing", "ourui": "preflight", "status": "B"},
    {"tw": "display", "ourui": "display=/layout=", "status": "A"},
    {"tw": "float", "ourui": "float=", "status": "A"},
    {"tw": "clear", "ourui": "clear=", "status": "A"},
    {"tw": "isolation", "ourui": "isolate=", "status": "A"},
    {"tw": "object-fit", "ourui": "fit=", "status": "A", "notes": "Image"},
    {"tw": "object-position", "ourui": "object_position=", "status": "A"},
    {"tw": "overflow", "ourui": "overflow=/overflow_x/y=", "status": "A"},
    {"tw": "overscroll", "ourui": "host", "status": "B"},
    {"tw": "position", "ourui": "pos=/placement=", "status": "A"},
    {"tw": "inset-sides", "ourui": "inset=/top/right/bottom/left=", "status": "A"},
    {"tw": "visibility", "ourui": "visible=/Show/When", "status": "A"},
    {"tw": "z-index", "ourui": "z=", "status": "A"},
    # Flex/Grid
    {"tw": "flex-basis", "ourui": "basis=", "status": "A"},
    {"tw": "flex-direction", "ourui": "direction=/layout=", "status": "A"},
    {"tw": "flex-wrap", "ourui": "wrap=", "status": "A"},
    {"tw": "flex", "ourui": "flex=", "status": "A"},
    {"tw": "flex-grow", "ourui": "grow=", "status": "A"},
    {"tw": "flex-shrink", "ourui": "shrink=", "status": "A"},
    {"tw": "order", "ourui": "order=", "status": "A"},
    {"tw": "grid-template-columns", "ourui": "grid_cols=", "status": "A"},
    {"tw": "grid-column", "ourui": "col_span=/col_start=", "status": "A"},
    {"tw": "grid-template-rows", "ourui": "grid_rows=", "status": "A"},
    {"tw": "grid-row", "ourui": "row_span=/row_start=", "status": "A"},
    {"tw": "grid-auto-flow", "ourui": "grid_flow=", "status": "A"},
    {"tw": "grid-auto-columns", "ourui": "grid_auto_cols=", "status": "A", "notes": "auto|min|max|fr"},
    {"tw": "grid-auto-rows", "ourui": "grid_auto_rows=", "status": "A", "notes": "auto|min|max|fr"},
    {"tw": "gap", "ourui": "gap=/gap_x/y=", "status": "A"},
    {"tw": "justify-content", "ourui": "justify=", "status": "A"},
    {"tw": "justify-items", "ourui": "justify_items=", "status": "A"},
    {"tw": "justify-self", "ourui": "self=", "status": "A"},
    {"tw": "align-content", "ourui": "align_content=", "status": "A"},
    {"tw": "align-items", "ourui": "align=", "status": "A"},
    {"tw": "align-self", "ourui": "self=", "status": "A"},
    {"tw": "place-content", "ourui": "place=", "status": "A"},
    {"tw": "place-items", "ourui": "place_items=", "status": "A"},
    {"tw": "place-self", "ourui": "self=", "status": "A"},
    # Spacing / sizing
    {"tw": "padding", "ourui": "pad=/pad_*", "status": "A"},
    {"tw": "margin", "ourui": "margin=/margin_*", "status": "A"},
    {"tw": "width", "ourui": "width=", "status": "A"},
    {"tw": "min-width", "ourui": "min_width=", "status": "A"},
    {"tw": "max-width", "ourui": "max_width=", "status": "A"},
    {"tw": "height", "ourui": "height=", "status": "A"},
    {"tw": "min-height", "ourui": "min_height=", "status": "A"},
    {"tw": "max-height", "ourui": "max_height=", "status": "A"},
    {"tw": "size", "ourui": "size=", "status": "A"},
    {"tw": "inline-size", "ourui": "inline_size=", "status": "A"},
    {"tw": "block-size", "ourui": "block_size=", "status": "A"},
    {"tw": "min-max-logical", "ourui": "min_/max_inline/block_size=", "status": "A"},
    # Typography
    {"tw": "font-family", "ourui": "Theme font_*", "status": "AB"},
    {"tw": "font-size", "ourui": "text=", "status": "A"},
    {"tw": "font-smoothing", "ourui": "preflight", "status": "B"},
    {"tw": "font-style", "ourui": "italic=", "status": "A"},
    {"tw": "font-weight", "ourui": "weight=", "status": "A"},
    {"tw": "letter-spacing", "ourui": "tracking=", "status": "A"},
    {"tw": "line-clamp", "ourui": "line_clamp=", "status": "A"},
    {"tw": "line-height", "ourui": "leading=", "status": "A"},
    {"tw": "list-style", "ourui": "List host", "status": "B"},
    {"tw": "text-align", "ourui": "align_text=", "status": "A"},
    {"tw": "color", "ourui": "color=", "status": "A"},
    {"tw": "text-decoration", "ourui": "decorate=", "status": "A"},
    {"tw": "text-transform", "ourui": "transform_text=", "status": "A"},
    {"tw": "text-overflow", "ourui": "ellipsis=", "status": "A"},
    {"tw": "text-wrap", "ourui": "wrap_text=", "status": "A"},
    {"tw": "white-space", "ourui": "whitespace=", "status": "A"},
    {"tw": "vertical-align", "ourui": "host", "status": "B"},
    {"tw": "word-break-hyphens", "ourui": "host", "status": "B"},
    # Backgrounds / borders / effects
    {"tw": "background-color", "ourui": "bg=/color tones", "status": "A"},
    {
        "tw": "background-image",
        "ourui": "bg_gradient=/bg_image=",
        "status": "A",
        "notes": "gradient dirs + theme stops; bg_image=none|safe url (per-node); Image/Canvas for rich media",
    },
    {"tw": "background-size-pos-repeat", "ourui": "bg_size/bg_position/bg_repeat=", "status": "A"},
    {"tw": "border-radius", "ourui": "radius=/Theme", "status": "A"},
    {"tw": "border-width-color", "ourui": "border=/border_w=", "status": "A"},
    {
        "tw": "outline",
        "ourui": "outline=/outline_color=/outline_offset=",
        "status": "A",
        "notes": "none|hidden|widths 0|1|2|4|8; theme roles; focus bag outline=",
    },
    {"tw": "box-shadow", "ourui": "shadow=/elev=", "status": "A"},
    {"tw": "text-shadow", "ourui": "host", "status": "B"},
    {"tw": "opacity", "ourui": "opacity=", "status": "A"},
    {
        "tw": "mix-blend",
        "ourui": "mix_blend=/backdrop_blend=",
        "status": "A",
        "notes": "TW mix-blend-mode + backdrop-blend-mode; full mode enum",
    },
    {
        "tw": "mask",
        "ourui": "mask=",
        "status": "A",
        "notes": "none|fade-t/r/b/l|fade-x/y|radial presets; arbitrary → Theme(css=)",
    },
    # Filters / transforms / motion
    {"tw": "filter-blur", "ourui": "blur=", "status": "A"},
    {"tw": "backdrop-filter", "ourui": "backdrop_blur=", "status": "A"},
    {"tw": "other-filters", "ourui": "filter=", "status": "A", "notes": "grayscale|sepia|invert|…"},
    {
        "tw": "transition-animation",
        "ourui": "motion= ADR-012",
        "status": "AB",
        "notes": "motion vocabulary ≠ CSS transition-* / duration-* / ease-* TOC",
    },
    {"tw": "transform-rotate-scale-translate", "ourui": "rotate=/scale=/translate_*=", "status": "A"},
    {"tw": "skew-perspective", "ourui": "skew_x=/skew_y=", "status": "A", "notes": "perspective stays escape"},
    # Tables / interactivity / SVG / a11y
    {"tw": "table-layout", "ourui": "table_layout=", "status": "A"},
    {"tw": "border-collapse", "ourui": "border_collapse=", "status": "A"},
    {"tw": "cursor", "ourui": "cursor=", "status": "A"},
    {"tw": "user-select", "ourui": "select=", "status": "A"},
    {"tw": "pointer-events", "ourui": "pointer=", "status": "A"},
    {"tw": "resize", "ourui": "resize=", "status": "A"},
    {"tw": "scroll-behavior", "ourui": "scroll=", "status": "A"},
    {"tw": "scroll-snap", "ourui": "snap=", "status": "A"},
    {"tw": "touch-action", "ourui": "touch=", "status": "A"},
    {
        "tw": "accent-color",
        "ourui": "accent_color=/accent=",
        "status": "A",
        "notes": "theme roles for form controls",
    },
    {"tw": "will-change", "ourui": "host motion", "status": "B"},
    {"tw": "svg-fill-stroke", "ourui": "fill=/stroke=", "status": "A"},
    {"tw": "forced-color-adjust", "ourui": "forced_colors=", "status": "A"},
    # Missing vs Tailwind v4 capability (docs-sourced) — props may still be absent (L3)
    # See docs/architecture/tailwind-gap.md — ring/divide/space are v4 *sections*, not always standalone pages.
    {
        "tw": "ring",
        "ourui": "ring=/ring_color=/ring_inset=",
        "status": "A",
        "notes": "TW v4: box-shadow § Adding a ring; widths 0|1|2|4|8 + default ring≈3px",
    },
    {
        "tw": "divide-x-y",
        "ourui": "divide=/divide_w=/divide_color=",
        "status": "A",
        "notes": "TW v4: border-width § Between children; x|y + widths 0|1|2|4|8",
    },
    {
        "tw": "space-x-y",
        "ourui": "space_x=/space_y=",
        "status": "A",
        "notes": "TW v4: margin § Adding space between children; SPACE scale",
    },
    {
        "tw": "bg-gradient",
        "ourui": "bg_gradient=/gradient_from=/gradient_to=",
        "status": "A",
        "notes": "TW v4: background-image; finite to-* dirs + theme role stops (not full palette)",
    },
    {
        "tw": "scroll-margin-padding",
        "ourui": "scroll_m=/scroll_p= + sides",
        "status": "A",
        "notes": "TW pages: scroll-margin + scroll-padding; SPACE scale",
    },
    {
        "tw": "caret-color",
        "ourui": "caret=/caret_color=",
        "status": "A",
        "notes": "TW caret-color; theme roles only",
    },
    {
        "tw": "placeholder-selection",
        "ourui": "placeholder_color=/selection=",
        "status": "A",
        "notes": "theme roles; selection={bg,color} or selection_bg=/selection_color=; not Input placeholder= text",
    },
    {
        "tw": "container-queries",
        "ourui": "container=/@md|@lg dict",
        "status": "A",
        "notes": "container=True|name; pad/direction/… dict keys @md|@lg|cq_md|cq_lg",
    },
    {
        "tw": "sr-only",
        "ourui": "sr_only=",
        "status": "A",
        "notes": "TW v4: display § Screen-reader only (sr-only)",
    },
    # Long-tail TW pages — high-ROI finite props (L3)
    {
        "tw": "appearance",
        "ourui": "appearance=",
        "status": "A",
        "notes": "none|auto",
    },
    {
        "tw": "backface-visibility",
        "ourui": "backface=",
        "status": "A",
        "notes": "visible|hidden",
    },
    {
        "tw": "color-scheme",
        "ourui": "color_scheme=",
        "status": "A",
        "notes": "normal|light|dark|light-dark",
    },
    {
        "tw": "content",
        "ourui": "before=/after=/before_content=/after_content=",
        "status": "A",
        "notes": "CSS content on ::before/::after; not Text content=; none|empty|quotes|short string",
    },
    {
        "tw": "field-sizing",
        "ourui": "field_sizing=",
        "status": "A",
        "notes": "content|fixed",
    },
    {
        "tw": "font-feature-settings",
        "ourui": "font_feature=",
        "status": "A",
        "notes": "normal|liga|no-liga|dlig|hist|calt|ss01-04|cv01-04|smcp; arbitrary → Theme(css=)",
    },
    {
        "tw": "font-stretch",
        "ourui": "font_stretch=",
        "status": "A",
        "notes": "ultra-condensed…ultra-expanded named widths",
    },
    {
        "tw": "font-variant-numeric",
        "ourui": "font_numeric=",
        "status": "A",
        "notes": "normal|ordinal|slashed-zero|lining|oldstyle|proportional|tabular|fractions",
    },
    {
        "tw": "scrollbar-color",
        "ourui": "scrollbar_color=",
        "status": "A",
        "notes": "auto|theme roles (thumb + muted track)",
    },
    {
        "tw": "scrollbar-gutter",
        "ourui": "scrollbar_gutter=",
        "status": "A",
        "notes": "auto|stable|stable-both",
    },
    {
        "tw": "scrollbar-width",
        "ourui": "scrollbar_width=",
        "status": "A",
        "notes": "auto|thin|none",
    },
    {
        "tw": "tab-size",
        "ourui": "tab_size=",
        "status": "A",
        "notes": "0|2|4|8",
    },
    {
        "tw": "text-indent",
        "ourui": "text_indent=",
        "status": "A",
        "notes": "SPACE scale",
    },
    {
        "tw": "zoom",
        "ourui": "zoom=",
        "status": "A",
        "notes": "0|50|75|90|95|100|105|110|125|150",
    },
]


def catalog_summary() -> dict[str, Any]:
    counts: dict[str, int] = {}
    for row in CATALOG:
        st = row["status"][0]  # A/B/C primary
        counts[st] = counts.get(st, 0) + 1
    return {
        "version": "1.12.0",
        "entries": len(CATALOG),
        "by_status": counts,
        "items": list(CATALOG),
    }


def assert_catalog_complete() -> None:
    assert len(CATALOG) >= 80, "Style catalog matrix too small"
    missing = [r for r in CATALOG if r["status"] not in {"A", "B", "C", "AB", "AC"}]
    assert not missing
