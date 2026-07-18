# Changelog

All notable changes to the OurUI package are documented here.

Format inspired by [Keep a Changelog](https://keepachangelog.com/). Versioning follows [SemVer](https://semver.org/) for the `ourui` Python package (`0.x` may still refine Stable surfaces with an ADR).

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
