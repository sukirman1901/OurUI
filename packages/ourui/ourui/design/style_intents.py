"""OurUI style intent props → host CSS classes (Tailwind-scale values, OurUI names).

Author writes width=\"lg\", not class=\"w-lg\". Emit owns .ourui-w-lg { width: var(--ourui-size-lg) }.
"""

from __future__ import annotations

from typing import Any

from ourui.design.scales import (
    ASPECT,
    BLUR,
    FRACTIONS,
    LEADING,
    OPACITY,
    RADIUS,
    SIZE,
    SPACE,
    TEXT_SIZE,
    TRACKING,
    WEIGHT,
    Z_INDEX,
    _css_ident,
    resolve_length,
)

# prop → (css_property or special, value_kind)
# value_kind: size|space|text|leading|weight|tracking|radius|z|blur|opacity|aspect|keyword|raw|flex|grid

_BOX_SIZE_PROPS = (
    "width",
    "height",
    "min_width",
    "max_width",
    "min_height",
    "max_height",
    "inline_size",
    "block_size",
    "min_inline_size",
    "max_inline_size",
    "min_block_size",
    "max_block_size",
)

_SPACE_SIDE_PROPS = (
    "pad",
    "pad_x",
    "pad_y",
    "pad_t",
    "pad_r",
    "pad_b",
    "pad_l",
    "margin",
    "margin_x",
    "margin_y",
    "margin_t",
    "margin_r",
    "margin_b",
    "margin_l",
    "gap",
    "gap_x",
    "gap_y",
)

STYLE_PASSTHROUGH: tuple[str, ...] = (
    *_BOX_SIZE_PROPS,
    "size",
    *_SPACE_SIDE_PROPS,
    "grow",
    "shrink",
    "basis",
    "wrap",
    "flex",
    "direction",
    "order",
    "grid_cols",
    "grid_rows",
    "col_span",
    "row_span",
    "col_start",
    "col_end",
    "row_start",
    "row_end",
    "grid_flow",
    "grid_auto_cols",
    "grid_auto_rows",
    "text_columns",
    "justify_items",
    "align_content",
    "place",
    "place_items",
    "self",
    "aspect",
    "overflow",
    "overflow_x",
    "overflow_y",
    "pos",
    "inset",
    "top",
    "right",
    "bottom",
    "left",
    "z",
    "visible",
    "isolate",
    "float",
    "clear",
    "display",
    "object_position",
    "text",
    "weight",
    "leading",
    "tracking",
    "align_text",
    "italic",
    "decorate",
    "transform_text",
    "ellipsis",
    "wrap_text",
    "whitespace",
    "line_clamp",
    "bg",
    "bg_size",
    "bg_position",
    "bg_repeat",
    "bg_clip",
    "border",
    "border_w",
    "radius",
    "outline",
    "shadow",
    "elev",
    "opacity",
    "blur",
    "backdrop_blur",
    "filter",
    "rotate",
    "scale_x",
    "scale_y",
    "scale",
    "translate_x",
    "translate_y",
    "skew_x",
    "skew_y",
    "origin",
    "cursor",
    "select",
    "pointer",
    "resize",
    "scroll",
    "snap",
    "touch",
    "accent",
    "fill",
    "stroke",
    "stroke_width",
    "table_layout",
    "border_collapse",
    "hide_below",
    "show_below",
    "forced_colors",
)


def _cls(prefix: str, key: str) -> str:
    return f"ourui-{prefix}-{_css_ident(str(key))}"


def _emit_map(prefix: str, prop: str, mapping: dict[str, str], *, var_prefix: str | None = None) -> list[str]:
    lines: list[str] = []
    vp = var_prefix or prefix
    for key in mapping:
        ident = _css_ident(key)
        lines.append(f".ourui-{prefix}-{ident} {{ {prop}: var(--ourui-{vp}-{ident}); }}")
    return lines


