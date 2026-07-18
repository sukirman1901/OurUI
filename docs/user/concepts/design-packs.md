# Design packs

The default pack is **`ourui-default`** (zinc/ink product defaults as of 1.0.1), produced from `ui.Theme` / `theme.py` tokens into Resolved Design. Pack recipes also seed page chrome (`max_width`, padding) and control padding.

## Authoring

```python
theme = ui.Theme(
    primary="#18181b",
    accent="#2563eb",
    # … see docs/user/reference/theme.md
)
```

Emit consumes **Resolved Design** (Host Contract): pack CSS variables (`--ourui-*`) plus per-node tone rules. Untoned buttons resolve to **primary**.

## Status

Pack API is **Stable** for the seeded default pack at OurUI **1.0**. Additional named packs (e.g. brand overrides as installable modules) may grow without breaking the Host Contract.
