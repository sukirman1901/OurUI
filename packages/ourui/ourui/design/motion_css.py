"""Host CSS for OurUI motion vocabulary (ADR-012 M1–M3)."""

from __future__ import annotations

# Shared tokens + all Stable pattern rules. Prefers-reduced-motion at end.
MOTION_HOST_CSS = r"""
/* M0 motion tokens */
:root, .ourui-root {
  --ourui-motion-ease: cubic-bezier(0.22, 1, 0.36, 1);
  --ourui-motion-ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ourui-motion-duration-fast: 150ms;
  --ourui-motion-duration: 280ms;
  --ourui-motion-duration-slow: 480ms;
}
/* --- enter / reveal --- */
.ourui-motion-reveal-fade-up,
.ourui-motion-text-fade-up,
.ourui-motion-stack-fly-in,
.ourui-motion-stack-cascade-drop,
.ourui-motion-hero-cta-rise,
.ourui-motion-hero-logo-lockup,
.ourui-motion-grid-masonry-flow,
.ourui-motion-grid-mosaic { animation: ourui-reveal-fade-up var(--ourui-motion-duration) var(--ourui-motion-ease-out) both; }
.ourui-motion-reveal-fade,
.ourui-motion-reveal-page-crossfade,
.ourui-motion-spotlight-stage-crossfade,
.ourui-motion-flow-fade-carousel > * { animation: ourui-reveal-fade var(--ourui-motion-duration) var(--ourui-motion-ease-out) both; }
.ourui-motion-reveal-mask-wipe,
.ourui-motion-hero-video-mask { animation: ourui-reveal-mask-wipe var(--ourui-motion-duration-slow) var(--ourui-motion-ease-out) both; }
.ourui-motion-reveal-split { animation: ourui-reveal-split var(--ourui-motion-duration-slow) var(--ourui-motion-ease-out) both; }
.ourui-motion-reveal-curtain { animation: ourui-reveal-curtain var(--ourui-motion-duration-slow) var(--ourui-motion-ease-out) both; }
.ourui-motion-reveal-ink { animation: ourui-reveal-ink var(--ourui-motion-duration-slow) var(--ourui-motion-ease-out) both; }
.ourui-motion-reveal-blur-in,
.ourui-motion-spotlight-blur-dim { animation: ourui-reveal-blur-in var(--ourui-motion-duration-slow) var(--ourui-motion-ease-out) both; }
.ourui-motion-reveal-scale-fade,
.ourui-motion-reveal-modal-scale,
.ourui-motion-micro-badge-pop,
.ourui-motion-micro-checkbox-pop,
.ourui-motion-micro-like-burst { animation: ourui-reveal-scale-fade var(--ourui-motion-duration) var(--ourui-motion-ease-out) both; }
.ourui-motion-reveal-drawer-slide { animation: ourui-drawer-in var(--ourui-motion-duration) var(--ourui-motion-ease-out) both; }
.ourui-motion-reveal-stagger-children > *,
.ourui-motion-hero-stagger-copy > *,
.ourui-motion-grid-bento-reveal > *,
.ourui-motion-grid-cascade > * {
  opacity: 0; transform: translateY(0.5rem);
  animation: ourui-reveal-fade-up var(--ourui-motion-duration) var(--ourui-motion-ease-out) forwards;
  animation-delay: calc(var(--ourui-stagger, 0) * 70ms);
}
/* --- press / hover / micro --- */
.ourui-motion-press-scale:active,
.ourui-motion-grid-tile-press:active { transform: scale(0.96); transition: transform var(--ourui-motion-duration-fast) var(--ourui-motion-ease); }
.ourui-motion-hover-lift,
.ourui-motion-hover-drag-lift {
  transition: transform var(--ourui-motion-duration-fast) var(--ourui-motion-ease), box-shadow var(--ourui-motion-duration-fast) var(--ourui-motion-ease);
}
.ourui-motion-hover-lift:hover,
.ourui-motion-hover-drag-lift:hover { transform: translateY(-2px); box-shadow: var(--ourui-elev-2); }
.ourui-motion-hover-underline-slide,
.ourui-motion-text-underline-reveal,
.ourui-motion-spotlight-tab-ink {
  text-decoration: none;
  background-image: linear-gradient(currentColor, currentColor);
  background-position: 0 100%; background-repeat: no-repeat; background-size: 0 2px;
  transition: background-size var(--ourui-motion-duration) var(--ourui-motion-ease-out);
}
.ourui-motion-hover-underline-slide:hover,
.ourui-motion-hover-underline-slide:focus-visible,
.ourui-motion-spotlight-tab-ink[data-active="true"] { background-size: 100% 2px; }
.ourui-motion-text-underline-reveal { animation: ourui-underline-grow var(--ourui-motion-duration-slow) var(--ourui-motion-ease-out) 0.15s forwards; }
.ourui-motion-hover-glow,
.ourui-motion-spotlight-ring:focus-visible { transition: box-shadow var(--ourui-motion-duration) var(--ourui-motion-ease); }
.ourui-motion-hover-glow:hover,
.ourui-motion-spotlight-ring:focus-visible { box-shadow: 0 0 0 3px color-mix(in srgb, var(--ourui-primary) 28%, transparent); }
.ourui-motion-hover-color-shift { transition: color var(--ourui-motion-duration-fast) var(--ourui-motion-ease), background-color var(--ourui-motion-duration-fast) var(--ourui-motion-ease); }
.ourui-motion-hover-color-shift:hover { color: var(--ourui-primary); }
.ourui-motion-hover-tilt { transition: transform var(--ourui-motion-duration-fast) var(--ourui-motion-ease); transform-style: preserve-3d; }
.ourui-motion-hover-magnetic { transition: transform var(--ourui-motion-duration-fast) var(--ourui-motion-ease); }
.ourui-motion-hover-border-draw { box-shadow: inset 0 0 0 1px transparent; transition: box-shadow var(--ourui-motion-duration) var(--ourui-motion-ease); }
.ourui-motion-hover-border-draw:hover { box-shadow: inset 0 0 0 1px var(--ourui-primary); }
.ourui-motion-hover-ripple { position: relative; overflow: hidden; }
.ourui-motion-hover-icon-swap { transition: opacity var(--ourui-motion-duration-fast) var(--ourui-motion-ease); }
.ourui-motion-hover-cursor-dot { cursor: none; }
.ourui-motion-micro-skeleton-shimmer {
  background: linear-gradient(90deg, color-mix(in srgb, var(--ourui-muted) 55%, transparent) 0%, color-mix(in srgb, var(--ourui-fg) 8%, transparent) 50%, color-mix(in srgb, var(--ourui-muted) 55%, transparent) 100%);
  background-size: 200% 100%; animation: ourui-shimmer 1.4s linear infinite; border-radius: var(--ourui-radius); min-height: 1em;
}
.ourui-motion-micro-progress-fill { transform-origin: left center; animation: ourui-progress-fill var(--ourui-motion-duration-slow) var(--ourui-motion-ease-out) both; }
.ourui-motion-micro-focus-ring-in:focus-visible { outline: 2px solid var(--ourui-primary); outline-offset: 2px; animation: ourui-reveal-fade var(--ourui-motion-duration-fast) var(--ourui-motion-ease-out) both; }
.ourui-motion-micro-hit-ripple { position: relative; overflow: hidden; }
.ourui-motion-micro-toggle-morph,
.ourui-motion-micro-spinner-replace,
.ourui-motion-micro-count-tick,
.ourui-motion-micro-toast-slide { transition: transform var(--ourui-motion-duration) var(--ourui-motion-ease), opacity var(--ourui-motion-duration) var(--ourui-motion-ease); }
.ourui-motion-feedback-toast-slide[data-open="true"],
.ourui-motion-feedback-toast-slide,
.ourui-motion-micro-toast-slide { animation: ourui-toast-slide var(--ourui-motion-duration) var(--ourui-motion-ease-out) both; }
.ourui-motion-feedback-success-pulse { animation: ourui-success-pulse var(--ourui-motion-duration-slow) var(--ourui-motion-ease-out) both; }
/* --- text --- */
.ourui-motion-text-line-mask { animation: ourui-text-line-mask var(--ourui-motion-duration-slow) var(--ourui-motion-ease-out) both; }
.ourui-motion-text-word-reveal .ourui-motion-word,
.ourui-motion-text-char-reveal .ourui-motion-char {
  display: inline-block; opacity: 0; transform: translateY(0.35em);
  animation: ourui-word-in var(--ourui-motion-duration) var(--ourui-motion-ease-out) forwards;
}
.ourui-motion-text-typewriter {
  overflow: hidden; white-space: nowrap; border-right: 2px solid currentColor; width: 0;
  animation: ourui-typewriter-width var(--ourui-typewriter-ms, 1600ms) steps(var(--ourui-typewriter-steps, 24), end) forwards,
    ourui-typewriter-caret 0.7s step-end infinite;
}
.ourui-motion-text-marquee,
.ourui-motion-flow-vertical-marquee { overflow: hidden; }
.ourui-motion-text-marquee { white-space: nowrap; }
.ourui-motion-text-marquee .ourui-motion-marquee-track,
.ourui-motion-flow-logo-marquee .ourui-motion-marquee-track,
.ourui-motion-flow-infinite-slider .ourui-motion-marquee-track {
  display: inline-flex; gap: var(--ourui-space-lg); width: max-content;
  animation: ourui-marquee-x 22s linear infinite;
}
.ourui-motion-flow-vertical-marquee .ourui-motion-marquee-track {
  display: flex; flex-direction: column; animation: ourui-marquee-y 18s linear infinite;
}
.ourui-motion-text-marquee:hover .ourui-motion-marquee-track,
.ourui-motion-flow-logo-marquee:hover .ourui-motion-marquee-track,
.ourui-motion-flow-infinite-slider:hover .ourui-motion-marquee-track,
.ourui-motion-flow-vertical-marquee:hover .ourui-motion-marquee-track,
.ourui-motion-text-marquee:focus-within .ourui-motion-marquee-track,
.ourui-motion-flow-logo-marquee:focus-within .ourui-motion-marquee-track { animation-play-state: paused; }
.ourui-motion-flow-logo-marquee,
.ourui-motion-flow-infinite-slider { overflow: hidden; display: flex; }
.ourui-motion-text-gradient-shift,
.ourui-motion-text-highlight-sweep {
  background: linear-gradient(90deg, var(--ourui-fg) 0%, var(--ourui-accent, var(--ourui-primary)) 40%, var(--ourui-fg) 80%);
  background-size: 200% 100%; -webkit-background-clip: text; background-clip: text; color: transparent;
  animation: ourui-gradient-shift 4s var(--ourui-motion-ease) infinite;
}
.ourui-motion-text-glitch { animation: ourui-glitch 0.45s var(--ourui-motion-ease-out) both; }
.ourui-motion-text-rolling { display: inline-block; overflow: hidden; height: 1.2em; vertical-align: bottom; }
.ourui-motion-text-rolling .ourui-motion-roll-inner { display: block; animation: ourui-roll-y 4s var(--ourui-motion-ease-out) infinite; }
.ourui-motion-text-scramble { font-variant-numeric: tabular-nums; }
.ourui-motion-text-count-up,
.ourui-motion-scroll-counter { font-variant-numeric: tabular-nums; }
/* --- scroll --- */
.ourui-motion-scroll-fade-in-view,
.ourui-motion-scroll-zoom[data-ourui-inview],
.ourui-motion-scroll-parallax-layer {
  opacity: 0; transform: translateY(0.75rem);
  transition: opacity var(--ourui-motion-duration) var(--ourui-motion-ease-out), transform var(--ourui-motion-duration) var(--ourui-motion-ease-out);
}
.ourui-motion-scroll-fade-in-view[data-ourui-inview="true"],
.ourui-motion-scroll-zoom[data-ourui-inview="true"],
.ourui-motion-scroll-parallax-layer[data-ourui-inview="true"],
.ourui-motion-scroll-counter[data-ourui-inview="true"],
.ourui-motion-scroll-reveal-line[data-ourui-inview="true"] { opacity: 1; transform: none; }
.ourui-motion-scroll-zoom[data-ourui-inview="true"] { transform: scale(1.04); }
.ourui-motion-scroll-sticky-sidebar,
.ourui-motion-scroll-sticky-cards > * { position: sticky; top: var(--ourui-space-lg); }
.ourui-motion-scroll-sticky-cards > * { margin-bottom: var(--ourui-space-md); }
.ourui-motion-scroll-horizontal,
.ourui-motion-flow-filmstrip,
.ourui-motion-flow-snap-carousel,
.ourui-motion-flow-story-rail,
.ourui-motion-flow-card-rail,
.ourui-motion-flow-peek-carousel,
.ourui-motion-flow-center-carousel {
  display: flex; gap: var(--ourui-space-md); overflow-x: auto; scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch; scrollbar-width: thin;
}
.ourui-motion-scroll-horizontal > *,
.ourui-motion-flow-filmstrip > *,
.ourui-motion-flow-snap-carousel > *,
.ourui-motion-flow-story-rail > *,
.ourui-motion-flow-card-rail > *,
.ourui-motion-flow-peek-carousel > *,
.ourui-motion-flow-center-carousel > * { scroll-snap-align: start; flex: 0 0 auto; }
.ourui-motion-flow-peek-carousel > * { flex-basis: 78%; }
.ourui-motion-flow-center-carousel > * { flex-basis: 60%; transition: transform var(--ourui-motion-duration) var(--ourui-motion-ease); }
.ourui-motion-scroll-snap-sections { scroll-snap-type: y mandatory; }
.ourui-motion-scroll-snap-sections > * { scroll-snap-align: start; min-height: 70vh; }
.ourui-motion-scroll-pin-section { position: sticky; top: 0; }
.ourui-motion-scroll-reveal-line {
  height: 2px; background: var(--ourui-primary); transform: scaleX(0); transform-origin: left;
  transition: transform var(--ourui-motion-duration-slow) var(--ourui-motion-ease-out); opacity: 1;
}
.ourui-motion-scroll-reveal-line[data-ourui-inview="true"] { transform: scaleX(1); }
.ourui-motion-scroll-progress-scrub,
.ourui-motion-scroll-opacity-scrub { transition: opacity 80ms linear; }
.ourui-motion-flow-autoplay-pause { position: relative; }
.ourui-motion-flow-thumbnail-sync { display: grid; gap: var(--ourui-space-sm); }
/* --- spotlight / grid / stack --- */
.ourui-motion-spotlight-dim-siblings:hover > *,
.ourui-motion-spotlight-center-stage > * { opacity: 0.45; transition: opacity var(--ourui-motion-duration-fast) var(--ourui-motion-ease); }
.ourui-motion-spotlight-dim-siblings:hover > *:hover,
.ourui-motion-spotlight-center-stage > *:hover,
.ourui-motion-spotlight-center-stage > *[data-active="true"] { opacity: 1; transform: scale(1.02); }
.ourui-motion-spotlight-card:hover { box-shadow: var(--ourui-elev-3); }
.ourui-motion-spotlight-beam { animation: ourui-beam 1.2s var(--ourui-motion-ease-out) both; }
.ourui-motion-spotlight-ken-burns { animation: ourui-ken-burns 12s var(--ourui-motion-ease) infinite alternate; }
.ourui-motion-spotlight-cursor { position: relative; }
.ourui-motion-spotlight-focus-shift > *[data-active="true"] { outline: 2px solid var(--ourui-primary); outline-offset: 4px; }
.ourui-motion-spotlight-accordion > * { transition: opacity var(--ourui-motion-duration) var(--ourui-motion-ease); }
.ourui-motion-grid-flip { perspective: 800px; }
.ourui-motion-grid-flip > * { transition: transform var(--ourui-motion-duration) var(--ourui-motion-ease); transform-style: preserve-3d; }
.ourui-motion-grid-flip > *:hover { transform: rotateY(180deg); }
.ourui-motion-grid-elastic-cell > *:hover,
.ourui-motion-grid-hover-expand > *:hover { flex-grow: 1.35; transition: flex-grow var(--ourui-motion-duration) var(--ourui-motion-ease); }
.ourui-motion-grid-gap-breathe { animation: ourui-gap-breathe 3s var(--ourui-motion-ease) infinite; }
.ourui-motion-grid-filter-reflow > *,
.ourui-motion-grid-shuffle > *,
.ourui-motion-grid-span-morph > * { transition: transform var(--ourui-motion-duration) var(--ourui-motion-ease), opacity var(--ourui-motion-duration) var(--ourui-motion-ease); }
.ourui-motion-stack-deck,
.ourui-motion-stack-fan,
.ourui-motion-stack-parallax { position: relative; }
.ourui-motion-stack-deck > *,
.ourui-motion-stack-fan > *,
.ourui-motion-stack-parallax > * {
  position: absolute; inset-inline: 0; margin-inline: auto; width: min(100%, 22rem);
  transition: transform var(--ourui-motion-duration) var(--ourui-motion-ease);
}
.ourui-motion-stack-deck > *:nth-child(1) { transform: translateY(0) rotate(0); z-index: 3; position: relative; }
.ourui-motion-stack-deck > *:nth-child(2) { transform: translateY(0.4rem) rotate(1.5deg); z-index: 2; }
.ourui-motion-stack-deck > *:nth-child(3) { transform: translateY(0.8rem) rotate(-1.5deg); z-index: 1; }
.ourui-motion-stack-fan > *:nth-child(1) { transform: rotate(-6deg); position: relative; }
.ourui-motion-stack-fan > *:nth-child(2) { transform: rotate(0deg); }
.ourui-motion-stack-fan > *:nth-child(3) { transform: rotate(6deg); }
.ourui-motion-stack-peel:hover { transform-origin: top left; transform: rotate(-4deg); }
.ourui-motion-stack-poster-burst > * { animation: ourui-reveal-scale-fade var(--ourui-motion-duration-slow) var(--ourui-motion-ease-out) both; animation-delay: calc(var(--ourui-stagger, 0) * 50ms); }
.ourui-motion-stack-scatter-gather > *,
.ourui-motion-stack-shuffle > *,
.ourui-motion-stack-to-row > *,
.ourui-motion-stack-collapse > *,
.ourui-motion-stack-swipe > * { transition: transform var(--ourui-motion-duration) var(--ourui-motion-ease), opacity var(--ourui-motion-duration) var(--ourui-motion-ease); }
/* --- hero / morph / perspective --- */
.ourui-motion-hero-floating-device,
.ourui-motion-hero-orb,
.ourui-motion-perspective-floating-cards > * { animation: ourui-float-y 5s var(--ourui-motion-ease) infinite alternate; }
.ourui-motion-hero-aurora,
.ourui-motion-morph-blob {
  background: radial-gradient(ellipse at 30% 40%, color-mix(in srgb, var(--ourui-primary) 28%, transparent), transparent 55%),
    radial-gradient(ellipse at 70% 60%, color-mix(in srgb, var(--ourui-accent, var(--ourui-primary)) 22%, transparent), transparent 50%);
  background-size: 140% 140%; animation: ourui-aurora 10s var(--ourui-motion-ease) infinite alternate;
}
.ourui-motion-hero-parallax,
.ourui-motion-hero-mouse-parallax,
.ourui-motion-perspective-z-parallax { will-change: transform; }
.ourui-motion-hero-scroll-collapse { transition: min-height var(--ourui-motion-duration) var(--ourui-motion-ease), opacity var(--ourui-motion-duration) var(--ourui-motion-ease); }
.ourui-motion-hero-particle-field::after {
  content: ""; position: absolute; inset: 0; pointer-events: none; opacity: 0.35;
  background-image: radial-gradient(circle, var(--ourui-fg) 1px, transparent 1px);
  background-size: 48px 48px; animation: ourui-particles 20s linear infinite;
}
.ourui-motion-hero-device-carousel > * { animation: ourui-reveal-fade var(--ourui-motion-duration-slow) var(--ourui-motion-ease-out) both; }
.ourui-motion-morph-fab,
.ourui-motion-morph-expand-tile,
.ourui-motion-morph-collapse-icon,
.ourui-motion-morph-button-to-input,
.ourui-motion-morph-chip-to-filter,
.ourui-motion-morph-avatar-profile,
.ourui-motion-morph-tab-content,
.ourui-motion-morph-image-crop,
.ourui-motion-morph-liquid-nav,
.ourui-motion-morph-shared-element,
.ourui-motion-morph-path {
  transition: border-radius var(--ourui-motion-duration) var(--ourui-motion-ease),
    width var(--ourui-motion-duration) var(--ourui-motion-ease),
    height var(--ourui-motion-duration) var(--ourui-motion-ease),
    transform var(--ourui-motion-duration) var(--ourui-motion-ease);
}
.ourui-motion-perspective-tilt-card,
.ourui-motion-perspective-hologram,
.ourui-motion-perspective-cardboard-fold {
  transform-style: preserve-3d; transition: transform var(--ourui-motion-duration-fast) var(--ourui-motion-ease);
}
.ourui-motion-perspective-coverflow,
.ourui-motion-perspective-orbit,
.ourui-motion-perspective-spatial-stack,
.ourui-motion-perspective-gallery { perspective: 900px; display: flex; gap: var(--ourui-space-md); }
.ourui-motion-perspective-coverflow > *:nth-child(odd) { transform: rotateY(18deg) scale(0.94); }
.ourui-motion-perspective-coverflow > *:nth-child(even) { transform: rotateY(-18deg) scale(0.94); }
.ourui-motion-perspective-cube { transform-style: preserve-3d; animation: ourui-cube 8s linear infinite; }
.ourui-motion-perspective-flip-board { transition: transform var(--ourui-motion-duration) var(--ourui-motion-ease); }
.ourui-motion-perspective-flip-board:hover { transform: rotateX(180deg); }
.ourui-motion-perspective-depth-modal { box-shadow: var(--ourui-elev-3); animation: ourui-reveal-scale-fade var(--ourui-motion-duration) var(--ourui-motion-ease-out) both; }
@keyframes ourui-reveal-fade-up { from { opacity: 0; transform: translateY(0.75rem); } to { opacity: 1; transform: none; } }
@keyframes ourui-reveal-fade { from { opacity: 0; } to { opacity: 1; } }
@keyframes ourui-reveal-mask-wipe { from { opacity: 0; clip-path: inset(0 0 100% 0); } to { opacity: 1; clip-path: inset(0 0 0 0); } }
@keyframes ourui-reveal-split { from { opacity: 0; clip-path: inset(0 50% 0 50%); } to { opacity: 1; clip-path: inset(0 0 0 0); } }
@keyframes ourui-reveal-curtain { from { opacity: 0; clip-path: inset(0 42% 0 42%); } to { opacity: 1; clip-path: inset(0 0 0 0); } }
@keyframes ourui-reveal-ink { from { opacity: 0; clip-path: circle(0% at 50% 50%); } to { opacity: 1; clip-path: circle(75% at 50% 50%); } }
@keyframes ourui-reveal-blur-in { from { opacity: 0; filter: blur(8px); } to { opacity: 1; filter: blur(0); } }
@keyframes ourui-reveal-scale-fade { from { opacity: 0; transform: scale(0.96); } to { opacity: 1; transform: none; } }
@keyframes ourui-drawer-in { from { opacity: 0; transform: translateX(-1rem); } to { opacity: 1; transform: none; } }
@keyframes ourui-text-line-mask { from { opacity: 0; clip-path: inset(100% 0 0 0); transform: translateY(0.4em); } to { opacity: 1; clip-path: inset(0 0 0 0); transform: none; } }
@keyframes ourui-word-in { to { opacity: 1; transform: none; } }
@keyframes ourui-toast-slide { from { opacity: 0; transform: translateY(0.75rem); } to { opacity: 1; transform: none; } }
@keyframes ourui-success-pulse {
  0% { box-shadow: 0 0 0 0 color-mix(in srgb, var(--ourui-primary) 45%, transparent); }
  70% { box-shadow: 0 0 0 0.6rem transparent; }
  100% { box-shadow: 0 0 0 0 transparent; }
}
@keyframes ourui-typewriter-width { from { width: 0; } to { width: 100%; } }
@keyframes ourui-typewriter-caret { 50% { border-color: transparent; } }
@keyframes ourui-marquee-x { from { transform: translateX(0); } to { transform: translateX(-50%); } }
@keyframes ourui-marquee-y { from { transform: translateY(0); } to { transform: translateY(-50%); } }
@keyframes ourui-underline-grow { to { background-size: 100% 2px; } }
@keyframes ourui-gradient-shift { 0% { background-position: 0% 50%; } 100% { background-position: 200% 50%; } }
@keyframes ourui-shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }
@keyframes ourui-progress-fill { from { transform: scaleX(0); } to { transform: scaleX(1); } }
@keyframes ourui-float-y { from { transform: translateY(0); } to { transform: translateY(-0.6rem); } }
@keyframes ourui-aurora { from { background-position: 0% 40%; } to { background-position: 80% 60%; } }
@keyframes ourui-particles { from { background-position: 0 0; } to { background-position: 48px 96px; } }
@keyframes ourui-ken-burns { from { transform: scale(1); } to { transform: scale(1.06); } }
@keyframes ourui-beam {
  from { opacity: 0; background-position: -100% 0; }
  to { opacity: 1; background-position: 200% 0; }
}
@keyframes ourui-glitch {
  0% { transform: translate(0); }
  20% { transform: translate(-2px, 1px); }
  40% { transform: translate(2px, -1px); }
  100% { transform: none; }
}
@keyframes ourui-roll-y {
  0%, 25% { transform: translateY(0); }
  50%, 75% { transform: translateY(-100%); }
  100% { transform: translateY(-200%); }
}
@keyframes ourui-gap-breathe {
  0%, 100% { gap: var(--ourui-space-md); }
  50% { gap: var(--ourui-space-lg); }
}
@keyframes ourui-cube {
  from { transform: rotateY(0); }
  to { transform: rotateY(360deg); }
}
@media (prefers-reduced-motion: reduce) {
  .ourui-motion-reveal-fade-up,
  .ourui-motion-reveal-fade,
  .ourui-motion-reveal-mask-wipe,
  .ourui-motion-reveal-split,
  .ourui-motion-reveal-curtain,
  .ourui-motion-reveal-ink,
  .ourui-motion-reveal-blur-in,
  .ourui-motion-reveal-scale-fade,
  .ourui-motion-reveal-drawer-slide,
  .ourui-motion-reveal-modal-scale,
  .ourui-motion-reveal-page-crossfade,
  .ourui-motion-text-line-mask,
  .ourui-motion-text-fade-up,
  .ourui-motion-text-typewriter,
  .ourui-motion-text-underline-reveal,
  .ourui-motion-text-gradient-shift,
  .ourui-motion-text-highlight-sweep,
  .ourui-motion-text-glitch,
  .ourui-motion-feedback-toast-slide,
  .ourui-motion-feedback-success-pulse,
  .ourui-motion-micro-skeleton-shimmer,
  .ourui-motion-micro-progress-fill,
  .ourui-motion-micro-like-burst,
  .ourui-motion-micro-badge-pop,
  .ourui-motion-micro-checkbox-pop,
  .ourui-motion-hero-floating-device,
  .ourui-motion-hero-orb,
  .ourui-motion-hero-aurora,
  .ourui-motion-hero-particle-field::after,
  .ourui-motion-spotlight-ken-burns,
  .ourui-motion-spotlight-beam,
  .ourui-motion-grid-gap-breathe,
  .ourui-motion-perspective-cube,
  .ourui-motion-morph-blob,
  .ourui-motion-text-rolling .ourui-motion-roll-inner {
    animation: none !important;
  }
  .ourui-motion-text-typewriter { width: auto; border-right: none; white-space: normal; }
  .ourui-motion-text-gradient-shift,
  .ourui-motion-text-highlight-sweep { color: var(--ourui-fg); background: none; -webkit-background-clip: unset; background-clip: unset; }
  .ourui-motion-press-scale:active,
  .ourui-motion-grid-tile-press:active,
  .ourui-motion-hover-lift:hover,
  .ourui-motion-hover-tilt,
  .ourui-motion-hover-magnetic { transform: none !important; }
  .ourui-motion-text-word-reveal .ourui-motion-word,
  .ourui-motion-text-char-reveal .ourui-motion-char,
  .ourui-motion-reveal-stagger-children > *,
  .ourui-motion-hero-stagger-copy > *,
  .ourui-motion-grid-bento-reveal > *,
  .ourui-motion-grid-cascade > * { opacity: 1; transform: none; animation: none; }
  .ourui-motion-scroll-fade-in-view,
  .ourui-motion-scroll-zoom,
  .ourui-motion-scroll-parallax-layer {
    opacity: 1; transform: none; transition: none;
  }
  .ourui-motion-text-marquee .ourui-motion-marquee-track,
  .ourui-motion-flow-logo-marquee .ourui-motion-marquee-track,
  .ourui-motion-flow-infinite-slider .ourui-motion-marquee-track,
  .ourui-motion-flow-vertical-marquee .ourui-motion-marquee-track { animation: none; }
}
"""


def motion_host_css() -> str:
    return MOTION_HOST_CSS
