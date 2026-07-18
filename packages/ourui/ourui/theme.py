"""OurUI design tokens — pack seed + CSS var helpers (not emit authority).

Emit consumes Resolved Design (RFC-003). DEFAULT_* / default_tokens() seed
`ourui.design.resolve` / `ui.Theme` analysis only.
"""

from __future__ import annotations

from typing import Any

# Logical token keys (authoring + dump). CSS vars are --ourui-<key with _ → -> -> -> -).
TOKEN_KEYS: tuple[str, ...] = (
    # Color
    "bg",
    "fg",
    "primary",
    "primary_fg",
    "muted",
    "muted_fg",
    "border",
    "card",
    "card_fg",
    "accent",
    "accent_fg",
    "danger",
    "danger_fg",
    # Shape
    "radius",
    # Space scale (S3)
    "space_xs",
    "space_sm",
    "space_md",
    "space_lg",
    "space_xl",
    "space_2xl",
    # Type (S3)
    "font_sans",
    "font_display",
    "text_xs",
    "text_sm",
    "text_md",
    "text_lg",
    "text_xl",
    "text_2xl",
    "leading_tight",
    "leading_normal",
    "leading_relaxed",
    # Elevation (S3)
    "elev_0",
    "elev_1",
    "elev_2",
    "elev_3",
)

# Semantic color roles usable in color= / bg=
COLOR_TOKEN_NAMES: tuple[str, ...] = (
    "primary",
    "muted",
    "accent",
    "danger",
    "card",
    "bg",
    "fg",
)

_TYPE_SPACE_ELEV: dict[str, str] = {
    "space_xs": "0.25rem",
    "space_sm": "0.5rem",
    "space_md": "0.75rem",
    "space_lg": "1.25rem",
    "space_xl": "2rem",
    "space_2xl": "3rem",
    "font_sans": '"DM Sans", "Segoe UI", system-ui, sans-serif',
    "font_display": '"Fraunces", "Iowan Old Style", Georgia, serif',
    "text_xs": "0.75rem",
    "text_sm": "0.875rem",
    "text_md": "1rem",
    "text_lg": "1.25rem",
    "text_xl": "1.75rem",
    "text_2xl": "2.5rem",
    "leading_tight": "1.2",
    "leading_normal": "1.5",
    "leading_relaxed": "1.7",
    "elev_0": "none",
    "elev_1": "0 1px 2px color-mix(in srgb, var(--ourui-fg) 12%, transparent)",
    "elev_2": "0 4px 14px color-mix(in srgb, var(--ourui-fg) 14%, transparent)",
    "elev_3": "0 12px 32px color-mix(in srgb, var(--ourui-fg) 18%, transparent)",
}

DEFAULT_LIGHT: dict[str, str] = {
    "bg": "#f7f6f2",
    "fg": "#1c1917",
    "primary": "#1a5f4a",
    "primary_fg": "#f5faf8",
    "muted": "#e7e5e0",
    "muted_fg": "#57534e",
    "border": "#d6d3d1",
    "card": "#ffffff",
    "card_fg": "#1c1917",
    "accent": "#0f766e",
    "accent_fg": "#f0fdfa",
    "danger": "#b91c1c",
    "danger_fg": "#fef2f2",
    "radius": "0.5rem",
    **_TYPE_SPACE_ELEV,
}

DEFAULT_DARK: dict[str, str] = {
    "bg": "#1c1917",
    "fg": "#f5f5f4",
    "primary": "#2dd4a8",
    "primary_fg": "#042f2e",
    "muted": "#292524",
    "muted_fg": "#a8a29e",
    "border": "#44403c",
    "card": "#292524",
    "card_fg": "#f5f5f4",
    "accent": "#14b8a6",
    "accent_fg": "#042f2e",
    "danger": "#f87171",
    "danger_fg": "#1c1917",
    "radius": "0.5rem",
    **_TYPE_SPACE_ELEV,
}

# Map Theme kwarg names → token keys (identity for all TOKEN_KEYS)
_KWARG_TO_KEY: dict[str, str] = {k: k for k in TOKEN_KEYS}


def css_var_name(key: str) -> str:
    return f"--ourui-{key.replace('_', '-')}"


def default_tokens() -> dict[str, dict[str, str]]:
    return {
        "light": dict(DEFAULT_LIGHT),
        "dark": dict(DEFAULT_DARK),
    }


def apply_theme_overrides(
    base: dict[str, dict[str, str]],
    *,
    light: dict[str, Any] | None = None,
    dark: dict[str, Any] | None = None,
) -> dict[str, dict[str, str]]:
    out = {
        "light": dict(base["light"]),
        "dark": dict(base["dark"]),
    }
    if light:
        for raw_key, value in light.items():
            key = _KWARG_TO_KEY.get(str(raw_key), str(raw_key))
            if key in TOKEN_KEYS and value is not None:
                out["light"][key] = str(value)
    if dark:
        for raw_key, value in dark.items():
            key = _KWARG_TO_KEY.get(str(raw_key), str(raw_key))
            if key in TOKEN_KEYS and value is not None:
                out["dark"][key] = str(value)
    return out


def theme_kwargs_to_overrides(attrs: dict[str, Any]) -> tuple[dict[str, str], dict[str, str]]:
    """Split ui.Theme kwargs into light overrides and optional dark dict."""
    light: dict[str, str] = {}
    dark: dict[str, str] = {}
    for key, value in attrs.items():
        if key == "dark" and isinstance(value, dict):
            for dk, dv in value.items():
                mapped = _KWARG_TO_KEY.get(str(dk), str(dk))
                if mapped in TOKEN_KEYS and dv is not None:
                    dark[mapped] = str(dv)
            continue
        if key == "name":
            continue
        mapped = _KWARG_TO_KEY.get(key, key)
        if mapped in TOKEN_KEYS and value is not None and not isinstance(value, dict):
            light[mapped] = str(value)
    return light, dark


def emit_tokens_css(tokens: dict[str, dict[str, str]]) -> str:
    """Emit :root and .dark blocks for --ourui-* variables."""
    lines: list[str] = [":root {"]
    for key in TOKEN_KEYS:
        val = tokens.get("light", {}).get(key, DEFAULT_LIGHT[key])
        lines.append(f"  {css_var_name(key)}: {val};")
    lines.append("}")
    lines.append(".dark {")
    for key in TOKEN_KEYS:
        val = tokens.get("dark", {}).get(key, DEFAULT_DARK[key])
        lines.append(f"  {css_var_name(key)}: {val};")
    lines.append("}")
    return "\n".join(lines) + "\n"
