"""OurUI style intent props → host CSS classes (scale tokens, OurUI names).

Author writes width=\"lg\", not class strings. Emit owns .ourui-w-lg { width: var(--ourui-size-lg) }.
"""

from __future__ import annotations

import re
from typing import Any

from ourui.design.scales import (
    ASPECT,
    BLUR,
    BREAKPOINTS,
    FRACTIONS,
    LEADING,
    OPACITY,
    RADIUS,
    RING,
    SIZE,
    SPACE,
    TEXT_SIZE,
    TRACKING,
    WEIGHT,
    Z_INDEX,
    _css_ident,
    resolve_length,
)

# Author-facing responsive breakpoints (mobile-first min-width). sm/xl remain in BREAKPOINTS for Theme.
_RESPONSIVE_BPS: tuple[str, ...] = ("md", "lg")
# Interactive state variants (TW hover: / focus-visible: without class strings)
_STATE_VARIANTS: tuple[str, ...] = ("hover", "focus")
# Container-query variants (TW @md / @lg) → CSS-safe class prefixes
_CONTAINER_VARIANT_MAP: dict[str, str] = {
    "@md": "cq-md",
    "@lg": "cq-lg",
    "cq_md": "cq-md",
    "cq_lg": "cq-lg",
}
_CONTAINER_MIN_WIDTH: dict[str, str] = {
    "cq-md": "28rem",
    "cq-lg": "32rem",
}
_CONTAINER_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,31}$")

_MIX_BLEND_MODES: tuple[str, ...] = (
    "normal",
    "multiply",
    "screen",
    "overlay",
    "darken",
    "lighten",
    "color-dodge",
    "color-burn",
    "hard-light",
    "soft-light",
    "difference",
    "exclusion",
    "hue",
    "saturation",
    "color",
    "luminosity",
    "plus-darker",
    "plus-lighter",
)

_MASK_PRESETS: dict[str, str] = {
    "none": "none",
    "fade-t": "linear-gradient(to top, transparent, black)",
    "fade-r": "linear-gradient(to right, transparent, black)",
    "fade-b": "linear-gradient(to bottom, transparent, black)",
    "fade-l": "linear-gradient(to left, transparent, black)",
    "fade-x": "linear-gradient(to right, transparent, black 15%, black 85%, transparent)",
    "fade-y": "linear-gradient(to bottom, transparent, black 15%, black 85%, transparent)",
    "radial": "radial-gradient(circle, black 35%, transparent 70%)",
}

_SAFE_BG_URL = re.compile(
    r"^(?:"
    r"https?://[A-Za-z0-9._~:/?#\[\]@!$&*+,;=%-]+"
    r"|/(?!/)[A-Za-z0-9._~/-]*"
    r"|\.\.?/[A-Za-z0-9._~/-]+"
    r"|[A-Za-z0-9._~/-]+\.(?:png|jpe?g|gif|webp|svg|avif)"
    r")$"
)


def _safe_bg_url(raw: str) -> str | None:
    """Allowlist relative/http(s) image URLs for ``bg_image=`` (no quotes/parens)."""
    s = raw.strip()
    if not s or len(s) > 512:
        return None
    if any(c in s for c in "\"'()\\\n\r<>"):
        return None
    low = s.lower()
    if low.startswith(("data:", "javascript:", "vbscript:")):
        return None
    if _SAFE_BG_URL.fullmatch(s):
        return s
    return None


