from configurations import Configuration
from pathlib import Path
import os
from datetime import timedelta
from celery.schedules import crontab
from dotenv import load_dotenv
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class Common(Configuration):

    # ADMIN_CHARTS_USE_JSONFIELD = False

    SECRET_KEY = "random"

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = ["*"]

    # Application definition

    INSTALLED_APPS = [
        'jazzmin',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # packages
        'storages',
        "django_celery_results",
        'celery',
        "django_celery_beat",
        'rest_framework',
        'ckeditor',
        'ckeditor_uploader',
        'corsheaders',
        'django_extensions',

        # apps
        'User.apps.UserConfig',
        'products.apps.ProductsConfig',
        'payments.apps.PaymentsConfig',
        'blogs.apps.BlogsConfig',
        'communication.apps.CommunicationConfig',
    ]

    MIDDLEWARE = [

        # 'django.middleware.cache.UpdateCacheMiddleware',  # new
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.common.CommonMiddleware",

        # 'django.middleware.cache.FetchFromCacheMiddleware',  # new
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',


    ]
    CORS_ORIGIN_ALLOW_ALL = True
    ROOT_URLCONF = 'Backend.urls'
    # CORS_ALLOW_ALL_ORIGINS = True

    CRONJOBS = [
    ('*/5 * * * *', 'products.tasks.update_values'),
    # Add more cron jobs as needed
    ]

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'Backend.wsgi.application'
    # Database
    # https://docs.djangoproject.com/en/4.2/ref/settings/#databases


    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
# docker build . -t backend -f ./Dockerfile

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    REST_FRAMEWORK = {
        'COERCE_DECIMAL_TO_STRING': False,
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE':  12,

    }

    # Internationalization
    # https://docs.djangoproject.com/en/4.2/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'Asia/Kolkata'

    USE_I18N = True

    USE_TZ = True

    CELERY_BROKER_URL = "redis://redis:6379"
    CELERY_RESULT_BACKEND = "redis://redis:6379"
    CELERY_TASK_TIME_LIMIT = 30 * 60 * 60 * 60 * 60

    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'Asia/Kolkata'
    CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

    # CELERY_BEAT_SCHEDULE = {
    # 'update_all_ratings': {
    #     'task': 'QBank.tasks.update_all_ratings',
    #     'schedule': crontab(hour=00, minute=0), # Run the task daily at midnight
    # },
