# Changelog

All notable changes to the OurUI package are documented here.

Format inspired by [Keep a Changelog](https://keepachangelog.com/). Versioning follows [SemVer](https://semver.org/) for the `ourui` Python package.

## [1.5.0] — 2026-07-18

### Added — Enterprise E2–E5

- **E2:** Pack `version` / Resolved Design `pack_version`; `ui.Theme(density=…)`; `ourui check --profile enterprise` (+ `--strict`); ADR-011
- **E3:** `deploy/Dockerfile`, Compose, K8s sample; `.github/workflows/ci-emit.yml`; expanded deploy guide
- **E4:** Enterprise Kit under `examples/enterprise/` (CRUD, settings, audit, AI console + OIDC stub)
- **E5:** CSP meta (`data-ourui-csp="1"`); dump `attestation`; trust guide; RFC-004 PDF host (Draft)

Dump schema **27** (additive): `emit.density` / `csp` / `attestation`.

### Notes

- Auth/ORM remain app-layer. Tree ready for a single PyPI release of `1.5.0`.

## [1.1.0] — 2026-07-18

### Added — Enterprise E1 (screen completeness)

- `ui.Show(show=State|bool, …)` — Dialog-style visibility
- `ui.When(show=, then=, else_=)` — both branches in DOM; host toggles
- Dynamic `ui.List(items=State)` / `ui.Table(rows=State)` — `applyState` rebuilds DOM from JSON
- ADR-010; reference `examples/enterprise/crud_app.py`
- Dump schema **26** (additive): `emit.show` / `when` / `dynamic_list`

### Notes

- Auth/ORM remain app-layer. Enterprise arc E2–E5 completed in `1.5.0`.

## [1.0.1] — 2026-07-18

### Changed — default visual quality

- Retuned `ourui-default` tokens: zinc/ink product palette (no cream + Fraunces + teal brochure)
- Untoned `ui.Button` resolves to **primary** (not muted gray chips)
- Page chrome: inset + max-width; Shell layouts stay full-bleed
- Host CSS recipes: button hover/focus, form fields, list/table separators, dialog elev
- Fonts: IBM Plex Sans; upgraded `demo/hello_sample.py` first impression

Dump schema remains **25 Frozen**.

## [1.0.0] — 2026-07-18

### Added — Phase T (Form & overlay)

- `ui.Form` + `on_submit=`
- `ui.Dialog` (`open=`, `title=`, `actions=`)
- `ui.Toast` (`open=`, `text=`)
- Field `helper=` + standardized `invalid=` helper text

### Added — Phase U (Data patterns)

- `ui.List`, `ui.Table`, `ui.Empty`, `ui.Spinner`, `ui.Alert`

### Added — Phase V (Compiler UX)

- Structured diagnostics + `ourui check`
- LSP `publishDiagnostics`
- `Derived` (Draft) computed values

### Added — Phase W

- GitHub Actions Trusted Publishing workflow
- Deploy guide + design packs concept docs

### Notes

- Dump schema **25** — **Frozen** for `1.0.x` (breaking changes → `2.0`)
- Host Contract remains primary (RTR + Resolved Design)

## [0.4.1] — 2026-07-18

### Added

- **`ui.Input(type="textarea")`** — multiline form field (playground / editor surfaces)
- **`ui.Frame`** — host escape iframe preview (`bind=` / `srcdoc=`) for compiled HTML Result panes
- Analysis: resolve `State(NAME)` initial from imported module-level string constants; sibling `from artifacts import …` strings for `ui.Code`

### Changed

- Host `applyState` updates iframe `srcdoc` and `<pre><code>` binds
- Demo playground: editable source → Run → live Result/HTML/JS/CSS/AST (no display-only hardcode)

Dump schema remains **21**.

## [0.4.0] — 2026-07-18

### Added

Phase **S3–S6** complete (dump schema **version 21**):

- **S3** — type / space / elevation tokens (`font_*`, `text_*`, `space_*`, `elev_*`); `ui.ThemeToggle` flips `.dark`
- **S3b** — `ui.Footer` (brand/links/meta); Hero/Section `pad=` rhythm
- **S4** — `gap=` / `pad=` / `align=` / `justify=` on Shell/Section; `layout=split-2|split-sidebar`
- **S4m** — `motion=enter|press|reveal` with `prefers-reduced-motion`
- **S5** — `ui.Canvas` WebGL escape (`mode=gradient|dither|raymarch`) via vendored Plasma engine
- **S6** — `menu=drawer` Nav, `ui.Menu`, `ui.Image`, `ui.Icon`, `ui.Meta`, `ui.Code`, `ui.CopyButton`, disabled/invalid/loading

### Notes

- Host Contract unchanged: emit still requires RTR + Resolved Design
- Demo rebuilt against full Phase S stack

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
