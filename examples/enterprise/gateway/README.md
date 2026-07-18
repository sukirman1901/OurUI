# Auth gateway (outside OurUI)

Put **identity in front of** `ourui serve --prod`. OurUI sessions (cookie + CSRF) still apply; the gateway only proves the caller is allowed to reach the host.

## Architecture

```text
Browser → FastAPI gateway (Bearer / OIDC) → ourui serve --prod
              ↑                                    ↑
         app-layer auth                    CSRF + session cookie
```

## Quick start

```bash
# Terminal 1 — OurUI host
pip install -e packages/ourui
ourui serve examples/enterprise/crud_app.py --prod --port 8765

# Terminal 2 — gateway
pip install fastapi uvicorn httpx
OURUI_GATEWAY_TOKEN=dev-token OURUI_UPSTREAM=http://127.0.0.1:8765 \
  uvicorn examples.enterprise.gateway.app:app --port 8080

# Call through gateway
curl -H "Authorization: Bearer dev-token" http://127.0.0.1:8080/
```

## Production checklist

- [ ] Replace Bearer demo with OIDC / IdP session (see [`../templates/AUTH_OIDC.md`](../templates/AUTH_OIDC.md))
- [ ] Terminate TLS at the edge; set `OURUI_COOKIE_SECURE=1` on the OurUI process
- [ ] Do not strip `Cookie` or `X-OurUI-CSRF` when proxying RPC
- [ ] Keep secrets in env / secret manager — never in Intent files
- [ ] Rate-limit at the gateway *and* keep OurUI `OURUI_RPC_RATE_LIMIT` as defense in depth

## What stays out of `ui.*`

Login screens, JWT validation, role claims, and ORM access belong here — not in the OurUI language surface.
