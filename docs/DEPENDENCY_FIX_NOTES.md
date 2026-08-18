# EMEC — Dependency Fix Notes

## What broke

Running `pip install -r requirements/dev.txt` on a real machine (Python
3.12/3.14) surfaced two separate problems that hadn't shown up in this
project's own sandboxed validation (which happened to have compatible
cached wheels available):

1. **`Pillow==10.3.0`** has no prebuilt wheel for newer Python versions, so
   pip fell back to building from source — which then failed because the
   sdist's own build script has a bug (`KeyError: '__version__'`) on newer
   setuptools. This is a known issue with that specific old Pillow release,
   not an environment misconfiguration.
2. **`django-taggit==5.0.3`** doesn't exist on PyPI (it was never
   published/was yanked) — pip listed it as unavailable.

Both are fixed by bumping to versions that are actually installable:
`Pillow==11.3.0`, `django-taggit==6.1.0`. Neither project code currently
uses a `TaggableManager` field, so the taggit bump has zero code impact —
it was listed as infrastructure for a future phase (Project tagging, per
`DATABASE_DESIGN.md`).

## The real bug this caused

Fixing the two installability issues above led to installing
**`django-ckeditor-5`** instead of the originally-specified
**`django-ckeditor`** — two different, unrelated packages with different
app names, different settings, and different APIs:

| | `django-ckeditor` (original) | `django-ckeditor-5` (now used) |
|---|---|---|
| App name(s) | `ckeditor`, `ckeditor_uploader` | `django_ckeditor_5` |
| Settings | `CKEDITOR_UPLOAD_PATH`, `CKEDITOR_CONFIGS` | `CKEDITOR_5_CONFIGS`, `CKEDITOR_5_UPLOAD_FILE_TYPES` |
| Editor version | CKEditor 4 (unmaintained upstream, known unresolved advisories) | CKEditor 5 (actively maintained) |

Since `requirements/base.txt` was updated to the newer package but
`config/settings/base.py` still referenced the old one's app names, Django
failed at startup with `ModuleNotFoundError: No module named 'ckeditor'`.

**This is now fixed properly, not patched around it:**

- `INSTALLED_APPS` registers `django_ckeditor_5` (not `ckeditor`/`ckeditor_uploader`)
- Settings use `CKEDITOR_5_CONFIGS` / `CKEDITOR_5_UPLOAD_FILE_TYPES`
- `config/urls.py` mounts `path("ckeditor5/", include("django_ckeditor_5.urls"))`,
  confirmed resolving to `/ckeditor5/image_upload/`
- Switching to the newer, maintained package is also the better outcome
  independent of the install issue — `django-ckeditor`'s bundled CKEditor 4
  has open security advisories (this is exactly what the `ckeditor.W001`
  warning in earlier phases' `manage.py check` output was flagging).

No model field currently uses either package's rich-text widget (content
fields are plain `TextField` pending a dedicated rich-text pass across every
app, per `DATABASE_DESIGN.md`), so this fix has no migration or template
impact — it's purely a dependency/settings correction.

## Verified

Re-ran the full validation cycle with the corrected dependency set: syntax
check, `manage.py check` (now clean — no `ckeditor.W001` warning), fresh
migrations, `seed_groups` + `seed_demo_content`, and a full HTTP smoke test
across every route (`/`, `/about/`, `/about/leadership/`, `/services/`,
`/industries/`, `/projects/`, `/research/`, `/training/`, `/careers/`,
`/blog/`, `/clients/`, `/resources/`, `/contact/`, `/robots.txt`,
`/sitemap.xml`, `/control/login/`) — all `200`, zero tracebacks.

## A second, separate bug this surfaced: SQLite hides field-length overflows

Running `seed_demo_content` against real PostgreSQL crashed with
`psycopg.errors.StringDataRightTruncation: value too long for type
character varying(160)` on `SiteConfiguration.default_meta_description`.

**Root cause**: every validation pass in this project (Phases 1–5) ran
against SQLite for speed, and *SQLite does not enforce `CharField`/
`SlugField` `max_length` at the database level* — it stores whatever you
give it. PostgreSQL does enforce it and throws. One seeded string was 161
characters against a 160-character field, and SQLite let it through
silently in every prior test run.

**Fixed**: trimmed the offending string, then added
`apps/core/management/commands/audit_field_lengths.py` — a permanent
management command that checks every `CharField`/`SlugField` value
currently in the database against its model's declared `max_length`,
regardless of which database backend you're running. It exits non-zero on
any violation, so it's meant to run after every `seed_*` command and can be
wired into CI going forward:

```bash
python manage.py seed_demo_content
python manage.py audit_field_lengths
```

Verified the tool actually works both ways: it passed clean against the
fixed seed data, then correctly caught a deliberately-corrupted 200-char
value in a test run (exit code 1, precise field/model/pk reported), then
passed clean again after restoring good data.

## A third dependency pin, same pattern: `psycopg`

On Python 3.14, `pip install` failed again — this time on
`psycopg-binary==3.1.19`, which has no prebuilt wheel past Python 3.13
(confirmed via `pip index versions psycopg`: the earliest version with a
`cp314` wheel is `3.2.10`). Bumped to `psycopg[binary]==3.2.10`.

This is the same class of issue as the Pillow/taggit fix earlier, not a new
kind of bug: an exact version pin chosen when this project was built has
since fallen behind what's available as prebuilt wheels for newer Python
releases. **The fix is always to bump that one specific pin**, checked
against `pip index versions <package>`, not to downgrade Python — Pillow
11.3.0 and psycopg 3.2.10 both now have wheels through 3.14, so the earlier
advice to avoid 3.13/3.14 entirely was already stale as soon as Pillow was
fixed, and is now corrected in the README.
