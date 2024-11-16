import os
import datetime as dt
from email.headerregistry import Address
from app_secrets.secret_key import SECRET_KEY
from app_secrets.db_credentials import db_host, db_port, db_database, db_username, db_password

deployment_dir = os.path.abspath(os.path.dirname(__file__))  # Directory containing this file.

class App_Config:
    # Flask Config
    DEBUG = False
    SECRET_KEY = SECRET_KEY
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
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_database}"
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 60,
        'pool_pre_ping': True
        }

    # Flask-Talisman Config.
    FLASK_TALISMAN_CONFIG = {
        "force_https": True,
        "content_security_policy":{
            "default-src":["self"],
            "script-src":["https://cdn.jsdelivr.net"],
            "style-src":["https://cdn.jsdelivr.net"],
        },
    }

    # Logging
    APP_LOG_ENABLED = True
    APP_LOG_DIR = os.path.join(deployment_dir, "logs")
    APP_LOG_FILE_NAME = "programming_quiz.log"
    APP_LOG_FILE_MAX_BYTES = 51200  # 50KiB
    APP_LOG_FILE_BACKUP_COUNT = 10

    # SMTP config.
    SMTP_SERVER = "smtp.example.com"
    SMTP_PORT = 465
    SMTP_SSL = True
    SMTP_USERNAME = "example"
    SMTP_PASSWORD = "example"
    SMTP_FROM = Address("SPQ NO REPLY", "noreply", "example.com")
    CONTACT_EMAIL_ADDRESS = "example@example.com"