def _css_content_value(raw: Any) -> str | None:
    """Map author content intent → CSS ``content`` value (or None if rejected)."""
    if not isinstance(raw, str):
        return None
    s = raw
    if s == "none":
        return "none"
    if s in ("", "empty"):
        return '""'
    if s in ("open-quote", "close-quote", "no-open-quote", "no-close-quote"):
        return s
    if len(s) > 64 or any(ord(c) < 32 for c in s):
        return None
    escaped = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _responsive_values(raw: Any) -> list[tuple[str | None, Any]]:
    """Expand intent values into (variant|None, value). None = base.

    Dict form (Tailwind ``md:`` / ``hover:`` / ``@md:`` without class strings)::

        pad={"base": "4", "md": "8"}
        opacity={"base": "100", "hover": "80"}
        shadow={"hover": "lg"}
        direction={"base": "col", "@md": "row"}
    """
    if raw is None:
        return []
    if isinstance(raw, dict):
        out: list[tuple[str | None, Any]] = []
        base = raw.get("base", raw.get("_"))
        if base is not None:
            out.append((None, base))
        for bp in _RESPONSIVE_BPS:
            if bp in raw and raw[bp] is not None:
                out.append((bp, raw[bp]))
        for st in _STATE_VARIANTS:
            if st in raw and raw[st] is not None:
                out.append((st, raw[st]))
        for key, pfx in _CONTAINER_VARIANT_MAP.items():
            if key in raw and raw[key] is not None:
                out.append((pfx, raw[key]))
        return out
    return [(None, raw)]

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
    "space_x",
    "space_y",
    "scroll_m",
    "scroll_mx",
    "scroll_my",
    "scroll_mt",
    "scroll_mr",
    "scroll_mb",
    "scroll_ml",
    "scroll_p",
    "scroll_px",
    "scroll_py",
    "scroll_pt",
    "scroll_pr",
    "scroll_pb",
    "scroll_pl",
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
    "bg_gradient",
    "bg_image",
    "gradient_from",
    "gradient_to",
    "border",
    "border_w",
    "radius",
    "outline",
    "outline_color",
    "outline_offset",
    "shadow",
    "elev",
    "ring",
    "ring_color",
    "ring_inset",
    "divide",
    "divide_w",
    "divide_color",
    "opacity",
    "blur",
    "backdrop_blur",
    "filter",
    "mix_blend",
    "backdrop_blend",
    "mask",
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
    "accent_color",
    "fill",
    "stroke",
    "stroke_width",
    "table_layout",
    "border_collapse",
    "hide_below",
    "show_below",
    "forced_colors",
    "sr_only",
    "caret",
    "caret_color",
    "appearance",
    "color_scheme",
    "field_sizing",
    "scrollbar_width",
    "scrollbar_gutter",
    "scrollbar_color",
    "tab_size",
    "text_indent",
    "zoom",
    "backface",
    "font_numeric",
    "font_stretch",
    "font_feature",
    "placeholder_color",
    "selection",
    "selection_bg",
    "selection_color",
    "container",
    "before",
    "after",
    "before_content",
    "after_content",
    "hover",
    "focus",
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
        # TW v4: outline-none → hidden a11y outline; outline-hidden style; outline / outline-N widths
        ".ourui-outline-none { outline: 2px solid transparent; outline-offset: 2px; }",
        ".ourui-outline-hidden { outline: 2px solid transparent; outline-offset: 2px; }",
        ".ourui-outline { outline-style: solid; outline-width: 1px; "
        "outline-color: var(--ourui-outline-color, var(--ourui-accent)); }",
    ]
    for w, px in (("0", "0"), ("1", "1px"), ("2", "2px"), ("4", "4px"), ("8", "8px")):
        lines.append(
            f".ourui-outline-{w} {{ outline-style: solid; outline-width: {px}; "
            f"outline-color: var(--ourui-outline-color, var(--ourui-accent)); }}"
        )
    for o, px in (("0", "0"), ("1", "1px"), ("2", "2px"), ("4", "4px"), ("8", "8px")):
        lines.append(f".ourui-outline-offset-{o} {{ outline-offset: {px}; }}")
    for role in ("primary", "accent", "muted", "danger", "border", "fg", "bg"):
        lines.append(f".ourui-outline-color-{role} {{ --ourui-outline-color: var(--ourui-{role}); }}")
    for role in ("primary", "accent", "muted", "danger", "border", "fg", "bg"):
        lines.append(f".ourui-accent-color-{role} {{ accent-color: var(--ourui-{role}); }}")
    lines += [
        ".ourui-font-numeric-normal { font-variant-numeric: normal; }",
        ".ourui-font-numeric-ordinal { font-variant-numeric: ordinal; }",
        ".ourui-font-numeric-slashed-zero { font-variant-numeric: slashed-zero; }",
        ".ourui-font-numeric-lining { font-variant-numeric: lining-nums; }",
        ".ourui-font-numeric-oldstyle { font-variant-numeric: oldstyle-nums; }",
        ".ourui-font-numeric-proportional { font-variant-numeric: proportional-nums; }",
        ".ourui-font-numeric-tabular { font-variant-numeric: tabular-nums; }",
        ".ourui-font-numeric-diagonal-fractions { font-variant-numeric: diagonal-fractions; }",
        ".ourui-font-numeric-stacked-fractions { font-variant-numeric: stacked-fractions; }",
        # Placeholder / selection (pseudo-elements; theme roles)
    ]
    _stretch = (
        ("ultra-condensed", "ultra-condensed"),
        ("extra-condensed", "extra-condensed"),
        ("condensed", "condensed"),
        ("semi-condensed", "semi-condensed"),
        ("normal", "normal"),
        ("semi-expanded", "semi-expanded"),
        ("expanded", "expanded"),
        ("extra-expanded", "extra-expanded"),
        ("ultra-expanded", "ultra-expanded"),
    )
    for key, val in _stretch:
        lines.append(f".ourui-font-stretch-{key} {{ font-stretch: {val}; }}")
    _feat = (
        ("normal", "normal"),
        ("liga", '"liga" 1'),
        ("no-liga", '"liga" 0'),
        ("dlig", '"dlig" 1'),
        ("no-dlig", '"dlig" 0'),
        ("hist", '"hist" 1'),
        ("calt", '"calt" 1'),
        ("no-calt", '"calt" 0'),
        ("ss01", '"ss01" 1'),
        ("ss02", '"ss02" 1'),
        ("ss03", '"ss03" 1'),
        ("ss04", '"ss04" 1'),
        ("cv01", '"cv01" 1'),
        ("cv02", '"cv02" 1'),
        ("cv03", '"cv03" 1'),
        ("cv04", '"cv04" 1'),
        ("smcp", '"smcp" 1'),
    )
    for key, val in _feat:
        lines.append(f".ourui-font-feature-{key} {{ font-feature-settings: {val}; }}")
    for role in ("primary", "accent", "muted", "danger", "border", "fg", "bg"):
        lines.append(f".ourui-placeholder-color-{role}::placeholder {{ color: var(--ourui-{role}); }}")
    for role in ("primary", "accent", "muted", "danger", "border", "fg", "bg", "card"):
        lines.append(f".ourui-selection-bg-{role}::selection {{ background-color: var(--ourui-{role}); }}")
        lines.append(f".ourui-selection-color-{role}::selection {{ color: var(--ourui-{role}); }}")
    lines += [
        # Shadow + ring compose via CSS vars (TW v4 ring lives on box-shadow)
        ".ourui-shadow-sm { --ourui-elev-shadow: var(--ourui-elev-1); "
        "box-shadow: var(--ourui-elev-shadow), var(--ourui-ring-shadow, 0 0 #0000); }",
        ".ourui-shadow-md { --ourui-elev-shadow: var(--ourui-elev-2); "
        "box-shadow: var(--ourui-elev-shadow), var(--ourui-ring-shadow, 0 0 #0000); }",
        ".ourui-shadow-lg { --ourui-elev-shadow: var(--ourui-elev-3); "
        "box-shadow: var(--ourui-elev-shadow), var(--ourui-ring-shadow, 0 0 #0000); }",
        ".ourui-shadow-none { --ourui-elev-shadow: none; "
        "box-shadow: var(--ourui-elev-shadow), var(--ourui-ring-shadow, 0 0 #0000); }",
    ]
    _ring_color_fallback = (
        "var(--ourui-ring-color, color-mix(in srgb, var(--ourui-primary) 40%, transparent))"
    )
    # Default `ring` ≈ Tailwind `ring` (3px)
    lines.append(
        f".ourui-ring {{ --ourui-ring-shadow: 0 0 0 3px {_ring_color_fallback}; "
        f"box-shadow: var(--ourui-elev-shadow, 0 0 #0000), var(--ourui-ring-shadow); }}"
    )
    for key, px in RING.items():
        lines.append(
            f".ourui-ring-{key} {{ --ourui-ring-shadow: 0 0 0 {px} {_ring_color_fallback}; "
            f"box-shadow: var(--ourui-elev-shadow, 0 0 #0000), var(--ourui-ring-shadow); }}"
        )
        lines.append(
            f".ourui-ring-inset-{key} {{ --ourui-ring-shadow: inset 0 0 0 {px} {_ring_color_fallback}; "
            f"box-shadow: var(--ourui-elev-shadow, 0 0 #0000), var(--ourui-ring-shadow); }}"
        )
    lines.append(
        f".ourui-ring-inset {{ --ourui-ring-shadow: inset 0 0 0 3px {_ring_color_fallback}; "
        f"box-shadow: var(--ourui-elev-shadow, 0 0 #0000), var(--ourui-ring-shadow); }}"
    )
    for role in ("primary", "accent", "muted", "danger", "border", "fg", "bg"):
        lines.append(f".ourui-ring-color-{role} {{ --ourui-ring-color: var(--ourui-{role}); }}")
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

    # Scroll margin / padding (SPACE scale)
    scroll_map = {
        "scroll-m": ("scroll-margin",),
        "scroll-mx": ("scroll-margin-inline",),
        "scroll-my": ("scroll-margin-block",),
        "scroll-mt": ("scroll-margin-top",),
        "scroll-mr": ("scroll-margin-right",),
        "scroll-mb": ("scroll-margin-bottom",),
        "scroll-ml": ("scroll-margin-left",),
        "scroll-p": ("scroll-padding",),
        "scroll-px": ("scroll-padding-inline",),
        "scroll-py": ("scroll-padding-block",),
        "scroll-pt": ("scroll-padding-top",),
        "scroll-pr": ("scroll-padding-right",),
        "scroll-pb": ("scroll-padding-bottom",),
        "scroll-pl": ("scroll-padding-left",),
    }
    for prefix, props in scroll_map.items():
        for key in SPACE:
            ident = _css_ident(key)
            body = " ".join(f"{p}: var(--ourui-space-{ident});" for p in props)
            lines.append(f".ourui-{prefix}-{ident} {{ {body} }}")

    # space-x / space-y between children (TW margin §)
    _sib = ":not([hidden]) ~ :not([hidden])"
    for key in SPACE:
        ident = _css_ident(key)
        lines.append(
            f".ourui-space-x-{ident} > {_sib} {{ margin-inline-start: var(--ourui-space-{ident}); }}"
        )
        lines.append(
            f".ourui-space-y-{ident} > {_sib} {{ margin-block-start: var(--ourui-space-{ident}); }}"
        )

    # divide-x / divide-y (TW border-width § Between children)
    for w, px in (("0", "0"), ("1", "1px"), ("2", "2px"), ("4", "4px"), ("8", "8px")):
        lines.append(f".ourui-divide-w-{w} {{ --ourui-divide-w: {px}; }}")
    _div_color = "var(--ourui-divide-color, var(--ourui-border))"
    lines += [
        f".ourui-divide-x > {_sib} {{ border-inline-start-width: var(--ourui-divide-w, 1px); "
        f"border-inline-start-style: solid; border-inline-start-color: {_div_color}; }}",
        f".ourui-divide-y > {_sib} {{ border-block-start-width: var(--ourui-divide-w, 1px); "
        f"border-block-start-style: solid; border-block-start-color: {_div_color}; }}",
    ]
    for role in ("primary", "accent", "muted", "danger", "border", "fg", "bg"):
        lines.append(f".ourui-divide-color-{role} {{ --ourui-divide-color: var(--ourui-{role}); }}")

    # sr-only (TW display § Screen-reader only)
    lines.append(
        ".ourui-sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; "
        "overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border-width: 0; }"
    )

    # caret-color
    for role in ("primary", "accent", "muted", "danger", "border", "fg", "bg"):
        lines.append(f".ourui-caret-{role} {{ caret-color: var(--ourui-{role}); }}")

    # Linear gradient subset (TW background-image)
    _grad_dirs = {
        "to-t": "to top",
        "to-tr": "to top right",
        "to-r": "to right",
        "to-br": "to bottom right",
        "to-b": "to bottom",
        "to-bl": "to bottom left",
        "to-l": "to left",
        "to-tl": "to top left",
    }
    _g_from = "var(--ourui-gradient-from, var(--ourui-primary))"
    _g_to = "var(--ourui-gradient-to, transparent)"
    for key, css_dir in _grad_dirs.items():
        lines.append(
            f".ourui-bg-gradient-{key} {{ background-image: linear-gradient({css_dir}, {_g_from}, {_g_to}); }}"
        )
    for role in ("primary", "accent", "muted", "danger", "border", "fg", "bg"):
        lines.append(f".ourui-gradient-from-{role} {{ --ourui-gradient-from: var(--ourui-{role}); }}")
        lines.append(f".ourui-gradient-to-{role} {{ --ourui-gradient-to: var(--ourui-{role}); }}")
    lines.append(".ourui-bg-image-none { background-image: none; }")

    for mode in _MIX_BLEND_MODES:
        lines.append(f".ourui-mix-blend-{mode} {{ mix-blend-mode: {mode}; }}")
        lines.append(f".ourui-backdrop-blend-{mode} {{ backdrop-blend-mode: {mode}; }}")
    for key, css in _MASK_PRESETS.items():
        lines.append(
            f".ourui-mask-{key} {{ -webkit-mask-image: {css}; mask-image: {css}; }}"
        )

    # Long-tail host utilities (TW v4 pages formerly catalog C)
    lines += [
        ".ourui-appearance-none { appearance: none; }",
        ".ourui-appearance-auto { appearance: auto; }",
        ".ourui-color-scheme-normal { color-scheme: normal; }",
        ".ourui-color-scheme-light { color-scheme: light; }",
        ".ourui-color-scheme-dark { color-scheme: dark; }",
        ".ourui-color-scheme-light-dark { color-scheme: light dark; }",
        ".ourui-field-sizing-content { field-sizing: content; }",
        ".ourui-field-sizing-fixed { field-sizing: fixed; }",
        ".ourui-scrollbar-width-auto { scrollbar-width: auto; }",
        ".ourui-scrollbar-width-thin { scrollbar-width: thin; }",
        ".ourui-scrollbar-width-none { scrollbar-width: none; }",
        ".ourui-scrollbar-gutter-auto { scrollbar-gutter: auto; }",
        ".ourui-scrollbar-gutter-stable { scrollbar-gutter: stable; }",
        ".ourui-scrollbar-gutter-stable-both { scrollbar-gutter: stable both-edges; }",
        ".ourui-backface-visible { backface-visibility: visible; }",
        ".ourui-backface-hidden { backface-visibility: hidden; }",
    ]
    for n in ("0", "2", "4", "8"):
        lines.append(f".ourui-tab-size-{n} {{ tab-size: {n}; }}")
    for key in SPACE:
        ident = _css_ident(key)
        lines.append(f".ourui-text-indent-{ident} {{ text-indent: var(--ourui-space-{ident}); }}")
    for z in ("0", "50", "75", "90", "95", "100", "105", "110", "125", "150"):
        val = str(int(z) / 100)
        lines.append(f".ourui-zoom-{z} {{ zoom: {val}; }}")
    for role in ("primary", "accent", "muted", "danger", "border", "fg", "bg"):
        lines.append(
            f".ourui-scrollbar-color-{role} {{ scrollbar-color: var(--ourui-{role}) var(--ourui-muted); }}"
        )
    lines.append(".ourui-scrollbar-color-auto { scrollbar-color: auto; }")

    # Responsive depth (md/lg) — mobile-first overrides for high-ROI props
    lines += _emit_responsive_depth_css()
    lines += _emit_container_query_css()

    # Hover / focus-visible state variants (finite high-ROI set)
    lines += _emit_state_variant_css()

    # Responsive hide/show helpers
    lines += [
        "@media (max-width: 767px) { .ourui-hide-below-md { display: none !important; } }",
        "@media (min-width: 768px) { .ourui-show-below-md { display: none !important; } }",
        "@media (max-width: 1023px) { .ourui-hide-below-lg { display: none !important; } }",
        "@media (min-width: 1024px) { .ourui-show-below-lg { display: none !important; } }",
    ]

    return "\n".join(lines) + "\n"


