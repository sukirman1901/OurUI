# RTR — Host-independent Render Tree

**Status:** Stable (Phase M — Render Lowering in `ourui dump`).

RTR is a tree of **HostNode** values. Emitters consume HostNode only ([I2](../../INVARIANTS.md)). RTR contains no Python language semantics ([I3](../../INVARIANTS.md)). HTML tags such as `button` appear only in emitters (Phase E).

## HostNode kinds

| Kind | Role |
|---|---|
| `Container` | Nested host structure (from Column/Row/Grid/Stack, or Box with children) |
| `Leaf` | Atomic control/surface without children |
| `Text` | Textual content node (`content`, `slot`) |
| `Drawing` | Reserved |
| `Slot` | Reserved |

## Layout → Host mapping (Phase D)

| LTR | HostNode |
|---|---|
| `Column` / `Row` / `Grid` / `Stack` | `Container` |
| `Box` (no children after text expand) | `Leaf` |
| `Box` (with children) | `Container` |
| `Spacer` | `Leaf` |
| title / subtitle / text props | additional `Text` nodes |

Attributes include semantic `role` (e.g. `button`, `card`) — **not** HTML tag names — plus `layout`, `from_layout`, `from_intent`. Provenance appends `lowering:render`.

## Dump

`ourui dump` includes an `rtr` section (document `version` ≥ 3).
