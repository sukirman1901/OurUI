"""OurUI Motion Vocabulary — named family.pattern intents (ADR-012).

Authors call patterns by name; the compiler emits CSS/JS presets.
Catalog M1–M3: all registered patterns are Stable with host emit.
Legacy S4m aliases: enter → reveal.fade-up, reveal → reveal.mask-wipe, press → press.scale.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

MOTION_CATALOG_VERSION = "1.2.0"

LEGACY_ALIASES: dict[str, str] = {
    "enter": "reveal.fade-up",
    "reveal": "reveal.mask-wipe",
    "press": "press.scale",
}


@dataclass(frozen=True)
class MotionPattern:
    id: str
    family: str
    status: str
    lane: str
    definition: str
    emit: bool = False


def _p(
    pid: str,
    *,
    status: str = "experimental",
    lane: str = "marketing",
    definition: str = "",
    emit: bool = False,
) -> MotionPattern:
    family = pid.split(".", 1)[0]
    return MotionPattern(
        id=pid,
        family=family,
        status=status,
        lane=lane,
        definition=definition or pid,
        emit=emit,
    )

# --- M1 ---
_M1: tuple[MotionPattern, ...] = (
    _p("reveal.fade-up", status="stable", lane='product', definition='Opacity 0→1 + slight translateY', emit=True),
    _p("reveal.fade", status="stable", lane='product', definition='Opacity-only enter', emit=True),
    _p("reveal.mask-wipe", status="stable", lane='both', definition='Clip-path wipe reveal', emit=True),
    _p("press.scale", status="stable", lane='product', definition='Scale down on :active', emit=True),
    _p("hover.lift", status="stable", lane='product', definition='Slight lift + depth on hover', emit=True),
    _p("hover.underline-slide", status="stable", lane='product', definition='Underline expands on hover/focus', emit=True),
    _p("text.line-mask", status="stable", lane='both', definition='Block text rises from a mask', emit=True),
    _p("text.fade-up", status="stable", lane='product', definition='Text block fade-up enter', emit=True),
    _p("text.word-reveal", status="stable", lane='marketing', definition='Words stagger in (host splits text)', emit=True),
    _p("feedback.toast-slide", status="stable", lane='product', definition='Toast edge slide enter', emit=True),
    _p("feedback.success-pulse", status="stable", lane='product', definition='One-shot success pulse ring', emit=True),
    _p("scroll.fade-in-view", status="stable", lane='product', definition='Fade-up when entering viewport (once)', emit=True),
)

# --- M2 ---
_M2: tuple[MotionPattern, ...] = (
    _p("reveal.split", status="stable", lane='marketing', definition='Split reveal from center', emit=True),
    _p("reveal.curtain", status="stable", lane='marketing', definition='Curtain open left/right', emit=True),
    _p("reveal.ink", status="stable", lane='marketing', definition='Radial ink spread', emit=True),
    _p("reveal.stagger-children", status="stable", lane='both', definition='Direct children stagger in', emit=True),
    _p("reveal.blur-in", status="stable", lane='marketing', definition='Blur→sharp + opacity', emit=True),
    _p("reveal.scale-fade", status="stable", lane='both', definition='Scale 0.96→1 + fade', emit=True),
    _p("text.char-reveal", status="stable", lane='marketing', definition='Character stagger reveal', emit=True),
    _p("text.typewriter", status="stable", lane='marketing', definition='Typewriter character reveal', emit=True),
    _p("text.marquee", status="stable", lane='marketing', definition='Headline horizontal marquee', emit=True),
    _p("text.underline-reveal", status="stable", lane='marketing', definition='Underline grows under text', emit=True),
    _p("text.gradient-shift", status="stable", lane='marketing', definition='Animated gradient on text', emit=True),
    _p("flow.logo-marquee", status="stable", lane='marketing', definition='Children scroll as logo marquee', emit=True),
    _p("hover.glow", status="stable", lane='marketing', definition='Accent glow on hover', emit=True),
    _p("hover.color-shift", status="stable", lane='product', definition='Token color shift on hover', emit=True),
    _p("spotlight.dim-siblings", status="stable", lane='marketing', definition='Hover one → dim siblings', emit=True),
    _p("micro.skeleton-shimmer", status="stable", lane='product', definition='Skeleton placeholder shine', emit=True),
    _p("hero.stagger-copy", status="stable", lane='marketing', definition='Hero title/sub/CTA stagger', emit=True),
)

# --- M3 (remainder of catalog) ---
_M3: tuple[MotionPattern, ...] = (
    _p("flow.autoplay-pause", status="stable", lane='marketing', definition='Autoplay with pause', emit=True),
    _p("flow.card-rail", status="stable", lane='marketing', definition='Draggable card rail', emit=True),
    _p("flow.center-carousel", status="stable", lane='marketing', definition='Center scale carousel', emit=True),
    _p("flow.fade-carousel", status="stable", lane='marketing', definition='Fade carousel', emit=True),
    _p("flow.filmstrip", status="stable", lane='marketing', definition='Filmstrip', emit=True),
    _p("flow.infinite-slider", status="stable", lane='marketing', definition='Infinite slider', emit=True),
    _p("flow.peek-carousel", status="stable", lane='marketing', definition='Peek carousel', emit=True),
    _p("flow.snap-carousel", status="stable", lane='marketing', definition='Snap carousel', emit=True),
    _p("flow.story-rail", status="stable", lane='marketing', definition='Story rail', emit=True),
    _p("flow.thumbnail-sync", status="stable", lane='marketing', definition='Thumb sync', emit=True),
    _p("flow.vertical-marquee", status="stable", lane='marketing', definition='Vertical marquee', emit=True),
    _p("grid.bento-reveal", status="stable", lane='marketing', definition='Bento stagger', emit=True),
    _p("grid.cascade", status="stable", lane='marketing', definition='Diagonal cascade', emit=True),
    _p("grid.elastic-cell", status="stable", lane='marketing', definition='Elastic active cell', emit=True),
    _p("grid.filter-reflow", status="stable", lane='marketing', definition='Filter reflow', emit=True),
    _p("grid.flip", status="stable", lane='marketing', definition='Flip grid cards', emit=True),
    _p("grid.gap-breathe", status="stable", lane='marketing', definition='Gap breathe (rare)', emit=True),
    _p("grid.hover-expand", status="stable", lane='marketing', definition='Hover expand cell', emit=True),
    _p("grid.masonry-flow", status="stable", lane='marketing', definition='Masonry enter', emit=True),
    _p("grid.mosaic", status="stable", lane='marketing', definition='Mosaic assemble', emit=True),
    _p("grid.shuffle", status="stable", lane='marketing', definition='Grid shuffle FLIP', emit=True),
    _p("grid.span-morph", status="stable", lane='marketing', definition='Col-span morph', emit=True),
    _p("grid.tile-press", status="stable", lane='product', definition='Tile press', emit=True),
    _p("hero.aurora", status="stable", lane='marketing', definition='Aurora background', emit=True),
    _p("hero.cta-rise", status="stable", lane='marketing', definition='CTA rise after copy', emit=True),
    _p("hero.device-carousel", status="stable", lane='marketing', definition='Device screen carousel', emit=True),
    _p("hero.floating-device", status="stable", lane='marketing', definition='Floating device', emit=True),
    _p("hero.logo-lockup", status="stable", lane='marketing', definition='Logo lockup assemble', emit=True),
    _p("hero.mouse-parallax", status="stable", lane='marketing', definition='Mouse parallax', emit=True),
    _p("hero.orb", status="stable", lane='marketing', definition='Orb motion', emit=True),
    _p("hero.parallax", status="stable", lane='marketing', definition='Parallax hero layers', emit=True),
    _p("hero.particle-field", status="stable", lane='marketing', definition='Sparse particles', emit=True),
    _p("hero.scroll-collapse", status="stable", lane='marketing', definition='Hero collapse on scroll', emit=True),
    _p("hero.video-mask", status="stable", lane='marketing', definition='Video mask reveal', emit=True),
    _p("hover.border-draw", status="stable", lane='marketing', definition='Border draw', emit=True),
    _p("hover.cursor-dot", status="stable", lane='marketing', definition='Cursor follow dot', emit=True),
    _p("hover.drag-lift", status="stable", lane='product', definition='Drag lift', emit=True),
    _p("hover.icon-swap", status="stable", lane='product', definition='Icon A→B fade', emit=True),
    _p("hover.magnetic", status="stable", lane='marketing', definition='Magnetic CTA offset', emit=True),
    _p("hover.ripple", status="stable", lane='product', definition='Ripple on pointerdown', emit=True),
    _p("hover.tilt", status="stable", lane='marketing', definition='Pointer tilt', emit=True),
    _p("micro.badge-pop", status="stable", lane='product', definition='Badge count pop', emit=True),
    _p("micro.checkbox-pop", status="stable", lane='product', definition='Checkbox scale-in', emit=True),
    _p("micro.count-tick", status="stable", lane='product', definition='Number tick slide', emit=True),
    _p("micro.focus-ring-in", status="stable", lane='product', definition='Focus ring fade-in', emit=True),
    _p("micro.hit-ripple", status="stable", lane='product', definition='Pointer ripple', emit=True),
    _p("micro.like-burst", status="stable", lane='marketing', definition='Like burst scale', emit=True),
    _p("micro.progress-fill", status="stable", lane='product', definition='Determinate progress fill', emit=True),
    _p("micro.spinner-replace", status="stable", lane='product', definition='Spinner→check crossfade', emit=True),
    _p("micro.toast-slide", status="stable", lane='product', definition='Alias path — prefer feedback.toast-slide', emit=True),
    _p("micro.toggle-morph", status="stable", lane='product', definition='Toggle morph icon/track', emit=True),
    _p("morph.avatar-profile", status="stable", lane='product', definition='Avatar to profile', emit=True),
    _p("morph.blob", status="stable", lane='marketing', definition='Blob morph', emit=True),
    _p("morph.button-to-input", status="stable", lane='product', definition='Search expand', emit=True),
    _p("morph.chip-to-filter", status="stable", lane='product', definition='Chip to filter', emit=True),
    _p("morph.collapse-icon", status="stable", lane='product', definition='Collapse to icon', emit=True),
    _p("morph.expand-tile", status="stable", lane='marketing', definition='Expand tile', emit=True),
    _p("morph.fab", status="stable", lane='product', definition='FAB morph to sheet', emit=True),
    _p("morph.image-crop", status="stable", lane='marketing', definition='Image crop morph', emit=True),
    _p("morph.liquid-nav", status="stable", lane='product', definition='Liquid nav indicator', emit=True),
    _p("morph.path", status="stable", lane='marketing', definition='SVG path morph', emit=True),
    _p("morph.shared-element", status="stable", lane='both', definition='Shared element FLIP', emit=True),
    _p("morph.tab-content", status="stable", lane='product', definition='Tab height morph', emit=True),
    _p("perspective.cardboard-fold", status="stable", lane='marketing', definition='Cardboard fold', emit=True),
    _p("perspective.coverflow", status="stable", lane='marketing', definition='Coverflow', emit=True),
    _p("perspective.cube", status="stable", lane='marketing', definition='Cube rotate', emit=True),
    _p("perspective.depth-modal", status="stable", lane='marketing', definition='Depth modal', emit=True),
    _p("perspective.flip-board", status="stable", lane='marketing', definition='Flip board', emit=True),
    _p("perspective.floating-cards", status="stable", lane='marketing', definition='Floating 3D cards', emit=True),
    _p("perspective.gallery", status="stable", lane='marketing', definition='Perspective gallery', emit=True),
    _p("perspective.hologram", status="stable", lane='marketing', definition='Hologram plane', emit=True),
    _p("perspective.orbit", status="stable", lane='marketing', definition='Orbit carousel', emit=True),
    _p("perspective.spatial-stack", status="stable", lane='marketing', definition='Spatial stack', emit=True),
    _p("perspective.tilt-card", status="stable", lane='marketing', definition='3D tilt card', emit=True),
    _p("perspective.z-parallax", status="stable", lane='marketing', definition='Z parallax scroll', emit=True),
    _p("reveal.drawer-slide", status="stable", lane='product', definition='Drawer panel slide', emit=True),
    _p("reveal.modal-scale", status="stable", lane='product', definition='Modal scale enter', emit=True),
    _p("reveal.page-crossfade", status="stable", lane='product', definition='Page/section crossfade', emit=True),
    _p("scroll.counter", status="stable", lane='marketing', definition='Count-up in view', emit=True),
    _p("scroll.horizontal", status="stable", lane='marketing', definition='Horizontal scroll track', emit=True),
    _p("scroll.opacity-scrub", status="stable", lane='marketing', definition='Opacity vs scroll', emit=True),
    _p("scroll.parallax-layer", status="stable", lane='marketing', definition='Layer parallax', emit=True),
    _p("scroll.pin-section", status="stable", lane='marketing', definition='Pin section', emit=True),
    _p("scroll.progress-scrub", status="stable", lane='marketing', definition='Scroll scrub timeline', emit=True),
    _p("scroll.reveal-line", status="stable", lane='marketing', definition='Path grow on scroll', emit=True),
    _p("scroll.snap-sections", status="stable", lane='marketing', definition='Snap sections', emit=True),
    _p("scroll.sticky-cards", status="stable", lane='marketing', definition='Sticky card stack', emit=True),
    _p("scroll.sticky-sidebar", status="stable", lane='product', definition='Sticky sidebar', emit=True),
    _p("scroll.zoom", status="stable", lane='marketing', definition='Scroll-linked zoom', emit=True),
    _p("spotlight.accordion", status="stable", lane='product', definition='Accordion soft', emit=True),
    _p("spotlight.beam", status="stable", lane='marketing', definition='Spotlight beam', emit=True),
    _p("spotlight.blur-dim", status="stable", lane='marketing', definition='Blur dim backdrop', emit=True),
    _p("spotlight.card", status="stable", lane='marketing', definition='Card vignette', emit=True),
    _p("spotlight.center-stage", status="stable", lane='marketing', definition='Center stage focus', emit=True),
    _p("spotlight.cursor", status="stable", lane='marketing', definition='Cursor spotlight', emit=True),
    _p("spotlight.focus-shift", status="stable", lane='marketing', definition='Focus shift panels', emit=True),
    _p("spotlight.ken-burns", status="stable", lane='marketing', definition='Ken Burns zoom', emit=True),
    _p("spotlight.ring", status="stable", lane='product', definition='Ring focus tour', emit=True),
    _p("spotlight.stage-crossfade", status="stable", lane='marketing', definition='Stage crossfade', emit=True),
    _p("spotlight.tab-ink", status="stable", lane='product', definition='Tab ink bar', emit=True),
    _p("stack.cascade-drop", status="stable", lane='marketing', definition='Cascade drop', emit=True),
    _p("stack.collapse", status="stable", lane='marketing', definition='Collapse to stack', emit=True),
    _p("stack.deck", status="stable", lane='marketing', definition='Deck stack', emit=True),
    _p("stack.fan", status="stable", lane='marketing', definition='Fan spread', emit=True),
    _p("stack.fly-in", status="stable", lane='marketing', definition='Card fly-in', emit=True),
    _p("stack.parallax", status="stable", lane='marketing', definition='Layered parallax stack', emit=True),
    _p("stack.peel", status="stable", lane='marketing', definition='Peel card', emit=True),
    _p("stack.poster-burst", status="stable", lane='marketing', definition='Poster burst', emit=True),
    _p("stack.scatter-gather", status="stable", lane='marketing', definition='Scatter gather', emit=True),
    _p("stack.shuffle", status="stable", lane='marketing', definition='Shuffle deck', emit=True),
    _p("stack.swipe", status="stable", lane='marketing', definition='Swipe deck', emit=True),
    _p("stack.to-row", status="stable", lane='marketing', definition='Stack to row', emit=True),
    _p("text.count-up", status="stable", lane='marketing', definition='Count-up text', emit=True),
    _p("text.glitch", status="stable", lane='marketing', definition='Short glitch', emit=True),
    _p("text.highlight-sweep", status="stable", lane='marketing', definition='Highlight sweep', emit=True),
    _p("text.rolling", status="stable", lane='marketing', definition='Rolling word slot', emit=True),
    _p("text.scramble", status="stable", lane='marketing', definition='Scramble→final', emit=True),
)

PATTERNS: dict[str, MotionPattern] = {p.id: p for p in (*_M1, *_M2, *_M3)}
FAMILIES: tuple[str, ...] = tuple(sorted({p.family for p in PATTERNS.values()}))


def resolve_motion(raw: str | None) -> str:
    if raw is None or raw == "" or raw == "none":
        return "none"
    if raw in LEGACY_ALIASES:
        return LEGACY_ALIASES[raw]
    if raw in PATTERNS:
        return raw
    return "none"


def is_known_motion(raw: str | None) -> bool:
    if raw is None or raw == "" or raw == "none":
        return True
    return raw in LEGACY_ALIASES or raw in PATTERNS


def motion_css_class(canonical: str) -> str:
    if not canonical or canonical == "none":
        return ""
    return "ourui-motion-" + canonical.replace(".", "-")


def list_patterns(*, status: str | None = None, emit_only: bool = False) -> list[MotionPattern]:
    items = list(PATTERNS.values())
    if status:
        items = [p for p in items if p.status == status]
    if emit_only:
        items = [p for p in items if p.emit]
    return sorted(items, key=lambda p: p.id)


def catalog_summary() -> dict[str, Any]:
    stable = [p.id for p in list_patterns(status="stable")]
    experimental = [p.id for p in list_patterns(status="experimental")]
    return {
        "version": MOTION_CATALOG_VERSION,
        "families": list(FAMILIES),
        "stable": stable,
        "stable_count": len(stable),
        "experimental_count": len(experimental),
        "total": len(PATTERNS),
        "aliases": dict(LEGACY_ALIASES),
        "phases": {"m1": len(_M1), "m2": len(_M2), "m3": len(_M3)},
    }


MOTION_INTENTS: frozenset[str] = frozenset(
    {"none", *LEGACY_ALIASES.keys(), *PATTERNS.keys()}
)
