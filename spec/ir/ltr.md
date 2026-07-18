# LTR — Layout Object Tree

**Status:** Stable (Phase M — Layout Lowering in `ourui dump`).

LTR is produced by **Layout Lowering**. It is a **Layout Object Tree**: layout boxes with axes and children. It must not contain Python language semantics or HTML tags.

If constraint solving later needs non-tree edges, the artifact may evolve toward a layout graph without renaming the stage acronym **LTR**.

## Layout object kinds (Phase C)

| Kind | Axis | Typical source (IIR) |
|---|---|---|
| `Column` | vertical | `Page`, `Hero`, `Section` |
| `Row` | horizontal | (reserved) |
| `Grid` | grid | `Grid` |
| `Box` | none | `Card`, `Button`, `Text` |
| `Stack` | overlay | (reserved) |
| `Spacer` | none | (reserved) |

Each LTR node keeps the same `NodeId` as its IIR source for traceability, appends `lowering:layout` to **provenance**, and stores `from_intent` in attributes.

## Dump

`ourui dump` includes an `ltr` section (document `version` ≥ 2).
