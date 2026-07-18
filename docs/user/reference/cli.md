# CLI reference

The `ourui` command compiles Python OurUI modules and runs the interactive server. Normative behavior is defined in the [Language Spec](../../../LANGUAGE_SPEC.md).

## Commands

| Command | Purpose |
|---------|---------|
| `ourui dump <file>` | JSON artifacts |
| `ourui emit <file>` | HTML document |
| `ourui check <file> [--profile default\|enterprise] [--strict]` | Compile diagnostics |
| `ourui serve <file> [--prod] [--workers N] [--session-dir DIR] [--host] [--port] [--title]` | HTTP server |
| `ourui lsp` | Stdio language server |

`<file>` is the path to a Python OurUI module (for example `app.py` or `examples/tutorial/01_page.py`).

## `ourui dump`

Dump the compiler pipeline as JSON: Semantic Graph, Dependency Graph, IIR, LTR, and RTR.

```bash
ourui dump app.py
ourui dump app.py -o build/artifacts.json
```

| Flag | Default | Description |
|------|---------|-------------|
| `source` | (required) | Path to a Python OurUI module |
| `-o`, `--output` | stdout | Write JSON to a file instead of stdout |

Use dump to inspect routes, tokens, handlers, and state bindings before deploy. See [Debugging with dump](../guides/debugging-with-dump.md).

## `ourui emit`

Emit a static HTML document from the compiled HostNode RTR. Does not start a server — `@server` handlers are not callable from static HTML alone.

```bash
ourui emit app.py
ourui emit app.py -o dist/index.html --title "My App"
```

| Flag | Default | Description |
|------|---------|-------------|
| `source` | (required) | Path to a Python OurUI module |
| `-o`, `--output` | stdout | Write HTML to a file instead of stdout |
| `--title` | source stem | HTML document `<title>` |

## `ourui serve`

Run the interactive runtime:

- **`GET /`** (and other registered routes) — emit HTML for the matching `ui.Page`
- **`POST /__ourui/call/<handler>`** — run a `@server` function and return updated state

```bash
ourui serve app.py
ourui serve app.py --host 0.0.0.0 --port 8080 --title "Counter"
ourui serve app.py --prod --workers 4 --session-dir /var/lib/ourui/sessions
```

| Flag | Default | Description |
|------|---------|-------------|
| `source` | (required) | Path to a Python OurUI module |
| `--host` | `127.0.0.1` | Bind address |
| `--port` | `8765` | Bind port |
| `--title` | source stem | HTML document title |
| `--prod` | off | Production mode: no HMR, session `State`, CSRF, CSP nonce, safe errors, `/__ourui/health` |
| `--workers` | `1` | Worker processes (**requires `--prod`** when `> 1`) |
| `--session-dir` | none | Directory for file-backed sessions (or set **`OURUI_SESSION_DIR`**) |

Env (prod): `OURUI_COOKIE_SECURE`, `OURUI_RPC_RATE_LIMIT`, `OURUI_SESSION_DIR` — see [Deploy](../guides/deploy.md).

### Dev vs production

| Behavior | Dev (default) | `--prod` |
|----------|---------------|----------|
| Hot reload (HMR) | On — `GET /__ourui/hmr` (SSE) | Off — returns 404 |
| `State` | Process-global (shared across tabs) | Per-session via `ourui_sid` cookie |
| CSRF | Not required | Required (`X-OurUI-CSRF` / `_csrf`) |
| Handler errors | Traceback in JSON response | Generic `internal server error` |
| Unknown routes | JSON `404` | HTML `404` page |
| Health check | — | `GET /__ourui/health` |

When `--workers > 1`, OurUI uses a file-backed session store so all workers share session state. See [Serve: dev and prod](../tutorial/06-serve-dev-and-prod.md) and [Deploying](../guides/deploying.md).

## `ourui check`

Run compile diagnostics (path + span). Exit **1** on errors.

```bash
ourui check app.py
ourui check app.py --profile enterprise
ourui check app.py --profile enterprise --strict
```

| Flag | Default | Description |
|------|---------|-------------|
| `source` | (required) | Path to a Python OurUI module |
| `--profile` | `default` | `default` = compile diags; `enterprise` = + a11y/escape warnings |
| `--strict` | off | Promote enterprise warnings to errors (exit 1) |

Enterprise warnings (missing labels, missing `alt=`, empty buttons, Canvas/Frame budget) print with exit **0** unless `--strict`. See [Trust and compliance](../guides/trust-and-compliance.md) and [ADR-011](../../decisions/ADR-011-pack-versioning-check-profile.md).

## `ourui lsp`

Start the OurUI Language Server over stdio (JSON-RPC). Use it from your editor for completions and hover on `ui.*` components and token names.

```bash
ourui lsp
```

See [LSP and editor setup](../guides/lsp-editor-setup.md).

## See also

- [Getting started](../getting-started.md)
- [Debugging with dump](../guides/debugging-with-dump.md)
