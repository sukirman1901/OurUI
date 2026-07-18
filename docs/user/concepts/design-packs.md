# Design packs

Phase W seed. The default pack is **`ourui-default`**, produced from `ui.Theme` / `theme.py` tokens into Resolved Design.

## Authoring

```python
theme = ui.Theme(
    primary="#18181b",
    accent="#0f766e",
    # … see docs/user/reference/theme.md
)
```

Emit consumes **Resolved Design** (Host Contract): pack CSS variables (`--ourui-*`) plus per-node tone rules.

## Status

Pack API is **Stable** for the seeded default pack at OurUI **1.0**. Additional named packs (e.g. brand overrides as installable modules) may grow without breaking the Host Contract.
