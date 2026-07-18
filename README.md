# OurUI

**Developer writes intent. Compiler writes implementation. Host receives primitives.**

OurUI is a **Python utility → HTML/CSS/JS compiler**: Tailwind-*depth* scales and values, authored as intent props (`aspect="video"`, `pad_x="4"`, …), not class strings and not Vite/Node. Thin `ui.*` primitives map to the host; **`ui.Theme`** is a thin brand sheet — craft depth is the utility catalog.

Package **1.11.0** ([CHANGELOG.md](CHANGELOG.md)). Style Intent Catalog (ADR-013) **L3 shipped** — niche **C** remain (`content`, font OT, container-queries, …). Dump schema **30**. Specs: [SPEC_STATUS.md](SPEC_STATUS.md) · Vision: [VISION.md](VISION.md) · Roadmap: [docs/roadmap.md](docs/roadmap.md).

## Quick start

```bash
pip install ourui
# or from this repo:
python3 -m venv .venv && source .venv/bin/activate
pip install -e packages/ourui pytest

ourui dump examples/example.py
ourui emit examples/example.py
ourui serve examples/example.py
ourui serve examples/tutorial/06_counter_app.py
# or: examples/landing/app.py
ourui lsp
pytest tests/p0
```

- `dump` — JSON artifacts (SG, IIR, Presentation Graph, Resolved Design, LTR, RTR, …)  
- `emit` — HTML + CSS + JS (requires Resolved Design)  
- `serve` — preview + RPC + HMR + routing; `--prod` / `--workers` for production sessions  
- `lsp` — completions + hover for `ui.*`, `State`, `@server`

**Samples:** [examples/tutorial/](examples/tutorial/) · [examples/landing/](examples/landing/) (dogfood) · [examples/gateway/](examples/gateway/) (auth outside `ui.*`)

## User documentation

**[docs/user/](docs/user/README.md)** — Getting started, Tutorial, Guides, Reference. Start with [style intents](docs/user/reference/style-intents.md) for the utility model (`aspect=`, …).

## Core documents

| Document | Role |
|---|---|
| [VISION.md](VISION.md) | Why OurUI exists + utilities vs blocks |
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
                                         (+ finite .ourui-* style utilities)
```

## License

MIT — see [LICENSE](LICENSE).
