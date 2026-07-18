# OurUI

**Developer writes intent. Compiler writes implementation. Host receives primitives.**

OurUI is a Python-first **language platform** for semantic UI — not a React/Tailwind clone. You author intent in Python; the compiler lowers through **OurIR** (IIR → LTR → RTR) plus Presentation Graph → Resolved Design, then the web host emits HTML/CSS/JS under the **Host Contract**.

Package **1.5.0** on [PyPI](https://pypi.org/project/ourui/) ([CHANGELOG.md](CHANGELOG.md)). Enterprise **E1–E5** shipped; dump schema **27**. Specs: [SPEC_STATUS.md](SPEC_STATUS.md) · Vision: [VISION.md](VISION.md) · Roadmap: [docs/roadmap.md](docs/roadmap.md).

## Quick start

```bash
pip install ourui
# or from this repo:
python3 -m venv .venv && source .venv/bin/activate
pip install -e packages/ourui pytest

ourui dump examples/example.py
ourui emit examples/example.py
ourui serve examples/example.py
ourui serve demo/app.py          # Plasma-shaped dogfood (S1–S6)
ourui lsp
pytest tests/p0
```

- `dump` — JSON artifacts (SG, IIR, Presentation Graph, Resolved Design, LTR, RTR, …)  
- `emit` — HTML + CSS + JS (requires Resolved Design)  
- `serve` — preview + RPC + HMR + routing; `--prod` / `--workers` for production sessions  
- `lsp` — completions + hover for `ui.*`, `State`, `@server`

**Demo:** http://127.0.0.1:8765/ · `/app` · `/embed` after `ourui serve demo/app.py`

## User documentation

**[docs/user/](docs/user/README.md)** — Getting started, Tutorial, Guides, Reference.

## Core documents

| Document | Role |
|---|---|
| [VISION.md](VISION.md) | Why OurUI exists + current capability |
| [DESIGN_PRINCIPLES.md](DESIGN_PRINCIPLES.md) | Engineering philosophy |
| [INVARIANTS.md](INVARIANTS.md) | Hard rules + LOCKED decisions |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Compilation Architecture |
| [LANGUAGE_SPEC.md](LANGUAGE_SPEC.md) | Normative language surface |
| [COMPILER_BOOK.md](COMPILER_BOOK.md) | Contributor compilation guide |
| [SPEC_STATUS.md](SPEC_STATUS.md) | Draft / Stable / Frozen |
| [docs/roadmap.md](docs/roadmap.md) | Product milestones |
| [RFC_PROCESS.md](RFC_PROCESS.md) | How architecture may change |

## Compilation Flow

```text
Parse → Analyze → Lower → Optimize → Emit
         │                    │
         └─ Semantic Graph    ├─ Presentation Graph → Resolved Design
                              └─ IIR → LTR → RTR ──┘
                                         Emit requires RTR + Resolved Design
```

## License

MIT — see [LICENSE](LICENSE).
