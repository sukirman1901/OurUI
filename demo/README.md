# OurUI Playground

Compiler REPL — write OurUI intent, press **Run**, inspect **Result / HTML / JS / CSS / AST**.

## Run

```bash
# from repo root (editable install)
python demo/bake_artifacts.py   # optional: refresh hello seed
ourui serve demo/app.py --port 8766
```

Open http://127.0.0.1:8766/

| Route | Pane |
|-------|------|
| `/` | Result — iframe preview of last compile |
| `/html` | Emitted HTML document |
| `/js` | Host JS (`emit_js`) |
| `/css` | Token/style CSS (`emit_css`) |
| `/ast` | `dump_json` (schema v21) |
| `/about` | About |

## How to use

1. Edit Python OurUI in the left **textarea**.
2. Click **Run** (collects `source` field → compiles on server).
3. Switch tabs for HTML / JS / CSS / AST; Result shows the compiled page in an iframe.
4. **Reset** restores the baked `hello_sample` seed.

## Files

| File | Role |
|------|------|
| `app.py` | Playground shell (editable REPL) |
| `hello_sample.py` | Canonical hello seed |
| `bake_artifacts.py` | Seeds `playground_artifacts.py` |
| `playground_artifacts.py` | Generated initial strings |

## Gaps

See [GAPS.md](GAPS.md).
