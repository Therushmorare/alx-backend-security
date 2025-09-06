import os
from pathlib import Path

# -----------------------------
# BASE DIRECTORY
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# SECURITY
# -----------------------------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "your-default-secret-key")
DEBUG = True  # Set False in production
ALLOWED_HOSTS = ["*"]  # Adjust for production

# -----------------------------
# INSTALLED APPS
# -----------------------------
INSTALLED_APPS = [
    # Django default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps
    "django_ratelimit",
    "django_ipgeolocation",

    # Project apps
    "ip_tracking",
]

# -----------------------------
# MIDDLEWARE
# -----------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # Custom middleware
    "ip_tracking.middleware.IPTrackingMiddleware",
]

# -----------------------------
# URL CONFIGURATION
# -----------------------------
ROOT_URLCONF = "alx_backend_security.urls"

# -----------------------------
# TEMPLATES
# -----------------------------
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

# -----------------------------
# WSGI
# -----------------------------
WSGI_APPLICATION = "alx_backend_security.wsgi.application"

# -----------------------------
# DATABASE
# -----------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "alx_security_db"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

# -----------------------------
# AUTHENTICATION & PASSWORD VALIDATION
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# -----------------------------
# INTERNATIONALIZATION
# -----------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# -----------------------------
# STATIC FILES
# -----------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# -----------------------------
# DEFAULT AUTO FIELD
# -----------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -----------------------------
# CACHING (Optional: Redis for caching IP geolocation)
# -----------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# -----------------------------
# DJANGO IP GEOLOCATION
# -----------------------------
IPGEOLOCATION_API_KEY = os.environ.get("IPGEOLOCATION_API_KEY", "your-api-key")
IPGEOLOCATION_CACHE_TIMEOUT = 24 * 60 * 60  # cache for 24 hours

# -----------------------------
# DJANGO RATELIMIT
# -----------------------------
RATELIMIT_USE_CACHE = "default"  # use the default cache (Redis)

