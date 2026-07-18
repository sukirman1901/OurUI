# Page measure (`Theme(page=)`)

Optional page max-width / padding on the thin theme sheet:

```python
theme = ui.Theme(
    density="compact",
    primary="#18181b",
    page={"max_width": "none", "pad_block": "0", "pad_inline": "0"},  # full-bleed
)
```

When `page["max_width"]` is `none`, emit sets `data-page-bleed="1"`.

Brand roles still come from `ourui.theme` defaults + `ui.Theme(...)` overrides. Craft depth (pad, width, aspect, …) is [Style intents](../reference/style-intents.md), not `page=`.
