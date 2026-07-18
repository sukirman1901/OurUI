# Threat model (OurUI host)

Scope: the thin Host (`ourui serve`) and emitted documents. Auth, SSO, and data stores are **app-layer** (see [gateway](../../../examples/enterprise/gateway/README.md)).

## Assets

| Asset | Notes |
|-------|--------|
| Session cookie (`ourui_sid`) | HttpOnly, SameSite=Lax; `Secure` when `OURUI_COOKIE_SECURE=1` |
| CSRF token | Per-session; required on prod RPC |
| `@server` handlers | Run in-process with session State |
| Dump / IR | Attestation includes schema, pack, `sha256` |

## Trust boundaries

1. **Browser ↔ Host** — same-origin RPC with cookie + CSRF; CSP meta (nonce in `--prod`).
2. **Gateway ↔ Host** — optional reverse proxy; gateway owns identity.
3. **Operator ↔ artifacts** — `ourui dump` attestation for CI pin.

## Threats and mitigations

| Threat | Mitigation |
|--------|------------|
| CSRF on RPC | Prod requires existing session + `X-OurUI-CSRF` / `_csrf`; GET mints meta token |
| Session fixation / blind POST | Prod POST rejects missing/unknown cookie (no create-on-POST) |
| XSS → script injection | Baseline CSP; prod emit uses per-request nonce on scripts |
| Error leakage | Prod RPC returns generic `internal server error` |
| RPC abuse | `OURUI_RPC_RATE_LIMIT` (default 60/min/client key) |
| Clickjacking | `X-Frame-Options: SAMEORIGIN` + related security headers |
| Frame/srcdoc XSS | Enterprise `SEC001` warning; sanitize at app layer |
| Supply-chain drift | Dump `attestation.sha256` + pinned package version |

## Out of scope (by design)

- OIDC / SSO inside `ui.*`
- Multi-tenant isolation beyond session bags
- WAF / bot management (edge)

## Related

- [Trust and compliance](trust-and-compliance.md)
- [Deploy](deploy.md)
