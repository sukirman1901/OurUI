# Compilation Flow

**Status:** Stable (aligned with Compilation Architecture).

Public phase names (not numbered passes):

```text
Parse → Analyze → Lower → Optimize → Emit
```

Lowering splits into:

```text
Intent Lowering → IIR
Layout Lowering → LTR
Render Lowering → RTR
```

See [ARCHITECTURE.md](../../ARCHITECTURE.md) for the Compilation Architecture document that embeds this flow.
