# Design packs

Named **packs** set brand expression. Named **recipes** bundle pack + density + page measure — intentional combinations, not a free token shuffle.

Anti-slop guardrails: no purple/indigo defaults, no cream+serif+terracotta brochure, no neon accents.

## Packs (`pack=`)

| Pack | Axis | Look |
|------|------|------|
| `ourui-default` | Product | Zinc/ink, blue accent, `0.375rem` radius, IBM Plex Sans |
| `ourui-editorial` | Reading | Warm stone, sharp `radius: 0`, quiet stone accent, narrower measure |
| `ourui-console` | Ops/data | Cool slate, cyan-700 accent, `0.25rem` radius, wider page |

```python
theme = ui.Theme(pack="ourui-editorial")
```

## Recipes (`recipe=`)

| Recipe | Pack | Density | Page max |
|--------|------|---------|----------|
| `product` | `ourui-default` | comfortable | 42rem |
| `ops` | `ourui-default` | compact | 72rem |
| `editorial` | `ourui-editorial` | comfortable | 36rem |
| `console` | `ourui-console` | compact | 80rem |

```python
theme = ui.Theme(recipe="ops")
# still allow overrides:
theme = ui.Theme(recipe="console", primary="#0f172a")
```

`recipe=` sets pack + density (unless you also pass `density=`). Color kwargs still override tokens.

## Authoring

```python
theme = ui.Theme(
    recipe="product",
    # or pack="ourui-default", density="comfortable",
    accent="#2563eb",
)
```

Emit consumes **Resolved Design**: `--ourui-*` vars, `--ourui-page-max-width`, density class. Dump includes `pack`, `pack_version`, optional `recipe` / `page`.

## Status

Pack API **Stable** at OurUI **1.7** (catalog v1.1.0). Additional packs/recipes may grow without breaking the Host Contract. See [ADR-011](../../decisions/ADR-011-pack-versioning-check-profile.md).
