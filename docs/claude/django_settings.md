# Django `settings.py` convention
Each settings belongs to a certain sections. The sections you can see bellow, also the section list is open-ended, so in the future if necessary might be added new section.
```python
# Python
from pathlib import Path
from dotenv import load_dotenv
import os

# Django
from django.utils.translation import gettext_lazy as _



# ==================================================
# Init
# ==================================================
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent


# ==================================================
# Django security
# ==================================================
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"
ALLOWED_HOSTS = [host for host in os.getenv("DJANGO_ALLOWED_HOSTS").split(",")]


# ==================================================
# Application definition
# ==================================================
INSTALLED_APPS = [
    "unfold",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    # Local
    "apps.core",
    "apps.authentication",
]


# ==================================================
# Web security
# ==================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

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


# ==================================================
# Backends
# ==================================================
AUTHENTICATION_BACKENDS = [
    "apps.authentication.backends.SerialNumberAuthenticationBackend",
    "apps.authentication.backends.CredentialsAuthenticationBackend",
]

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ==================================================
# Connections
# ==================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT")
    }
}


# ==================================================
# Server config
# ==================================================
WSGI_APPLICATION = "config.wsgi.application"
ROOT_URLCONF = "config.urls"

AUTH_USER_MODEL = "authentication.User"

STATIC_URL = "static/"
STATIC_ROOT = "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ==================================================
# Other
# ==================================================
UNFOLD = {
    "SITE_TITLE": _("EStore"),
    "SITE_HEADER": _("EStore"),
    "SITE_SYMBOL": "store",
    "SIDEBAR": {
        "show_all_applications": lambda request: request.user.is_superuser,
        "navigation": "apps.core.callbacks.navigation_callback"
    },
}
```