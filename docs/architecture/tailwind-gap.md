# Tailwind gap analysis (OurUI foundation)

**Status:** Living note (ADR-013) · Evidence-based against **Tailwind CSS v4 docs**  
**Package:** OurUI **1.11.0** · Matrix: [`style_catalog.py`](../../packages/ourui/ourui/design/style_catalog.py) (catalog **1.11.0** — **0 C**)

> **Honesty:** An earlier gap pass used memory + partial search and treated some v3 page names as current TOC. This document replaces that with a **docs-sourced** audit. Prefer this file over chat summaries.

## Sources (what was actually read)

| Source | What we took |
|---|---|
| GitHub tree `tailwindlabs/tailwindcss.com` `src/docs/*.mdx` | **197** doc pages (full utility/docs inventory) |
| Raw MDX for key pages | Section headings + class tables (`box-shadow`, `border-width`, `margin`, `background-image`, `display`, `hover-focus-and-other-states`, `caret-color`, `scroll-margin`, …) |
| Live redirects (`curl -L`) | e.g. `/docs/ring-width` → `box-shadow#adding-a-ring`; `/docs/space` → `margin#adding-space-between-children` |

OurUI does **not** copy the class-string API. Gap = **capability families** (CSS values / authoring surface), not 1:1 `class=` parity.

## Verdict

| Dimension | Assessment (sourced) |
|---|---|
| Docs inventory | 197 MDX pages; ~184 utility/concept pages after excluding install/meta |
| OurUI matrix | aggregated families, not 1 page = 1 row |
| Skeleton coverage | Most TW utility pages map to a catalog row |
| **Unmapped TW pages** | **0** utility **C** remaining (model diffs stay **AB**/escape notes) |
| Variant depth | Responsive **A** (dict md/lg on high-ROI props); hover/focus/placeholder/selection **A** |
| High-ROI emit batch | ~~ring / divide / space / gradients / scroll-m/p / sr-only / caret~~ **A** (L3 batch) |

