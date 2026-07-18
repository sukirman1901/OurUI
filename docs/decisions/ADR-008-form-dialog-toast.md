# ADR-008: Form, Dialog, and Toast intents (Phase T)

**Status:** Accepted + Implemented (Phase T / `1.0`)  
**Date:** 2026-07-18  

## Context

Phase S shipped individual controls but not form submit shells or overlay chrome. Authors needed `ui.Form`, `ui.Dialog`, and `ui.Toast` without inventing HTML.

## Decision

- `ui.Form` — intent container; `on_submit=` handler; host collects `[data-ourui-field]` on submit / Enter  
- `ui.Dialog` — modal overlay; `open=` State bind; `title=` / `actions=` / children  
- `ui.Toast` — ephemeral message; `text=` / `open=` / `tone=`  
- Field `invalid=` + `helper=` standardized for `aria-invalid` + helper text  

Follow ADR-005: intent + emit + escape — overlays are emit/host JS, not raw DOM authoring.

## Consequences

Dump schema includes Form/Dialog/Toast kinds. Host JS handles dialog open/close and form submit → `invoke`.
