"""
Django settings for the personal portfolio project.

Configuration is environment-driven so the same code runs in development and
production without edits. Copy ``.env.example`` to ``.env`` and adjust values.
"""

import os
from pathlib import Path

# --- Optional dependencies (graceful fallback if not installed) ---------
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover - dotenv is optional in production
    pass

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(key, default=False):
    """Read a boolean environment variable."""
    return os.environ.get(key, str(default)).strip().lower() in {"1", "true", "yes", "on"}


def env_list(key, default=""):
    """Read a comma-separated environment variable into a list."""
    raw = os.environ.get(key, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


def env_int(key, default):
    """Read an integer environment variable, falling back on empty/invalid values."""
    raw = os.environ.get(key, "")
    try:
        return int(raw)
    except (TypeError, ValueError):
        return default


# --- Core security settings ---------------------------------------------
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-dev-only-change-me-in-production",
)

DEBUG = env_bool("DEBUG", True)

# Hosts. Always allow localhost and any *.vercel.app subdomain so the app runs
# on Vercel even if ALLOWED_HOSTS is not set in the dashboard.
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "localhost,127.0.0.1")
ALLOWED_HOSTS += [".vercel.app", ".now.sh"]

# Vercel exposes the current deployment host in VERCEL_URL (without scheme).
_vercel_url = os.environ.get("VERCEL_URL")
if _vercel_url:
    ALLOWED_HOSTS.append(_vercel_url)

# CSRF trusted origins must include the scheme. Trust the *.vercel.app domain
# so admin/form POSTs work in production.
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS += ["https://*.vercel.app"]
if _vercel_url:
    CSRF_TRUSTED_ORIGINS.append(f"https://{_vercel_url}")


# --- Applications --------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "personalpotfolio",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# WhiteNoise is only needed for production static-file delivery. Keeping it out
# of local development avoids requiring a collected manifest during tests.
try:
    import whitenoise  # noqa: F401
except ImportError:  # pragma: no cover
    whitenoise = None

ROOT_URLCONF = "myproject.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "myproject.wsgi.application"
ASGI_APPLICATION = "myproject.asgi.application"


# --- Database ------------------------------------------------------------
# Defaults to SQLite for development. Set DATABASE_URL (e.g. a PostgreSQL
# URL) in production and the app will use it automatically.
#
# On serverless hosts (e.g. Vercel) the project root is read-only; only /tmp is
# writable. When no DATABASE_URL is set there, point SQLite at /tmp so the app
# still runs (data is ephemeral — use a real DATABASE_URL for persistence).
_on_serverless = bool(os.environ.get("VERCEL") or os.environ.get("VERCEL_URL"))
_sqlite_path = "/tmp/db.sqlite3" if _on_serverless else str(BASE_DIR / "db.sqlite3")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": _sqlite_path,
    }
}

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    try:
        import dj_database_url

        DATABASES["default"] = dj_database_url.parse(
            DATABASE_URL, conn_max_age=600, ssl_require=env_bool("DB_SSL_REQUIRE", False)
        )
    except ImportError:  # pragma: no cover
        # dj-database-url not installed; keep SQLite fallback.
        pass


# --- Password validation -------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --- Internationalization ------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Karachi"
USE_I18N = True
USE_TZ = True


# --- Static & media files ------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Serve static files with WhiteNoise in production. On serverless hosts
# (e.g. Vercel) there is no build/collectstatic step, so WhiteNoise is told to
# use the staticfiles finders and serve directly from STATICFILES_DIRS.
if not DEBUG and whitenoise is not None:
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
    # Serve straight from the app's static sources — no collectstatic needed.
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_AUTOREFRESH = True
    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"
        },
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --- Production security hardening --------------------------------------
# These settings only activate when DEBUG is False, keeping local dev simple.
if not DEBUG:
    SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = env_int("SECURE_HSTS_SECONDS", 31536000)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    X_FRAME_OPTIONS = "DENY"
