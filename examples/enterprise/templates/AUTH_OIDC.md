# Auth / OIDC template (outside OurUI)

**Status:** Stub for Enterprise Kit  
**Rule:** Do **not** put SSO inside `ui.*`. Wire identity in your app server, then serve OurUI pages behind it.

## Pattern

```text
Browser → FastAPI (OIDC / session cookie) → ourui serve --prod
              ↑                                    ↑
         app-layer auth                    CSRF + session cookie
```

Runnable Bearer-token proxy: [`../gateway/`](../gateway/) (swap Bearer for OIDC in production).

1. Use a FastAPI (or similar) app with an OIDC library (`authlib`, `fastapi-sso`, IdP SDK, etc.).
2. Protect routes that call `ourui` emit/serve or that proxy `POST /__ourui/call/<handler>`.
3. Pass the authenticated user id into `@server` handlers via your own request context — not via a language primitive.
4. Keep refresh tokens / client secrets in env vars; never in Intent files.
5. When proxying, forward `Cookie` and `X-OurUI-CSRF` unchanged.

## Sketch (non-normative)

```python
# Prefer examples/enterprise/gateway/app.py as the starting point.
from fastapi import Depends, FastAPI
# from your_oidc import require_user

app = FastAPI()

@app.get("/")
async def home(user=Depends(require_user)):
    # Option A: reverse-proxy to `ourui serve --prod`
    # Option B: call ourui.pipeline.emit_html(...) and return HTML
    ...
```

## Checklist

- [ ] IdP client registered; redirect URIs match deploy host
- [ ] Session cookie `HttpOnly` + `Secure` in production (`OURUI_COOKIE_SECURE=1` on OurUI)
- [ ] CSRF: OurUI prod RPC + any extra gateway forms
- [ ] Map roles/claims to app authorization (not to OurUI components)

See also [Trust and compliance](../../../docs/user/guides/trust-and-compliance.md), [Threat model](../../../docs/user/guides/threat-model.md), and [Deploy](../../../docs/user/guides/deploy.md).
