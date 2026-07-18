# IIR — Intent IR

IIR is the first OurIR stage. It expresses developer intent without host semantics ([I4](../../INVARIANTS.md)).

## Domains

| Domain | Examples |
|---|---|
| Intent Domain | `Page`, `Hero`, `Section` |
| Behavior Domain | events, state links, server calls (post-P0) |
| Presentation Domain | `Button`, `Card`, `Text`, `Grid` |

## P0 shape

Each IIR node mirrors node identity ([node.md](node.md)) with:

- `domain`: `intent` | `presentation` | `behavior`
- `kind`: string
- `props`: canonical attribute map
- `children`: list of child node ids
