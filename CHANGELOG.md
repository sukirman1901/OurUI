# Changelog

All notable changes to the OurUI package are documented here.

Format inspired by [Keep a Changelog](https://keepachangelog.com/). Versioning follows [SemVer](https://semver.org/) for the `ourui` Python package (`0.x` may still refine Stable surfaces with an ADR).

## [0.3.3] — 2026-07-18

### Added

- **`ui.Nav`** (Phase S3a) — chrome bar with `brand=` / `items=` / `actions=`
- `placement=` intent enum (`sticky-top`, `fixed-top`, …) mapped by emit — not raw CSS `position`
- `tone=solid|glass` nav surfaces; page pad when `fixed-top` via `:has()`
- Dump schema **version 15**
- Demo landing uses Nav + S2 playground controls

## [0.3.2] — 2026-07-18

### Added

- **`ui.Select`**, **`ui.Toggle`**, **`ui.Slider`** (Phase S2 complete for core controls)
- Checkbox fields collect as booleans; range/select as values
- Dump schema **version 14**

## [0.3.1] — 2026-07-18

### Added

- **`ui.Input`** (Phase S2) — form fields with `name=`, `type=`, `placeholder=`, `label=`, `bind=`
- Button clicks collect `[data-ourui-field]` values into the `@server` RPC payload
- Dump schema **version 13**

### Notes

- Host Contract unchanged: Input chrome is host-private CSS; structure via RTR
- Remaining S2: Slider, Select, Toggle

## [0.3.0] — 2026-07-18

### Changed

- **Host Contract primary** (RFC-003): `emit_css` / `emit_html_document` / `emit_bundle` **require** `resolved_design`
- Removed emit fallback that invented tones via `default_tokens()` / Theme tables
- `_BASE_CSS` documented as host-private chrome (layout only)
- Dump flag `emit.host_contract_primary`

### Notes

- Generation 3 complete: web Host consumes `RTR + Resolved Design`
- `theme.py` / `DEFAULT_*` remain Design System pack seeds only
- Optional later: CSS AST / `ourui-web` split (RFC-003 Step F)

## [0.2.2] — 2026-07-18

### Added

- **Host Contract Spike B** (RFC-003): web emit consumes `RTR + Resolved Design`
- CSS: pack variables from `resolved_design.tokens`; per-node button/link rules from `resolved_design.nodes`
- Dump flag `emit.host_contract`

### Notes

- Layout chrome remains host-private `_BASE_CSS`
- `0.3.0` will mark emit contract-primary (finish migration off Theme/`DEFAULT_*` as emit authority)

## [0.2.1] — 2026-07-18

### Added

- **Resolved Design** in `ourui dump` (RFC-002 — `Presentation Graph` + Design System pack → host-neutral resolved values)
- `ourui.design.resolve` with default pack `ourui-default` (seeded from `theme.py`)
- Dump schema **version 12**

### Notes

- HTML/CSS emit still provisional (does **not** consume Resolved Design yet — RFC-003 Host Contract)
- Generation 3 focus: Host Contract → web emit refactor → `0.3.0` (not Material / Plasma / Nav)
- `ui.Theme` overrides continue to merge into SG tokens and now flow into Resolved Design

## [0.2.0] — 2026-07-18

### Added

- **Presentation Graph** in `ourui dump` (RFC-001 Option A — Presentation Lowering from IIR)
- Dump schema **version 11**
- RFC ladder docs: RFC-001 Accepted, RFC-002/003 stubs, architecture sketch
- Spike notes for production options A/B/C

### Notes

- HTML/CSS emit remains provisional (Theme + base CSS); Design System resolve + host CSS AST are RFC-002/003
- Chrome freeze (e.g. `ui.Nav`) continues until Design System / Host RFCs progress

## [0.1.2] — 2026-07-18

### Added

- `ui.Link` — in-app and external navigation (`href=`, auto `target=_blank` for http(s))
- `ui.Shell` and `layout=` intents (`stack`, `row`, `split-3`, `grid`) with emit CSS (including responsive `split-3`)
- Dump schema **version 10** (HostNode `href`, `external`, `shell_layout`)
- ADRs 005–007 (intent+emit+escape, chrome/placement notes, site structure stack)
- `demo/` Plasma-shaped dogfood app documenting remaining gaps

## [0.1.1] — 2026-07-18

### Fixed

- Package README and PyPI project URLs now point at absolute GitHub links (`sukirman1901/OurUI`) so Documentation / Changelog / License open correctly from PyPI

## [0.1.0] — 2026-07-18

First public P0 release of the OurUI compiler and runtime.

### Added

- CLI: `ourui dump`, `ourui emit`, `ourui serve`, `ourui lsp`
- Compilation pipeline: Semantic Graph → IIR → LTR → RTR → HTML/CSS/JS
- Authoring: `ui.*` components, function/`Component` classes, `State`, `@server`, routing (`route=`), `ui.Theme` (`--ourui-*` tokens)
- Dev serve with HMR; production `--prod` with session State; multi-worker file sessions (`--workers`, `--session-dir`)
- User documentation under `docs/user/`
- Tutorial examples under `examples/tutorial/` with smoke tests

### Notes

- Not yet: forms, Redis sessions, client-only State, PDF emit, Rust engine, published docs site
- Install: `pip install -e packages/ourui` (local) or build wheels from `packages/ourui` for distribution
