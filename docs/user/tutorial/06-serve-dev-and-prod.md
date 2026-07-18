# Tutorial 06 — Serve: dev and prod

## Goal

Run the full sample app with **`ourui serve`**, understand **development vs production** behavior, and use CLI flags for sessions, workers, and health checks.

The app for this step is **`examples/tutorial/06_counter_app.py`** — the same counter demo from [Getting started](../getting-started.md). It combines routing concepts from earlier tutorials: `ui.Page`, `State`, `@server`, components, and `ui.Theme`.

## Code

**`examples/tutorial/06_counter_app.py`** (abbreviated)

```python
from ourui import Component, State, server, ui

theme = ui.Theme(primary="#1a5f4a", primary_fg="#f5faf8")
count = State(0)

@server
def increment() -> int:
    count.set(count.get() + 1)
    return count.get()

page = ui.Page(
    ui.Hero(title="Welcome", subtitle="Build SaaS in Python", ...),
    CounterPanel("Counter"),
)
```

### Development (default)

Hot reload and shared in-process state — best for local iteration:

```bash
ourui serve examples/tutorial/06_counter_app.py
```

Optional flags (same as production):

```bash
ourui serve examples/tutorial/06_counter_app.py --host 127.0.0.1 --port 8765 --title "Counter demo"
```

| Behavior | Dev (default) |
|----------|-----------------|
| Hot reload (HMR) | **On** — edit the `.py` file and the browser reloads via `GET /__ourui/hmr` (SSE) |
| `State` | **Process-global** — shared across browser tabs |
| Sessions | None |
| Error responses | Server tracebacks included in JSON on handler failures |
| Unknown routes | JSON `404` |

### Production

Per-browser sessions, safe errors, and a health endpoint:

```bash
ourui serve examples/tutorial/06_counter_app.py --prod
```

| Behavior | `--prod` |
|----------|----------|
| Hot reload | **Off** — `/__ourui/hmr` returns 404 |
| `State` | **Per-session** — isolated via `ourui_sid` cookie |
| Error responses | Generic message only (no traceback in the HTTP response) |
| Unknown routes | HTML `404` page |
| Health check | **`GET /__ourui/health`** |

Example health response:

```bash
curl -s http://127.0.0.1:8765/__ourui/health
```

```json
{"ok": true, "mode": "prod", "workers": 1, "store": "memory", "pid": 12345}
```

In dev mode, `"mode"` is `"dev"` and the store is still reported (memory in single-worker dev).

### Multiple workers

Scale HTTP workers (production only):

```bash
ourui serve examples/tutorial/06_counter_app.py --prod --workers 4
```

**`--workers N`** requires **`--prod`**. When `N > 1`, OurUI uses a **file-backed session store** so all workers share session state. The startup banner shows `store=file` and the resolved session directory.

### Session directory

Control where session JSON files are stored:

```bash
ourui serve examples/tutorial/06_counter_app.py --prod --workers 2 --session-dir /var/lib/ourui/sessions
```

Or set the environment variable (used when `--session-dir` is omitted):

```bash
export OURUI_SESSION_DIR=/var/lib/ourui/sessions
ourui serve examples/tutorial/06_counter_app.py --prod --workers 2
```

File storage is also selected automatically when **`--workers > 1`** even without an explicit directory — OurUI then defaults to `$TMPDIR/ourui-sessions` (or `/tmp/ourui-sessions`).

### CLI reference (`ourui serve`)

Verified against the current CLI:

| Flag | Default | Description |
|------|---------|-------------|
| `source` | (required) | Path to a Python OurUI module |
| `--host` | `127.0.0.1` | Bind address |
| `--port` | `8765` | Bind port |
| `--title` | source stem | HTML document title |
| `--prod` | off | Production mode: no HMR, session State, safe errors, `/__ourui/health` |
| `--workers` | `1` | Worker processes (**requires `--prod`** when `> 1`) |
| `--session-dir` | none | Directory for file-backed sessions (or set **`OURUI_SESSION_DIR`**) |

On startup, the banner prints each page URL, `POST /__ourui/call/<handler>`, and `GET /__ourui/health`. In dev mode it also lists `GET /__ourui/hmr (SSE reload)`.

## What you learned

- **`ourui serve`** is the interactive runtime: **`GET /`** (and other routes) emit HTML; **`POST /__ourui/call/<handler>`** runs `@server` functions.
- **Dev mode** (no flags) enables **HMR** and keeps **`State` in memory** for fast local development.
- **`--prod`** turns off HMR, scopes **`State` to sessions**, hides tracebacks from clients, and exposes **`GET /__ourui/health`** for load balancers and orchestrators.
- **`--workers N`** with **`--prod`** runs multiple processes; **`N > 1`** forces a **file session store** so state stays consistent across workers.
- Use **`--session-dir`** or **`OURUI_SESSION_DIR`** when you need durable or shared session storage across restarts or machines.
- **`06_counter_app.py`** is the reference app that ties together pages, theme, state, server handlers, and components — run it in dev while learning, then try **`--prod`** before deploying.

## Next

- [Guides: Project layout](../guides/project-layout.md) — organizing a real project (coming soon)
- [Guides: Deploying](../guides/deploying.md) — production deployment (coming soon)
- [Reference: CLI](../reference/cli.md) — full CLI lookup (coming soon)
