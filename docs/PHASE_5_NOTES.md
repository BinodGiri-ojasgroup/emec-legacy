# EMEC — Services (Phase 5)

## What this phase delivers

Extends the `Service`/`ServiceCategory` models seeded minimally in Phase 3
— the same tables, migrated additively (`0002_service_canonical_url_...`),
nothing dropped or renamed:

- **SEO fields** (`SEOModel`) — `seo_title`, `seo_description`, `og_image`,
  `canonical_url`, `noindex`, all editable per-service in Django Admin.
- **`description`** — the full service write-up shown on the detail page
  (plain text/paragraphs for now; a CKEditor pass across all rich-text
  fields site-wide is a deliberate later pass rather than one-off per app).
- **`hero_image`** — detail-page header image.
- **`related_industries`** M2M → `Industry` — surfaced as an "Relevant
  Industries" sidebar on the service detail page, and the reverse relation
  (`Industry.related_services`) is what Phase 6 will use to show "Services
  for this industry."
- **`ServiceProcessStep`** — a *per-service* ordered delivery process,
  managed as an inline on the Service admin form. This is intentionally a
  separate model from `pages.ProcessStep` (the homepage's single global
  "How We Engineer Solutions" sequence) — a service's specific delivery
  steps and the company's overall engineering philosophy are different
  content that happen to both be numbered sequences.

## Admin

`ServiceAdmin` now has a proper fieldset layout (content / related
industries / visibility / collapsed SEO), a `filter_horizontal` widget for
the industries M2M, and a `ServiceProcessStepInline` so an editor manages a
service's entire delivery process from one screen — confirmed rendering
correctly in an authenticated admin session (the M2M widget and inline both
present on the change form).

## Templates

`/services/<slug>/` now renders: hero image, full description, an ordered
"How We Deliver This" process list (numbered — legitimate here, same reasoning
as the homepage), a "Relevant Industries" sidebar linking to
`/industries/<slug>/`, and a "Discuss This Service" CTA into `/contact/`.
The list page (`/services/`) is unchanged in structure from Phase 3 — cards
already had everything they needed.

## Seed data

`seed_demo_content` now gives all six seeded services real descriptions
(EMEC-specific, not filler), three process steps each, and links each to
2 of the 3 relevant seeded industries — confirmed end-to-end via a real
HTTP request showing "How We Deliver This," "Scope & Assess," and "Relevant
Industries" all rendering on a live detail page.

## What's next — Phase 6 (Industries)

`Industry` gets the same treatment: SEO fields, rich description, hero
image — plus surfacing the `related_services` reverse relation this phase
just created, and a `related_projects` reverse relation once `Project` is
extended in Phase 7.
