# Style intents (ADR-013)

OurUI maps presentation concerns to **intent props**, not Tailwind utility classes.
Scales (spacing, size, type, …) come from Tailwind-compatible CSS values; authoring stays OurUI.

See [ADR-013](../../decisions/ADR-013-style-intent-catalog.md) and the machine matrix in
`ourui.design.style_catalog`.

## Authoring

```python
from ourui import ui

theme = ui.Theme(
    recipe="product",
    sizes={"lg": "36rem"},  # override --ourui-size-lg
    space={"4": "1.25rem"},
)

ui.Shell(
    ui.Text("Sidebar"),
    layout="row",
    width="full",
    gap="4",
    pad_x="6",
    grow="1",
)
ui.Shell(
    ui.Card("Wide", width="lg", max_width="full", radius="lg", shadow="md"),
    grid_cols="3",
    gap="4",
)
```

## Families (examples)

| Concern | Props |
|---|---|
| Box size | `width=` `height=` `min_width=` `max_width=` `size=` + logical `inline_size=` / `block_size=` |
| Space | `pad=` `pad_x=` `pad_y=` `pad_t/r/b/l=` `margin=` `margin_*` `gap=` `gap_x=` `gap_y=` |
| Flex | `grow=` `shrink=` `basis=` `wrap=` `flex=` `direction=` `order=` |
| Grid | `grid_cols=` `grid_rows=` `col_span=` `row_span=` `grid_flow=` `grid_auto_cols=` `grid_auto_rows=` (Table keeps `columns=` / `rows=` for data) |
| Type | `text=` (scale keys only) `weight=` `leading=` `tracking=` `align_text=` `decorate=` `text_columns=` |
| Surface | `radius=` `border=` `border_w=` `shadow=` / `elev=` `opacity=` `blur=` `filter=` `bg_size=` `bg_position=` `bg_repeat=` |
| Position | `pos=` `inset=` `top=` … `z=` `overflow=` `aspect=` `object_position=` |
| Transform | `rotate=` `scale=` `translate_x/y=` `skew_x/y=` |
| Responsive | `hide_below=` `show_below=` (`md` \| `lg`) |

Values are scale keys (`lg`, `4`, `1/2`) or allowlisted literals (`12rem`, `50%`).
Emit produces `.ourui-w-lg { width: var(--ourui-size-lg); }` — never `class="w-lg"` in source.

## Custom

- Token colors / fonts: `ui.Theme(primary=..., font_sans=...)`
- Scale tables: `ui.Theme(space={...}, sizes={...}, type={...})`

## Escape vs kit

- **C / escape:** blend, mask, arbitrary background-image, perspective — use `Canvas` / `Frame` / host CSS.
- **Kit:** not part of the language ([ADR-014](../../decisions/ADR-014-language-primitives-vs-kit.md)). Compose primitives in app code or a future out-of-language kit.
