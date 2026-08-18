# EMEC — Official Website (Django)

The flagship digital identity of Electro Mnemonic Engineering Consultancy
(EMEC), founded 2070 B.S. (2013 A.D.), Nepal — parent engineering company of
the group (Nepal Agro Yantra, Ojas Solutions, RC Interior, and future
ventures).

This repository is built **in phases**, each one production-quality and
fully integrated with what came before. See `docs/` for the architecture,
full database schema, design system, and wireframes behind every decision.

## Phase status

| Phase | Scope | Status |
|---|---|---|
| 1 | Architecture, folder structure, DB design, design system, wireframes, app scaffolding, navigation, UI kit | ✅ delivered |
| 2 | Authentication (custom User model), permission groups, admin dashboard, starter content seeding | ✅ delivered |
| 3 | Homepage (full section build) | ✅ delivered |
| 4 | About (Team app, full About page) | ✅ delivered |
| 5 | Services | ✅ delivered |
| 6 | Industries | next |
| 7 | Projects / Case Studies | planned |
| 8 | Research | planned |
| 9 | Training / Events | planned |
| 10 | Careers | planned |
| 11 | Testimonials / Clients / Partners | planned |
| 12 | Blog / News | planned |
| 13 | Media Library | planned |
| 14 | Contact | planned |

## Requirements

- **Python 3.11–3.14.** All pinned dependencies in `requirements/` have
  prebuilt wheels through 3.14 as of the versions currently pinned. If a
  future `pip install` fails with a build error on a fresh Python release,
  it's almost always one specific package lacking a wheel for that version
  yet — bump *that one pin* (check `pip index versions <package>` for what's
  actually available) rather than downgrading Python. 3.12 is what this
  project is most tested against.
- **PostgreSQL** (no SQLite fallback — dev intentionally mirrors prod).
- **That's it.** No Node.js, no npm, no build step of any kind. CSS is a
  single hand-written file at `static/css/site.css` — edit it directly and
  refresh the browser.

## Local setup

```bash
# 1. Python environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt

# 2. Environment variables
cp .env.example .env
# edit .env with your local DB credentials

# 3. Database (PostgreSQL required — no SQLite fallback, dev mirrors prod)
# `createdb` alone is not enough — it creates the database but not the
# role your .env authenticates as. Create both, matching whatever
# DB_USER/DB_PASSWORD/DB_NAME you put in .env (defaults shown below):
psql postgres -c "CREATE ROLE emec WITH LOGIN PASSWORD 'emec' CREATEDB;"
createdb -O emec emec
# If this fails to connect at all, Postgres likely isn't running yet
# (`brew services start postgresql@15`, or open Postgres.app), or your
# local install expects `psql -U $(whoami) postgres` instead of `psql postgres`.

# 4. Django
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_groups          # idempotent — permission groups
python manage.py seed_demo_content    # idempotent — real EMEC starter copy
python manage.py audit_field_lengths  # confirms no seeded value overflows its field (SQLite hides this; Postgres won't)
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site and `http://127.0.0.1:8000/control/`
for the admin (branded login + dashboard with live content counts).

## Documentation

- `docs/ARCHITECTURE.md` — folder structure, app boundaries, request flow, admin strategy
- `docs/DATABASE_DESIGN.md` — full schema for every app, built and planned
- `docs/DESIGN_SYSTEM.md` — color tokens, typography, the signature "trace" motif
- `docs/WIREFRAMES.md` — page-level structure for every recurring page type
- `docs/PHASE_2_NOTES.md` — custom User model, permission groups, admin dashboard, seed commands
- `docs/PHASE_3_NOTES.md` — homepage build, what was pulled forward from Services/Industries/Projects/Research/Testimonials/Blog
- `docs/PHASE_4_NOTES.md` — full Team app, About page leadership integration
- `docs/PHASE_5_NOTES.md` — full Services build (SEO, description, hero image, process steps, related industries)
- `docs/DEPENDENCY_FIX_NOTES.md` — the Pillow/taggit/CKEditor/psycopg dependency fixes and why
- `docs/NO_BUILD_STEP_NOTES.md` — why/how the Tailwind+Node.js build step was removed in favor of plain CSS
- `docs/DJANGO_314_AND_MEDIA_FIX_NOTES.md` — Django 5.2 bump for real Python 3.14 support, django-cleanup ordering fix, and 8 orphaned media fields wired up

## Conventions

- Every app owns its own `models.py`, `admin.py`, `urls.py`, `views.py` — no
  business logic lives in `config/`.
- Every content model inherits from `apps.core.models_base` abstractions
  (`TimeStampedModel`, `SlugModel`, `PublishableModel`, `OrderableModel`,
  `SEOModel`) rather than redefining those fields.
- Nothing user-facing is hardcoded in a template that should be editable —
  if in doubt, it's a Django Admin field.
- Settings are environment-driven (`python-decouple`); `dev.py` and `prod.py`
  both import from `base.py` and only override what genuinely differs.
