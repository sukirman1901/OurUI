# OurUI

**Developer writes intent. Compiler writes implementation. Host receives primitives.**

OurUI is a **Python intent → HTML/CSS/JS compiler**: you write props (`aspect="video"`, `pad_x="4"`, `ring="2"`, …); the compiler emits finite `.ourui-*` CSS and host HTML/JS — no class-string authoring, no Node/Vite toolchain. Thin `ui.*` primitives map to the host; **`ui.Theme`** is a thin brand sheet — craft depth is the style-intent catalog.

Package **1.11.1** · Style Intent Catalog **L3 complete** · Dump schema **30**.

## Quick start

```bash
pip install ourui
# or from this repo:
python3 -m venv .venv && source .venv/bin/activate
pip install -e packages/ourui

ourui dump app.py
ourui emit app.py
ourui serve app.py
ourui lsp
```

- `dump` — JSON artifacts (SG, IIR, Presentation Graph, Resolved Design, LTR, RTR, …)
- `emit` — HTML + CSS + JS (requires Resolved Design)
- `serve` — preview + RPC + HMR + routing; `--prod` / `--workers` for production sessions
- `lsp` — completions + hover for `ui.*`, `State`, `@server`

## Documentation

**[docs/user/](docs/user/README.md)** — Getting started, Tutorial, Guides, Reference.  
Start with [style intents](docs/user/reference/style-intents.md).

## Package

Source: [`packages/ourui/`](packages/ourui/) · PyPI: [ourui](https://pypi.org/project/ourui/)

## License

MIT — see [LICENSE](LICENSE).
