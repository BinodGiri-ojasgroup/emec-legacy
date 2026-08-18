# EMEC — About / Team (Phase 4)

## What this phase delivers

Unlike Services/Industries/Projects/Research/Testimonials/Blog in Phase 3,
`apps.team`'s spec in `DATABASE_DESIGN.md` was already minimal by design —
so Phase 4 ships it in full, not a cut-down version. No "full build lands
later" placeholder here.

- **`Department`** — `name`, `slug`. Simple grouping (Engineering, Research
  & Innovation, etc.) — not to be confused with `contact.Department`
  (Phase 14), which is about inquiry routing, not org structure.
- **`TeamMember`** — `name`, `role_title`, `department` FK, `bio`, `photo`,
  `email`, `linkedin_url`, `is_leadership`, `is_active`, plus the usual
  Slug/Orderable/Timestamped base fields.

## Routes

- `/about/leadership/` — leadership grid (`is_leadership=True, is_active=True`)
- `/about/leadership/<slug>/` — individual profile page

Both were live and tested in Phase 1/2's URL scaffolding
(`config/urls.py` already mounted `apps.team.urls` at `/about/leadership/`)
but returned a `ComingSoonView` until now.

## About page integration

`AboutView` now queries `TeamMember` directly (same pattern as the
homepage's Phase 3 sections) and `templates/pages/about.html` renders a
Leadership grid between Values and Our Group, linking through to each
member's full profile and to `/about/leadership/` for the complete roster.
No hardcoded bios in the template — everything is Django Admin content.

## Seed data note

`seed_demo_content` seeds three placeholder leadership profiles (role
titles and bios are real EMEC positioning; names are literally
"EMEC Team Member 1/2/3") because I don't have real leadership names to
seed. **These need to be edited in Django Admin with actual names/photos
before launch** — flagged in the command's own output, not just here.

## Verified end-to-end

Migration generated and applied cleanly, permission groups re-seeded
(Content Editors and Site Administrators now include `team`), full
authenticated smoke test confirmed the About page rendering the Leadership
section with real seeded profiles, and both `/about/leadership/` and its
slug-based detail route returning `200`.

## What's next — Phase 5 (Services)

`apps.services.Service` gets its full build: SEO fields, rich-text
description, hero image, `ServiceProcessStep` (per-service process, distinct
from the homepage's global `ProcessStep`), and `related_industries` M2M —
extending the same model seeded in Phase 3, not replacing it.
