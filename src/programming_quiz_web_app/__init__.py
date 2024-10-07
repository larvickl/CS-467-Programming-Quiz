import os
import logging
from typing import Any
from flask import Flask
from logging.handlers import RotatingFileHandler

def create_app(app_config: Any) -> Flask:
    # Create Flask app.
    app = Flask(__name__)
    app.config.from_object(app_config)

    # Register Blueprints
    from programming_quiz_web_app.main import bp as main_bp
    app.register_blueprint(main_bp)

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