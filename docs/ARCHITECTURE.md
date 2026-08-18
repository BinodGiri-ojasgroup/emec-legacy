# EMEC — Architecture (Phase 1)

## Why this structure

The build follows one rule throughout: **every business domain is an
isolated, reusable Django app with its own models, admin, views, urls, and
(later) templates.** Nothing is hardcoded into a monolithic `main` app. This
is what lets the master prompt's phase plan work — each phase adds or
completes exactly one app without touching the others' internals.

```
emec/
├── manage.py
├── .env.example
├── requirements/
│   ├── base.txt                # shared across all environments
│   ├── dev.txt                 # + debug toolbar, pytest, linters
│   └── prod.txt                # + gunicorn, sentry, S3/Anymail
├── config/                     # project-level wiring only — no business logic
│   ├── settings/
│   │   ├── base.py              # everything environment-agnostic
│   │   ├── dev.py                # local overrides
│   │   └── prod.py               # hardening, error tracking, object storage
│   ├── urls.py                 # namespaced includes per app
│   ├── wsgi.py / asgi.py
├── apps/
│   ├── core/                   # shared foundation — see below
│   ├── pages/                  # Home, About, Timeline, Values, Group Companies
│   ├── team/                   # Leadership & staff
│   ├── services/               # Service catalogue
│   ├── industries/             # Industries served
│   ├── projects/               # Portfolio / case studies
│   ├── research/               # Papers, patents, whitepapers
│   ├── training/               # Workshops, courses, events
│   ├── careers/                # Job listings & applications
│   ├── testimonials/           # Clients, partners, testimonials, awards
│   ├── blog/                   # News & blog
│   ├── media_library/          # Central document/CAD/brochure library
│   └── contact/                # Offices, departments, inquiry forms
├── templates/
│   ├── base.html               # root layout
│   ├── components/             # header, footer, trace_divider, stat_card…
│   └── pages/                  # page-specific templates
├── static/
│   ├── css/site.css            # single hand-written stylesheet — no build step
│   ├── js/site.js              # vanilla JS — scroll reveal + theme toggle
│   └── img/
├── media/                      # user uploads (git-ignored)
└── docs/                       # this file, DATABASE_DESIGN.md, WIREFRAMES.md
```

## `apps.core` — the foundation everything else inherits

Rather than repeating `created_at`, `slug`, `status`, `display_order`, and
SEO fields on every model, `apps/core/models_base.py` defines abstract base
classes that every other app's models inherit from:

- **`TimeStampedModel`** — `created_at` / `updated_at`
- **`SlugModel`** — auto-generates a unique slug from a configurable source field
- **`PublishableModel`** — draft / scheduled / published / archived workflow with an `is_live` property, so editors can prepare content ahead of time
- **`OrderableModel`** — manual `display_order` for drag-sortable admin lists
- **`SEOModel`** — per-object `seo_title`, `seo_description`, `og_image`, `canonical_url`, `noindex`
- **`AddressModel`** — physical address fields, used by `contact.Office`

This is the single decision that keeps Django Admin, querysets, and SEO
output consistent from Phase 1 through Phase 14, and it's why adding a new
content type later (e.g. "Awards") is a five-minute job, not a redesign.

`apps.core` also owns things that are inherently global, not tied to one
content type:

- **`SiteConfiguration`** — singleton (see `SingletonModel`) holding brand
  identity, contact defaults, footer copy, tracking IDs, and feature flags
  (`show_careers`, `show_blog`, etc.) so a section can be hidden without a
  deploy while its content is still being populated.
- **`NavigationMenu` / `NavigationItem`** — MPTT tree, one level of dropdown
  support, six named slots (header primary/utility, three footer columns,
  footer legal row). Marketing can restructure the entire site's navigation
  from Django Admin.
- **`SocialLink`**, **`Announcement`** (dismissible top banner).
- **`SiteConfigMiddleware`** attaches `request.site_config` once per request
  and enforces `maintenance_mode`.
- **Context processors** (`site_config`, `seo_defaults`) inject navigation,
  site config, and SEO fallbacks into every template automatically — no view
  needs to fetch these manually.
- **`sitemaps.py`** is a central registry; each app adds its own `Sitemap`
  subclass as it lands, and `config/urls.py` never changes.

## Request flow

```
request
  → SiteConfigMiddleware (loads SiteConfiguration, checks maintenance mode)
  → URLconf (config/urls.py → apps/<app>/urls.py, namespaced)
  → View (Class-Based View, queries its app's models)
  → Template (extends templates/base.html, pulls nav/site_config from
     context processors, renders app-specific templates/components)
```

## Admin strategy

Django Admin is mounted at `/control/` (not the default `/admin/`, as a
trivial hardening measure against automated scanning). Singleton content
(`SiteConfiguration`, `HomePage`, `AboutPage`) blocks add/delete entirely via
a `SingletonAdminMixin` so editors can never accidentally create a second
homepage. Tree content (navigation) uses `django-mptt`'s
`DraggableMPTTAdmin` for visual drag-reordering.

## What Phase 1 deliberately does NOT include

Per the phased delivery plan, the following are intentionally out of scope
for Phase 1 and land in later phases, even though the apps are already
scaffolded:

- Full models for Team, Services, Industries, Projects, Research, Training,
  Careers, Testimonials, Blog, Media Library, Contact (schemas are specified
  in `DATABASE_DESIGN.md`; each app currently exposes a `ComingSoonView` so
  the full URL graph and design system are provable end-to-end today)
- Authentication/permission groups beyond Django's defaults (Phase 2)
  fully-built Homepage sections (Phase 3) and About page (Phase 4)
- Search, filtering, caching *usage* (the infrastructure — django-watson,
  django-filter, Redis cache config — is already installed and configured;
  it gets wired into each app's views as that app is built)

## Security & performance already in place

- `django-axes` (login throttling), CSRF/XSS headers, HttpOnly cookies,
  HSTS + SSL redirect in prod, admin at a non-default path
- Redis cache backend (falls back to local memory in dev if `REDIS_URL`
  unset) with three named TTL tiers (`CACHE_TTL_SHORT/MEDIUM/LONG`)
- Whitenoise for compressed, manifest-hashed static files
- `django-cleanup` auto-deletes orphaned media files on model delete
- `django-imagekit` installed for responsive image generation, wired in per
  model as image-heavy apps (Projects, Media Library) land
