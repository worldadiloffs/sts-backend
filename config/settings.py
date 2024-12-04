from pathlib import Path
import os 
import logging
from os import getenv
from typing import Any

from django.core.cache import cache
from redis.exceptions import RedisError

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!gcbfyy!^c7l3044hkw18rjjs+f(@zx()smn%bn8u&ap^un@6f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", '167.172.107.185', 'api.sts-shop.uz', '192.168.1.150']


# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #global
    "rest_framework",
    "django_countries",
    "django_filters",
    "rest_framework_simplejwt",
    'rest_framework_simplejwt.token_blacklist',
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "django_extensions",
    "ckeditor",
    'ckeditor_uploader',
    "corsheaders",
    "axes",
    "silk",
    'modeltranslation',
    
    # admin settings
    'jazzmin',
    'jsoneditor',
    'django.contrib.admin',
    'import_export',


    #local
    'account',
    'product',
    'category',
    'settings',
    'home',
    'blog',
    'payments',
    'clickApp',
    'ordersts',
    'importdata',
    'xodimlar',
    'cashback',
    'calculator',
    'backend',
    # 'bot',
    'servis',

]


IMPORT_EXPORT_USE_TRANSACTIONS = True  # Wrap import/export in a transaction for atomic operations
IMPORT_EXPORT_SKIP_ADMIN_LOG = True 

JSON_EDITOR_JS = "https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/8.6.4/jsoneditor.js"
JSON_EDITOR_CSS = (
    "https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/8.6.4/jsoneditor.css"
)

CORS_ALLOW_ALL_ORIGINS = True

SILKY_MIDDLEWARE_CLASS = "silk.middleware.SilkyMiddleware"

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    'http://localhost:5173/',
]
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

MIDDLEWARE = [
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "config.midilware.errorshandler.Custom404Middleware",
    SILKY_MIDDLEWARE_CLASS,
    "axes.middleware.AxesMiddleware",
]



# if DEBUG:
#     MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

# if request.user.is_staff:
#     # AxesMiddleware faqat adminlar uchun
#     MIDDLEWARE.append("axes.middleware.AxesMiddleware")



ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR /'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'home.content_prosess.canvass', 
                'home.content_prosess.order',
                'product.content_process.content_product'
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
AUTH_USER_MODEL = "account.User"



# redis 
REDIS_URL = "redis://redis_broker:6379"


# PAYCOM_SETTINGS = {
#     "KASSA_ID": getenv("Payme_KASSA_ID"),  # token
#     "SECRET_KEY": getenv("Payme_SECRET_KEY"),  # password
#     # "ACCOUNTS": {
#     #     "KEY": "order_id"
#     # },
#     "ACCOUNTS": {
#         "KEY":"order_id"
#     },
#     "Token":getenv("Payme_Token")
# }


PAYCOM_SETTINGS = {
    "KASSA_ID": "668a95269fc37c5dfda18f54",  # token
    "SECRET_KEY":"NjSuX@XDz89bzhk%FftRfX@4DI%CP7Nr8t%6",
    # "ACCOUNTS": {
    #     "KEY": "order_id"
    # },
    "ACCOUNTS": {
        "KEY":"order_id"
    },
    "Token":"668a95269fc37c5dfda18f54"
}

CLICK_SETTINGS = {
    'service_id': '37647',
    'merchant_id': '7844',
    'secret_key': '0MnCNnMB7xFuGyp',
    'merchant_user_id': '46754'
}




logger = logging.getLogger(__name__)

USE_REDIS_FOR_CACHE = getenv("USE_REDIS_FOR_CACHE", default="true").lower() == "true"
REDIS_URL = getenv("REDIS_URL", default="redis://localhost:6379/0")

CACHES: dict[str, Any] = {}

if USE_REDIS_FOR_CACHE:
    logger.info("Using Redis for cache")
    CACHES["default"] = {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }

    # Ping the cache to see if it's working
    try:
        cache.set("ping", "pong")

        if cache.get("ping") != "pong":
            msg = "Cache is not working properly."
            raise ValueError(msg)  # noqa: TRY301

        cache.delete("ping")

        logger.info("Cache is working properly")
    except (ValueError, RedisError):
        logger.exception("Cache is not working. Using dummy cache instead")
        CACHES["default"] = {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
else:
    logger.warning("Using dummy cache")
    CACHES["default"] = {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }



DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "azamatdevblog",
        "USER": "azamatdevhik",
        "PASSWORD": "createdatastshik123",
        "HOST": "127.0.0.1",
        "PORT": "5432",
        'TEST': {
            'NAME': 'mytestdatabase',  # Custom test database name
            'MIRROR': 'default',  # Use the same database configuration for tests
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


STATIC_URL = 'https://stsmarket-static.vercel.app/static/'

# STATIC_ROOT = os.path.join(BASE_DIR ,'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
MODELTRANSLATION_LANGUAGES = ('ru',  'uz')

LANGUAGES = (
    ('ru', 'Russion'),
     ('uz', 'Uzbek')
)
LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LANGUAGE_CODE = "ru"

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_TZ = False


from datetime import timedelta, timezone
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "TEST_REQUEST_RENDERER_CLASSES": [
        "rest_framework.renderers.MultiPartRenderer",
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.TemplateHTMLRenderer",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "authentication": "5/hour",
        "verify_authentication": "8/hour",
    },
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # "ACCESS_TOKEN_LIFETIME": timedelta(seconds=30),
    # "REFRESH_TOKEN_LIFETIME": timedelta(minutes=2),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    # "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "DEFAULT_PAGINATION_CLASS": "config.utils.custom_pagination.CustomPagination",
    "PAGE_SIZE": 12,
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=100),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
}



