# ourui 1.12.0

Python-first UI compiler — write intent in Python, emit HTML/CSS/JS.

**Developer writes intent. Compiler writes implementation. Host receives primitives.**

Style intent props (`aspect=`, `pad_x=`, `ring=`, `transition_duration=`, `brightness=`, …) compile to `.ourui-*` CSS utility classes. 45 utilities across transitions, filters, effects, typography, and layout. 7 new design scales. 225 passthrough properties. 7,983 lines of generated CSS.

`ui.Theme` = thin brand sheet (+ optional `css=` escape). Craft depth is the utility catalog.

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
