# OurUI user documentation

Learn how to build web apps in Python with OurUI. These pages cover **Stable P0** APIs only — no compiler or IR deep dives.

## Getting started

- [Getting started](getting-started.md) — install, run your first app, open it in the browser

## Tutorial

Work through the examples in order. Each step links to a runnable file under `examples/tutorial/`.

1. [Your first page](tutorial/01-your-first-page.md) — `ui.Page`, `Hero`, `Section`
2. [Components](tutorial/02-components.md) — function components and `Component` classes
3. [State and server](tutorial/03-state-and-server.md) — `State`, `@server`, interactive buttons
4. [Routing](tutorial/04-routing.md) — multiple pages with `route=`
5. [Theme and tokens](tutorial/05-theme-tokens.md) — `ui.Theme` and `color=`
6. [Serve: dev and prod](tutorial/06-serve-dev-and-prod.md) — `ourui serve`, `--prod`, workers

## Guides

Task-oriented how-tos:

- [Project layout](guides/project-layout.md) — `app.py`, `examples/`, venv
- [Deploying](guides/deploying.md) — `--prod`, workers, session directory
- [LSP and editor setup](guides/lsp-editor-setup.md) — `ourui lsp` in your editor
- [Debugging with dump](guides/debugging-with-dump.md) — routes, tokens, serve errors

## Reference

API and CLI lookup (coming soon):

- [CLI](reference/cli.md)
- [UI components](reference/ui-components.md)
- [State](reference/state.md)
- [Server handlers](reference/server.md)
- [Theme](reference/theme.md)
- [Routing](reference/routing.md)
- [Component authoring](reference/component-authoring.md)

## Concepts

Light background (coming soon):

- [How OurUI compiles](concepts/how-ourui-compiles.md)
- [What P0 includes](concepts/what-p0-includes.md)
