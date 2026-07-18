# Trust and compliance

Enterprise E5 baseline for emitted documents and dump artifacts. OurUI is a **compiler + thin host** — auth, SSO, and data stores stay at the app layer.

## Content Security Policy (CSP)

HTML emit includes a baseline CSP meta tag with `data-ourui-csp="1"`:

```text
default-src 'self';
script-src 'self' 'unsafe-inline';
style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
font-src 'self' https://fonts.gstatic.com
```

**Why `'unsafe-inline'`?** The Host Contract shim and Plasma engine ship as inline `<script>` / `<style>` blocks today. Treat this as a documented baseline, not a hardened production policy.

**Recommendation:** Prefer `Content-Security-Policy-Report-Only` (HTTP header) on your reverse proxy while you audit fonts and handlers, then tighten `script-src` once you move scripts to nonces or external bundles (future emit option).

## SBOM / supply chain

Record what you run:

```bash
pip install ourui==1.5.0
pip freeze | grep -i ourui
```

For org SBOM pipelines, include the pinned `ourui` version and Python interpreter from your container image (`deploy/Dockerfile`). OurUI does not vendor a CycloneDX generator — use your standard `pip` / container SBOM tool.

## Dump attestation

`ourui dump` / `compile_dump` includes:

```json
"attestation": {
  "schema": 27,
  "pack": "ourui-default",
  "pack_version": "1.0.0"
}
```

Use this to pin IR schema + design pack in CI gates. Optional content hashes of the dump (sans `attestation`) may be added later; schema + pack pin is enough for E5.

## Accessibility check profile

```bash
ourui check app.py --profile enterprise
ourui check app.py --profile enterprise --strict
```

Enterprise warnings (missing field labels, missing `alt=`, empty buttons, Canvas/Frame escape budget) print with exit **0** unless `--strict` promotes them to errors. See [ADR-011](../../decisions/ADR-011-pack-versioning-check-profile.md).

## PDF host

A second Host (PDF) is **Draft** only — [RFC-004](../../rfcs/RFC-004-second-host-pdf.md). Implementation deferred; any future PDF path must consume RTR + Resolved Design via the Host Contract (RFC-003).
