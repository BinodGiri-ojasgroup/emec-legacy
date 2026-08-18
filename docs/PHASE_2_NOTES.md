# EMEC — Authentication, Admin & Core Models (Phase 2)

## Custom User model

`apps.accounts.User` extends `AbstractUser` and is set as `AUTH_USER_MODEL`
from this project's very first migration. Swapping the user model after
tables exist is a genuinely painful migration in Django, so this is done now
even though full role-based workflows (e.g. careers reviewers, research
approvers) don't have content to act on yet.

The model adds exactly what a multi-department content team needs:
`role`, `job_title`, `phone`, `avatar`, `is_department_head` — nothing else.
Authorization itself is **not** reimplemented on top of `role`; `role` only
determines which Django Group an account gets seeded into. Actual
permissions live in Django's standard Group/Permission tables, so an admin
can always hand-adjust access for one person without touching code.

## Permission groups

`python manage.py seed_groups` (idempotent — safe to re-run after every
phase) creates:

| Group | Scope today | Grows to include |
|---|---|---|
| Site Administrators | Full access: core, pages, accounts | Everything, always |
| Content Editors | Add/change (no delete) on pages | Services, Industries, Projects copy |
| Research Managers | — (research app has no models yet) | Full CRUD on Research once Phase 8 lands |
| Training Coordinators | — | Full CRUD on Training once Phase 9 lands |
| Careers / HR Managers | — | Full CRUD on Careers + application review once Phase 10 lands |
| Viewers | Read-only across every app that has models | Read-only, always |

This mapping is defined in code
(`apps/core/management/commands/seed_groups.py`) rather than configured by
hand in the admin UI, so it's versioned, reviewable, and reproducible in
every environment.

## Starter content

`python manage.py seed_demo_content` (idempotent) populates
`SiteConfiguration`, navigation menus (header + three footer columns +
legal row), the homepage (hero copy, four statistics), and the About page
(story, vision, mission, five core values, a six-entry B.S./A.D. timeline,
and the three seeded group companies — Nepal Agro Yantra, Ojas Solutions,
RC Interior). This is real EMEC-specific copy, not lorem ipsum — it exists
so Phase 3's homepage build has genuine content to render against, and so a
stakeholder can see a working, on-brand site today rather than an empty
shell.

## Admin dashboard

`/control/` now shows a small stats panel above Django's standard app list
— live counts for navigation items, homepage statistics, timeline events,
core values, group companies, and staff accounts, each linking straight to
its changelist. This is implemented as a wrapper around the default
`AdminSite.index()` view (see `apps/core/admin_dashboard.py`) rather than a
replacement `AdminSite` subclass, specifically so every app's existing
`@admin.register(...)` calls keep working unchanged — a new app only needs
one line added to `DASHBOARD_SECTIONS` to appear on the dashboard.

The admin is also lightly rebranded (`templates/admin/base_site.html`,
`login.html`, `index.html`) — EMEC's palette on the header/login screen —
without reskinning Django's admin CSS wholesale, which would turn every
future Django upgrade into a manual re-audit.

## Verified end-to-end

This phase was validated with a real request/response cycle, not just a
syntax check: migrations were generated and applied, both seed commands
were run, a superuser was created, and an authenticated session confirmed
the branded login page, the dashboard's live counts, and the seeded
homepage content rendering through the full template chain (header → hero →
statistics → footer).

## Audit trail

Two audit mechanisms are already active without extra code:

- **`django.contrib.admin.models.LogEntry`** — every add/change/delete made
  through Django Admin is logged automatically (visible per-user in
  "Recent actions" and queryable for a full audit report).
- **`django-axes`** — every login attempt (success and failure) is recorded,
  with automatic lockout after 5 failed attempts (`AXES_FAILURE_LIMIT`).

A dedicated `AuditLog` model for public-facing actions (inquiry submissions,
job applications) is specified in `DATABASE_DESIGN.md` and lands with
`apps.contact`/`apps.careers` in their respective phases, since there's
nothing to audit yet.

## What's next — Phase 3 (Homepage)

The Homepage model, seed data, and design system are already in place.
Phase 3 replaces the current placeholder sections (Capabilities, Industries,
Projects, Research, Process, Training, Testimonials, News) with their real,
data-driven builds — most of which depend on apps that don't have models
yet, so Phase 3 will pull forward the minimum viable slice of Services,
Projects, etc. needed to make the homepage real, with each getting its full
build in its own later phase.
