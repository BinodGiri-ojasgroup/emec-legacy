"""
Careers -- models.

Schema for this app is specified in docs/DATABASE_DESIGN.md. Full model
implementation lands in Phase 10 (Careers) of the build, keeping every phase's
diff reviewable and each app's migrations meaningful rather than one giant
initial migration for the whole site. Importing this module today is always
safe (no models yet = no migrations required).
"""
from django.db import models  # noqa: F401  (kept so imports elsewhere don't break)
