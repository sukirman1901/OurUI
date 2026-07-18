# Gaps — Plasma-shaped SaaS dogfood (`demo/app.py`)

## Closed in Phase S1

| Was missing | Now |
|-------------|-----|
| In-app navigation | **`ui.Link(href=…)`** — landing ↔ `/app` ↔ `/embed` |
| Studio 3-column chrome | **`ui.Shell(layout="split-3")`** (+ responsive stack &lt;768) |
| Section stack intent | **`layout="stack"`** on Section |

## Closed in Phase S2

| Was missing | Now |
|-------------|-----|
| Text form field → server | **`ui.Input`** |
| Dropdown / checkbox / range | **`ui.Select`**, **`ui.Toggle`**, **`ui.Slider`** |

## Still open (S3–S6 / product)

| Plasma capability | Status |
|-------------------|--------|
| `ui.Nav` + placement | **S3a** |
| WebGL / canvas / shaders | **S5** escape |
| Dropdown menus / clipboard / code block | **S6** |
| Image / logo / fonts / SEO meta | **S6** |
| Redis share API | App concern + future data layer |
| Auth / billing / tables | Classic SaaS — later |

## Verdict

S1 unlocked IA + Studio regions. **S2 form controls** (`Input` / `Select` / `Toggle` / `Slider`) post to `@server`. Next product chrome is **S3a Nav**.
