# RFC Process

OurUI is past the “ideas only” stage. Architecture changes need process so the vocabulary does not explode and LOCKED decisions stay trustworthy.

## When to write an ADR

Use an **Architecture Decision Record** (`docs/decisions/ADR-NNN-title.md`) when you need to record *why* a local or historical choice was made, without changing LOCKED vocabulary.

Examples: choice of JSON key names in dump format; packaging layout; test golden strategy.

## When to write an RFC

Use an **RFC** when a change:

- Touches anything listed as **LOCKED** in [INVARIANTS.md](INVARIANTS.md), or
- Introduces **new vocabulary**, or
- Changes Compilation Flow phases, OurIR stages, or emitter contracts.

Place RFCs in `docs/rfcs/` (create on first use) as `RFC-NNN-title.md`.

## Lifecycle

1. **Draft** — author opens RFC with motivation, design, alternatives, and impact on invariants.  
2. **Review** — discussion; implementation spikes encouraged.  
3. **Accepted** or **Rejected** — maintainer decision.  
4. **Implemented** — code + spec updates land together.  
5. **Locked / Frozen** — if appropriate, update [INVARIANTS.md](INVARIANTS.md) and [SPEC_STATUS.md](SPEC_STATUS.md).

## Approval

Maintainers approve RFCs. Opinions without implementation evidence that the current design failed are insufficient to change LOCKED items.

## Vocabulary freeze

No new official terms without an accepted RFC. See the vocabulary list in [INVARIANTS.md](INVARIANTS.md).

## Relationship to implementation phases

- Phase A froze Core Documents.  
- Phase B+ must validate design with code (`ourui dump`, then LTR/RTR/emit).  
- RFCs that only add abstraction without an implementation path should be rejected.
