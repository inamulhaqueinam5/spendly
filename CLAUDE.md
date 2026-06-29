# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

"Spendly" — a Flask expense-tracker built as a **teaching scaffold**. The app is delivered in numbered steps that a student implements; much of the code is intentionally stubbed and meant to be filled in. When working here, respect that staging: don't implement a later step's feature unless asked, and keep changes scoped to the step in question.

- `database/db.py` is a stub (Step 1): the student must add `get_db()` (SQLite connection with `row_factory` and foreign keys enabled), `init_db()` (`CREATE TABLE IF NOT EXISTS`), and `seed_db()`.
- `static/js/main.js` is empty by design — JS is added as features are built.
- Several routes in `app.py` are placeholders returning plain strings (e.g. `logout` → "coming in Step 3", `add_expense` → "Step 7"). These map to upcoming steps.

## Commands

Setup (Windows / PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the dev server (note: **port 5001**, not the Flask default 5000):
```powershell
python app.py
```

Tests (pytest + pytest-flask are in requirements, no tests committed yet):
```powershell
pytest                 # all tests
pytest path/to/test_file.py::test_name   # a single test
```

## Architecture

Standard Flask layout, all routes in a single `app.py` (no blueprints):

- `app.py` — Flask app + all route definitions. Real pages render templates; not-yet-built pages return placeholder strings.
- `templates/` — Jinja2. `base.html` is the shared layout (navbar, footer, fonts, `style.css`, `main.js`); all pages extend it via `{% block content %}`. Brand is "Spendly".
- `static/css/style.css` — single consolidated stylesheet. A previous `landing.css` was merged into `style.css`; do not reintroduce separate per-page CSS files (verify with the 404 check on `/static/css/landing.css`).
- `static/js/main.js` — single shared script, loaded globally from `base.html`.
- `database/` — `db.py` (the SQLite layer, to be implemented). SQLite is the intended database (no DB file committed yet).

## Conventions

- Git commit messages follow `area: short imperative summary` (e.g. `landing: add privacy policy page and route`).
- Verify page changes by hitting the running server with curl and checking the HTTP status, e.g. `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5001/`.
