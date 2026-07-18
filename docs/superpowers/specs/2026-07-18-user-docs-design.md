# User documentation (A–Z) — Design

**Date:** 2026-07-18  
**Status:** Approved for implementation planning  
**Phase:** Q (User docs) — precedes or pairs with packaging/release

## Problem

OurUI P0 (phases A–P) ships a working compiler and runtime, but documentation is oriented to **contributors and normative specs** (`LANGUAGE_SPEC.md`, `COMPILER_BOOK.md`, `spec/**`, ADRs). There is no Svelte/Next-style **user guide**: how to write apps, what you need end-to-end, and where to look things up.

Release without that guide leaves public and onboarding readers blocked after the README quick start.

## Goals

- English **user documentation** detailed enough for public + internal onboarding.
- Coverage mirroring mature frameworks: Getting started, Learn (tutorial), Guides, Reference, light Concepts.
- Delivered as **Markdown in-repo** (no docs site generator in v1).
- Document **only Stable P0** behavior; explicit P0 limits.

## Non-goals (v1)

- MkDocs / VitePress / hosted docs site (defer).
- Indonesian translation.
- Rewriting `COMPILER_BOOK` / IR specs as the primary user path.
- New product features (forms, Redis, client-only State, etc.) — only document what exists.

## Audience

**D — mixed:** Python developers new to OurUI and full-stack developers used to Django/FastAPI who want a compiled Python UI surface. Assume Python fluency; do not assume IR/compiler knowledge.

## Approach

Full information architecture under `docs/user/` (framework-style TOC), separate from normative/contributor docs. README becomes a short door into that tree.

## Information architecture

```text
docs/user/
  README.md
  getting-started.md
  tutorial/
    01-your-first-page.md
    02-components.md
    03-state-and-server.md
    04-routing.md
    05-theme-tokens.md
    06-serve-dev-and-prod.md
  guides/
    project-layout.md
    deploying.md
    lsp-editor-setup.md
    debugging-with-dump.md
  reference/
    cli.md
    ui-components.md
    state.md
    server.md
    theme.md
    routing.md
    component-authoring.md
  concepts/
    how-ourui-compiles.md
    what-p0-includes.md
```

### Boundaries

| Location | Role |
|---|---|
| `docs/user/**` | How to use OurUI |
| `LANGUAGE_SPEC.md`, `spec/**` | Normative language/IR contracts |
| `COMPILER_BOOK.md` | Contributor compilation guide |
| Root `README.md` | One-screen quick start + link to `docs/user/` |

User pages may link to normative docs; they must not become a second IR manual.

## Content design

### Getting started

Single page: venv → `pip install -e packages/ourui` → minimal `app.py` → `ourui serve` → browser. Success = rendered page (and a click if the sample includes `@server`). No IR.

### Tutorial (linear)

Six steps, each with: goal → runnable code → short explanation → next link. Prefer `examples/tutorial/*.py` as the runnable source of truth for snippets (v1).

1. First page (`ui.Page`, `Hero`, `Section`)  
2. Components (function + `Component` class)  
3. `State` + `@server` + binds  
4. Routing (`route=`)  
5. `ui.Theme` + `color=` tokens  
6. Dev serve vs `--prod` / workers / session-dir  

### Guides

Task-oriented: project layout, deploying (`--prod`, workers, session dir), LSP setup, debugging via `ourui dump` and serve errors (dev traceback vs prod).

### Reference

One topic per file: CLI, `ui.*` kinds, State, server, theme, routing, component authoring. Tables, short signatures, 3–10 line examples. Cross-links to tutorial.

### Concepts

- How OurUI compiles (Parse → Analyze → Lower → Emit) in plain language.  
- What P0 includes / excludes (honest limits).

### Writing standards

- English; imperative voice.  
- Only Stable APIs.  
- CLI claims must match current CLI.  
- Non-reference pages end with “See also”.

### v1 success criteria

A new reader can complete without `COMPILER_BOOK`: (1) hello page, (2) State + server, (3) two routes, (4) Theme, (5) `serve --prod`.

## Maintenance and testing

- Behavior source of truth: code + `tests/p0`.  
- Docs updates ship in the same PR as user-visible API changes.  
- Runnable tutorial modules under `examples/tutorial/` with light smoke tests (`dump`/`emit` or serve health) so snippets do not rot.  
- `concepts/what-p0-includes.md` lists missing features explicitly.

## Ship order

1. Skeleton `docs/user/` + getting-started + tutorial 01–03 + examples  
2. Tutorial 04–06 + guides + reference + concepts  
3. README + `docs/roadmap.md` Phase Q Done  
4. Packaging/PyPI release remains a **separate** follow-up phase

## Open decisions locked in brainstorming

- Audience: public + onboarding  
- Completeness: Svelte/Next-like layers  
- Format: Markdown in repo (Approach 1)  
- Language: English only  
- Visual companion: declined / text-only  

## Out of scope reminders

No docs site, no i18n, no new runtime features as part of this docs phase.
