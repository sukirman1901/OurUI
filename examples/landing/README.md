# OurUI landing (dogfood)

Marketing homepage authored in OurUI — thin primitives + style intents, with `Theme(page=…)` for full-bleed.

## Layout

```text
examples/landing/
├── README.md
├── app.py                 # CLI entry — OurUI analyzes this file
├── components/
│   └── site_header.py
└── pages/
    └── home.py
```

## Sections (app composition)

Header → Hero → Trust strip → Intent/Compiler/Host → Style intents gallery → CTA → Footer

Hand-rolled composition in this example — not language kinds.

## Run

```bash
source .venv/bin/activate
ourui serve examples/landing/app.py
```
