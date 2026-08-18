# EMEC — Django/Python 3.14 Fix + Media Rendering Fixes

## 1. Django version — real Python 3.14 incompatibility

**Symptom:** `/control/` admin pages crashed with
`AttributeError: 'super' object has no attribute 'dicts' and no __dict__
for setting new attributes`, deep in `django/template/context.py`'s
`Context.__copy__`, whenever an admin page used an inclusion tag (which is
most of them — pagination, filters, changelist rows).

**Root cause:** this is a genuine Django/Python incompatibility, not
anything in this project's code. Python 3.14 changed how `super` objects
behave under `copy.copy()` (they became copyable, which broke an assumption
`BaseContext.__copy__()` relied on). **Django only fixed this starting in
5.2** — Django 5.0 and 5.1 both predate Python 3.14's release and never
received the fix. Confirmed via Django's own tracking ticket (#35844:
"Django 5.2 will be the first version to support Python 3.14").

**Fix:** bumped `Django==5.0.6` → `Django==5.2.17` (the current 5.2 LTS
patch release). Verified every other pinned dependency resolves cleanly
against Django 5.2 with no conflicts (`pip install --dry-run` against the
full `requirements/dev.txt`), then did a full install and re-ran the entire
validation suite — `manage.py check`, migrations, both seed commands, the
field-length audit, and a full HTTP smoke test across all 16 routes. All
clean.

If you're not on Python 3.14, this bug never affected you — but the fix is
safe either way, since Django 5.2 also supports 3.11/3.12/3.13.

## 2. `django-cleanup` app ordering — a real bug, found during this pass

While fixing the above, I found a second, unrelated real bug: `settings/base.py`
registered `django_cleanup.apps.CleanupConfig` inside `THIRD_PARTY_APPS`,
which is listed *before* `LOCAL_APPS` in `INSTALLED_APPS`. django-cleanup's
own documentation is explicit that it must be **last** in `INSTALLED_APPS`,
because it needs every model already registered to hook its
delete-old-file-on-save / delete-file-on-delete signal handlers correctly.
It was silently failing to do that for every app-owned model (Project,
Service, TeamMember, etc.) — meaning old uploaded files were never actually
being cleaned up when replaced or deleted. Fixed: `django_cleanup` is now
appended after `LOCAL_APPS`, not bundled into `THIRD_PARTY_APPS`.

## 3. Media upload worked — but 8 uploaded images never rendered anywhere

This was the real "media... rendering on the frontend" bug. Media
*upload* itself was never broken — `MEDIA_URL`/`MEDIA_ROOT` were configured
correctly and `config/urls.py` correctly serves `/media/` in debug mode.
The actual problem: **several `ImageField`/`FileField` fields were
editable in Django Admin but no template ever displayed them.** An editor
could upload a homepage hero image, save it successfully, see zero errors —
and it would never appear anywhere on the site. That's indistinguishable
from "upload is broken" unless you go looking at the templates.

Audited every `ImageField`/`FileField` across every model against actual
template usage. Found and fixed 8 orphaned fields:

| Field | Where it's now rendered |
|---|---|
| `HomePage.hero_image` / `hero_video` | Homepage hero section (video takes priority if both are set) |
| `AboutPage.hero_image` | Top of the About page |
| `TimelineEvent.image` | Each timeline entry on the About page |
| `GroupCompany.logo` | Group company cards on the About page |
| `Industry.image` | Industry card (list page) and industry detail page |
| `ResearchItem.cover_image` | Research card (list page) and research detail page |
| `Testimonial.photo` | Next to the featured quote on the homepage |
| `SiteConfiguration.logo_dark` | Header — now actually swaps with `logo` based on the light/dark toggle (previously only `logo` was ever used, `logo_dark` was dead) |

## Verified with real files, not just template syntax

Confirming a template *compiles* doesn't prove an uploaded image renders —
so I attached real PNG files to every one of these 8 fields via the ORM,
booted the dev server, and confirmed each image tag actually appears in the
rendered HTML **and** that the file itself serves with `200` from
`/media/...`. All 8 confirmed. Then re-ran the full 16-route smoke test to
confirm nothing else regressed.
