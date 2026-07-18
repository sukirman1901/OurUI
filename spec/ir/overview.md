# OurIR overview

**Status:** Stable (Phase M).

**OurIR** is the IR Stack: **IIR → LTR → RTR**.

| Stage | Produced by | Consumed by |
|---|---|---|
| IIR | Intent Lowering | Layout Lowering / dump |
| LTR | Layout Lowering | Render Lowering |
| RTR | Render Lowering | Emitters (HostNode) |

P0 produces IIR only (plus analysis artifacts).

See [ARCHITECTURE.md](../../ARCHITECTURE.md).
