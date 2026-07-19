"""Design scales for OurUI tokens (intent props → ``--ourui-*``, not class-string API).

Numeric space/size/type tables power finite ``.ourui-*`` utilities.
"""

from __future__ import annotations

from typing import Any

# Spacing scale (rem) — Tailwind-compatible numeric + named aliases
SPACE: dict[str, str] = {
    "0": "0",
    "px": "1px",
    "0.5": "0.125rem",
    "1": "0.25rem",
    "1.5": "0.375rem",
    "2": "0.5rem",
    "2.5": "0.625rem",
    "3": "0.75rem",
    "3.5": "0.875rem",
    "4": "1rem",
    "5": "1.25rem",
    "6": "1.5rem",
    "7": "1.75rem",
    "8": "2rem",
    "9": "2.25rem",
    "10": "2.5rem",
    "11": "2.75rem",
    "12": "3rem",
    "14": "3.5rem",
    "16": "4rem",
    "20": "5rem",
    "24": "6rem",
    "28": "7rem",
    "32": "8rem",
    "36": "9rem",
    "40": "10rem",
    "44": "11rem",
    "48": "12rem",
    "52": "13rem",
    "56": "14rem",
    "60": "15rem",
    "64": "16rem",
    "72": "18rem",
    "80": "20rem",
    "96": "24rem",
    # Aliases (existing OurUI + Tailwind-ish names)
    "none": "0",
    "xs": "0.25rem",
    "sm": "0.5rem",
    "md": "0.75rem",
    "lg": "1.25rem",
    "xl": "2rem",
    "2xl": "3rem",
}

# Container / width scale (Tailwind container-* / max-w-*)
SIZE: dict[str, str] = {
    "3xs": "16rem",
    "2xs": "18rem",
    "xs": "20rem",
    "sm": "24rem",
    "md": "28rem",
    "lg": "32rem",
    "xl": "36rem",
    "2xl": "42rem",
    "3xl": "48rem",
    "4xl": "56rem",
    "5xl": "64rem",
    "6xl": "72rem",
    "7xl": "80rem",
    "auto": "auto",
    "px": "1px",
    "full": "100%",
    "screen": "100vw",
    "dvw": "100dvw",
    "dvh": "100dvh",
    "lvw": "100lvw",
    "lvh": "100lvh",
    "svw": "100svw",
    "svh": "100svh",
    "min": "min-content",
    "max": "max-content",
    "fit": "fit-content",
}

# Width/height fractions
FRACTIONS: dict[str, str] = {
    "1/2": "50%",
    "1/3": "33.333333%",
    "2/3": "66.666667%",
    "1/4": "25%",
    "2/4": "50%",
    "3/4": "75%",
    "1/5": "20%",
    "2/5": "40%",
    "3/5": "60%",
    "4/5": "80%",
    "1/6": "16.666667%",
    "5/6": "83.333333%",
    "1/12": "8.333333%",
    "5/12": "41.666667%",
    "7/12": "58.333333%",
    "11/12": "91.666667%",
}

TEXT_SIZE: dict[str, str] = {
    "xs": "0.75rem",
    "sm": "0.875rem",
    "md": "1rem",
    "base": "1rem",
    "lg": "1.125rem",
    "xl": "1.5rem",
    "2xl": "2rem",  # aligned with theme token text_2xl
    "3xl": "2.25rem",
    "4xl": "3rem",
    "5xl": "3.75rem",
    "6xl": "4.5rem",
    "7xl": "6rem",
    "display": "clamp(2rem, 4.5vw, 3.5rem)",
}

LEADING: dict[str, str] = {
    "none": "1",
    "tight": "1.25",
    "snug": "1.375",
    "normal": "1.5",
    "relaxed": "1.65",  # aligned with theme token leading_relaxed
    "loose": "2",
}

WEIGHT: dict[str, str] = {
    "thin": "100",
    "light": "300",
    "normal": "400",
    "medium": "500",
    "semibold": "600",
    "bold": "700",
    "extrabold": "800",
    "black": "900",
}

TRACKING: dict[str, str] = {
    "tighter": "-0.05em",
    "tight": "-0.025em",
    "normal": "0em",
    "wide": "0.025em",
    "wider": "0.05em",
    "widest": "0.1em",
}

