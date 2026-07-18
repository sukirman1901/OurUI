# OurUI user documentation

Learn how to build web apps in Python with OurUI. Stable surface: `ourui` **1.11.1**, dump schema **30**.

**Focus:** **utility → HTML/CSS/JS** compile (e.g. `aspect=`, `ring=`, `pad={"md":"8"}`). `ui.Theme` is a thin brand sheet (+ optional `css=`). See [VISION.md](../../VISION.md).

## Getting started

- [Getting started](getting-started.md) — install, counter sample, landing dogfood
- [Deploy](guides/deploy.md) — serve, Docker/Compose/K8s, CI emit
- [Trust and compliance](guides/trust-and-compliance.md) — CSP, attestation, a11y check
- [Threat model](guides/threat-model.md) — host threats and mitigations (prod serve)
- [Style intents](reference/style-intents.md) — **craft foundation** (ADR-013)
- [Theme](reference/theme.md) — thin roles, density, `page=`
- [Page measure](concepts/page-measure.md)
- [Motion](concepts/motion.md)

## Tutorial

1. [Your first page](tutorial/01-your-first-page.md)
2. [Components](tutorial/02-components.md)
3. [State and server](tutorial/03-state-and-server.md)
4. [Routing](tutorial/04-routing.md)
5. [Theme and style intents](tutorial/05-theme-tokens.md)
6. [Serve: dev and prod](tutorial/06-serve-dev-and-prod.md)

## Guides

- [Project layout](guides/project-layout.md)
- [Deploying](guides/deploying.md)
- [LSP and editor setup](guides/lsp-editor-setup.md)
- [Debugging with dump](guides/debugging-with-dump.md)

## Reference

- [CLI](reference/cli.md)
- [UI components](reference/ui-components.md)
- [Style intents](reference/style-intents.md)
- [State](reference/state.md)
- [Server handlers](reference/server.md)
- [Theme](reference/theme.md)
- [Routing](reference/routing.md)
- [Component authoring](reference/component-authoring.md)

## Concepts

- [How OurUI compiles](concepts/how-ourui-compiles.md)
- [What Stable includes](concepts/what-p0-includes.md)
- [Page measure](concepts/page-measure.md)
- [Motion](concepts/motion.md)

## Samples

[`examples/tutorial/`](../../examples/tutorial/) · [`examples/landing/`](../../examples/landing/) · [`examples/gateway/`](../../examples/gateway/)
