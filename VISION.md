# Vision

## Why

Python teams building SaaS and AI products are forced into a second stack (JavaScript, HTML, CSS, framework glue) for the UI. Context switching slows delivery and pushes layout craft into ad-hoc CSS strings or a Node toolchain.

OurUI exists so those teams author **UI intent in Python** and let the compiler emit HTML/CSS/JS — without class-string CSS authoring or a Node build step.

## Mission

Give Python developers a single authoring surface for modern web UIs — **intent props → compile → host document** — without writing JavaScript by default.

## What we are building (north-star)

**Package = style intents**, not blocks.

Canonical example — sizing a media box:

| Intent | Emitted CSS |
|---|---|
| `aspect="square"` | `aspect-ratio: 1 / 1` via `.ourui-aspect-square` |
| `aspect="video"` | `aspect-ratio: 16 / 9` |
| `aspect="auto"` / allowlisted literal | auto / resolved length |

Same pattern for `pad=`, `width=`, `gap=`, `ring=`, … — **Python props**, finite `.ourui-*` utilities.

**`ui.Theme`** is only a thin brand sheet (colors, density, page measure). It does **not** replace the utility catalog.

Thin host primitives (`ui.Nav`, `ui.Button`, `ui.ThemeToggle`, …) exist so emit has something to map — not a component marketplace. Composed section patterns stay **out of** Stable `ui.*` while product focus is language + catalog ([ADR-014](docs/decisions/ADR-014-language-primitives-vs-kit.md)).


## Slogan

> Developer writes intent. Compiler writes implementation. Host receives primitives.

## Where we are (`1.11.1`)

| Layer | Reality | Status |
|---|---|---|
| **Compiler spine** | Intent → SG → IIR → LTR → RTR → HTML/CSS/JS | Shipped |
| **Utility / style-intent catalog** | Scales + props (`aspect=`, `pad_x=`, `ring=`, …) ADR-013 | **L3 complete** |
| **`ui.Theme`** | Thin brand roles (`--ourui-*`) + density + `page=` + `css=` | Shipped — supporting sheet, **not** craft depth |
| **Thin primitives** | Page, Nav, Form, State, `@server`, … | Shipped for emit |
| **Examples** | Tutorial + landing dogfood | Dogfood only |

Dump schema **25** remains **Frozen** for language/IR breaking changes in `1.x`; schemas **26–30** are additive. Current package: **1.11.1** (schema **30**).

Host strategy (ADR-005): **intent + emit + escape** — not class-string authoring, not a React clone.

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
- **Utility-complete foundation** — broad layout/type/effect coverage via intent props + emit.
- A compilation path that AI and humans can inspect (Semantic Graph, Analysis Views, OurIR).
- Host Contract so web (today) and PDF/native (later) share the same resolved design inputs.

## Non-goals

- Running Python in the browser as the primary UI runtime.
- Shipping a React/Vue-compatible runtime under the hood as the long-term architecture.
- Exposing CSS **class strings** as the Stable authoring API.
- Growing Stable `ui.*` with composed section patterns while the language surface is still settling.
- Replacing the entire JS ecosystem for every use case on day one.
- Treating `ui.Theme` color roles alone as “craft is solved.”

## Product principles

1. **Python-first** — one language for UI intent and server hooks.
2. **Compile over runtime** — resolve as much as possible before the browser.
3. **Host Contract** — Resolved Design inputs stay host-agnostic.
4. **Escape hatches** — `Theme(css=)`, `Canvas`, literals — when intents are not enough.
5. **Honest status** — Stable / Draft / Experimental labeled in docs and dumps.
