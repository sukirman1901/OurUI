# Design resolution package (RFC-002).

from ourui.design.motion import (
    MOTION_CATALOG_VERSION,
    MOTION_INTENTS,
    catalog_summary,
    list_patterns,
    motion_css_class,
    resolve_motion,
)
from ourui.design.resolve import (
    DEFAULT_PAGE,
    DENSITY_COMPACT,
    ResolvedDesign,
    resolve_design,
)
from ourui.design.style_catalog import catalog_summary as style_catalog_summary

__all__ = [
    "DEFAULT_PAGE",
    "DENSITY_COMPACT",
    "MOTION_CATALOG_VERSION",
    "MOTION_INTENTS",
    "ResolvedDesign",
    "catalog_summary",
    "list_patterns",
    "motion_css_class",
    "resolve_design",
    "resolve_motion",
    "style_catalog_summary",
]
