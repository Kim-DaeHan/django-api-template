"""
Development settings for social_api project.
"""

import dj_database_url
from decouple import config

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# Database
DATABASES = {
    "default": dj_database_url.config(
        default=config(
            "DATABASE_URL",
            default="postgresql://postgres:password@localhost:5432/social_api_dev",
        ),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Development-specific apps
INSTALLED_APPS += [
    "django_extensions",  # 개발 도구
]

# Email backend for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Cache (개발환경에서는 로컬 메모리 캐시 사용)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Django Debug Toolbar (선택사항)
if DEBUG:
    INTERNAL_IPS = [
        "127.0.0.1",
        "localhost",
    ]
