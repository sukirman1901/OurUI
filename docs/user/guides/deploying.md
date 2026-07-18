# Deploying

Run OurUI in production on a single machine with **`ourui serve --prod`**. Sessions are in-memory or **file-backed** — there is **no Redis** integration. For Docker/K8s recipes and Trusted Publishing, prefer the newer [Deploy](deploy.md) guide.

## Production command

Point the CLI at your app module and enable production mode:

```bash
ourui serve app.py --prod --host 0.0.0.0 --port 8765
```

| Flag | Purpose |
|------|---------|
| **`--prod`** | Session-scoped `State`, no HMR, CSRF, safe client errors, `GET /__ourui/health` |
| **`--host`** | Bind address (default `127.0.0.1`; use `0.0.0.0` to accept external traffic) |
| **`--port`** | Listen port (default `8765`) |
| **`--title`** | HTML document title (defaults to the source file stem) |
| **`--workers N`** | Worker processes (**requires `--prod`** when `N > 1`) |
| **`--session-dir DIR`** | Directory for file-backed session JSON |

Full flag list: [Reference: CLI](../reference/cli.md).

## What `--prod` changes

Compared to dev mode (no flags):

- **Hot reload off** — `/__ourui/hmr` returns 404.
- **`State` is per-session** — isolated via the `ourui_sid` cookie (`HttpOnly; SameSite=Lax`; `Secure` when `OURUI_COOKIE_SECURE=1`).
- **CSRF** — RPC requires the session CSRF token (host JS sends it automatically after GET).
- **Session gate** — POST does not create sessions; load a page first.
- **Rate limit** — `OURUI_RPC_RATE_LIMIT` (default 60/min).
- **Errors are safe** — RPC failures return `internal server error`; tracebacks stay on stderr.
- **CSP nonce** — scripts use a per-request nonce.
- **Health endpoint** — `GET /__ourui/health` for load balancers and process managers.

Example health check:

```bash
curl -s http://127.0.0.1:8765/__ourui/health
```

```json
{"ok": true, "mode": "prod", "workers": 1, "store": "memory", "pid": 12345}
```

## Single process (default)

With **`--prod`** and **`--workers 1`** (the default), sessions live **in memory** in one process. This is the simplest deployment: one VM, one container, or one systemd service.

```bash
ourui serve app.py --prod --host 0.0.0.0
```

Restarting the process clears all session state.

## Multiple workers on one machine

Use **`--workers N`** with **`N > 1`** to fork worker processes that share a listening socket. **`--workers` requires `--prod`.**

When **`N > 1`**, OurUI automatically selects a **file-backed session store** so every worker reads and writes the same session files:

```bash
ourui serve app.py --prod --workers 4 --host 0.0.0.0
```

The startup banner reports `store=file` and the resolved session directory.

## Session directory

Control where session JSON files are stored:

```bash
ourui serve app.py --prod --workers 2 --session-dir /var/lib/ourui/sessions
```

Or set the environment variable (used when **`--session-dir`** is omitted):

```bash
export OURUI_SESSION_DIR=/var/lib/ourui/sessions
ourui serve app.py --prod --workers 2
```

If you use **`--workers > 1`** without an explicit directory, OurUI defaults to **`$TMPDIR/ourui-sessions`** (or **`/tmp/ourui-sessions`**).

Each session is one JSON file, locked with **`fcntl.flock`**. This model is intended for **single-machine** multi-process serving — not a distributed Redis cluster.

## What P0 does not include

- **Redis** or other external session backends
- Sticky sessions behind a load balancer across **multiple machines**
- TLS termination (put a reverse proxy in front)
- Automatic process supervision (use systemd, Docker, or your orchestrator)

For deeper runtime behavior, see [Tutorial 06 — Serve: dev and prod](../tutorial/06-serve-dev-and-prod.md).

## Minimal systemd example

```ini
[Unit]
Description=OurUI app
After=network.target

[Service]
Type=simple
User=ourui
WorkingDirectory=/opt/my-app
Environment=OURUI_SESSION_DIR=/var/lib/ourui/sessions
ExecStart=/opt/my-app/.venv/bin/ourui serve /opt/my-app/app.py --prod --host 127.0.0.1 --port 8765 --workers 2
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Place nginx or Caddy in front for HTTPS and proxy to `127.0.0.1:8765`.

## Checklist before go-live

1. Run with **`--prod`** — never ship dev mode (global in-memory `State`, HMR, verbose errors).
2. Set **`--host`** and **`--port`** for your network layout.
3. If using **`--workers > 1`**, set **`--session-dir`** or **`OURUI_SESSION_DIR`** to a persistent path.
4. Verify **`GET /__ourui/health`** returns `"ok": true`.
5. Exercise `@server` handlers and confirm session state survives refreshes.

## See also

- [Tutorial 06 — Serve: dev and prod](../tutorial/06-serve-dev-and-prod.md) — dev vs prod behavior in detail
- [Reference: CLI](../reference/cli.md) — all commands and flags
- [Debugging with dump](debugging-with-dump.md) — inspect routes and tokens before deploy