RADIUS: dict[str, str] = {
    "none": "0",
    "sm": "0.125rem",
    "md": "0.375rem",
    "lg": "0.5rem",
    "xl": "0.75rem",
    "2xl": "1rem",
    "3xl": "1.5rem",
    "full": "9999px",
}

# Ring width (px) — Tailwind v4 box-shadow ring section (ring / ring-<n>)
RING: dict[str, str] = {
    "0": "0px",
    "1": "1px",
    "2": "2px",
    "4": "4px",
    "8": "8px",
}

Z_INDEX: dict[str, str] = {
    "auto": "auto",
    "0": "0",
    "10": "10",
    "20": "20",
    "30": "30",
    "40": "40",
    "50": "50",
}

BLUR: dict[str, str] = {
    "none": "0",
    "sm": "4px",
    "md": "8px",
    "lg": "12px",
    "xl": "16px",
    "2xl": "24px",
    "3xl": "40px",
}

OPACITY: dict[str, str] = {
    "0": "0",
    "5": "0.05",
    "10": "0.1",
    "20": "0.2",
    "25": "0.25",
    "30": "0.3",
    "40": "0.4",
    "50": "0.5",
    "60": "0.6",
    "70": "0.7",
    "75": "0.75",
    "80": "0.8",
    "90": "0.9",
    "95": "0.95",
    "100": "1",
}

BREAKPOINTS: dict[str, str] = {
    "sm": "640px",
    "md": "768px",
    "lg": "1024px",
    "xl": "1280px",
    "2xl": "1536px",
}

ASPECT: dict[str, str] = {
    "auto": "auto",
    "square": "1 / 1",
    "video": "16 / 9",
    "photo": "4 / 3",
    # Tailwind-class ratios (author as aspect="16/9"; CSS ident → 16-9)
    "2/3": "2 / 3",
    "3/2": "3 / 2",
    "3/4": "3 / 4",
    "4/3": "4 / 3",
    "4/5": "4 / 5",
    "5/4": "5 / 4",
    "9/16": "9 / 16",
    "16/9": "16 / 9",
    "21/9": "21 / 9",
}

DURATION: dict[str, str] = {
    "0": "0ms",
    "75": "75ms",
    "100": "100ms",
    "150": "150ms",
    "200": "200ms",
    "300": "300ms",
    "500": "500ms",
    "700": "700ms",
    "1000": "1000ms",
}

EASING: dict[str, str] = {
    "default": "cubic-bezier(0.4, 0, 0.2, 1)",
    "linear": "linear",
    "in": "cubic-bezier(0.4, 0, 1, 1)",
    "out": "cubic-bezier(0, 0, 0.2, 1)",
    "in-out": "cubic-bezier(0.4, 0, 0.2, 1)",
    "bounce": "cubic-bezier(0.34, 1.56, 0.64, 1)",
}

ANIMATE: dict[str, str] = {
    "spin": "spin 1s linear infinite",
    "ping": "ping 1s cubic-bezier(0, 0, 0.2, 1) infinite",
    "pulse": "pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
    "bounce": "bounce 1s infinite",
}

FILTER_BRIGHTNESS: dict[str, str] = {
    "0": "0",
    "50": ".5",
    "75": ".75",
    "90": ".9",
    "95": ".95",
    "100": "1",
    "105": "1.05",
    "110": "1.1",
    "125": "1.25",
    "150": "1.5",
    "200": "2",
}

FILTER_CONTRAST: dict[str, str] = {
    "0": "0",
    "50": ".5",
    "75": ".75",
    "100": "1",
    "125": "1.25",
    "150": "1.5",
    "200": "2",
}

FILTER_SATURATE: dict[str, str] = {
    "0": "0",
    "50": ".5",
    "100": "1",
    "150": "1.5",
    "200": "2",
}

FILTER_HUE: dict[str, str] = {
    "0": "0deg",
    "15": "15deg",
    "30": "30deg",
    "60": "60deg",
    "90": "90deg",
    "180": "180deg",
}


def _css_ident(key: str) -> str:
    return key.replace("/", "-").replace(".", "-")


