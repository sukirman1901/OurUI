# Vision

## Why

Python teams building SaaS and AI products are forced into a second stack (JavaScript, HTML, CSS, framework glue) for the UI. Context switching slows delivery and pushes layout craft into ad-hoc CSS strings or a Node toolchain.

OurUI exists so those teams author **utility-depth intent in Python** and let the compiler emit HTML/CSS/JS — the same *compile model* as Tailwind, without Tailwind class strings or Vite.

## Mission

Give Python developers a single authoring surface for modern web UIs — **intent props → compile → host document** — without writing JavaScript by default.

## What we are building (north-star)

**Package = utilities**, not blocks.

Canonical example — Tailwind’s aspect-ratio family:

| Tailwind | CSS | OurUI |
|---|---|---|
| `aspect-square` | `aspect-ratio: 1 / 1` | `aspect="square"` → emit `.ourui-*` |
| `aspect-video` | `aspect-ratio: 16 / 9` | `aspect="video"` |
| `aspect-auto` / `aspect-[…]` | auto / arbitrary | scale + allowlisted literal |

Same pattern for pad, width, gap, blur, … — **Tailwind TOC depth**, Python props, finite CSS utilities.

**`ui.Theme`** is only a thin brand sheet (colors, density, page measure). It does **not** replace the utility catalog.

Thin host primitives (`ui.Nav`, `ui.Button`, `ui.ThemeToggle`, …) exist so emit has something to map — not a component marketplace. Composed section patterns stay **out of** Stable `ui.*` while foundation is incomplete ([ADR-014](docs/decisions/ADR-014-language-primitives-vs-kit.md)).


## Slogan

> Developer writes intent. Compiler writes implementation. Host receives primitives.

## Where we are (`1.11.0`)

| Layer | Reality | Status |
|---|---|---|
| **Compiler spine** | Intent → SG → IIR → LTR → RTR → HTML/CSS/JS | Shipped |
| **Utility / style-intent catalog** | Scales + props (`aspect=`, `pad_x=`, `ring=`, …) ADR-013 | **L3 shipped** (niche **C** remain) |
| **`ui.Theme`** | Thin brand roles (`--ourui-*`) + density + `page=` + `css=` | Shipped — supporting sheet, **not** craft depth |
| **Thin primitives** | Page, Nav, Form, State, `@server`, … | Shipped for emit |
| **Examples** | Tutorial + landing dogfood | Dogfood only |

Dump schema **25** remains **Frozen** for language/IR breaking changes in `1.x`; schemas **26–30** are additive. Current package: **1.11.0** (schema **30**).

Host strategy (ADR-005): **intent + emit + escape** — not class-string authoring, not a React clone. Utility **values/scales** may match Tailwind; authoring stays OurUI props.

Package: [ourui on PyPI](https://pypi.org/project/ourui/) · Samples: `ourui serve examples/tutorial/06_counter_app.py` · Dogfood: `examples/landing/`


## Values

- **Intent over markup** — props and kinds, not DOM tags or utility class soup in source.
- **Compile-time honesty** — prefer known structure at compile time over heavy runtimes.
- **Inspectability** — every stage is dumpable and serializable.
- **Utilities first** — finish catalog depth before growing composed UI inside the language.
- **Long-horizon design** — vocabulary changes through ADR/RFC, not fashion.

## Goals

- Python as the only authoring language for application UI.
- Near-zero browser runtime for static intent; selective interactivity via `@server` / `State`.
- **Utility-complete foundation** — Tailwind-class coverage via intent props + emit (aspect-ratio and peers).
- A compilation path that AI and humans can inspect (Semantic Graph, Analysis Views, OurIR).
- Host Contract so web (today) and PDF/native (later) share the same resolved design inputs.

## Non-goals

- Running Python in the browser as the primary UI runtime.
- Shipping a React/Vue-compatible runtime under the hood as the long-term architecture.
- Exposing Tailwind **class strings** (`class="aspect-video"`) as the Stable authoring API.
- Growing Stable `ui.*` with composed section patterns while the utility catalog is incomplete.
- Replacing the entire JS ecosystem for every use case on day one.
- Treating `ui.Theme` color roles alone as “craft is solved.”

## Product principles

1. **Python-first** — one language for UI intent and server hooks.
2. **No JS for app authors** — developers do not write HTML/CSS/JS by default.
3. **Compiled output** — host primitives and finite `.ourui-*` utilities are emitted.
4. **Utility-native** — scales and intent props are the craft depth story (ADR-013).
5. **AI & realtime ready** — graphs and serializable IR support agents and live systems.
6. **Escape honestly** — WebGL and similar host capabilities arrive as named escapes, not style soup.
7. **Compose later** — app-level composition of primitives + utilities when needed; not language growth for patterns.
