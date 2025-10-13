"""
Configurações do projeto Monografias
Django 5.2.7 + PostgreSQL + django-allauth
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# === Base e variáveis de ambiente ===
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")  # Carrega variáveis do arquivo .env na raiz do projeto

# === Segurança ===
SECRET_KEY = os.getenv("SECRET_KEY", "chave-secreta-padrao")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = ["*"]

# === Aplicações instaladas ===
INSTALLED_APPS = [
    # Django nativos
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Aplicações do projeto
    'accounts',
    'core',

    # Apps de terceiros
    'simple_history',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

SITE_ID = 1

# === Modelo de usuário customizado ===
AUTH_USER_MODEL = 'accounts.Usuario'

# === Middleware ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

# === URLs e WSGI ===
ROOT_URLCONF = 'monografias.urls'
WSGI_APPLICATION = 'monografias.wsgi.application'

# === Templates ===
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # pasta templates/ na raiz do projeto
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

# === Banco de dados (PostgreSQL) ===
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "monografias"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# === Validação de senha ===
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# === Localização ===
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# === Arquivos estáticos ===
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

# === Configuração padrão de ID ===
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# === Autenticação (django-allauth) ===
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# === Configurações de login/logout ===
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True

# === Formulário customizado de cadastro ===
ACCOUNT_FORMS = {
    'signup': 'accounts.forms.CustomSignupForm',
}

# === Outras boas práticas ===
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # mostra e-mails no terminal