def emit_scale_css_vars(*, overrides: dict[str, dict[str, str]] | None = None) -> str:
    """Emit :root custom properties for all scales."""
    ov = overrides or {}
    space = {**SPACE, **(ov.get("space") or {})}
    size = {**SIZE, **(ov.get("sizes") or {})}
    text = {**TEXT_SIZE, **(ov.get("type") or {})}
    lines = [":root {"]
    for k, v in space.items():
        lines.append(f"  --ourui-space-{_css_ident(k)}: {v};")
    for k, v in size.items():
        lines.append(f"  --ourui-size-{_css_ident(k)}: {v};")
    for k, v in FRACTIONS.items():
        lines.append(f"  --ourui-frac-{_css_ident(k)}: {v};")
    for k, v in text.items():
        lines.append(f"  --ourui-text-{_css_ident(k)}: {v};")
    for k, v in LEADING.items():
        lines.append(f"  --ourui-leading-{_css_ident(k)}: {v};")
    for k, v in WEIGHT.items():
        lines.append(f"  --ourui-weight-{_css_ident(k)}: {v};")
    for k, v in TRACKING.items():
        lines.append(f"  --ourui-tracking-{_css_ident(k)}: {v};")
    for k, v in RADIUS.items():
        lines.append(f"  --ourui-radius-{_css_ident(k)}: {v};")
    for k, v in Z_INDEX.items():
        lines.append(f"  --ourui-z-{_css_ident(k)}: {v};")
    for k, v in BLUR.items():
        lines.append(f"  --ourui-blur-{_css_ident(k)}: {v};")
    for k, v in OPACITY.items():
        lines.append(f"  --ourui-opacity-{_css_ident(k)}: {v};")
    for k, v in ASPECT.items():
        lines.append(f"  --ourui-aspect-{_css_ident(k)}: {v};")
    for k, v in DURATION.items():
        lines.append(f"  --ourui-duration-{_css_ident(k)}: {v};")
    for k, v in EASING.items():
        lines.append(f"  --ourui-easing-{_css_ident(k)}: {v};")
    for k, v in ANIMATE.items():
        lines.append(f"  --ourui-animate-{_css_ident(k)}: {v};")
    for k, v in FILTER_BRIGHTNESS.items():
        lines.append(f"  --ourui-filter-brightness-{_css_ident(k)}: {v};")
    for k, v in FILTER_CONTRAST.items():
        lines.append(f"  --ourui-filter-contrast-{_css_ident(k)}: {v};")
    for k, v in FILTER_SATURATE.items():
        lines.append(f"  --ourui-filter-saturate-{_css_ident(k)}: {v};")
    for k, v in FILTER_HUE.items():
        lines.append(f"  --ourui-filter-hue-{_css_ident(k)}: {v};")
    lines.append("}")
    return "\n".join(lines) + "\n"


def resolve_length(value: str, *, kind: str = "size") -> str | None:
    """Map intent value → CSS length. kind: size|space|frac|literal."""
    if not isinstance(value, str) or not value:
        return None
    v = value.strip()
    if kind == "space" and v in SPACE:
        return f"var(--ourui-space-{_css_ident(v)})"
    if v in SIZE:
        return f"var(--ourui-size-{_css_ident(v)})"
    if v in FRACTIONS:
        return f"var(--ourui-frac-{_css_ident(v)})"
    if v in SPACE and kind in {"space", "any"}:
        return f"var(--ourui-space-{_css_ident(v)})"
    # Allowlisted literals
    if v.endswith(("%", "rem", "em", "px", "vh", "vw", "dvh", "dvw", "svh", "svw", "ch", "fr")):
        return v
    if v in {"0", "auto", "none", "inherit", "unset"}:
        return v
    return None


def scale_catalog() -> dict[str, Any]:
    return {
        "space": dict(SPACE),
        "sizes": dict(SIZE),
        "fractions": dict(FRACTIONS),
        "text": dict(TEXT_SIZE),
        "leading": dict(LEADING),
        "weight": dict(WEIGHT),
        "tracking": dict(TRACKING),
        "radius": dict(RADIUS),
        "z_index": dict(Z_INDEX),
        "blur": dict(BLUR),
        "opacity": dict(OPACITY),
        "breakpoints": dict(BREAKPOINTS),
        "aspect": dict(ASPECT),
        "durations": dict(DURATION),
        "easings": dict(EASING),
        "animate": dict(ANIMATE),
        "filter_brightness": dict(FILTER_BRIGHTNESS),
        "filter_contrast": dict(FILTER_CONTRAST),
        "filter_saturate": dict(FILTER_SATURATE),
        "filter_hue": dict(FILTER_HUE),
    }
