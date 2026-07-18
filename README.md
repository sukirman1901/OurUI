# OurUI

**Developer writes intent. Compiler writes implementation. Host receives primitives.**

OurUI is a Python-first language platform for building SaaS and AI web apps. You author UI in Python; the compiler lowers intent through the **OurIR** stack and emits host primitives. No JavaScript required from application developers.

P0 specs are **Stable** ([SPEC_STATUS.md](SPEC_STATUS.md), tag `spec-p0-stable`). Package release **0.3.1** on [PyPI](https://pypi.org/project/ourui/) ([CHANGELOG.md](CHANGELOG.md)). Generations 1–3 complete; Phase **S2** starts form controls (`ui.Input` → `@server`). Production serve is **Stable** for single-process and file-backed multi-worker (`--prod --workers N`).

## Quick start (P0)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e packages/ourui pytest
ourui dump examples/example.py
ourui emit examples/example.py
ourui serve examples/example.py
ourui serve examples/example.py --prod
ourui serve examples/example.py --prod --workers 4 --session-dir /tmp/ourui-sessions
ourui lsp
pytest tests/p0
```

- `dump` — JSON artifacts (SG, DG, IIR, Presentation Graph, Resolved Design, LTR, RTR, handlers)  
- `emit` — HTML + CSS + JS shim  
- `serve` — preview + RPC + HMR + multi-page routing; `--prod` for sessions/safe errors; `--workers` / `--session-dir` for multi-process file sessions  
- `lsp` — stdio Language Server (completions + hover for `ui.*`, `State`, `@server`)

## User documentation

Full Getting started, Tutorial, Guides, and Reference: **[docs/user/](docs/user/README.md)**.

## Core documents

| Document | Role |
|---|---|
| [VISION.md](VISION.md) | Why OurUI exists |
| [DESIGN_PRINCIPLES.md](DESIGN_PRINCIPLES.md) | Engineering philosophy |
| [INVARIANTS.md](INVARIANTS.md) | Hard rules + LOCKED decisions |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Compilation Architecture |
| [LANGUAGE_SPEC.md](LANGUAGE_SPEC.md) | DSL (P0 subset) |
| [COMPILER_BOOK.md](COMPILER_BOOK.md) | How compilation works (contributor guide) |
| [SPEC_STATUS.md](SPEC_STATUS.md) | Draft / Stable / Frozen |
| [RFC_PROCESS.md](RFC_PROCESS.md) | How architecture may change |

Background research (archived): [docs/archive/deep-research-report.md](docs/archive/deep-research-report.md)

## Compilation Flow

```text
Parse → Analyze → Lower → Optimize → Emit
```

P0 stops after **Intent Lowering** (IIR) and JSON dump.

## License

MIT — see [LICENSE](LICENSE).