def emit_utility_css() -> str:
    """Finite OurUI utility tables derived from scales."""
    lines: list[str] = ["/* OurUI style intent utilities (generated from design.scales) */"]

    # Box size keywords + scale + fractions
    for prefix, css_prop in (
        ("w", "width"),
        ("h", "height"),
        ("min-w", "min-width"),
        ("max-w", "max-width"),
        ("min-h", "min-height"),
        ("max-h", "max-height"),
        ("inline", "inline-size"),
        ("block", "block-size"),
        ("min-inline", "min-inline-size"),
        ("max-inline", "max-inline-size"),
        ("min-block", "min-block-size"),
        ("max-block", "max-block-size"),
    ):
        for key, val in SIZE.items():
            lines.append(f".ourui-{prefix}-{_css_ident(key)} {{ {css_prop}: var(--ourui-size-{_css_ident(key)}); }}")
        for key in FRACTIONS:
            lines.append(
                f".ourui-{prefix}-{_css_ident(key)} {{ {css_prop}: var(--ourui-frac-{_css_ident(key)}); }}"
            )

    # size= sets both width and height
    for key in SIZE:
        ident = _css_ident(key)
        lines.append(
            f".ourui-size-{ident} {{ width: var(--ourui-size-{ident}); height: var(--ourui-size-{ident}); }}"
        )
    for key in FRACTIONS:
        ident = _css_ident(key)
        lines.append(
            f".ourui-size-{ident} {{ width: var(--ourui-frac-{ident}); height: var(--ourui-frac-{ident}); }}"
        )

    # Spacing
    pad_map = {
        "pad": "padding",
        "pad-x": ("padding-inline",),
        "pad-y": ("padding-block",),
        "pad-t": ("padding-top",),
        "pad-r": ("padding-right",),
        "pad-b": ("padding-bottom",),
        "pad-l": ("padding-left",),
        "m": "margin",
        "mx": ("margin-inline",),
        "my": ("margin-block",),
        "mt": ("margin-top",),
        "mr": ("margin-right",),
        "mb": ("margin-bottom",),
        "ml": ("margin-left",),
        "gap": "gap",
        "gap-x": ("column-gap",),
        "gap-y": ("row-gap",),
    }
    for prefix, css in pad_map.items():
        props = css if isinstance(css, tuple) else (css,)
        for key in SPACE:
            ident = _css_ident(key)
            body = " ".join(f"{p}: var(--ourui-space-{ident});" for p in props)
            lines.append(f".ourui-{prefix}-{ident} {{ {body} }}")

    # Flex
    lines += [
        ".ourui-grow-0 { flex-grow: 0; }",
        ".ourui-grow-1 { flex-grow: 1; }",
        ".ourui-shrink-0 { flex-shrink: 0; }",
        ".ourui-shrink-1 { flex-shrink: 1; }",
        ".ourui-wrap-nowrap { flex-wrap: nowrap; }",
        ".ourui-wrap-wrap { flex-wrap: wrap; }",
        ".ourui-wrap-wrap-reverse { flex-wrap: wrap-reverse; }",
        ".ourui-flex-1 { flex: 1 1 0%; }",
        ".ourui-flex-auto { flex: 1 1 auto; }",
        ".ourui-flex-none { flex: none; }",
        ".ourui-direction-row { flex-direction: row; }",
        ".ourui-direction-col { flex-direction: column; }",
        ".ourui-direction-row-reverse { flex-direction: row-reverse; }",
        ".ourui-direction-col-reverse { flex-direction: column-reverse; }",
    ]
    for key in list(SIZE) + list(FRACTIONS) + ["auto"]:
        if key == "auto":
            lines.append(".ourui-basis-auto { flex-basis: auto; }")
        elif key in SIZE:
            lines.append(f".ourui-basis-{_css_ident(key)} {{ flex-basis: var(--ourui-size-{_css_ident(key)}); }}")
        else:
            lines.append(f".ourui-basis-{_css_ident(key)} {{ flex-basis: var(--ourui-frac-{_css_ident(key)}); }}")
    for i in range(0, 13):
        lines.append(f".ourui-order-{i} {{ order: {i}; }}")
        lines.append(f".ourui-order-neg-{i} {{ order: -{i}; }}")

    # Grid
    for n in range(1, 13):
        lines.append(
            f".ourui-grid-cols-{n} {{ grid-template-columns: repeat({n}, minmax(0, 1fr)); }}"
        )
        lines.append(f".ourui-grid-rows-{n} {{ grid-template-rows: repeat({n}, minmax(0, 1fr)); }}")
        lines.append(f".ourui-col-span-{n} {{ grid-column: span {n} / span {n}; }}")
        lines.append(f".ourui-row-span-{n} {{ grid-row: span {n} / span {n}; }}")
        lines.append(f".ourui-col-start-{n} {{ grid-column-start: {n}; }}")
        lines.append(f".ourui-row-start-{n} {{ grid-row-start: {n}; }}")
    lines += [
        ".ourui-col-span-full { grid-column: 1 / -1; }",
        ".ourui-row-span-full { grid-row: 1 / -1; }",
        ".ourui-grid-cols-none { grid-template-columns: none; }",
        ".ourui-grid-flow-row { grid-auto-flow: row; }",
        ".ourui-grid-flow-col { grid-auto-flow: column; }",
        ".ourui-grid-flow-dense { grid-auto-flow: dense; }",
        ".ourui-grid-flow-row-dense { grid-auto-flow: row dense; }",
        ".ourui-grid-flow-col-dense { grid-auto-flow: column dense; }",
        ".ourui-grid-auto-cols-auto { grid-auto-columns: auto; }",
        ".ourui-grid-auto-cols-min { grid-auto-columns: min-content; }",
        ".ourui-grid-auto-cols-max { grid-auto-columns: max-content; }",
        ".ourui-grid-auto-cols-fr { grid-auto-columns: minmax(0, 1fr); }",
        ".ourui-grid-auto-rows-auto { grid-auto-rows: auto; }",
        ".ourui-grid-auto-rows-min { grid-auto-rows: min-content; }",
        ".ourui-grid-auto-rows-max { grid-auto-rows: max-content; }",
        ".ourui-grid-auto-rows-fr { grid-auto-rows: minmax(0, 1fr); }",
    ]
    for n in range(1, 7):
        lines.append(f".ourui-text-columns-{n} {{ columns: {n}; }}")
    lines.append(".ourui-text-columns-auto { columns: auto; }")

    # Object / background placement
    for pos, css in (
        ("center", "center"),
        ("top", "top"),
        ("bottom", "bottom"),
        ("left", "left"),
        ("right", "right"),
        ("top-left", "left top"),
        ("top-right", "right top"),
        ("bottom-left", "left bottom"),
        ("bottom-right", "right bottom"),
    ):
        lines.append(f".ourui-object-position-{pos} {{ object-position: {css}; }}")
        lines.append(f".ourui-bg-position-{pos} {{ background-position: {css}; }}")
    for sz in ("auto", "cover", "contain"):
        lines.append(f".ourui-bg-size-{sz} {{ background-size: {sz}; }}")
    for rep in ("repeat", "no-repeat", "repeat-x", "repeat-y", "space", "round"):
        lines.append(f".ourui-bg-repeat-{rep} {{ background-repeat: {rep}; }}")

    # Filter presets (beyond blur=)
    for name, css in (
        ("none", "none"),
        ("grayscale", "grayscale(100%)"),
        ("sepia", "sepia(100%)"),
        ("invert", "invert(100%)"),
        ("saturate", "saturate(1.5)"),
        ("contrast", "contrast(1.25)"),
    ):
        lines.append(f".ourui-filter-{name} {{ filter: {css}; }}")

    # Skew
    for deg in ("0", "1", "2", "3", "6", "12"):
        lines.append(f".ourui-skew-x-{deg} {{ transform: skewX({deg}deg); }}")
        lines.append(f".ourui-skew-y-{deg} {{ transform: skewY({deg}deg); }}")
        lines.append(f".ourui-skew-x-neg-{deg} {{ transform: skewX(-{deg}deg); }}")
        lines.append(f".ourui-skew-y-neg-{deg} {{ transform: skewY(-{deg}deg); }}")

    # Align extras
    for name, css in (
        ("justify-items-start", "justify-items: start"),
        ("justify-items-center", "justify-items: center"),
        ("justify-items-end", "justify-items: end"),
        ("justify-items-stretch", "justify-items: stretch"),
        ("align-content-start", "align-content: flex-start"),
        ("align-content-center", "align-content: center"),
        ("align-content-end", "align-content: flex-end"),
        ("align-content-between", "align-content: space-between"),
        ("place-center", "place-items: center; place-content: center"),
        ("place-items-start", "place-items: start"),
        ("place-items-center", "place-items: center"),
        ("place-items-end", "place-items: end"),
        ("place-items-stretch", "place-items: stretch"),
        ("self-auto", "align-self: auto"),
        ("self-start", "align-self: flex-start"),
        ("self-center", "align-self: center"),
        ("self-end", "align-self: flex-end"),
        ("self-stretch", "align-self: stretch"),
    ):
        lines.append(f".ourui-{name} {{ {css}; }}")

    # Layout misc
    lines += _emit_map("aspect", "aspect-ratio", ASPECT)
    for ov in ("auto", "hidden", "clip", "scroll", "visible"):
        lines.append(f".ourui-overflow-{ov} {{ overflow: {ov}; }}")
        lines.append(f".ourui-overflow-x-{ov} {{ overflow-x: {ov}; }}")
        lines.append(f".ourui-overflow-y-{ov} {{ overflow-y: {ov}; }}")
    for pos in ("static", "relative", "absolute", "fixed", "sticky"):
        lines.append(f".ourui-pos-{pos} {{ position: {pos}; }}")
    for key in SPACE:
        ident = _css_ident(key)
        for side, prop in (("inset", "inset"), ("top", "top"), ("right", "right"), ("bottom", "bottom"), ("left", "left")):
            lines.append(f".ourui-{side}-{ident} {{ {prop}: var(--ourui-space-{ident}); }}")
    lines += _emit_map("z", "z-index", Z_INDEX, var_prefix="z")
    lines += [
        ".ourui-visible { visibility: visible; }",
        ".ourui-invisible { visibility: hidden; }",
        ".ourui-isolate { isolation: isolate; }",
        ".ourui-float-left { float: left; }",
        ".ourui-float-right { float: right; }",
        ".ourui-float-none { float: none; }",
        ".ourui-clear-both { clear: both; }",
        ".ourui-clear-none { clear: none; }",
        ".ourui-display-block { display: block; }",
        ".ourui-display-flex { display: flex; }",
        ".ourui-display-grid { display: grid; }",
        ".ourui-display-none { display: none; }",
        ".ourui-display-contents { display: contents; }",
        ".ourui-display-inline { display: inline; }",
        ".ourui-display-inline-flex { display: inline-flex; }",
    ]

    # Typography
    lines += _emit_map("text", "font-size", TEXT_SIZE, var_prefix="text")
    lines += _emit_map("leading", "line-height", LEADING)
    lines += _emit_map("weight", "font-weight", WEIGHT)
    lines += _emit_map("tracking", "letter-spacing", TRACKING)
    for a in ("start", "center", "end", "justify"):
        lines.append(f".ourui-text-align-{a} {{ text-align: {a}; }}")
    lines += [
        ".ourui-italic { font-style: italic; }",
        ".ourui-not-italic { font-style: normal; }",
        ".ourui-underline { text-decoration-line: underline; }",
        ".ourui-line-through { text-decoration-line: line-through; }",
        ".ourui-no-underline { text-decoration-line: none; }",
        ".ourui-uppercase { text-transform: uppercase; }",
        ".ourui-lowercase { text-transform: lowercase; }",
        ".ourui-capitalize { text-transform: capitalize; }",
        ".ourui-normal-case { text-transform: none; }",
        ".ourui-truncate { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }",
        ".ourui-text-wrap-balance { text-wrap: balance; }",
        ".ourui-text-wrap-pretty { text-wrap: pretty; }",
        ".ourui-whitespace-normal { white-space: normal; }",
        ".ourui-whitespace-nowrap { white-space: nowrap; }",
        ".ourui-whitespace-pre { white-space: pre; }",
        ".ourui-whitespace-pre-wrap { white-space: pre-wrap; }",
    ]
    for n in range(1, 7):
        lines.append(
            f".ourui-line-clamp-{n} {{ display: -webkit-box; -webkit-line-clamp: {n}; "
            f"-webkit-box-orient: vertical; overflow: hidden; }}"
        )

    # Borders / radius / opacity / blur / shadow hooks
    lines += _emit_map("radius", "border-radius", RADIUS, var_prefix="radius")
    for w in ("0", "1", "2", "4", "8"):
        px = {"0": "0", "1": "1px", "2": "2px", "4": "4px", "8": "8px"}[w]
        lines.append(f".ourui-border-w-{w} {{ border-width: {px}; border-style: solid; }}")
    lines += [
        ".ourui-border { border-width: 1px; border-style: solid; border-color: var(--ourui-border); }",
        ".ourui-border-0 { border-width: 0; }",
        ".ourui-outline-none { outline: 2px solid transparent; outline-offset: 2px; }",
        ".ourui-shadow-sm { box-shadow: var(--ourui-elev-1); }",
        ".ourui-shadow-md { box-shadow: var(--ourui-elev-2); }",
        ".ourui-shadow-lg { box-shadow: var(--ourui-elev-3); }",
        ".ourui-shadow-none { box-shadow: none; }",
    ]
    lines += _emit_map("opacity", "opacity", OPACITY)
    for key in BLUR:
        ident = _css_ident(key)
        lines.append(f".ourui-blur-{ident} {{ filter: blur(var(--ourui-blur-{ident})); }}")
        lines.append(
            f".ourui-backdrop-blur-{ident} {{ backdrop-filter: blur(var(--ourui-blur-{ident})); }}"
        )

    # Transforms
    for deg in ("0", "1", "2", "3", "6", "12", "45", "90", "180"):
        lines.append(f".ourui-rotate-{deg} {{ transform: rotate({deg}deg); }}")
        lines.append(f".ourui-rotate-neg-{deg} {{ transform: rotate(-{deg}deg); }}")
    for s in ("0", "50", "75", "90", "95", "100", "105", "110", "125", "150"):
        val = str(int(s) / 100)
        lines.append(f".ourui-scale-{s} {{ transform: scale({val}); }}")
    for key in SPACE:
        ident = _css_ident(key)
        lines.append(
            f".ourui-translate-x-{ident} {{ transform: translateX(var(--ourui-space-{ident})); }}"
        )
        lines.append(
            f".ourui-translate-y-{ident} {{ transform: translateY(var(--ourui-space-{ident})); }}"
        )

    # Interactivity
    for c in ("auto", "default", "pointer", "wait", "text", "move", "not-allowed", "grab"):
        lines.append(f".ourui-cursor-{c} {{ cursor: {c}; }}")
    lines += [
        ".ourui-select-none { user-select: none; }",
        ".ourui-select-text { user-select: text; }",
        ".ourui-select-all { user-select: all; }",
        ".ourui-pointer-events-none { pointer-events: none; }",
        ".ourui-pointer-events-auto { pointer-events: auto; }",
        ".ourui-resize-none { resize: none; }",
        ".ourui-resize-y { resize: vertical; }",
        ".ourui-resize-x { resize: horizontal; }",
        ".ourui-scroll-smooth { scroll-behavior: smooth; }",
        ".ourui-snap-x { scroll-snap-type: x mandatory; }",
        ".ourui-snap-y { scroll-snap-type: y mandatory; }",
        ".ourui-snap-start { scroll-snap-align: start; }",
        ".ourui-snap-center { scroll-snap-align: center; }",
        ".ourui-touch-manipulation { touch-action: manipulation; }",
        ".ourui-fill-current { fill: currentColor; }",
        ".ourui-stroke-current { stroke: currentColor; }",
        ".ourui-table-auto { table-layout: auto; }",
        ".ourui-table-fixed { table-layout: fixed; }",
        ".ourui-border-collapse { border-collapse: collapse; }",
        ".ourui-border-separate { border-collapse: separate; }",
        ".ourui-forced-colors-auto { forced-color-adjust: auto; }",
        ".ourui-forced-colors-none { forced-color-adjust: none; }",
    ]

    # Responsive hide/show helpers
    lines += [
        "@media (max-width: 767px) { .ourui-hide-below-md { display: none !important; } }",
        "@media (min-width: 768px) { .ourui-show-below-md { display: none !important; } }",
        "@media (max-width: 1023px) { .ourui-hide-below-lg { display: none !important; } }",
        "@media (min-width: 1024px) { .ourui-show-below-lg { display: none !important; } }",
    ]

    return "\n".join(lines) + "\n"


