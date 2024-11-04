import os
import logging
from typing import Any
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from logging.handlers import RotatingFileHandler
from flask_jwt_extended import JWTManager
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
talisman = Talisman()
csrf = CSRFProtect()
jwt = JWTManager()
mail = Mail()

def create_app(app_config: Any) -> Flask:
    """Create a flask application.

    Parameters
    ----------
    app_config : Any
        The class used to configure the Flask application.

    Returns
    -------
    Flask
        The Flask application.
    """
    # Create Flask app.
    app = Flask(__name__)
    app.config.from_object(app_config)

    # Initialize Flask-Talisman
    talisman.init_app(app, **app.config["FLASK_TALISMAN_CONFIG"])

    # Initialize CSRF protection.
    csrf.init_app(app)

    # Initialize the database.
    db.init_app(app)
    migrate.init_app(app, db, directory=os.path.join(os.path.abspath(os.path.dirname(__file__)), "migrations"))

    # Initialize the JWT manager
    jwt.init_app(app)

    # Intitialize emails 
    mail.init_app(app)
    
    # Register Blueprints
    from programming_quiz_web_app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from programming_quiz_web_app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

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