SMS_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzQxNzgwNDEsImlhdCI6MTczMTU4NjA0MSwicm9sZSI6InVzZXIiLCJzaWduIjoiY2Y0N2M0NzdmYmE2OWMxNmM4ZDllMmZmMjE5MDFhNzg3N2NkYmNmYTVkM2FiZGI3NjU4ZTVhYjgxZjk2MThjOCIsInN1YiI6IjgyOCJ9.yMab0e2Af9rJbAp2ZC_VD3MrRPTWQM5keelmy5oUr-8"
EXPIRY_TIME_OTP = 60


SPECTACULAR_SETTINGS = {
    "TITLE": "Backend",
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    "COMPONENT_SPLIT_REQUEST": True,
    "VERSION": 1,
}



USE_SILK = getenv("USE_SILK", default="false").lower() == "true"

SILKY_AUTHENTICATION = True  # User must login
SILKY_AUTHORISATION = True  # User must have permissions
AXES_ENABLED = os.environ.get("AXES_ENABLED", default="true").lower() == "true"
AXES_FAILURE_LIMIT = int(os.environ.get("AXES_FAILURE_LIMIT", default="50"))

JAZZMIN_UI_TWEAKS = {
    # "theme": "slate",
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-secondary",
    "accent": "accent-indigo",
    "navbar": "navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-light-navy",
    "sidebar_nav_small_text": True,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",""" """
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-outline-success"
    },
    "actions_sticky_top": True
}

JAZZMIN_SETTINGS = {
    "site_title": "Backend",
    "site_header": "Backend",
    "site_brand": "Backend",
    "search_model": ["account.User","product.product"],
    "site_logo_classes": "img-circle",
    "site_logo_classes": "img-circle",
    "welcome_sign": "Backend",
    # "site_logo": "media/logosts_utFgGsN.webp",
 
    "user_avatar": "True",
      # Whether to display the side menu
    "show_sidebar": True,
      # Hide these apps when generating side menu e.g (auth)
    # "hide_apps": ["cash"],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # Whether to aut expand the menu
    "navigation_expanded": False,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    "changeform_format": "horizontal_tabs",
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,
        "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

   
        {"model": "account.User"},
         {"model": "product.product"},
         {"model": "ordersts.order"},
         {"models": "home.banner"},
     
    ],
        "custom_links": {
        "books": [{
            "name": "Make Messages", 
            "url": "make_messages", 
            "icon": "fas fa-comments",
            "permissions": ["books.view_book"]
        }]
    },    
}


site_name = 'https://api.sts-shop.uz' # media url 

SITE_PREFEX = 'https://api.sts-shop.uz'

CRM_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6"
CRM_KEY = "hikvision"
CRM_URL = "https://hikvision.uz/" 

CLOUDFLARE_ACCOUNT_ID='7f335618b5f365f445e09b38ef177bc2'
CLOUDFLARE_API_KEY="ttbHQk5U0bYfEgWSkVXnUw6KQMOSEOlsFRnEk9lC"
CLOUDFLARE_ACCOUNT_HASH="Gu1Q4_5sCtQOwE1U01VyXA"
CLOUDFLARE_IMAGES_DOMAIN="imagedelivery.net"
CLOUDFLARE_EMAIL="azamatnarzulloyev2@gmail.com"




if int(os.environ.get("test", 1)) == 1:
    data = os.environ.get("test")
    import sentry_sdk

    sentry_sdk.init(
        dsn="https://67203abc136def9ec4785ef62813ae9a@o4506868426145792.ingest.us.sentry.io/4506868430667776",
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )



CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH="media/uploads/ckeditor/"


CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'licenseKey': "RVRWTnkwcDdPTkVUVWtacER1dkxpUXYxa3dGOE9TeEF2VGVzczVJMG9BQWIzWkpCSnJYY1JJV2oxcWd6UVE9PS1NakF5TkRFd01UUT0=",
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}