def style_intent_classes(attrs: dict[str, Any]) -> list[str]:
    """Map node attributes → OurUI utility class names."""
    classes: list[str] = []

    def add(prefix: str, raw: Any) -> None:
        if raw is None or isinstance(raw, dict):
            return
        key = str(raw).strip()
        if not key:
            return
        classes.append(_cls(prefix, key))

    # Box
    prop_prefix = {
        "width": "w",
        "height": "h",
        "min_width": "min-w",
        "max_width": "max-w",
        "min_height": "min-h",
        "max_height": "max-h",
        "inline_size": "inline",
        "block_size": "block",
        "min_inline_size": "min-inline",
        "max_inline_size": "max-inline",
        "min_block_size": "min-block",
        "max_block_size": "max-block",
        "size": "size",
    }
    for prop, prefix in prop_prefix.items():
        add(prefix, attrs.get(prop))

    # Space
    space_prefix = {
        "pad": "pad",
        "pad_x": "pad-x",
        "pad_y": "pad-y",
        "pad_t": "pad-t",
        "pad_r": "pad-r",
        "pad_b": "pad-b",
        "pad_l": "pad-l",
        "margin": "m",
        "margin_x": "mx",
        "margin_y": "my",
        "margin_t": "mt",
        "margin_r": "mr",
        "margin_b": "mb",
        "margin_l": "ml",
        "gap": "gap",
        "gap_x": "gap-x",
        "gap_y": "gap-y",
    }
    for prop, prefix in space_prefix.items():
        add(prefix, attrs.get(prop))

    # Flex / grid
    grow = attrs.get("grow")
    if grow in (True, 1, "1", "true"):
        classes.append("ourui-grow-1")
    elif grow in (False, 0, "0", "false"):
        classes.append("ourui-grow-0")
    elif grow is not None:
        add("grow", grow)
    shrink = attrs.get("shrink")
    if shrink in (True, 1, "1", "true"):
        classes.append("ourui-shrink-1")
    elif shrink in (False, 0, "0", "false"):
        classes.append("ourui-shrink-0")
    elif shrink is not None:
        add("shrink", shrink)
    add("basis", attrs.get("basis"))
    add("wrap", attrs.get("wrap"))
    add("flex", attrs.get("flex"))
    direction = attrs.get("direction")
    if direction in {"column", "col"}:
        classes.append("ourui-direction-col")
    elif direction in {"row"}:
        classes.append("ourui-direction-row")
    elif direction in {"column-reverse", "col-reverse"}:
        classes.append("ourui-direction-col-reverse")
    elif direction in {"row-reverse"}:
        classes.append("ourui-direction-row-reverse")
    elif direction is not None:
        add("direction", direction)
    if attrs.get("order") is not None:
        order = attrs.get("order")
        try:
            n = int(order)  # type: ignore[arg-type]
            classes.append(f"ourui-order-neg-{-n}" if n < 0 else f"ourui-order-{n}")
        except (TypeError, ValueError):
            pass
    add("grid-cols", attrs.get("grid_cols"))
    add("grid-rows", attrs.get("grid_rows"))
    add("col-span", attrs.get("col_span"))
    add("row-span", attrs.get("row_span"))
    add("col-start", attrs.get("col_start"))
    add("row-start", attrs.get("row_start"))
    add("grid-flow", attrs.get("grid_flow"))
    add("grid-auto-cols", attrs.get("grid_auto_cols"))
    add("grid-auto-rows", attrs.get("grid_auto_rows"))
    tc = attrs.get("text_columns")
    if tc is not None:
        add("text-columns", tc)

    add("justify-items", attrs.get("justify_items"))
    add("align-content", attrs.get("align_content"))
    if attrs.get("place") == "center":
        classes.append("ourui-place-center")
    add("place-items", attrs.get("place_items"))
    add("self", attrs.get("self"))

    add("aspect", attrs.get("aspect"))
    add("overflow", attrs.get("overflow"))
    add("overflow-x", attrs.get("overflow_x"))
    add("overflow-y", attrs.get("overflow_y"))
    add("pos", attrs.get("pos"))
    for side in ("inset", "top", "right", "bottom", "left"):
        add(side, attrs.get(side))
    add("z", attrs.get("z"))
    if attrs.get("visible") is False:
        classes.append("ourui-invisible")
    elif attrs.get("visible") is True:
        classes.append("ourui-visible")
    if attrs.get("isolate") in (True, "true", 1):
        classes.append("ourui-isolate")
    add("float", attrs.get("float"))
    add("clear", attrs.get("clear"))
    add("display", attrs.get("display"))
    op = attrs.get("object_position")
    if isinstance(op, str) and op:
        classes.append(f"ourui-object-position-{_css_ident(op)}")
    add("bg-size", attrs.get("bg_size"))
    bp = attrs.get("bg_position")
    if isinstance(bp, str) and bp:
        classes.append(f"ourui-bg-position-{_css_ident(bp)}")
    add("bg-repeat", attrs.get("bg_repeat"))

    # text= is content on many roles; only map known type-scale keys to font-size
    text_val = attrs.get("text")
    if isinstance(text_val, str) and text_val in TEXT_SIZE:
        add("text", text_val)
    add("weight", attrs.get("weight"))
    add("leading", attrs.get("leading"))
    add("tracking", attrs.get("tracking"))
    if attrs.get("align_text"):
        classes.append(f"ourui-text-align-{_css_ident(str(attrs['align_text']))}")
    if attrs.get("italic") in (True, "true", 1, "italic"):
        classes.append("ourui-italic")
    deco = attrs.get("decorate")
    if deco in {"underline", "line-through", "no-underline"}:
        classes.append(f"ourui-{deco}")
    tt = attrs.get("transform_text")
    if tt in {"uppercase", "lowercase", "capitalize", "normal-case"}:
        classes.append(f"ourui-{tt}")
    if attrs.get("ellipsis") in (True, "true", 1, "truncate"):
        classes.append("ourui-truncate")
    wt = attrs.get("wrap_text")
    if wt in {"balance", "pretty"}:
        classes.append(f"ourui-text-wrap-{wt}")
    add("whitespace", attrs.get("whitespace"))
    if attrs.get("line_clamp") is not None:
        add("line-clamp", attrs.get("line_clamp"))

    if attrs.get("border") in (True, "true", 1, "border"):
        classes.append("ourui-border")
    add("border-w", attrs.get("border_w"))
    add("radius", attrs.get("radius"))
    sh = attrs.get("shadow") or attrs.get("elev")
    if sh in {"sm", "md", "lg", "none"}:
        classes.append(f"ourui-shadow-{sh}")
    add("opacity", attrs.get("opacity"))
    add("blur", attrs.get("blur"))
    add("backdrop-blur", attrs.get("backdrop_blur"))
    filt = attrs.get("filter")
    if filt in {"none", "grayscale", "sepia", "invert", "saturate", "contrast"}:
        classes.append(f"ourui-filter-{filt}")

    add("rotate", attrs.get("rotate"))
    if attrs.get("scale") is not None:
        add("scale", attrs.get("scale"))
    add("translate-x", attrs.get("translate_x"))
    add("translate-y", attrs.get("translate_y"))
    for skew_prop, prefix in (("skew_x", "skew-x"), ("skew_y", "skew-y")):
        raw = attrs.get(skew_prop)
        if raw is None:
            continue
        try:
            n = int(raw)  # type: ignore[arg-type]
            if n < 0:
                classes.append(f"ourui-{prefix}-neg-{-n}")
            else:
                classes.append(f"ourui-{prefix}-{n}")
        except (TypeError, ValueError):
            add(prefix, raw)

    add("cursor", attrs.get("cursor"))
    sel = attrs.get("select")
    if sel in {"none", "text", "all"}:
        classes.append(f"ourui-select-{sel}")
    ptr = attrs.get("pointer")
    if ptr in {"none", "auto"}:
        classes.append(f"ourui-pointer-events-{ptr}")
    add("resize", attrs.get("resize"))
    if attrs.get("scroll") == "smooth":
        classes.append("ourui-scroll-smooth")
    snap = attrs.get("snap")
    if snap in {"x", "y", "start", "center"}:
        classes.append(f"ourui-snap-{snap}")
    if attrs.get("touch") == "manipulation":
        classes.append("ourui-touch-manipulation")
    if attrs.get("fill") == "current":
        classes.append("ourui-fill-current")
    if attrs.get("stroke") == "current":
        classes.append("ourui-stroke-current")
    tl = attrs.get("table_layout")
    if tl in {"auto", "fixed"}:
        classes.append(f"ourui-table-{tl}")
    bc = attrs.get("border_collapse")
    if bc == "collapse":
        classes.append("ourui-border-collapse")
    elif bc == "separate":
        classes.append("ourui-border-separate")

    hb = attrs.get("hide_below")
    if hb in {"md", "lg"}:
        classes.append(f"ourui-hide-below-{hb}")
    sb = attrs.get("show_below")
    if sb in {"md", "lg"}:
        classes.append(f"ourui-show-below-{sb}")
    fc = attrs.get("forced_colors")
    if fc in {"auto", "none"}:
        classes.append(f"ourui-forced-colors-{fc}")

    # Deduplicate preserving order
    seen: set[str] = set()
    out: list[str] = []
    for c in classes:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def collect_inline_literal_css(nodes: dict[str, Any]) -> str:
    """Scan RTR nodes for allowlisted length literals → per-id CSS rules."""
    chunks: list[str] = []
    for nid in sorted(nodes):
        attrs = (nodes[nid] or {}).get("attributes") or {}
        if not isinstance(attrs, dict):
            continue
        rule = inline_literal_rules(str(nid), attrs)
        if rule:
            chunks.append(rule)
    return "".join(chunks)


def inline_literal_rules(nid: str, attrs: dict[str, Any]) -> str:
    """Emit per-node rules for allowlisted CSS literals not in scale tables."""
    decls: list[str] = []
    for prop, css_name in (
        ("width", "width"),
        ("height", "height"),
        ("min_width", "min-width"),
        ("max_width", "max-width"),
        ("min_height", "min-height"),
        ("max_height", "max-height"),
    ):
        raw = attrs.get(prop)
        if not isinstance(raw, str):
            continue
        if raw in SIZE or raw in FRACTIONS or raw in SPACE:
            continue
        resolved = resolve_length(raw, kind="size")
        if resolved:
            decls.append(f"  {css_name}: {resolved};")
    if not decls:
        return ""
    return f'[data-ourui-id="{nid}"] {{\n' + "\n".join(decls) + "\n}\n"