def _emit_responsive_depth_css() -> list[str]:
    """Emit ``.ourui-md-*`` / ``.ourui-lg-*`` under min-width media queries."""
    pad_map = {
        "pad": ("padding",),
        "pad-x": ("padding-inline",),
        "pad-y": ("padding-block",),
        "pad-t": ("padding-top",),
        "pad-r": ("padding-right",),
        "pad-b": ("padding-bottom",),
        "pad-l": ("padding-left",),
        "m": ("margin",),
        "mx": ("margin-inline",),
        "my": ("margin-block",),
        "mt": ("margin-top",),
        "mr": ("margin-right",),
        "mb": ("margin-bottom",),
        "ml": ("margin-left",),
        "gap": ("gap",),
        "gap-x": ("column-gap",),
        "gap-y": ("row-gap",),
        "scroll-m": ("scroll-margin",),
        "scroll-mx": ("scroll-margin-inline",),
        "scroll-my": ("scroll-margin-block",),
        "scroll-mt": ("scroll-margin-top",),
        "scroll-mr": ("scroll-margin-right",),
        "scroll-mb": ("scroll-margin-bottom",),
        "scroll-ml": ("scroll-margin-left",),
        "scroll-p": ("scroll-padding",),
        "scroll-px": ("scroll-padding-inline",),
        "scroll-py": ("scroll-padding-block",),
        "scroll-pt": ("scroll-padding-top",),
        "scroll-pr": ("scroll-padding-right",),
        "scroll-pb": ("scroll-padding-bottom",),
        "scroll-pl": ("scroll-padding-left",),
    }
    box_prefixes = (
        ("w", "width"),
        ("h", "height"),
        ("min-w", "min-width"),
        ("max-w", "max-width"),
        ("min-h", "min-height"),
        ("max-h", "max-height"),
    )
    _sib = ":not([hidden]) ~ :not([hidden])"
    out: list[str] = []
    for bp in _RESPONSIVE_BPS:
        min_w = BREAKPOINTS[bp]
        out.append(f"@media (min-width: {min_w}) {{")
        pfx = f"{bp}-"
        for prefix, props in pad_map.items():
            for key in SPACE:
                ident = _css_ident(key)
                body = " ".join(f"{p}: var(--ourui-space-{ident});" for p in props)
                out.append(f"  .ourui-{pfx}{prefix}-{ident} {{ {body} }}")
        for key in SPACE:
            ident = _css_ident(key)
            out.append(
                f"  .ourui-{pfx}space-x-{ident} > {_sib} {{ margin-inline-start: var(--ourui-space-{ident}); }}"
            )
            out.append(
                f"  .ourui-{pfx}space-y-{ident} > {_sib} {{ margin-block-start: var(--ourui-space-{ident}); }}"
            )
        for prefix, css_prop in box_prefixes:
            for key in SIZE:
                ident = _css_ident(key)
                out.append(
                    f"  .ourui-{pfx}{prefix}-{ident} {{ {css_prop}: var(--ourui-size-{ident}); }}"
                )
            for key in FRACTIONS:
                ident = _css_ident(key)
                out.append(
                    f"  .ourui-{pfx}{prefix}-{ident} {{ {css_prop}: var(--ourui-frac-{ident}); }}"
                )
        for key in SIZE:
            ident = _css_ident(key)
            out.append(
                f"  .ourui-{pfx}size-{ident} {{ width: var(--ourui-size-{ident}); "
                f"height: var(--ourui-size-{ident}); }}"
            )
        for key, _ in TEXT_SIZE.items():
            ident = _css_ident(key)
            out.append(f"  .ourui-{pfx}text-{ident} {{ font-size: var(--ourui-text-{ident}); }}")
        for n in range(1, 13):
            out.append(
                f"  .ourui-{pfx}grid-cols-{n} {{ grid-template-columns: repeat({n}, minmax(0, 1fr)); }}"
            )
        out += [
            f"  .ourui-{pfx}grow-0 {{ flex-grow: 0; }}",
            f"  .ourui-{pfx}grow-1 {{ flex-grow: 1; }}",
            f"  .ourui-{pfx}direction-row {{ flex-direction: row; }}",
            f"  .ourui-{pfx}direction-col {{ flex-direction: column; }}",
            f"  .ourui-{pfx}direction-row-reverse {{ flex-direction: row-reverse; }}",
            f"  .ourui-{pfx}direction-col-reverse {{ flex-direction: column-reverse; }}",
        ]
        out.append("}")
    return out


