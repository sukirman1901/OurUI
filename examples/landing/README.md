# OurUI landing (dogfood)

Marketing landing authored in OurUI — dogfood for language primitives + `recipe="marketing"` host chrome.

## Layout

```text
examples/landing/
├── README.md
├── app.py                 # CLI entry — OurUI analyzes this file
├── components/
│   └── site_header.py     # mirror of site_header() (keep in sync with app.py)
└── pages/
    └── home.py            # mirror of home_page() (keep in sync with app.py)
```

OurUI compiles a **single** entry module. Edit the live tree in `app.py`; keep the `components/` and `pages/` mirrors aligned when you change the header or shell.

## Run

```bash
# from repo root, with venv active
source .venv/bin/activate
ourui serve examples/landing/app.py
```

Inspect IR:

```bash
ourui dump examples/landing/app.py
ourui emit examples/landing/app.py
```

## Scope

| Now | Next |
|-----|------|
| Full-bleed glass `ui.Nav` (`recipe=marketing` + sticky + drawer) | Hero / sections composed with style intents |
| Docs / Tutorial / Examples links | Logo cloud, features |
| ThemeToggle + GitHub + Get started CTA | Testimonials, CTA, footer |

Prefer **intent props** (`width=`, `pad_x=`, `gap=`, …) over hand-authored host CSS — see [Style intents](../../docs/user/reference/style-intents.md). Kit/block patterns stay out of the language ([ADR-014](../../docs/decisions/ADR-014-language-primitives-vs-kit.md)).

Requires `ourui` **1.9.1+** (Style Intent Catalog + marketing recipe).
