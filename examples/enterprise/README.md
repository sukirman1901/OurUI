# Enterprise Kit 1.0

Clone-ready screens for org apps built with OurUI. **Auth and databases are templates**, not language features — keep SSO/ORM outside `ui.*`.

## What’s included

| App | Role |
|-----|------|
| [`crud_app.py`](crud_app.py) | Admin list + Form + Show/When + dynamic Table |
| [`settings_app.py`](settings_app.py) | ThemeToggle, form fields, Show/When |
| [`audit_app.py`](audit_app.py) | Audit-style Table from `State` |
| [`ai_console_app.py`](ai_console_app.py) | Textarea + Code/Frame bind + `@server` echo |
| [`templates/AUTH_OIDC.md`](templates/AUTH_OIDC.md) | Wire FastAPI + OIDC **outside** OurUI |

## Run locally

From the repo root (editable install):

```bash
pip install -e packages/ourui
ourui serve examples/enterprise/crud_app.py
ourui serve examples/enterprise/settings_app.py --port 8766
```

Check with the enterprise a11y profile:

```bash
ourui check examples/enterprise/crud_app.py --profile enterprise
```

Deploy recipes: [`docs/user/guides/deploy.md`](../../docs/user/guides/deploy.md) and [`deploy/`](../../deploy/).

## Branding

Override tokens with `ui.Theme(...)` (and `density="compact"` if needed). Pack identity is `ourui-default` @ `1.0.0` in Resolved Design / dump attestation.

## Out of scope

Redis, billing, ORM, and SSO live in your FastAPI (or other) layer — see the OIDC stub. Do not expect `ui.Login` or similar.
