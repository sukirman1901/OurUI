# Vision

## Why

Python teams building SaaS and AI products are forced into a second stack (JavaScript, HTML, CSS, framework glue) for the UI. Context switching slows delivery, fragments ownership, and pushes design systems into ad-hoc CSS strings.

OurUI exists so those teams can express **intent** in Python and let the compiler produce host implementations.

## Mission

Give Python developers a single authoring surface for modern web UIs — compiled, explicit, and inspectable — without requiring them to write JavaScript.

## Vision

A language platform where:

- UI, theme tokens, and server interactions are written in Python.
- The compiler owns implementation details (layout, host primitives, emit).
- The browser (or other hosts) receives only primitives.
- Tooling and AI can query graphs and OurIR artifacts with the same vocabulary as humans.

## Slogan

> Developer writes intent. Compiler writes implementation. Host receives primitives.

## Where we are (`0.4.0`)

| Capability generation | Proof | Status |
|---|---|---|
| **1 — Language infrastructure** | Intent → SG → IIR → LTR → RTR → running app | Done |
| **2 — Semantic presentation** | Presentation Graph + Design System → Resolved Design | Done |
| **3 — Host Contract** | Emit requires `RTR + Resolved Design` | Done |

**Phase S (language surface)** is complete through **S6**: navigation chrome, form controls, type/space/elevation tokens, theme toggle, Footer, layout intents, motion presets, `ui.Canvas` WebGL escape, and host polish (Image/Icon/Meta/Code/drawer).

Host strategy (ADR-005): **intent + emit + escape** — not a React/Tailwind clone in Python. Escapes (`ui.Canvas`) are explicit; tokens and layout stay semantic.

Package: [ourui on PyPI](https://pypi.org/project/ourui/) · Demo: `ourui serve demo/app.py` → http://127.0.0.1:8765/

## Values

- **Intent over markup** — developers describe what they mean, not DOM tags.
- **Compile-time honesty** — prefer known structure at compile time over heavy runtimes.
- **Inspectability** — every stage is dumpable and serializable.
- **Long-horizon design** — vocabulary and invariants change only through process, not fashion.

## Goals

- Python as the only authoring language for application UI.
- Near-zero browser runtime for static intent; selective interactivity via `@server` / `State`.
- Design tokens as first-class language concepts (color, type, space, elevation).
- A compilation path that AI and humans can inspect (Semantic Graph, Analysis Views, OurIR).
- Host Contract so web (today) and PDF/native (later) share the same resolved design inputs.

## Non-goals

- Running Python in the browser as the primary UI runtime.
- Shipping a React/Vue-compatible runtime under the hood as the long-term architecture.
- Exposing full CSS/Tailwind utility catalogs as the Stable authoring API.
- Replacing the entire JS ecosystem for every use case on day one.
- Designing by endless documentation without implementation proof.

## Product principles

1. **Python-first** — one language for UI intent and server hooks.
2. **No JS for app authors** — developers do not write HTML/CSS/JS by default.
3. **Compiled output** — host primitives are emitted; Virtual DOM monoliths are not the goal.
4. **Design-system native** — tokens, not raw style strings, are the default.
5. **AI & realtime ready** — graphs and serializable IR support agents and live systems.
6. **Escape honestly** — WebGL and similar host capabilities arrive as named escapes, not style soup.
