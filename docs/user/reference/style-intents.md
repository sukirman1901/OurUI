# Style intents (ADR-013)

OurUI’s package north-star is **utility-depth compile**: Tailwind TOC families become **intent props** and finite `.ourui-*` CSS — not class strings, not Vite. `ui.Theme` only overrides brand roles / scales; it is not this catalog.

## Teaching example — ring (box-shadow)

Tailwind v4 documents rings under [`box-shadow`](https://tailwindcss.com/docs/box-shadow) (“Adding a ring”), not a standalone `/docs/ring-width` page.

| Tailwind | OurUI |
|---|---|
| `ring-2` | `ring="2"` |
| `ring` (≈3px) | `ring=True` or `ring="ring"` |
| `ring-4` + color | `ring="4", ring_color="primary"` |
| `inset-ring-2` | `ring="2", ring_inset=True` |

```python
ui.Button("Save", color="primary", ring="2", ring_color="primary")
```

## Teaching example — outline / accent / font-numeric

| Tailwind | OurUI |
|---|---|
| `outline-2` | `outline="2"` |
| `outline-none` | `outline="none"` |
| `outline-primary` + offset | `outline_color="primary", outline_offset="2"` |
| `accent-primary` | `accent_color="primary"` or `accent="primary"` |
| `tabular-nums` | `font_numeric="tabular"` |
| `focus-visible:outline-2` | `focus={"outline": "2"}` |

```python
ui.Button("Save", outline="2", outline_color="primary", focus={"outline": "2"})
ui.Input(accent_color="accent")
ui.Text("1,234.56", font_numeric="tabular")
```

## Teaching example — placeholder / selection

| Tailwind | OurUI |
|---|---|
| `placeholder:text-muted` | `placeholder_color="muted"` (not `placeholder=` — that is the input string) |
| `selection:bg-primary` | `selection={"bg": "primary"}` or `selection_bg="primary"` |
| `selection:text-fg` | `selection={"color": "fg"}` or `selection_color="fg"` |

```python
ui.Input(
    placeholder="Email",
    placeholder_color="muted",
    selection={"bg": "primary", "color": "fg"},
)
```

## Teaching example — content (pseudo) + container queries

| Tailwind | OurUI |
|---|---|
| `after:content-['↗']` | `after={"content": "↗"}` or `after_content="↗"` |
| `before:content-none` | `before={"content": "none"}` |
| `@container` | `container=True` (or `container="sidebar"`) |
| `@md:flex-row` | `direction={"base": "col", "@md": "row"}` |
| `@lg:p-8` | `pad={"@lg": "8"}` (aliases `cq_md` / `cq_lg`) |

```python
ui.Shell(
    ui.Link("Docs", href="/docs", after={"content": " ↗"}),
    container=True,
    direction={"base": "col", "@md": "row"},
    pad={"base": "4", "@lg": "8"},
)
```

Note: Text **`content=`** remains the text string — CSS `content` is only via `before` / `after`.

## Teaching example — L3 batch (divide / space / scroll / sr-only / caret / gradient)

| Tailwind | OurUI |
|---|---|
| `divide-x` / `divide-y` | `divide="x"` / `divide="y"` (+ `divide_w=` `divide_color=`) |
| `space-x-4` / `space-y-2` | `space_x="4"` / `space_y="2"` |
| `scroll-mt-4` / `scroll-p-8` | `scroll_mt="4"` / `scroll_p="8"` |
| `sr-only` | `sr_only=True` |
| `caret-primary` | `caret="primary"` or `caret_color="primary"` |
| `bg-linear-to-r` + stops | `bg_gradient="to-r", gradient_from="primary", gradient_to="accent"` |

```python
ui.Shell(
    ui.Text("One"),
    ui.Text("Two"),
    divide="y",
    space_y="4",
    scroll_m="4",
)
ui.Label("Screen reader only", sr_only=True)
ui.Shell(bg_gradient="to-r", gradient_from="primary", gradient_to="accent", pad="8")
```

## Teaching example — responsive depth (dict, not `md:` classes)

Mobile-first: string props apply at all sizes; dict keys `base` / `md` / `lg` emit `.ourui-*` plus `.ourui-md-*` / `.ourui-lg-*` under min-width media queries.

| Tailwind | OurUI |
|---|---|
| `p-4 md:p-8` | `pad={"base": "4", "md": "8"}` |
| `md:w-lg` | `width={"md": "lg"}` |
| `grid-cols-1 md:grid-cols-3` | `grid_cols={"base": 1, "md": 3}` |
| `flex-col md:flex-row` | `direction={"base": "col", "md": "row"}` |

```python
ui.Shell(
    ui.Text("Sidebar"),
    pad={"base": "4", "md": "8"},
    width={"base": "full", "md": "lg"},
    direction={"base": "col", "md": "row"},
    gap={"md": "6"},
)
```

## Teaching example — hover / focus (state variants)

| Tailwind | OurUI |
|---|---|
| `opacity-100 hover:opacity-80` | `opacity={"base": "100", "hover": "80"}` |
| `hover:shadow-lg` | `shadow={"hover": "lg"}` or `hover={"shadow": "lg"}` |
| `hover:scale-105` | `scale={"hover": "105"}` |
| `focus-visible:ring-2` | `focus={"ring": "2"}` |

```python
ui.Button(
    "Save",
    color="primary",
    opacity={"hover": "90"},
    hover={"shadow": "md"},
    focus={"ring": "2"},
)
```

## Teaching example — aspect-ratio

| Tailwind | CSS | OurUI |
|---|---|---|
| `aspect-square` | `aspect-ratio: 1 / 1` | `aspect="square"` |
| `aspect-video` | `aspect-ratio: 16 / 9` | `aspect="video"` or `aspect="16/9"` |
| `aspect-auto` | `aspect-ratio: auto` | `aspect="auto"` |
| `aspect-3/2` etc. | `3 / 2` … | `aspect="3/2"` (also `2/3`, `4/3`, `9/16`, `21/9`, …) |
| `aspect-[…]` | arbitrary | allowlisted literal / escape |

```python
ui.Shell(ui.Image(src="/hero.jpg", alt="…"), aspect="video", width="full")
```

Emit produces utilities like `.ourui-aspect-video { aspect-ratio: var(--ourui-aspect-video); }` — never `class="aspect-video"` in source.

See [ADR-013](../../decisions/ADR-013-style-intent-catalog.md), the machine matrix in `ourui.design.style_catalog`, and [Tailwind gap](../../architecture/tailwind-gap.md). The catalog is **foundation — still incomplete**.

## Authoring

```python
from ourui import ui

theme = ui.Theme(
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
| Space | `pad=` `pad_x=` `pad_y=` `pad_t/r/b/l=` `margin=` `margin_*` `gap=` `gap_x=` `gap_y=` `space_x=` `space_y=` `scroll_m=` `scroll_p=` + sides |
| Flex | `grow=` `shrink=` `basis=` `wrap=` `flex=` `direction=` `order=` |
| Grid | `grid_cols=` `grid_rows=` `col_span=` `row_span=` `grid_flow=` `grid_auto_cols=` `grid_auto_rows=` (Table keeps `columns=` / `rows=` for data) |
| Type | `text=` (scale keys only) `weight=` `leading=` `tracking=` `align_text=` `decorate=` `text_columns=` `font_numeric=` `font_stretch=` `font_feature=` |
| Surface | `radius=` `border=` `border_w=` `outline=` `outline_color=` `outline_offset=` `shadow=` / `elev=` `ring=` `ring_color=` `ring_inset=` `divide=` `divide_w=` `divide_color=` `bg_gradient=` `gradient_from=` `gradient_to=` `bg_image=` `mix_blend=` `backdrop_blend=` `mask=` `opacity=` `blur=` `filter=` `bg_size=` `bg_position=` `bg_repeat=` |
| Position | `pos=` `inset=` `top=` … `z=` `overflow=` `aspect=` `object_position=` |
| Interactivity | `cursor=` `select=` `pointer=` `caret=` / `caret_color=` `accent=` / `accent_color=` `placeholder_color=` `selection=` / `selection_bg=` / `selection_color=` `sr_only=` `appearance=` `color_scheme=` `scrollbar_width=` `scrollbar_gutter=` `scrollbar_color=` `hover=` / `focus=` bags `before=` / `after=` / `before_content=` / `after_content=` |
| Type extras | `tab_size=` `text_indent=` (SPACE) |
| Transform | `rotate=` `scale=` `translate_x/y=` `skew_x/y=` `backface=` `zoom=` |
| Form extras | `field_sizing=` |
| Responsive | `hide_below=` `show_below=` (`md` \| `lg`); dict overrides `pad={"base":"4","md":"8"}` `width={"md":"lg"}` `grid_cols=` `direction=` `grow=` `text=` (type scale); **container:** `container=True` + `@md`/`@lg`/`cq_md`/`cq_lg` dict keys |

Values are scale keys (`lg`, `4`, `1/2`) or allowlisted literals (`12rem`, `50%`).

## Custom

- Theme roles / fonts: `ui.Theme(primary=..., font_sans=...)` — see [Theme](theme.md)
- Scale tables: `ui.Theme(space={...}, sizes={...}, type={...})`
- Author CSS escape: `ui.Theme(css="…")` — raw CSS appended after utilities (no package edit)

## Escape vs compose

- **C / escape:** arbitrary mask/font-feature beyond allowlists — `Theme(css=)`. Rich media still `Image` / `Canvas`.
- **Compose in app code:** section patterns built from primitives + utilities — not new Stable `ui.*` kinds while foundation is incomplete ([ADR-014](../../decisions/ADR-014-language-primitives-vs-kit.md)).
