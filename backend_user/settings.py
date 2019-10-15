"""
Django settings for backend_user project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c6^l-8kg4!7to28mc2)#k*@9pl(90g0(q%ow1ahjd$9d6skj)r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
FLAG = 3
ALLOWED_HOSTS = ['*']

EMAIL_HOST = 'mail.mindzzle.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'admin@mindzzle.com'
EMAIL_HOST_PASSWORD = '1q2w3e4r5t6y'
EMAIL_USE_TLS = False
SECURE_CONTENT_TYPE_NOSNIFF  = True
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTIFICATION_CLASSES' : (
        'rest_framework.authentication.TokenAuthentication',
    )
}
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', 
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'registrations',
    'user_type',
    'friend_list',
    'country',
    'region',
    'city',
    'message',
    'experiences',
    'education',
    'award',
    'certification',
    'join_company',
    'business_account',
    'business_type',
    'employee_sign',
    'history_hierarchy',
    'hierarchy',
    'contract',
    'job_contract',
    'level',
    'time_contract',
    'type_time',
    'role_type',
    'contact',
    'private',
    'email_app',
    'log_app',
    'notification',
    'file_upload',
    'OCR_Reader',
    'business_img',
    'user_img',
    'vendor_api',
    'goal',
    'goal_assignment',
    'log_created_goal',
    'type_goal',
    'review_scheduler',
    'goal_negotiation',
    'awards_BA',
    'certifications_BA',
    'recruitment',
    'interview',
    'jobfair_online',
    'test_form',
    'chatapp',
    'license_company',
    'approval_config',
    'jobdesc',
    'sipromo_api',
    'haloarif',
    'orderlicense',
    #'category_goal',
    'warna_goal',
    'time_period',
    'KPI',
    'KPI_assign',
    'task',
    'task_assign',
    'goal_category',
    'goal_activity',
    'goal_files',
    'goal_notes',
    'goal_setting',
    'goal_pinned',
    'kpi_category',
    'task_timer',
    'task_checklist_item',
    'task_checklist_template',
    'task_tag',
    'tag',
    'milestone',
    'task_comment',
    'task_follower',
    'feeds',
    'friends',
    'group_user',
    'setting_approval',

]

SITE_ID = 1

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]
ROOT_URLCONF = 'backend_user.urls'

PROJECT_ROOT = os.path.dirname


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                "django.core.context_processors.tz",

            ],
        },
    },
]
WSGI_APPLICATION = 'backend_user.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
     'ENGINE': 'django.db.backends.postgresql',
     'HOST': '35.198.248.235',
     'PORT': '5432',
     'NAME': 'userdbdev',
     'USER': 'postgres',
     'PASSWORD': 'your_password'
    }
}

# DATABASES = {
#     'default': {
#      'ENGINE': 'django.db.backends.postgresql',
#      'HOST': '35.198.248.235',
#      'PORT': '5432',
#      'NAME': 'userdbstaging',
#      'USER': 'postgres',
#      'PASSWORD': 'your_password'
#     }
# }


# 35.198.248.235
# 10.148.0.3
# DATABASES = {
#     'default': {
#      'ENGINE': 'django.db.backends.postgresql',
#      'HOST': '35.247.162.159',
#      'PORT': '5432',
#      'NAME': 'userprod',
#      'USER': 'user',
#      'PASSWORD': 'U53rDB2016'
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = (
    'http://dev-user.mindzzle.com',
)
