import dj_database_url
import os
from .common import Common
import sentry_sdk

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Prod(Common):

    sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

    INSTALLED_APPS = Common.INSTALLED_APPS
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DEBUG = True

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = "your_secret_key"

    # SECURITY WARNING: update this when you have the production host
    ALLOWED_HOSTS = ['*']

    CSRF_TRUSTED_ORIGINS = ['*']

    MIDDLEWARE = Common.MIDDLEWARE + ["whitenoise.middleware.WhiteNoiseMiddleware"]

    # STATICFILES_STORAGES = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    STATIC_ROOT=os.path.join(BASE_DIR,'static')
    STATIC_URL = "/static/"

    MEDIA_ROOT = os.path.join(BASE_DIR,'media')
    MEDIA_URL = '/media_files/'

    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_REGION_NAME =  "ap-south-1"

    AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
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
    
   
    # TODO Database
    DATABASES = {
        

        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL')),
        
        
    }
  
