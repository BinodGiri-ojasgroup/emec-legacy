"""
EMEC — Base settings.

Shared by every environment. Environment-specific files (dev.py / prod.py)
import * from this module and override what differs. Nothing environment-
specific (DEBUG, ALLOWED_HOSTS values, DB creds) lives here — it is always
read from the environment via python-decouple, so the same codebase runs
unmodified in dev, staging, and prod.
"""
from pathlib import Path
from decouple import config, Csv

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------
SECRET_KEY = config("DJANGO_SECRET_KEY", default="unsafe-dev-key-change-me")
DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default="", cast=Csv())

SITE_ID = 1

# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.postgres",
]

THIRD_PARTY_APPS = [
    "mptt",
    "django_ckeditor_5",
    "imagekit",
    "taggit",
    "django_htmx",
    "django_filters",
    "watson",
    "django_extensions",
    "axes",
]

# Every business domain is an isolated, reusable Django app.
# See docs/ARCHITECTURE.md for the rationale behind each boundary.
LOCAL_APPS = [
    "apps.accounts",        # custom User model — must be migrated first
    "apps.core",            # site-wide config, navigation, offices, SEO mixins, base models
    "apps.pages",           # editable singleton pages: Home, About, Vision/Mission/Values
    "apps.team",            # leadership & staff profiles
    "apps.services",        # service catalogue (engineering domains / services offered)
    "apps.industries",      # industries served
    "apps.projects",        # portfolio / case studies
    "apps.research",        # papers, patents, whitepapers, innovation concepts
    "apps.training",        # workshops, courses, events, registrations
    "apps.careers",         # job listings & applications
    "apps.testimonials",    # clients, partners, testimonials, awards
    "apps.blog",            # news & blog
    "apps.media_library",   # central document/CAD/brochure library
    "apps.contact",         # offices, departments, inquiry forms
]

INSTALLED_APPS = (
    DJANGO_APPS
    + THIRD_PARTY_APPS
    + LOCAL_APPS
    + ["django_cleanup.apps.CleanupConfig"]  # MUST be last — needs every model already registered
)

AUTH_USER_MODEL = "accounts.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "axes.middleware.AxesMiddleware",
    "apps.core.middleware.SiteConfigMiddleware",   # injects SiteConfiguration into request
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site_config",     # global nav/footer/site settings
                "apps.core.context_processors.seo_defaults",    # default meta/OG fallbacks
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ---------------------------------------------------------------------------
# Database (PostgreSQL only — no SQLite fallback, dev mirrors prod exactly)
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="emec"),
        "USER": config("DB_USER", default="emec"),
        "PASSWORD": config("DB_PASSWORD", default="emec"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
        "CONN_MAX_AGE": config("DB_CONN_MAX_AGE", default=60, cast=int),
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 10}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesBackend",              # must be first — brute-force protection
    "django.contrib.auth.backends.ModelBackend",
]

# ---------------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kathmandu"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static & media files
# ---------------------------------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# File upload limits — generous enough for CAD/PDF brochures, still bounded.
FILE_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024   # 20MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024

# ---------------------------------------------------------------------------
# Forms
#
# No crispy-forms/Tailwind form-styling package. Forms (Contact in Phase 14,
# Careers applications in Phase 10, Event registration in Phase 9) are
# rendered with plain Django form templates styled directly against
# static/css/site.css — the same hand-written stylesheet as everything
# else, no separate forms-theming dependency to keep in sync.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# CKEditor 5 (rich text for blog / research / project long-form content)
#
# django-ckeditor-5 (package: django-ckeditor-5, app: django_ckeditor_5) —
# NOT the old django-ckeditor package (app: ckeditor/ckeditor_uploader).
# That package is effectively unmaintained and its old CKEditor 4 bundle has
# unresolved security advisories; django-ckeditor-5 is the actively
# maintained CKEditor 5 integration. No model uses CKEditor5Field yet (rich
# text fields are still plain TextField pending a dedicated pass across all
# content apps), but the app is wired up now so that pass is a model-field
# change only, not a dependency swap.
# ---------------------------------------------------------------------------
CKEDITOR_5_UPLOAD_FILE_TYPES = ["jpeg", "jpg", "png", "gif", "webp"]
CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading", "|", "bold", "italic", "link", "bulletedList", "numberedList",
            "blockQuote", "|", "undo", "redo",
        ],
    },
    "extends": {
        "toolbar": [
            "heading", "|", "bold", "italic", "link", "bulletedList", "numberedList",
            "blockQuote", "imageUpload", "insertTable", "codeBlock", "|", "undo", "redo",
        ],
        "image": {
            "toolbar": ["imageTextAlternative", "|", "imageStyle:alignLeft", "imageStyle:alignRight", "imageStyle:alignCenter", "imageStyle:side"],
            "styles": ["full", "side", "alignLeft", "alignRight", "alignCenter"],
        },
        "table": {"contentToolbar": ["tableColumn", "tableRow", "mergeTableCells"]},
    },
}

# ---------------------------------------------------------------------------
# Caching (Redis in dev+prod; falls back gracefully if REDIS_URL unset)
# ---------------------------------------------------------------------------
REDIS_URL = config("REDIS_URL", default="")
if REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        }
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"
else:
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

CACHE_TTL_SHORT = 60 * 5          # 5 min  — highly dynamic content (job listings, events)
CACHE_TTL_MEDIUM = 60 * 60        # 1 hour — services, industries, projects
CACHE_TTL_LONG = 60 * 60 * 24     # 24 hr  — site config, navigation, footer

# ---------------------------------------------------------------------------
# Email
# ---------------------------------------------------------------------------
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = config("EMAIL_HOST", default="")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="no-reply@emec.com.np")
SERVER_EMAIL = config("SERVER_EMAIL", default="server@emec.com.np")

# Where inquiry-form notifications are routed. Overridden per-department at
# the model level (contact.Department.notify_email) — this is the fallback.
INQUIRY_NOTIFY_EMAIL = config("INQUIRY_NOTIFY_EMAIL", default="info@emec.com.np")

# ---------------------------------------------------------------------------
# Security (baseline; hardened further in prod.py)
# ---------------------------------------------------------------------------
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1   # hours
AXES_RESET_ON_SUCCESS = True

# ---------------------------------------------------------------------------
# SEO / structured data defaults (consumed by apps.core.context_processors)
# ---------------------------------------------------------------------------
SITE_NAME = "Electro Mnemonic Engineering Consultancy"
SITE_DOMAIN = config("SITE_DOMAIN", default="www.emec.com.np")
DEFAULT_SEO_TITLE = "EMEC — Electro Mnemonic Engineering Consultancy"
DEFAULT_SEO_DESCRIPTION = (
    "EMEC is a multidisciplinary engineering consultancy founded in 2013, "
    "delivering R&D, product engineering, automation, embedded systems, and "
    "AI solutions across Nepal's industrial sector."
)

# ---------------------------------------------------------------------------
# Login / admin
# ---------------------------------------------------------------------------
LOGIN_URL = "/control/login/"
LOGIN_REDIRECT_URL = "/control/"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "[{asctime}] {levelname} {name}: {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django.request": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        "apps": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}