Canonical match that is real: [`aspect-ratio`](https://tailwindcss.com/docs/aspect-ratio) ↔ OurUI `aspect=`.

## Important v4 structure (do not hallucinate v3 TOC)

In **Tailwind v4 docs**, several v3 “standalone” pages are **sections of other pages**:

| Capability | Official v4 location (verified) |
|---|---|
| **ring** / inset-ring | [`box-shadow`](https://tailwindcss.com/docs/box-shadow) → “Adding a ring” (redirect from `/docs/ring-width`) |
| **divide-x/y** | [`border-width`](https://tailwindcss.com/docs/border-width) → “Between children” |
| **space-x/y** | [`margin`](https://tailwindcss.com/docs/margin) → “Adding space between children” |
| **gradients** (`bg-linear-*`, `from`/`via`/`to`) | [`background-image`](https://tailwindcss.com/docs/background-image) |
| **sr-only** / **not-sr-only** | [`display`](https://tailwindcss.com/docs/display) → “Screen-reader only” |
| **placeholder:** / **selection:** variants | [`hover-focus-and-other-states`](https://tailwindcss.com/docs/hover-focus-and-other-states) (pseudo-elements) |
| **@container** queries | Same states doc (media/feature / container section) — not a separate `src/docs/@container.mdx` |
| **caret-color** | Standalone [`caret-color`](https://tailwindcss.com/docs/caret-color) |

So “missing from TOC as its own page” ≠ “missing from Tailwind”. Catalog **C** for remaining rows means: **OurUI has no author intent yet**, while Tailwind ships the utilities.

## Gap types (re-validated)

### A — Shallow OurUI status (matrix honesty)

| Tailwind docs | OurUI | Status |
|---|---|---|
| [`responsive-design`](https://tailwindcss.com/docs/responsive-design) — prefixes on utilities | `hide_below=` / `show_below=` + dict `md`/`lg` on pad/width/gap/… | **A** |
| `transition-*` + [`animation`](https://tailwindcss.com/docs/animation) | `motion=` (ADR-012) | **AB** |
| [`hover-focus-and-other-states`](https://tailwindcss.com/docs/hover-focus-and-other-states) | `hover=` / `focus=` + dict `opacity={"hover":…}` | **A** (disabled/invalid still host) |
| [`colors`](https://tailwindcss.com/docs/colors) / [`color`](https://tailwindcss.com/docs/color) | Theme roles | **A** (roles ≠ full palette utils) |

### B — High-ROI capabilities (L3 batch — Done)

| OurUI row | Tailwind evidence | Props | Status |
|---|---|---|---|
| `ring` | `box-shadow` § ring | `ring=` / `ring_color=` / `ring_inset=` | **A** |
| `divide-x-y` | `border-width` between children | `divide=` / `divide_w=` / `divide_color=` | **A** |
| `space-x-y` | `margin` space between children | `space_x=` / `space_y=` | **A** |
| `bg-gradient` | `background-image` gradients | `bg_gradient=` / `gradient_from=` / `gradient_to=` | **A** |
| `scroll-margin-padding` | [`scroll-margin`](https://tailwindcss.com/docs/scroll-margin), [`scroll-padding`](https://tailwindcss.com/docs/scroll-padding) | `scroll_m=` / `scroll_p=` + sides | **A** |
| `caret-color` | [`caret-color`](https://tailwindcss.com/docs/caret-color) | `caret=` / `caret_color=` | **A** |
| `outline` | [`outline-*`](https://tailwindcss.com/docs/outline-width) | `outline=` / `outline_color=` / `outline_offset=` | **A** |
| `accent-color` | [`accent-color`](https://tailwindcss.com/docs/accent-color) | `accent_color=` / `accent=` | **A** |
| `font-variant-numeric` | [`font-variant-numeric`](https://tailwindcss.com/docs/font-variant-numeric) | `font_numeric=` | **A** |
| `placeholder` / `selection` | [`hover-focus-and-other-states`](https://tailwindcss.com/docs/hover-focus-and-other-states) | `placeholder_color=` / `selection=` | **A** |
| `font-stretch` | [`font-stretch`](https://tailwindcss.com/docs/font-stretch) | `font_stretch=` | **A** |
| `font-feature-settings` | [`font-feature-settings`](https://tailwindcss.com/docs/font-feature-settings) | `font_feature=` (named subset) | **A** |
| `mix-blend` | [`mix-blend-mode`](https://tailwindcss.com/docs/mix-blend-mode) | `mix_blend=` / `backdrop_blend=` | **A** |
| `mask` | [`mask-image`](https://tailwindcss.com/docs/mask-image) | `mask=` fade/radial presets | **A** |
| `background-image` | [`background-image`](https://tailwindcss.com/docs/background-image) | `bg_gradient=` + `bg_image=` | **A** |
| `content` | [`content`](https://tailwindcss.com/docs/content) | `before=` / `after=` / `*_content=` | **A** |
| `container-queries` | [`@container`](https://tailwindcss.com/docs/hover-focus-and-other-states#container-queries) | `container=` + `@md`/`@lg` dict | **A** |
| `sr-only` | `display` screen-reader only | `sr_only=` | **A** |

### C — Remaining deferred / niche (still **C**)

*None* in the style catalog matrix. Arbitrary beyond allowlists → `Theme(css=)` / `Image` / `Canvas`.


### C′ — Long-tail shipped (**A**, catalog 1.5.0)

| Tailwind | OurUI props |
|---|---|
| appearance | `appearance=` |
| backface-visibility | `backface=` |
| color-scheme | `color_scheme=` |
| field-sizing | `field_sizing=` |
| scrollbar-* | `scrollbar_width=` `scrollbar_gutter=` `scrollbar_color=` |
| tab-size | `tab_size=` |
| text-indent | `text_indent=` |
| zoom | `zoom=` |

### D — Model differences (not bugs)

| Tailwind | OurUI |
|---|---|
| Class strings + variants | Intent props |
| Class detection / JIT scan | Compile-time AST (**B**) |
| Full color palette utilities | `ui.Theme` roles |
| CSS `transition-*` TOC | Parallel `motion=` |

## Strong coverage (sourced — do not over-invest)

Layout, flex, grid, gap/align/place, padding/margin/sizing, core typography pages that map to existing **A** props, filters, transforms, basic interactivity — already represented.

## L3 priority

1. ~~**ring**~~ **Done**
2. ~~Responsive depth beyond hide/show~~ **Done** (`pad={"base","md","lg"}` …)
3. ~~**divide** / **space-x** / **scroll-m/p** / **gradient** / **sr-only** / **caret**~~ **Done** (batch)
4. ~~Host chrome slim~~ **Done** (tokenized bleed/code/dialog; no `!important` on legacy gap/pad; `Theme(css=)` for app escape)
5. ~~Long-tail **C** pages~~ **Done** — catalog **0 C** (`content` + container-queries shipped)

## Related

- [ADR-013](../decisions/ADR-013-style-intent-catalog.md)
- [Style intents (user)](../user/reference/style-intents.md)
- [Roadmap L3](../roadmap.md)
