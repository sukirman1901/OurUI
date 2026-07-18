# RFC-004: Second host — PDF (deferred)

**Status:** Draft  
**Depends on:** [RFC-003](RFC-003-host-emit.md) Accepted  
**Track:** Generation 3+ (second host)

## Motivation

Some workflows need printable or archival PDF output from the same Intent → RTR + Resolved Design pipeline used for HTML.

## Center of this RFC

**Yes** — a second Host that consumes the **Host Contract**:

```text
RTR  +  Resolved Design  →  PDF Host  →  PDF bytes
```

**Not** — a parallel language surface, React print CSS hacks, or PDF generation inside `ui.*`.

## Non-goals (this draft)

- Implementing a PDF emitter in `ourui` 1.x (deferred)
- Changing dump schema beyond additive attestation/CSP/security flags already shipped
- Shipping browser print-to-PDF as the normative Host

## Open questions

- Pagination / page-break intent vs pure layout RTR
- Font embedding vs host-supplied fonts
- How attestation pins map to PDF metadata

## Status

**Deferred implementation.** Any PDF host must honor RFC-003 Host Contract inputs only. Resume when a concrete Host lands.
