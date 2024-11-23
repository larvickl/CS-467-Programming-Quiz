import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from logging.handlers import RotatingFileHandler
from programming_quiz_web_app.default_config import App_Config

db = SQLAlchemy()
migrate = Migrate()
talisman = Talisman()
csrf = CSRFProtect()

def create_app(app_config_env_var: str = "FLASK_APP_CONFIG", app_config_prefix: str = "SPQ_CONFIG") -> Flask:
    """Create a flask application.

    Parameters
    ----------
    app_config_env_var : str, optional
        The environmental variable containing the path to a python config file.
        All variables in such a config file that consist of only capital letters and
        underscores will be added to the flask config.  If the environmental variable
        given is not set, no config file will be loaded. By default "FLASK_APP_CONFIG"
    app_config_prefix : str, optional
        All environmental variables prefixed with this string will be added to the
        Flask configuration.  The prefix is removed before adding to the Flask config. 
        Note that if the same configuration setting is set by both a "app_config_env_var" 
        config file and a "app_config_prefix", the setting from the config file will take 
        precedence.  By default "SPQ_CONFIG"

    Returns
    -------
    Flask
        The flask application.

    Raises
    ------
    KeyError
        If a required configuration variable is not set (i.e., "SECRET_KEY" 
        or "SQLALCHEMY_DATABASE_URI").
    ValueError
        If a required configuration variable is in the application configuration
        but has a value of None.
    """
    # Create Flask app.
    app = Flask(__name__)

    # Apply configuration.
    app.config.from_object(App_Config)  # Apply default config.
    app.config.from_prefixed_env(prefix=app_config_prefix)  # Apply config from environmental variables.
    if os.environ.get(app_config_env_var) is not None:
        app.config.from_envvar(app_config_env_var)  # Apply configuration from config file pointed to by env var.

    # Check configuration for required keys not included in default_config.
    for required_key in ["SECRET_KEY", "SQLALCHEMY_DATABASE_URI"]:
        if required_key not in app.config.keys():
            raise KeyError(f"{required_key} must be defined in the application configuration!")
        if app.config[required_key] is None:
            raise ValueError(f"{required_key} must not be None!")

    # Initialize Flask-Talisman
    talisman.init_app(app, **app.config["FLASK_TALISMAN_CONFIG"])

    # Initialize CSRF protection.
    csrf.init_app(app)

    # Initialize the database.
    db.init_app(app)
    migrate.init_app(app, db, directory=os.path.join(os.path.abspath(os.path.dirname(__file__)), "migrations"))

    # Register Blueprints
    from programming_quiz_web_app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from programming_quiz_web_app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from programming_quiz_web_app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from programming_quiz_web_app.employer import bp as employer_bp
    app.register_blueprint(employer_bp)

    from programming_quiz_web_app.vite import bp as vite_bp
    app.register_blueprint(vite_bp)

    # Setup Logger.
    if app.config["APP_LOG_ENABLED"] is True and not app.debug:
        log_file_dir = app.config["APP_LOG_DIR"]
        # Make log directories if they do not exist.
        if os.path.isdir(log_file_dir) is False:
            os.makedirs(log_file_dir)
        # Startup Logging.
        file_handler = RotatingFileHandler(
            filename=os.path.join(log_file_dir, app.config["APP_LOG_FILE_NAME"]),
            maxBytes=app.config["APP_LOG_FILE_MAX_BYTES"],
            backupCount=app.config["APP_LOG_FILE_BACKUP_COUNT"])
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Programming Quiz Server Startup')

    # Return Flask app.
    return app
