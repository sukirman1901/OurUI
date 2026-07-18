# OurUI

**Developer writes intent. Compiler writes implementation. Host receives primitives.**

OurUI is a Python-first language platform for building SaaS and AI web apps. You author UI in Python; the compiler lowers intent through the **OurIR** stack and emits host primitives. No JavaScript required from application developers.

P0 specs are **Stable** ([SPEC_STATUS.md](SPEC_STATUS.md), tag `spec-p0-stable`). Single-process production serve (`ourui serve --prod`) is **Stable**; multi-worker runtime remains **Experimental**.

## Quick start (P0)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e packages/ourui pytest
ourui dump examples/example.py
ourui emit examples/example.py
ourui serve examples/example.py
ourui serve examples/example.py --prod
ourui lsp
pytest tests/p0
```

- `dump` — JSON artifacts (SG, DG, IIR, LTR, RTR, handlers)  
- `emit` — HTML + CSS + JS shim  
- `serve` — preview + RPC + HMR + multi-page routing (SSE reload on save); `--prod` disables HMR, uses session State, safe errors  
- `lsp` — stdio Language Server (completions + hover for `ui.*`, `State`, `@server`)


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

TBD.
