"""Named Design System packs + recipes (anti-slop catalog).

Packs = brand/expression axes (not a utility shuffle).
Recipes = intentional bundles (pack + density + page chrome).

Avoided on purpose: purple/indigo defaults, cream+serif+terracotta brochure,
broadsheet newspaper chrome, neon accents.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from ourui.theme import DEFAULT_DARK, DEFAULT_LIGHT, TOKEN_KEYS

PACK_VERSION = "1.1.0"

# Shared type/space/elev — IBM Plex only (no Fraunces / display-serif brochure).
_TYPE_SPACE_ELEV: dict[str, str] = {
    "space_xs": "0.25rem",
    "space_sm": "0.5rem",
    "space_md": "0.75rem",
    "space_lg": "1.25rem",
    "space_xl": "2rem",
    "space_2xl": "3rem",
    "font_sans": '"IBM Plex Sans", "Segoe UI", system-ui, sans-serif',
    "font_display": '"IBM Plex Sans", "Segoe UI", system-ui, sans-serif',
    "text_xs": "0.75rem",
    "text_sm": "0.875rem",
    "text_md": "1rem",
    "text_lg": "1.125rem",
    "text_xl": "1.5rem",
    "text_2xl": "2rem",
    "leading_tight": "1.25",
    "leading_normal": "1.5",
    "leading_relaxed": "1.65",
    "elev_0": "none",
    "elev_1": "0 1px 2px color-mix(in srgb, var(--ourui-fg) 8%, transparent)",
    "elev_2": "0 4px 16px color-mix(in srgb, var(--ourui-fg) 10%, transparent)",
    "elev_3": "0 12px 28px color-mix(in srgb, var(--ourui-fg) 14%, transparent)",
}

DENSITY_COMPACT: dict[str, str] = {
    "space_sm": "0.375rem",
    "space_md": "0.5rem",
    "space_lg": "0.75rem",
}

_CONTROL = {
    "pad_block": "space_sm",
    "pad_inline": "space_md",
    "radius": "radius",
}

_PAGE_PRODUCT = {
    "max_width": "42rem",
    "pad_block": "space_xl",
    "pad_inline": "space_lg",
    "gap": "space_lg",
}


def _modes(light: dict[str, str], dark: dict[str, str]) -> dict[str, dict[str, str]]:
    return {"light": dict(light), "dark": dict(dark)}


def _pack(
    pack_id: str,
    *,
    light: dict[str, str],
    dark: dict[str, str],
    page: dict[str, str] | None = None,
    density_default: str = "comfortable",
    label: str = "",
) -> dict[str, Any]:
    return {
        "id": pack_id,
        "version": PACK_VERSION,
        "label": label,
        "modes": _modes(light, dark),
        "control": dict(_CONTROL),
        "page": dict(page or _PAGE_PRODUCT),
        "density": {
            "default": density_default,
            "compact": dict(DENSITY_COMPACT),
        },
    }


# --- ourui-default: zinc / ink product (existing 1.0.1 defaults) ---------------

_DEFAULT_LIGHT = dict(DEFAULT_LIGHT)
_DEFAULT_DARK = dict(DEFAULT_DARK)

# --- ourui-editorial: warm stone, sharp radius (NOT cream brochure) ------------

_EDITORIAL_LIGHT: dict[str, str] = {
    "bg": "#f5f5f4",  # stone-100
    "fg": "#1c1917",  # stone-900
    "primary": "#1c1917",
    "primary_fg": "#fafaf9",
    "muted": "#e7e5e4",
    "muted_fg": "#78716c",
    "border": "#d6d3d1",
    "card": "#fafaf9",
    "card_fg": "#1c1917",
    "accent": "#44403c",  # stone-700 — quiet ink accent, not teal/terracotta
    "accent_fg": "#fafaf9",
    "danger": "#b91c1c",
    "danger_fg": "#fef2f2",
    "radius": "0",
    **_TYPE_SPACE_ELEV,
    "text_xl": "1.625rem",
    "text_2xl": "2.125rem",
    "leading_relaxed": "1.7",
    "elev_1": "none",
    "elev_2": "none",
    "elev_3": "0 1px 0 color-mix(in srgb, var(--ourui-fg) 12%, transparent)",
}

_EDITORIAL_DARK: dict[str, str] = {
    "bg": "#1c1917",
    "fg": "#fafaf9",
    "primary": "#fafaf9",
    "primary_fg": "#1c1917",
    "muted": "#292524",
    "muted_fg": "#a8a29e",
    "border": "#44403c",
    "card": "#292524",
    "card_fg": "#fafaf9",
    "accent": "#a8a29e",
    "accent_fg": "#1c1917",
    "danger": "#f87171",
    "danger_fg": "#450a0a",
    "radius": "0",
    **_TYPE_SPACE_ELEV,
    "text_xl": "1.625rem",
    "text_2xl": "2.125rem",
    "leading_relaxed": "1.7",
    "elev_1": "none",
    "elev_2": "none",
    "elev_3": "0 1px 0 color-mix(in srgb, var(--ourui-fg) 20%, transparent)",
}

# --- ourui-console: cool slate + restrained cyan (ops / data) ------------------

_CONSOLE_LIGHT: dict[str, str] = {
    "bg": "#f8fafc",  # slate-50
    "fg": "#0f172a",  # slate-900
    "primary": "#0f172a",
    "primary_fg": "#f8fafc",
    "muted": "#f1f5f9",
    "muted_fg": "#64748b",
    "border": "#e2e8f0",
    "card": "#ffffff",
    "card_fg": "#0f172a",
    "accent": "#0e7490",  # cyan-700 — not neon cyan / not purple
    "accent_fg": "#ecfeff",
    "danger": "#dc2626",
    "danger_fg": "#fef2f2",
    "radius": "0.25rem",
    **_TYPE_SPACE_ELEV,
    "text_md": "0.9375rem",
    "text_sm": "0.8125rem",
    "elev_1": "0 1px 2px color-mix(in srgb, var(--ourui-fg) 6%, transparent)",
    "elev_2": "0 2px 8px color-mix(in srgb, var(--ourui-fg) 8%, transparent)",
    "elev_3": "0 8px 20px color-mix(in srgb, var(--ourui-fg) 10%, transparent)",
}

_CONSOLE_DARK: dict[str, str] = {
    "bg": "#020617",
    "fg": "#f8fafc",
    "primary": "#f8fafc",
    "primary_fg": "#020617",
    "muted": "#1e293b",
    "muted_fg": "#94a3b8",
    "border": "#334155",
    "card": "#0f172a",
    "card_fg": "#f8fafc",
    "accent": "#0891b2",
    "accent_fg": "#ecfeff",
    "danger": "#f87171",
    "danger_fg": "#450a0a",
    "radius": "0.25rem",
    **_TYPE_SPACE_ELEV,
    "text_md": "0.9375rem",
    "text_sm": "0.8125rem",
}

PACKS: dict[str, dict[str, Any]] = {
    "ourui-default": _pack(
        "ourui-default",
        light=_DEFAULT_LIGHT,
        dark=_DEFAULT_DARK,
        label="Zinc/ink product UI",
    ),
    "ourui-editorial": _pack(
        "ourui-editorial",
        light=_EDITORIAL_LIGHT,
        dark=_EDITORIAL_DARK,
        page={
            "max_width": "36rem",
            "pad_block": "space_xl",
            "pad_inline": "space_lg",
            "gap": "space_lg",
        },
        label="Warm stone, sharp edges, reading measure",
    ),
    "ourui-console": _pack(
        "ourui-console",
        light=_CONSOLE_LIGHT,
        dark=_CONSOLE_DARK,
        page={
            "max_width": "80rem",
            "pad_block": "space_lg",
            "pad_inline": "space_lg",
            "gap": "space_md",
        },
        density_default="compact",
        label="Cool slate ops/console surfaces",
    ),
}

# Recipes = intentional combinations (not free shuffle).
RECIPES: dict[str, dict[str, Any]] = {
    "product": {
        "pack": "ourui-default",
        "density": "comfortable",
        "label": "Default product screens",
    },
    "ops": {
        "pack": "ourui-default",
        "density": "compact",
        "page": {
            "max_width": "72rem",
            "pad_block": "space_lg",
            "pad_inline": "space_lg",
            "gap": "space_md",
        },
        "label": "Admin/ops density on product pack",
    },
    "editorial": {
        "pack": "ourui-editorial",
        "density": "comfortable",
        "label": "Long-form / reading surfaces",
    },
    "console": {
        "pack": "ourui-console",
        "density": "compact",
        "label": "Wide dense console / tables",
    },
}

DEFAULT_PACK_ID = "ourui-default"


def list_packs() -> list[str]:
    return sorted(PACKS)


def list_recipes() -> list[str]:
    return sorted(RECIPES)


def get_pack(pack_id: str | None) -> dict[str, Any]:
    key = pack_id if pack_id in PACKS else DEFAULT_PACK_ID
    return deepcopy(PACKS[key])


def get_recipe(recipe_id: str | None) -> dict[str, Any] | None:
    if not recipe_id or recipe_id not in RECIPES:
        return None
    return dict(RECIPES[recipe_id])


def materialize_pack(
    *,
    pack_id: str | None = None,
    recipe_id: str | None = None,
) -> dict[str, Any]:
    """Resolve pack (+ optional recipe page/density defaults) for resolve_design."""
    recipe = get_recipe(recipe_id)
    if recipe is not None:
        pack_id = str(recipe.get("pack") or pack_id or DEFAULT_PACK_ID)
    pack = get_pack(pack_id)
    if recipe is not None:
        page_over = recipe.get("page")
        if isinstance(page_over, dict):
            pack["page"] = {**(pack.get("page") or {}), **page_over}
        dens = recipe.get("density")
        if dens in {"compact", "comfortable"}:
            dens_meta = dict(pack.get("density") or {})
            dens_meta["default"] = dens
            pack["density"] = dens_meta
        pack["recipe"] = recipe_id
    return pack


def pack_token_seed(pack_id: str | None = None) -> dict[str, dict[str, str]]:
    """Light/dark token maps for Semantic Graph init / Theme reset."""
    pack = get_pack(pack_id)
    modes = pack.get("modes") or {}
    light = {k: modes.get("light", {}).get(k, DEFAULT_LIGHT[k]) for k in TOKEN_KEYS}
    dark = {k: modes.get("dark", {}).get(k, DEFAULT_DARK[k]) for k in TOKEN_KEYS}
    return {"light": light, "dark": dark}
