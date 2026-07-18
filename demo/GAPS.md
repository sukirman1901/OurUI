# Gaps — Plasma-shaped SaaS dogfood (`demo/app.py`)

## Closed in Phase S1

| Was missing | Now |
|-------------|-----|
| In-app navigation | **`ui.Link(href=…)`** — landing ↔ `/app` ↔ `/embed` |
| Studio 3-column chrome | **`ui.Shell(layout="split-3")`** (+ responsive stack &lt;768) |
| Section stack intent | **`layout="stack"`** on Section |

## Closed in Phase S2 (partial)

| Was missing | Now |
|-------------|-----|
| Text form field → server | **`ui.Input(name=…)`** — values collected on button click into `@server` payload |

## Still open (S2–S6 / product)

| Plasma capability | Status |
|-------------------|--------|
| Slider / Select / Toggle | **S2** remaining |
| `ui.Nav` + placement | **S3a** |
| WebGL / canvas / shaders | **S5** escape |
| Dropdown / clipboard / code block | **S6** |
| Image / logo / fonts / SEO meta | **S6** |
| Redis share API | App concern + future data layer |
| Auth / billing / tables | Classic SaaS — later |

## Verdict

S1 unlocked IA + Studio regions. S2 started **form → `@server`**. Plasma-class tooling still needs remaining S2 controls + S5 Canvas.
