# Debugging with dump

Inspect what the compiler sees before you run or deploy. Use **`ourui dump`** for JSON artifacts and compare **dev vs prod** error behavior from **`ourui serve`**.

## Dump compiler output

Dump the full pipeline for a module:

```bash
ourui dump app.py
```

Write to a file for repeated inspection:

```bash
ourui dump app.py -o build/artifacts.json
```

Preview the top of the document:

```bash
ourui dump app.py | head
```

The JSON includes **`version`** (dump schema **30**), **`semantic_graph`**, **`dependency_graph`**, **`iir`**, **`presentation_graph`**, **`resolved_design`**, **`ltr`**, **`rtr`**, **`attestation`** (schema / motion_catalog / `sha256`), **`style_catalog`** (ADR-013 matrix), **`motion`**, and an **`emit`** capability map (incl. `style_intents`). You rarely need every section — start with the semantic graph and `resolved_design.tokens`.

## Check routes

For apps with multiple pages, open **`semantic_graph.routes`**. It maps URL paths to root node IDs:

```bash
ourui dump examples/tutorial/04_routing.py | python3 -c "
import json, sys
sg = json.load(sys.stdin)['semantic_graph']
print(json.dumps(sg['routes'], indent=2))
"
```

Example output:

```json
{
  "/": "n0001",
  "/about": "n0003"
}
```

If a route is missing, verify the module defines **`ui.Page(..., route="/path")`** at top level and that you passed the correct source file to the CLI.

## Check design tokens

Theme overrides land in **`semantic_graph.tokens`**, split by **`light`** and **`dark`**:

```bash
ourui dump examples/tutorial/05_theme.py | python3 -c "
import json, sys
sg = json.load(sys.stdin)['semantic_graph']
print('light primary:', sg['tokens']['light'].get('primary'))
"
```

Compare token values here when colors look wrong in the browser but your Python source looks correct.

## Other useful sections

| Section | Use when |
|---------|----------|
| **`semantic_graph.nodes`** | Inspect the UI tree the analyzer built (kinds, attributes, spans) |
| **`dependency_graph`** | See component expansion edges |
| **`iir` / `ltr` / `rtr`** | Trace lowering stages (advanced) |
| **`source`** | Confirm which file path was compiled |

Spans include **`start_line`**, **`end_line`**, and **`path`** — tie compiler nodes back to your editor.

## Serve errors: dev vs prod

When an **`@server`** handler raises, **`ourui serve`** returns JSON with **`"ok": false`**.

### Development (default)

Dev mode includes the **traceback in the HTTP response** so you can debug from the browser network tab or client code:

```json
{
  "ok": false,
  "error": "division by zero",
  "traceback": "Traceback (most recent call last):\n  ..."
}
```

The full traceback is also printed on **server stderr**.

### Production (`--prod`)

Prod mode returns only a **safe error string** — no traceback in the response:

```json
{
  "ok": false,
  "error": "division by zero"
}
```

Tracebacks still appear on **server stderr**; check process logs or your orchestrator.

Reproduce locally:

```bash
# Dev — traceback in JSON response
ourui serve app.py

# Prod — traceback hidden from clients
ourui serve app.py --prod
```

Trigger a failing handler from the browser or with curl:

```bash
curl -s -X POST http://127.0.0.1:8765/__ourui/call/my_handler \
  -H 'Content-Type: application/json' \
  -d '{}'
```

## Suggested workflow

1. **`ourui dump app.py`** — confirm **`routes`** and **`tokens`** match intent.
2. **`ourui serve app.py`** — iterate with HMR and verbose RPC errors.
3. Fix handler bugs using dev tracebacks, then re-dump if routing or theme changed.
4. **`ourui serve app.py --prod`** — verify errors are sanitized before deploy (see [Deploying](deploying.md)).

## See also

- [Tutorial 06 — Serve: dev and prod](../tutorial/06-serve-dev-and-prod.md) — prod flags and health checks
- [Deploying](deploying.md) — production serving
- [Reference: CLI](../reference/cli.md) — `ourui dump` and `ourui serve` flags
