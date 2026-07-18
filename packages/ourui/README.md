# ourui 0.4.0

Python package for the **OurUI** compiler and runtime.

**Developer writes intent. Compiler writes implementation. Host receives primitives.**

Stable through Phase **S6** (dump schema **21**): Nav, forms, tokens, layout, motion, Canvas, polish.

## Install

```bash
pip install ourui
```

From a clone of the repository (editable):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e packages/ourui
```

## Quick commands

```bash
ourui dump path/to/app.py
ourui emit path/to/app.py
ourui serve path/to/app.py
ourui serve path/to/app.py --prod
ourui lsp
```

Demo (from repo root): `ourui serve demo/app.py` → http://127.0.0.1:8765/

## Documentation

- [User guide](https://github.com/sukirman1901/OurUI/tree/main/docs/user)
- [Vision](https://github.com/sukirman1901/OurUI/blob/main/VISION.md)
- [Changelog](https://github.com/sukirman1901/OurUI/blob/main/CHANGELOG.md)
- [License (MIT)](https://github.com/sukirman1901/OurUI/blob/main/LICENSE)
- [Repository](https://github.com/sukirman1901/OurUI)

## Requirements

- Python 3.11+
- No runtime dependencies (stdlib only)
