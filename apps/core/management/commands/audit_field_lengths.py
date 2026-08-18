"""
Guards against a specific, easy-to-miss class of bug: SQLite does not
enforce CharField/SlugField max_length at the database level, but
PostgreSQL does. Development and CI historically ran against SQLite (fast,
no server needed), so a seed value a few characters over its field's
max_length passes silently in SQLite and then throws
`psycopg.errors.StringDataRightTruncation` the first time it hits a real
Postgres database.

Run this after any `seed_*` command (regardless of which database backend
you're on) to catch overflows before they surface as a runtime crash:

    python manage.py audit_field_lengths

Exits non-zero if any violation is found, so it's safe to wire into CI.
"""
from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Check every CharField/SlugField value in the database against its max_length (catches bugs SQLite hides but Postgres rejects)."

    def handle(self, *args, **options):
        violations = []

        for model in apps.get_models():
            char_fields = [
                f for f in model._meta.get_fields()
                if hasattr(f, "max_length") and f.max_length
                and f.get_internal_type() in ("CharField", "SlugField")
            ]
            if not char_fields:
                continue

            for obj in model.objects.all():
                for f in char_fields:
                    val = getattr(obj, f.name, None)
                    if val and len(val) > f.max_length:
                        violations.append((model.__name__, obj.pk, f.name, f.max_length, len(val), val[:60]))

        if violations:
            self.stdout.write(self.style.ERROR(f"Found {len(violations)} field-length violation(s):\n"))
            for model_name, pk, field_name, max_length, actual, preview in violations:
                self.stdout.write(
                    f"  {model_name}(pk={pk}).{field_name}: "
                    f"max_length={max_length}, actual={actual} -> {preview!r}..."
                )
            self.stdout.write(self.style.ERROR(
                "\nThese will pass on SQLite but crash on PostgreSQL "
                "(StringDataRightTruncation). Fix the source values."
            ))
            raise SystemExit(1)

        self.stdout.write(self.style.SUCCESS(
            "No violations — every CharField/SlugField value fits its max_length."
        ))