def _emit_container_query_css() -> list[str]:
    """Emit ``.ourui-cq-md-*`` / ``.ourui-cq-lg-*`` under ``@container`` queries + host container."""
    out: list[str] = [
        ".ourui-container { container-type: inline-size; }",
    ]
    # Reuse the same depth utilities as viewport md/lg, under @container
    pad_map = {
        "pad": ("padding",),
        "pad-x": ("padding-inline",),
        "pad-y": ("padding-block",),
        "pad-t": ("padding-top",),
        "pad-r": ("padding-right",),
        "pad-b": ("padding-bottom",),
        "pad-l": ("padding-left",),
        "gap": ("gap",),
        "gap-x": ("column-gap",),
        "gap-y": ("row-gap",),
    }
    box_prefixes = (
        ("w", "width"),
        ("h", "height"),
        ("min-w", "min-width"),
        ("max-w", "max-width"),
    )
    for cq, min_w in _CONTAINER_MIN_WIDTH.items():
        out.append(f"@container (min-width: {min_w}) {{")
        pfx = f"{cq}-"
        for prefix, props in pad_map.items():
            for key in SPACE:
                ident = _css_ident(key)
                body = " ".join(f"{p}: var(--ourui-space-{ident});" for p in props)
                out.append(f"  .ourui-{pfx}{prefix}-{ident} {{ {body} }}")
        for prefix, css_prop in box_prefixes:
            for key in SIZE:
                ident = _css_ident(key)
                out.append(
                    f"  .ourui-{pfx}{prefix}-{ident} {{ {css_prop}: var(--ourui-size-{ident}); }}"
                )
            for key in FRACTIONS:
                ident = _css_ident(key)
                out.append(
                    f"  .ourui-{pfx}{prefix}-{ident} {{ {css_prop}: var(--ourui-frac-{ident}); }}"
                )
        for key, _ in TEXT_SIZE.items():
            ident = _css_ident(key)
            out.append(f"  .ourui-{pfx}text-{ident} {{ font-size: var(--ourui-text-{ident}); }}")
        for n in range(1, 13):
            out.append(
                f"  .ourui-{pfx}grid-cols-{n} {{ grid-template-columns: repeat({n}, minmax(0, 1fr)); }}"
            )
        out += [
            f"  .ourui-{pfx}grow-0 {{ flex-grow: 0; }}",
            f"  .ourui-{pfx}grow-1 {{ flex-grow: 1; }}",
            f"  .ourui-{pfx}direction-row {{ flex-direction: row; }}",
            f"  .ourui-{pfx}direction-col {{ flex-direction: column; }}",
            f"  .ourui-{pfx}direction-row-reverse {{ flex-direction: row-reverse; }}",
            f"  .ourui-{pfx}direction-col-reverse {{ flex-direction: column-reverse; }}",
        ]
        out.append("}")
    # Shared pseudo content keywords (strings → per-node rules)
    out += [
        ".ourui-before-content-none::before { content: none; }",
        '.ourui-before-content-empty::before { content: ""; }',
        ".ourui-after-content-none::after { content: none; }",
        '.ourui-after-content-empty::after { content: ""; }',
    ]
    return out


