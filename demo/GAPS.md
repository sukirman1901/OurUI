# Gaps — OurUI Playground (`demo/app.py`)

## Closed

| Want | Reality |
|------|---------|
| Editable source | `ui.Input(type="textarea")` bound to `source_code` |
| Run → compile | `@server run_playground` → `emit_all` / `dump_json` |
| Live Result | `ui.Frame` iframe `srcdoc` from `preview_html` |
| Live HTML/JS/CSS/AST | `ui.Code` bound to artifact States |
| Tab set like Svelte | Result · HTML · JS · CSS · AST |

## Intentional limits

| Want | Reality |
|------|---------|
| Monaco / syntax highlight | Textarea only — not an IDE embed |
| Tab swap without navigation | Tabs are **routes** |
| Multi-tenant sandbox | Localhost dogfood; iframe sandbox only |

## Seed artifacts

`python demo/bake_artifacts.py` refreshes initial hello sample strings in `playground_artifacts.py`. Day-to-day editing uses **Run**, not rebake.

## Out of language scope

Redis, auth, billing, tables — unchanged.
