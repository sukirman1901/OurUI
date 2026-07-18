# OurUI user documentation

Learn how to build web apps in Python with OurUI. These pages cover the **Stable** language surface through Phase **S6** (`ourui` **0.4.0**) — Getting started through Reference. Compiler/IR deep dives live in the repo root docs.

## Getting started

- [Getting started](getting-started.md) — install, run your first app, open the Plasma demo

## Tutorial

Work through the examples in order. Each step links to a runnable file under `examples/tutorial/`.

1. [Your first page](tutorial/01-your-first-page.md) — `ui.Page`, `Hero`, `Section`
2. [Components](tutorial/02-components.md) — function components and `Component` classes
3. [State and server](tutorial/03-state-and-server.md) — `State`, `@server`, interactive buttons
4. [Routing](tutorial/04-routing.md) — multiple pages with `route=`
5. [Theme and tokens](tutorial/05-theme-tokens.md) — `ui.Theme`, type/space/elevation, ThemeToggle
6. [Serve: dev and prod](tutorial/06-serve-dev-and-prod.md) — `ourui serve`, `--prod`, workers

## Guides

- [Project layout](guides/project-layout.md)
- [Deploying](guides/deploying.md)
- [LSP and editor setup](guides/lsp-editor-setup.md)
- [Debugging with dump](guides/debugging-with-dump.md)

## Reference

- [CLI](reference/cli.md)
- [UI components](reference/ui-components.md) — Page through Canvas, Nav, forms, polish
- [State](reference/state.md)
- [Server handlers](reference/server.md)
- [Theme](reference/theme.md)
- [Routing](reference/routing.md)
- [Component authoring](reference/component-authoring.md)

## Concepts

- [How OurUI compiles](concepts/how-ourui-compiles.md)
- [What Stable includes](concepts/what-p0-includes.md) — supported features and out-of-scope list

## Demo

Plasma-shaped dogfood: `ourui serve demo/app.py` → http://127.0.0.1:8765/ ([demo/README.md](../../demo/README.md)).