# }

    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATIC_URL = "/static/"

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media_files/'

    AUTH_USER_MODEL = 'User.User'

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
    CORS_ALLOW_ALL_ORIGINS = True
    # Simple JWT configuration
    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(days=24),
        'REFRESH_TOKEN_LIFETIME': timedelta(days=24),
        'ROTATE_REFRESH_TOKENS': True,
        'BLACKLIST_AFTER_ROTATION': True,
    }

    # Set the refresh token cookie name and options
    SIMPLE_JWT['REFRESH_TOKEN_COOKIE_NAME'] = 'refresh_token'
    SIMPLE_JWT['REFRESH_TOKEN_COOKIE_SAMESITE'] = None

    # CHANGE THIS TO TRUE IN PRODUCTION
    SIMPLE_JWT['REFRESH_TOKEN_COOKIE_SECURE'] = False

    REST_FRAMEWORK = {
        'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework_simplejwt.authentication.JWTAuthentication',
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        ]

    }

    ####################################
    ##  CKEDITOR CONFIGURATION ##
    ####################################

    CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

    CKEDITOR_UPLOAD_PATH = 'uploads/'
    CKEDITOR_IMAGE_BACKEND = "pillow"

    CKEDITOR_CONFIGS = {
        'default': {
            'toolbar': None,
        },
    }

    # JAZZMIN_SETTINGS = {
    #     # title of the window (Will default to current_admin_site.site_title if absent or None)
    #     "site_title": "World One Admin",

    #     # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    #     "site_header": "WORLD-ONE",

    #     # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    #     "site_brand": "WORLD-ONE",

    #     # Logo to use for your site, must be present in static files, used for brand on top left
    #     # "site_logo": "books/img/logo.png",

    #     # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    #     "login_logo": None,

    #     # Logo to use for login form in dark themes (defaults to login_logo)
    #     "login_logo_dark": None,

    #     # CSS classes that are applied to the logo above
    #     "site_logo_classes": "img-circle",

    #     # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    #     "site_icon": None,

    #     # Welcome text on the login screen
    #     "welcome_sign": "Welcome to the WORLD-ONE",

    #     # Copyright on the footer
    #     "copyright": "WORLD-ONE PVT LTD",

    #     # List of model admins to search from the search bar, search bar omitted if excluded
    #     # If you want to use a single search field you dont need to use a list, you can use a simple string
    #     "search_model": ["auth.User", "auth.Group"],

    #     # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    #     "user_avatar": "avatar",

    #     ############
    #     # Top Menu #
    #     ############

    #     # Links to put along the top menu
    #     "topmenu_links": [

    #         # Url that gets reversed (Permissions can be added)
    #         {"name": "Home",  "url": "admin:index",
    #          "permissions": ["auth.view_user"]},


    #         # model admin to link to (Permissions checked against model)
    #         {"model": "auth.User"},

    #         # App with dropdown menu to all its models pages (Permissions checked against models)
    #         # {"app": "books"},
    #     ],

    #     #############
    #     # User Menu #
    #     #############

    #     # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    #     # "usermenu_links": [
    #     #     {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
    #     #     {"model": "auth.user"}
    #     # ],

    #     #############
    #     # Side Menu #
    #     #############

    #     # Whether to display the side menu
    #     "show_sidebar": True,

    #     # Whether to aut expand the menu
    #     "navigation_expanded": True,

    #     # Hide these apps when generating side menu e.g (auth)
    #     "hide_apps": ["django_celery_results"],

    #     # Hide these models when generating side menu (e.g auth.user)
    #     'hide_models': [
    #         'django_celery_results.TaskResult',      # Celery Task results
    #         'django_celery_results.GroupResult',     # Celery Group results
    #         'django_celery_beat.PeriodicTask',       # Celery Periodic Tasks
    #         'django_celery_beat.ClockedSchedule',    # Clocked
    #         'django_celery_beat.CrontabSchedule',    # Crontabs
    #         'django_celery_beat.IntervalSchedule',   # Intervals
    #         'django_celery_beat.SolarSchedule',      # Solar events
    #     ],
    #     # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)

    #     # Custom links to append to app groups, keyed on app name


    #     # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    #     # for the full list of 5.13.0 free icon classes
    #     "icons": {
    #         "auth": "fas fa-users-cog",
    #         "auth.user": "fas fa-user",
    #         "auth.Group": "fas fa-users",
    #     },
    #     # Icons that are used when one is not manually specified
    #     "default_icon_parents": "fas fa-chevron-circle-right",
    #     "default_icon_children": "fas fa-circle",

    #     #################
    #     # Related Modal #
    #     #################
    #     # Use modals instead of popups
    #     "related_modal_active": False,

    #     #############
    #     # UI Tweaks #
    #     #############
    #     # Relative paths to custom CSS/JS scripts (must be present in static files)
    #     "custom_css": None,
    #     "custom_js": None,
    #     # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    #     "use_google_fonts_cdn": True,
    #     # Whether to show the UI customizer on the sidebar
    #     "show_ui_builder": False,

    #     ###############
    #     # Change view #
    #     ###############
    #     # Render out the change view as a single form, or in tabs, current options are
    #     # - single
    #     # - horizontal_tabs (default)
    #     # - vertical_tabs
    #     # - collapsible
    #     # - carousel
    #     "changeform_format": "horizontal_tabs",
    #     # override change forms on a per modeladmin basis
    #     "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    #     # Add a language dropdown into the admin
    #     "language_chooser": False,
    # }
