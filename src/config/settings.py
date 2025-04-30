import os
import re
from pathlib import Path

db_regex = (
    r"^(?P<db_engine>.*):\/{2}"
    r"((?P<db_username>[^:]*):(?P<db_password>[^@]*)@"
    r"(?P<db_hostname>[^:/]*)(:(?P<db_port>\d+))?\/)?(?P<db_name>.*)$"
)

SUPPORTED_DB_ENGINES = {
    "postgresql": "django.db.backends.postgresql",
    "sqlite3": "django.db.backends.sqlite3",
}


def get_config_from_connection_string(connection_string: str) -> dict:
    try:
        match = re.search(db_regex, connection_string)
        if match is None:
            raise ValueError("Datbase URI is invalid")

        return {
            "ENGINE": SUPPORTED_DB_ENGINES[match.group("db_engine")],
            "NAME": match.group("db_name"),
            "USER": match.group("db_username"),
            "PASSWORD": match.group("db_password"),
            "HOST": match.group("db_hostname"),
            "PORT": match.group("db_port"),
            "ATOMIC_REQUESTS": True,
        }
    except AttributeError:
        raise ValueError(
            (
                f"Database connection string '{connection_string}'"
                "does not match with expected regex."
            )
        )
    except KeyError:
        raise ValueError(
            f"Database connection string '{connection_string}'"
            "includes unexpected db_engine"
        )


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DC_DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("DC_DJANGO_SECRET_KEY is not specified")

DEBUG = True

ALLOWED_HOSTS = ["0.0.0.0", "localhost", "127.0.0.1"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "src.core.apps.CoreConfig",
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

ROOT_URLCONF = "src.config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "src.config.wsgi.application"

DATABASES = {
    "default": get_config_from_connection_string(
        os.getenv("DC_DATABASE_URL", "invalid")
    ),
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CELERY_BROKER_URL = os.getenv("DC_CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]

DC_WEATHER_CHECK_INTERVAL = os.getenv("DC_WEATHER_CHECK_INTERVAL", 10)
DC_MAX_PRECIPITATION_MM = os.getenv("DC_MAX_PRECIPITATION_MM", 5)
