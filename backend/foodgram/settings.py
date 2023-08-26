import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('SECRET_KEY', '123')

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'recipes',
    'django_filters',
    'colorfield',
    'api',
    'django_cleanup',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'foodgram.urls'

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

WSGI_APPLICATION = 'foodgram.wsgi.application'

AUTH_USER_MODEL = 'users.User'


DATABASE = os.getenv("USE_POSTGRESQL") == 'True'

if os.getenv("USE_POSTGRESQL") is True:
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
            'NAME': os.getenv('DB_NAME', default='postgres'),
            'USER': os.getenv('POSTGRES_USER', default='postgres'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
            'HOST': os.getenv('DB_HOST', default='db'),
            'PORT': os.getenv('DB_PORT', default='5432')
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

DJOSER = {
    'HIDE_USERS': False,
    'SERIALIZERS': {
        'current_user': 'api.serializers.UserReadSerializer',
        'user': 'api.serializers.UserReadSerializer',
    },
    'PERMISSIONS': {
        'user': ('rest_framework.permissions.IsAuthenticated',),
        'user_list': ('rest_framework.permissions.AllowAny',),
        'set_username': ('rest_framework.permissions.IsAdminUser',),
        'user_delete': ('rest_framework.permissions.IsAdminUser',),
        'password_reset': ('rest_framework.permissions.IsAdminUser',),
        'password_reset_confirm': ('rest_framework.permissions.IsAdminUser',),
        'username_reset': ('rest_framework.permissions.IsAdminUser',),
        'username_reset_confirm': ('rest_framework.permissions.IsAdminUser',),
    }
}

# Константы, которые используются в проекте

MIN_COOK_TIME = 1  # Минимальное время приготовления блюда
MAX_COOK_TIME = 10080  # Максимальное время приготовления блюда
MIN_AMOUNT = 1  # Минимальное количество ингредиента
ING_IN_PAGE = 26  # Количество ингредиентов на одной странице в списке покупок
ING_INDEX = 0  # Значение, которое создает новую страницу со списком покупок
FIELD_LENGTH = 200  # Максимальная длинна поля в моделях рецептов
FIELD_LENGTH_USER = 150  # Максимальная длинна поля в модели юзеров
MAX_LENGTH_EMAIL = 254  # Максимальная длинна email для пользователя
MAX_SIZE_IMAGE = 1 * 1024 * 1024  # Максимальный размер картинки