def _emit_state_variant_css() -> list[str]:
    """Emit ``.ourui-hover-*`` / ``.ourui-focus-*`` (focus-visible) for high-ROI props."""
    out: list[str] = []
    _ring_color_fallback = (
        "var(--ourui-ring-color, color-mix(in srgb, var(--ourui-primary) 40%, transparent))"
    )
    _bg_fg = {
        "primary": ("primary", "primary-fg"),
        "accent": ("accent", "accent-fg"),
        "muted": ("muted", "muted-fg"),
        "danger": ("danger", "danger-fg"),
        "border": ("border", "fg"),
        "fg": ("fg", "bg"),
        "bg": ("bg", "fg"),
        "card": ("card", "card-fg"),
    }
    for state, pseudo in (("hover", "hover"), ("focus", "focus-visible")):
        pfx = f"{state}-"
        for key in OPACITY:
            ident = _css_ident(key)
            out.append(
                f".ourui-{pfx}opacity-{ident}:{pseudo} {{ opacity: var(--ourui-opacity-{ident}); }}"
            )
        for sh, elev in (("sm", "1"), ("md", "2"), ("lg", "3")):
            out.append(
                f".ourui-{pfx}shadow-{sh}:{pseudo} {{ --ourui-elev-shadow: var(--ourui-elev-{elev}); "
                f"box-shadow: var(--ourui-elev-shadow), var(--ourui-ring-shadow, 0 0 #0000); }}"
            )
        out.append(
            f".ourui-{pfx}shadow-none:{pseudo} {{ --ourui-elev-shadow: none; "
            f"box-shadow: var(--ourui-elev-shadow), var(--ourui-ring-shadow, 0 0 #0000); }}"
        )
        for s in ("0", "50", "75", "90", "95", "100", "105", "110", "125", "150"):
            val = str(int(s) / 100)
            out.append(f".ourui-{pfx}scale-{s}:{pseudo} {{ transform: scale({val}); }}")
        out += [
            f".ourui-{pfx}underline:{pseudo} {{ text-decoration-line: underline; }}",
            f".ourui-{pfx}line-through:{pseudo} {{ text-decoration-line: line-through; }}",
            f".ourui-{pfx}no-underline:{pseudo} {{ text-decoration-line: none; }}",
            f".ourui-{pfx}ring:{pseudo} {{ --ourui-ring-shadow: 0 0 0 3px {_ring_color_fallback}; "
            f"box-shadow: var(--ourui-elev-shadow, 0 0 #0000), var(--ourui-ring-shadow); }}",
        ]
        for key, px in RING.items():
            out.append(
                f".ourui-{pfx}ring-{key}:{pseudo} {{ --ourui-ring-shadow: 0 0 0 {px} {_ring_color_fallback}; "
                f"box-shadow: var(--ourui-elev-shadow, 0 0 #0000), var(--ourui-ring-shadow); }}"
            )
        out.append(
            f".ourui-{pfx}outline:{pseudo} {{ outline-style: solid; outline-width: 1px; "
            f"outline-color: var(--ourui-outline-color, var(--ourui-accent)); }}"
        )
        for w, px in (("0", "0"), ("1", "1px"), ("2", "2px"), ("4", "4px"), ("8", "8px")):
            out.append(
                f".ourui-{pfx}outline-{w}:{pseudo} {{ outline-style: solid; outline-width: {px}; "
                f"outline-color: var(--ourui-outline-color, var(--ourui-accent)); }}"
            )
        for role, (fill, fg) in _bg_fg.items():
            out.append(
                f".ourui-{pfx}bg-{role}:{pseudo} {{ background-color: var(--ourui-{fill}); "
                f"color: var(--ourui-{fg}); }}"
            )
    return out


