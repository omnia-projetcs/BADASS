import os

SECRET_KEY = os.environ["LAB_SESSION_KEY"]
DEBUG = False
ALLOWED_HOSTS = ["web", "localhost", "127.0.0.1"]
ROOT_URLCONF = "billing.urls"
INSTALLED_APPS = ["django.contrib.auth", "django.contrib.contenttypes", "django.contrib.sessions", "billing"]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware", "django.contrib.sessions.middleware.SessionMiddleware",
              "django.middleware.csrf.CsrfViewMiddleware", "django.contrib.auth.middleware.AuthenticationMiddleware"]
DATABASES = {"default": {"ENGINE": "django.db.backends.postgresql", "HOST": "db", "NAME": "billing",
                         "USER": "billing", "PASSWORD": os.environ["LAB_DB_PASSWORD"]}}
CACHES = {"default": {"BACKEND": "django.core.cache.backends.redis.RedisCache", "LOCATION": "redis://cache:6379/1"}}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
USE_TZ = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_SAMESITE = "Strict"
WEBHOOK_KEY = os.environ["LAB_WEBHOOK_KEY"]
