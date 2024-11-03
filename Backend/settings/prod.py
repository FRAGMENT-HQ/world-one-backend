import dj_database_url
import os
from .common import Common
from google.oauth2 import service_account


BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))


class Prod(Common):

    INSTALLED_APPS = Common.INSTALLED_APPS
    BASE_DIR = os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    DEBUG = True

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = "your_secret_key"

    # SECURITY WARNING: update this when you have the production host
    ALLOWED_HOSTS = ['*']

    CSRF_TRUSTED_ORIGINS = ["http://localhost:3000", "https://backend.worldoneforex.com", "http://backend.worldoneforex.com",
                            "https://worldoneforex.com", "http://worldoneforex.com", "https://www.worldoneforex.com", "http://www.worldoneforex.com"]

    MIDDLEWARE = Common.MIDDLEWARE + \
        ["whitenoise.middleware.WhiteNoiseMiddleware"]

    # STATICFILES_STORAGES = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATIC_URL = "/static/"

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media_files/'

    GS_BUCKET_NAME = 'world_one'
    GCS_CREDENTIALS_JSON = os.path.join(BASE_DIR, 'world-one.json')
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        os.path.join(BASE_DIR, 'world-one.json')
    )

    GS_PROJECT_ID = 'world-one-428913'
    GS_DEFAULT_ACL = 'private'
    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
        "mediafiles": {
            "BACKEND": 'Backend.storage_backends.MediaStorage',
        },
        "default": {
            "BACKEND": 'Backend.storage_backends.MediaStorage',
        },
    }
