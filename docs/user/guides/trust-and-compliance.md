# Trust and compliance

Enterprise trust baseline for emitted documents, dump artifacts, and production host hardening. OurUI is a **compiler + thin host** — auth, SSO, and data stores stay at the app layer ([gateway](../../../examples/enterprise/gateway/README.md), [threat model](threat-model.md)).

## Content Security Policy (CSP)

HTML emit includes a CSP meta tag with `data-ourui-csp="1"`.

**Static emit / dev:** `script-src` allows `'unsafe-inline'` (inline Host shim + Plasma).

**`ourui serve --prod`:** per-request nonce on `<script>` tags and matching `script-src 'nonce-…'` (no `'unsafe-inline'` for scripts).

**Recommendation:** Prefer `Content-Security-Policy-Report-Only` on your reverse proxy while auditing third-party fonts, then rely on the nonce path in production.

## Production host controls

| Control | Behavior |
|---------|----------|
| Session cookie | `HttpOnly; SameSite=Lax`; add `Secure` with `OURUI_COOKIE_SECURE=1` |
| CSRF | Meta `ourui-csrf` + header `X-OurUI-CSRF` / body `_csrf` required on prod RPC |
| Session gate | Prod POST does not create sessions — GET first |
| Rate limit | `OURUI_RPC_RATE_LIMIT` (default `60` / minute / client key; `0` disables) |
| Errors | Prod RPC returns generic `internal server error` |
| Headers | `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`, `Permissions-Policy` |

## SBOM / supply chain

```bash
pip install ourui==1.9.1
pip freeze | grep -i ourui
```

Include the pinned `ourui` version and Python interpreter from your container image (`deploy/Dockerfile`).

## Dump attestation

`ourui dump` / `compile_dump` includes:

```json
"attestation": {
  "schema": 28,
  "pack": "ourui-default",
  "pack_version": "1.0.0",
  "sha256": "<hex digest of dump without sha256 field>"
}
```

Pin schema + pack + hash in CI gates.

## Accessibility / security check profile

```bash
ourui check app.py --profile enterprise
ourui check app.py --profile enterprise --strict
```

Enterprise warnings include a11y codes, escape budget (`ESC001`), and Frame/srcdoc (`SEC001`). Exit **0** unless `--strict`.

## PDF host

A second Host (PDF) is **Draft** only — [RFC-004](../../rfcs/RFC-004-second-host-pdf.md).
