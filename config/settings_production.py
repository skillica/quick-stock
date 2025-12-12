from .settings import *
import environ
import os
env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = False
ALLOWED_HOSTS = [env('PA_DOMAIN')]
SECRET_KEY = env('DJANGO_SECRET_KEY')

DATABASES = {
    'default': env.db(),
}

STATIC_ROOT = BASE_DIR / 'staticfiles'