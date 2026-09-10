import os
from pathlib import Path
from dotenv import load_dotenv
from django.conf.global_settings import MEDIA_URL



BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")



SECRET_KEY =os.getenv("DJANGO_SECRET_KEY")

DEBUG = False
ALLOWED_HOSTS = []




INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # COURSE_TODO: register only the packages introduced in the current exercise.
    'core',
    'crispy_forms',
    'crispy_bootstrap5',
    'apps.users.apps.UsersConfig',
    'apps.workspaces.apps.WorkspacesConfig',
    'apps.clients.apps.ClientsConfig',
    'apps.projects.apps.ProjectsConfig',
    'apps.tags.apps.TagsConfig',
    'apps.time_entries.apps.TimeEntriesConfig',
    'apps.contact_notes.apps.ContactNotesConfig',

]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

AUTH_USER_MODEL = "users.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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
    }
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
# COURSE_TODO: configure static and media files for local development.

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


LOGIN_URL = "users:login"
LOGIN_REDIRECT_URL = "users:profile"
LOGOUT_REDIRECT_URL = "workspaces:landing"