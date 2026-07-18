# Motion vocabulary

Named **`family.pattern`** intents — call a reveal, don’t prescribe layout. Compiler emits CSS/JS presets ([ADR-012](../../decisions/ADR-012-motion-vocabulary.md)).

## Authoring

```python
ui.Section(..., motion="reveal.fade-up")
ui.Text("Hello", motion="text.word-reveal")
ui.Button("Save", motion="press.scale")
ui.Section(..., motion="scroll.counter")   # count-up in view
ui.Hero(..., motion="hero.parallax")
# legacy S4m aliases still work:
ui.Hero(..., motion="enter")   # → reveal.fade-up
```

## Catalog (complete)

| Phase | Count | Focus |
|-------|------:|-------|
| **M1** | 12 | Product: fade, press, hover, toast, scroll-in-view |
| **M2** | 17 | Marketing: split/ink, text marquee/typewriter, logo marquee |
| **M3** | 117 | Scroll, flow/carousel, grid, stack, hero, morph, perspective, micro… |
| **Total** | **146** | All Stable + emit (catalog v1.2.0) |

Registry: `ourui.design.motion`. Host CSS: `ourui.design.motion_css`. Dump `motion` summary (schema **30**).

Browse families: `reveal.*`, `text.*`, `press.*`, `hover.*`, `scroll.*`, `flow.*`, `grid.*`, `spotlight.*`, `stack.*`, `hero.*`, `micro.*`, `feedback.*`, `morph.*`, `perspective.*`.

## Smooth bar

- Shared tokens: `--ourui-motion-ease`, `--ourui-motion-duration-fast|…|slow`
- Prefer `transform` / `opacity` (+ clip-path for reveals)
- `prefers-reduced-motion: reduce` disables or instant-settles
- Marquees pause on hover/focus; budget ≤2–3 motions per viewport
