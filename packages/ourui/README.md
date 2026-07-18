# ourui 1.0.0

Python package for the **OurUI** compiler and runtime.

**Developer writes intent. Compiler writes implementation. Host receives primitives.**

Dump schema **25** (Frozen for 1.0.x). Stable through Phase **S6** plus Phase **T–W**: Form/Dialog/Toast, List/Table/status, diagnostics/`ourui check`, Trusted Publishing recipe.

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
ourui check path/to/app.py
ourui serve path/to/app.py
```

See the repository root README and `docs/user/` for language docs.
