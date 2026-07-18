# ourui 0.3.0

Python package for the **OurUI** compiler and runtime.

**Developer writes intent. Compiler writes implementation. Host receives primitives.**

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

Links below open on GitHub (PyPI cannot host the docs tree inside the wheel):

- [User guide](https://github.com/sukirman1901/OurUI/tree/main/docs/user)
- [Changelog](https://github.com/sukirman1901/OurUI/blob/main/CHANGELOG.md)
- [License (MIT)](https://github.com/sukirman1901/OurUI/blob/main/LICENSE)
- [Repository](https://github.com/sukirman1901/OurUI)

## Requirements

- Python 3.11+
- No runtime dependencies (stdlib only)
