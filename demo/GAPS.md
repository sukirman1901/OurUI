# Gaps — Plasma-shaped SaaS dogfood (`demo/app.py`)

## Closed

| Phase | Deliverable |
|-------|-------------|
| **S1** | `ui.Link`, `ui.Shell` / `layout=` |
| **S2** | `ui.Input` / `Select` / `Toggle` / `Slider` → `@server` |
| **S3a** | `ui.Nav` + `placement=` + `tone=solid\|glass` |
| **S3** | Type / space / elevation tokens + `ui.ThemeToggle` |
| **S3b** | `ui.Footer` + Hero/Section `pad=` rhythm |
| **S4** | `gap=` / `pad=` / `align=` / `justify=` + `split-sidebar` |
| **S4m** | `motion=enter\|press\|reveal` + reduced-motion |
| **S5** | `ui.Canvas` Plasma escape (gradient / dither / raymarch) |
| **S6** | Drawer nav, Menu, Image, Icon, Meta, Code, CopyButton, control states |

## Still open (out of language scope)

| Plasma capability | Status |
|-------------------|--------|
| Redis share API | App concern + future data layer |
| Auth / billing / tables | Classic SaaS — later |

## Verdict

Landing + Studio dogfood the full Phase S arc. Living WebGL backgrounds ship via **S5 Canvas**. Remaining gaps are product/backend, not language surface.
