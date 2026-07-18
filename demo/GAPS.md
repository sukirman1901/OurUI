# Gaps — Plasma-shaped SaaS dogfood (`demo/app.py`)

## Closed in Phase S1

| Was missing | Now |
|-------------|-----|
| In-app navigation | **`ui.Link(href=…)`** — landing ↔ `/app` ↔ `/embed` |
| Studio 3-column chrome | **`ui.Shell(layout="split-3")`** (+ responsive stack &lt;768) |
| Section stack intent | **`layout="stack"`** on Section |

## Still open (S2–S6 / product)

| Plasma capability | Status |
|-------------------|--------|
| WebGL / canvas / shaders | **S5** escape |
| Sliders / color / select / toggle | **S2** |
| Dropdown / clipboard / code block | **S6** |
| Image / logo / fonts / SEO meta | **S6** |
| Redis share API | App concern + future data layer |
| Auth / billing / tables | Classic SaaS — later |

## Verdict

S1 makes the **IA clickable** and the Studio **region layout** real.  
Plasma-class **tooling** still needs S2 controls + S5 Canvas.
