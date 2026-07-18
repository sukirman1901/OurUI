# OurUI landing (dogfood)

Marketing landing authored in OurUI. **Phase 1:** site header only (Quiet compiler / svelte.dev-style chrome).

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

## Monitor (phase 1)

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
| Full-bleed glass `ui.Nav` (`recipe=marketing` + sticky + drawer) | Hero (full-bleed) |
| Docs / Tutorial / Examples | Logo cloud, features |
| ThemeToggle + GitHub + Get started CTA (button-styled link) | Testimonials, CTA, footer |

## Theme

`ui.Theme(recipe="marketing")` — full-bleed chrome and sections; body copy keeps a reading measure.
