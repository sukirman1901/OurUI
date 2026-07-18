# ourui 1.11.1

Python package for the **OurUI** compiler and runtime.

**Developer writes intent. Compiler writes implementation. Host receives primitives.**

**Package goal:** style **intent props** in Python (`aspect=`, `pad_x=`, `ring=`, …) → HTML/CSS/JS. **`ui.Theme`** = thin brand sheet (+ optional `css=` escape). Style Intent Catalog (ADR-013) **L3 complete**.

Dump schema **30** (additive). Theme defaults from `theme.py`. Thin primitives for emit — craft depth is the utility catalog.

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
ourui serve examples/tutorial/06_counter_app.py
```

See the repository root README and `docs/user/` for language docs. Style utilities: `docs/user/reference/style-intents.md`.
