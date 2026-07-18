# Design packs

The default pack is **`ourui-default`** @ **`1.0.0`** (zinc/ink product defaults as of 1.0.1), produced from `ui.Theme` / `theme.py` tokens into Resolved Design. Pack recipes also seed page chrome (`max_width`, padding), control padding, and density recipes.

## Authoring

```python
theme = ui.Theme(
    primary="#18181b",
    accent="#2563eb",
    density="comfortable",  # or "compact"
    # … see docs/user/reference/theme.md
)
```

Emit consumes **Resolved Design** (Host Contract): pack CSS variables (`--ourui-*`) plus per-node tone rules. Untoned buttons resolve to **primary**. Compact density adds `ourui-density-compact` on `<html>` / `.ourui-root`. Dump includes `pack_version` and optional `density`.

## Status

Pack API is **Stable** for the seeded default pack at OurUI **1.5**. Additional named packs (e.g. brand overrides as installable modules) may grow without breaking the Host Contract. See [ADR-011](../../decisions/ADR-011-pack-versioning-check-profile.md).