def style_intent_classes(attrs: dict[str, Any]) -> list[str]:
    """Map node attributes → OurUI utility class names."""
    classes: list[str] = []

    def add(prefix: str, raw: Any) -> None:
        for bp, val in _responsive_values(raw):
            if val is None:
                continue
            key = str(val).strip()
            if not key:
                continue
            p = f"{bp}-{prefix}" if bp else prefix
            classes.append(_cls(p, key))

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
        "space_x": "space-x",
        "space_y": "space-y",
        "scroll_m": "scroll-m",
        "scroll_mx": "scroll-mx",
        "scroll_my": "scroll-my",
        "scroll_mt": "scroll-mt",
        "scroll_mr": "scroll-mr",
        "scroll_mb": "scroll-mb",
        "scroll_ml": "scroll-ml",
        "scroll_p": "scroll-p",
        "scroll_px": "scroll-px",
        "scroll_py": "scroll-py",
        "scroll_pt": "scroll-pt",
        "scroll_pr": "scroll-pr",
        "scroll_pb": "scroll-pb",
        "scroll_pl": "scroll-pl",
    }
    for prop, prefix in space_prefix.items():
        add(prefix, attrs.get(prop))

    # Flex / grid
    def _bp_cls(bp: str | None, name: str) -> str:
        return f"ourui-{bp}-{name}" if bp else f"ourui-{name}"

    for bp, grow in _responsive_values(attrs.get("grow")):
        if grow in (True, 1, "1", "true"):
            classes.append(_bp_cls(bp, "grow-1"))
        elif grow in (False, 0, "0", "false"):
            classes.append(_bp_cls(bp, "grow-0"))
        elif grow is not None:
            add("grow" if bp is None else f"{bp}-grow", grow)
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
    for bp, direction in _responsive_values(attrs.get("direction")):
        if direction in {"column", "col"}:
            classes.append(_bp_cls(bp, "direction-col"))
        elif direction in {"row"}:
            classes.append(_bp_cls(bp, "direction-row"))
        elif direction in {"column-reverse", "col-reverse"}:
            classes.append(_bp_cls(bp, "direction-col-reverse"))
        elif direction in {"row-reverse"}:
            classes.append(_bp_cls(bp, "direction-row-reverse"))
        elif direction is not None:
            add("direction" if bp is None else f"{bp}-direction", direction)
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
    bg_pos = attrs.get("bg_position")
    if isinstance(bg_pos, str) and bg_pos:
        classes.append(f"ourui-bg-position-{_css_ident(bg_pos)}")
    add("bg-repeat", attrs.get("bg_repeat"))

    # text= is content on many roles; only map known type-scale keys to font-size
    text_val = attrs.get("text")
    if isinstance(text_val, dict):
        for bp, tv in _responsive_values(text_val):
            if isinstance(tv, str) and tv in TEXT_SIZE:
                add("text" if bp is None else f"{bp}-text", tv)
    elif isinstance(text_val, str) and text_val in TEXT_SIZE:
        add("text", text_val)
    add("weight", attrs.get("weight"))
    add("leading", attrs.get("leading"))
    add("tracking", attrs.get("tracking"))
    if attrs.get("align_text"):
        classes.append(f"ourui-text-align-{_css_ident(str(attrs['align_text']))}")
    if attrs.get("italic") in (True, "true", 1, "italic"):
        classes.append("ourui-italic")
    deco = attrs.get("decorate")
    for bp, d in _responsive_values(deco):
        if d in {"underline", "line-through", "no-underline"}:
            classes.append(f"ourui-{bp}-{d}" if bp else f"ourui-{d}")
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

    for bp, ov in _responsive_values(attrs.get("outline")):
        if ov in ("none", "hidden"):
            classes.append(f"ourui-{bp}-outline-{ov}" if bp else f"ourui-outline-{ov}")
        elif ov in (True, "true", 1, "outline"):
            classes.append(f"ourui-{bp}-outline" if bp else "ourui-outline")
        elif ov is not None and str(ov) in {"0", "1", "2", "4", "8"}:
            classes.append(f"ourui-{bp}-outline-{ov}" if bp else f"ourui-outline-{ov}")
    oc = attrs.get("outline_color")
    if isinstance(oc, str) and oc in {"primary", "accent", "muted", "danger", "border", "fg", "bg"}:
        classes.append(f"ourui-outline-color-{oc}")
    oo = attrs.get("outline_offset")
    if oo is not None and str(oo) in {"0", "1", "2", "4", "8"}:
        classes.append(f"ourui-outline-offset-{oo}")

    ac = attrs.get("accent_color") or attrs.get("accent")
    if isinstance(ac, str) and ac in {"primary", "accent", "muted", "danger", "border", "fg", "bg"}:
        classes.append(f"ourui-accent-color-{ac}")

    fn = attrs.get("font_numeric")
    _fn_map = {
        "normal": "normal",
        "ordinal": "ordinal",
        "slashed-zero": "slashed-zero",
        "slashed_zero": "slashed-zero",
        "lining": "lining",
        "lining-nums": "lining",
        "oldstyle": "oldstyle",
        "oldstyle-nums": "oldstyle",
        "proportional": "proportional",
        "proportional-nums": "proportional",
        "tabular": "tabular",
        "tabular-nums": "tabular",
        "diagonal-fractions": "diagonal-fractions",
        "stacked-fractions": "stacked-fractions",
    }
    if isinstance(fn, str) and fn in _fn_map:
        classes.append(f"ourui-font-numeric-{_fn_map[fn]}")

    _stretch_keys = {
        "ultra-condensed",
        "extra-condensed",
        "condensed",
        "semi-condensed",
        "normal",
        "semi-expanded",
        "expanded",
        "extra-expanded",
        "ultra-expanded",
    }
    fs = attrs.get("font_stretch")
    if isinstance(fs, str):
        key = fs.replace("_", "-")
        if key in _stretch_keys:
            classes.append(f"ourui-font-stretch-{key}")

    _feat_keys = {
        "normal",
        "liga",
        "no-liga",
        "dlig",
        "no-dlig",
        "hist",
        "calt",
        "no-calt",
        "ss01",
        "ss02",
        "ss03",
        "ss04",
        "cv01",
        "cv02",
        "cv03",
        "cv04",
        "smcp",
    }
    ff = attrs.get("font_feature")
    if isinstance(ff, str):
        key = ff.replace("_", "-")
        if key in _feat_keys:
            classes.append(f"ourui-font-feature-{key}")

    _pseudo_roles = {"primary", "accent", "muted", "danger", "border", "fg", "bg", "card"}
    pc = attrs.get("placeholder_color")
    if isinstance(pc, str) and pc in _pseudo_roles and pc != "card":
        classes.append(f"ourui-placeholder-color-{pc}")
    sel_bag = attrs.get("selection")
    sel_bg = attrs.get("selection_bg")
    sel_fg = attrs.get("selection_color")
    if isinstance(sel_bag, dict):
        if sel_bg is None:
            sel_bg = sel_bag.get("bg")
        if sel_fg is None:
            sel_fg = sel_bag.get("color") or sel_bag.get("fg")
    if isinstance(sel_bg, str) and sel_bg in _pseudo_roles:
        classes.append(f"ourui-selection-bg-{sel_bg}")
    if isinstance(sel_fg, str) and sel_fg in _pseudo_roles:
        classes.append(f"ourui-selection-color-{sel_fg}")

    sh = attrs.get("shadow") or attrs.get("elev")
    for bp, sv in _responsive_values(sh):
        if sv in {"sm", "md", "lg", "none"}:
            classes.append(f"ourui-{bp}-shadow-{sv}" if bp else f"ourui-shadow-{sv}")
    ring = attrs.get("ring")
    ring_inset = attrs.get("ring_inset") in (True, "true", 1, "inset")
    for bp, rv in _responsive_values(ring):
        if rv in (True, "true", 1, "ring"):
            if ring_inset and bp is None:
                classes.append("ourui-ring-inset")
            elif bp:
                classes.append(f"ourui-{bp}-ring")
            else:
                classes.append("ourui-ring")
        elif rv is not None and str(rv) in RING:
            key = str(rv)
            if ring_inset and bp is None:
                classes.append(f"ourui-ring-inset-{key}")
            elif bp:
                classes.append(f"ourui-{bp}-ring-{key}")
            else:
                classes.append(f"ourui-ring-{key}")
    rc = attrs.get("ring_color")
    if isinstance(rc, str) and rc in {"primary", "accent", "muted", "danger", "border", "fg", "bg"}:
        classes.append(f"ourui-ring-color-{rc}")

    div = attrs.get("divide")
    if div in ("x", "y"):
        classes.append(f"ourui-divide-{div}")
    elif div in (True, "true", 1, "divide"):
        classes.append("ourui-divide-y")
    dw = attrs.get("divide_w")
    if dw is not None and str(dw) in {"0", "1", "2", "4", "8"}:
        classes.append(f"ourui-divide-w-{dw}")
    dc = attrs.get("divide_color")
    if isinstance(dc, str) and dc in {"primary", "accent", "muted", "danger", "border", "fg", "bg"}:
        classes.append(f"ourui-divide-color-{dc}")

    if attrs.get("sr_only") in (True, "true", 1, "sr-only", "sr_only"):
        classes.append("ourui-sr-only")

    caret = attrs.get("caret_color") or attrs.get("caret")
    if isinstance(caret, str) and caret in {"primary", "accent", "muted", "danger", "border", "fg", "bg"}:
        classes.append(f"ourui-caret-{caret}")

    grad = attrs.get("bg_gradient")
    if isinstance(grad, str) and grad in {
        "to-t",
        "to-tr",
        "to-r",
        "to-br",
        "to-b",
        "to-bl",
        "to-l",
        "to-tl",
    }:
        classes.append(f"ourui-bg-gradient-{grad}")
    bi = attrs.get("bg_image")
    if bi == "none":
        classes.append("ourui-bg-image-none")
    # URL form handled in inline_literal_rules → per-node background-image

    mb = attrs.get("mix_blend")
    if isinstance(mb, str):
        key = mb.replace("_", "-")
        if key in _MIX_BLEND_MODES:
            classes.append(f"ourui-mix-blend-{key}")
    bb = attrs.get("backdrop_blend")
    if isinstance(bb, str):
        key = bb.replace("_", "-")
        if key in _MIX_BLEND_MODES:
            classes.append(f"ourui-backdrop-blend-{key}")
    mk = attrs.get("mask")
    if isinstance(mk, str):
        key = mk.replace("_", "-")
        if key in _MASK_PRESETS:
            classes.append(f"ourui-mask-{key}")

    gf = attrs.get("gradient_from")
    if isinstance(gf, str) and gf in {"primary", "accent", "muted", "danger", "border", "fg", "bg"}:
        classes.append(f"ourui-gradient-from-{gf}")
    gt = attrs.get("gradient_to")
    if isinstance(gt, str) and gt in {"primary", "accent", "muted", "danger", "border", "fg", "bg"}:
        classes.append(f"ourui-gradient-to-{gt}")

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

    ap = attrs.get("appearance")
    if ap in {"none", "auto"}:
        classes.append(f"ourui-appearance-{ap}")
    cs = attrs.get("color_scheme")
    if cs in {"normal", "light", "dark", "light-dark"}:
        classes.append(f"ourui-color-scheme-{cs}")
    fs = attrs.get("field_sizing")
    if fs in {"content", "fixed"}:
        classes.append(f"ourui-field-sizing-{fs}")
    sw = attrs.get("scrollbar_width")
    if sw in {"auto", "thin", "none"}:
        classes.append(f"ourui-scrollbar-width-{sw}")
    sg = attrs.get("scrollbar_gutter")
    if sg in {"auto", "stable"}:
        classes.append(f"ourui-scrollbar-gutter-{sg}")
    elif sg in {"stable-both", "stable_both", "both-edges"}:
        classes.append("ourui-scrollbar-gutter-stable-both")
    sc = attrs.get("scrollbar_color")
    if sc == "auto":
        classes.append("ourui-scrollbar-color-auto")
    elif isinstance(sc, str) and sc in {"primary", "accent", "muted", "danger", "border", "fg", "bg"}:
        classes.append(f"ourui-scrollbar-color-{sc}")
    ts = attrs.get("tab_size")
    if ts is not None and str(ts) in {"0", "2", "4", "8"}:
        classes.append(f"ourui-tab-size-{ts}")
    add("text-indent", attrs.get("text_indent"))
    zm = attrs.get("zoom")
    if zm is not None and str(zm) in {"0", "50", "75", "90", "95", "100", "105", "110", "125", "150"}:
        classes.append(f"ourui-zoom-{zm}")
    bf = attrs.get("backface")
    if bf in {"visible", "hidden"}:
        classes.append(f"ourui-backface-{bf}")

    # container-type host (TW @container)
    ct = attrs.get("container")
    if ct in (True, "true", 1, "normal", "inline-size"):
        classes.append("ourui-container")
    elif isinstance(ct, str) and _CONTAINER_NAME_RE.fullmatch(ct):
        classes.append("ourui-container")
        # container-name via per-node rule in inline_literal_rules

    # before/after CSS content (TW content-* + before:/after: — not Text ``content=``)
    def _pseudo_content_classes(side: str, raw: Any) -> None:
        val = raw
        if isinstance(raw, dict):
            val = raw.get("content")
        css_val = _css_content_value(val) if val is not None else None
        if css_val is None:
            return
        if css_val == "none":
            classes.append(f"ourui-{side}-content-none")
        elif css_val == '""':
            classes.append(f"ourui-{side}-content-empty")

    before_raw = attrs.get("before_content")
    if before_raw is None:
        before_raw = attrs.get("before")
    after_raw = attrs.get("after_content")
    if after_raw is None:
        after_raw = attrs.get("after")
    _pseudo_content_classes("before", before_raw)
    _pseudo_content_classes("after", after_raw)

    # hover= / focus= bags (multi-prop state overrides)
    _bg_roles = {"primary", "accent", "muted", "danger", "border", "fg", "bg", "card"}
    for state in _STATE_VARIANTS:
        bag = attrs.get(state)
        if not isinstance(bag, dict):
            continue
        if "opacity" in bag:
            add("opacity", {state: bag["opacity"]})
        sh_v = bag.get("shadow") if bag.get("shadow") is not None else bag.get("elev")
        if sh_v is not None:
            for bp, sv in _responsive_values({state: sh_v}):
                if sv in {"sm", "md", "lg", "none"}:
                    classes.append(f"ourui-{bp}-shadow-{sv}" if bp else f"ourui-shadow-{sv}")
        if "scale" in bag:
            add("scale", {state: bag["scale"]})
        deco_v = bag.get("decorate")
        if deco_v in {"underline", "line-through", "no-underline"}:
            classes.append(f"ourui-{state}-{deco_v}")
        ring_v = bag.get("ring")
        if ring_v in (True, "true", 1, "ring"):
            classes.append(f"ourui-{state}-ring")
        elif ring_v is not None and str(ring_v) in RING:
            classes.append(f"ourui-{state}-ring-{ring_v}")
        ol_v = bag.get("outline")
        if ol_v in (True, "true", 1, "outline"):
            classes.append(f"ourui-{state}-outline")
        elif ol_v is not None and str(ol_v) in {"0", "1", "2", "4", "8"}:
            classes.append(f"ourui-{state}-outline-{ol_v}")
        bg_v = bag.get("bg")
        if isinstance(bg_v, str) and bg_v in _bg_roles:
            classes.append(f"ourui-{state}-bg-{bg_v}")

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
    bi = attrs.get("bg_image")
    if isinstance(bi, str) and bi != "none":
        url = _safe_bg_url(bi)
        if url:
            decls.append(f'  background-image: url("{url}");')
    ct = attrs.get("container")
    if isinstance(ct, str) and ct not in {"normal", "inline-size", "true"} and _CONTAINER_NAME_RE.fullmatch(ct):
        decls.append(f"  container-name: {ct};")

    chunks: list[str] = []
    if decls:
        chunks.append(f'[data-ourui-id="{nid}"] {{\n' + "\n".join(decls) + "\n}\n")

    for side, keys in (
        ("before", ("before_content", "before")),
        ("after", ("after_content", "after")),
    ):
        raw: Any = None
        for k in keys:
            if attrs.get(k) is not None:
                raw = attrs.get(k)
                break
        val = raw.get("content") if isinstance(raw, dict) else raw
        css_val = _css_content_value(val) if val is not None else None
        if css_val is None or css_val in {"none", '""'}:
            continue
        # open-quote etc. or quoted string → per-node pseudo
        chunks.append(f'[data-ourui-id="{nid}"]::{side} {{\n  content: {css_val};\n}}\n')

    return "".join(chunks)
