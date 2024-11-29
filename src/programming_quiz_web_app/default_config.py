import datetime as dt
from email.headerregistry import Address
from programming_quiz_web_app.default_timezones import all_time_zones

class App_Config:
    # Flask Config
    DEBUG = False
    SESSION_COOKIE_NAME = "programming_quiz_session_cookie"
    SESSION_COOKIE_DOMAIN = None
    SESSION_COOKIE_PATH = None
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "Strict"
    PERMANENT_SESSION_LIFETIME = dt.timedelta(days=2)
    SESSION_REFRESH_EACH_REQUEST = False
    SEND_FILE_MAX_AGE_DEFAULT = None
    SERVER_NAME = None
    APPLICATION_ROOT = "/"
    PREFERRED_URL_SCHEME = "https"
    MAX_CONTENT_LENGTH = None
    MAX_COOKIE_SIZE = 4093

    # SQLALCHEMY Config
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 60,
        'pool_pre_ping': True
        }

    # Flask-login Config
    REMEMBER_COOKIE_NAME = "remember_token"
    REMEMBER_COOKIE_DURATION = dt.timedelta(days=2)
    REMEMBER_COOKIE_DOMAIN = None
    REMEMBER_COOKIE_PATH = APPLICATION_ROOT if APPLICATION_ROOT is not None else "/"
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_REFRESH_EACH_REQUEST = False
    REMEMBER_COOKIE_SAMESITE = "Strict"

    # Flask-Talisman Config.
    FLASK_TALISMAN_CONFIG = {
        "force_https": True,
        "content_security_policy":{
            "default-src":["'self'", "data:"],
            "script-src":["'self'", "https://cdn.jsdelivr.net"],
            "style-src":["'self'", "https://cdn.jsdelivr.net"],
        },
    }

    # Logging
    APP_LOG_ENABLED = True
    APP_LOG_DIR = "/var/logs/programming_quiz_web_app"
    APP_LOG_FILE_NAME = "programming_quiz.log"
    APP_LOG_FILE_MAX_BYTES = 51200  # 50KiB
    APP_LOG_FILE_BACKUP_COUNT = 10

    # Timezones
    APP_ALL_TIMEZONES = all_time_zones

    # SMTP config.
    SMTP_SERVER = "smtp.example.com"
    SMTP_PORT = 465
    SMTP_SSL = True
    SMTP_USERNAME = "example"
    SMTP_PASSWORD = "example"
    SMTP_FROM = Address("SPQ NO REPLY", "noreply", "example.com")
    CONTACT_EMAIL_ADDRESS = "example@example.com"

    # Vite Config.
    VITE_MODE = "production"
    VITE_ORIGIN = "http://localhost:5173"
