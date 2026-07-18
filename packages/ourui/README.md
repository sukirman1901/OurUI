# ourui 1.7.0

Python package for the **OurUI** compiler and runtime.

**Developer writes intent. Compiler writes implementation. Host receives primitives.**

Dump schema **29** (additive). Named packs + recipes (`pack=` / `recipe=`) on `ui.Theme`.

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
ourui check path/to/app.py --profile enterprise
ourui serve path/to/app.py
ourui serve examples/enterprise/crud_app.py
```

See the repository root README and `docs/user/` for language docs.
