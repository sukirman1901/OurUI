# Changelog

All notable changes to the OurUI package are documented here.

Format inspired by [Keep a Changelog](https://keepachangelog.com/). Versioning follows [SemVer](https://semver.org/) for the `ourui` Python package (`0.x` may still refine Stable surfaces with an ADR).

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
