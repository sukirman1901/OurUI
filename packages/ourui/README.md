# ourui 0.1.0

Python package for the **OurUI** compiler and runtime.

**Developer writes intent. Compiler writes implementation. Host receives primitives.**

## Install

From a clone of the repository:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e packages/ourui
```

Build distributable artifacts (wheel + sdist):

```bash
pip install build
python -m build packages/ourui
# artifacts under packages/ourui/dist/
```

## Quick commands

```bash
ourui dump path/to/app.py
ourui emit path/to/app.py
ourui serve path/to/app.py
ourui serve path/to/app.py --prod
ourui lsp
```

## Documentation

- User guide: [`docs/user/`](../../docs/user/README.md) (from repo root)
- Changelog: [`CHANGELOG.md`](../../CHANGELOG.md)
- License: MIT ([`LICENSE`](LICENSE))

## Requirements

- Python 3.11+
- No runtime dependencies (stdlib only)
