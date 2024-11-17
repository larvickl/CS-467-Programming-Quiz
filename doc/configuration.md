# Configuration
This file details setting the static configuration for the Software Programming Quiz web application.

## Configuration Sources
Configuration variables for the flask application may be set in one of three locations.
### default_config.py
This repository contains a default configuration file named "default_config.py" in the same directory as the "\_\_init\_\_.py" file that defines the application factory function.  This file contains sensible configuration values for most production environments.  This file is automatically loaded when an application is created.

This file does not define "SECRET_KEY" or "SQLALCHEMY_DATABASE_URI", which MUST be explicitly defined by the deployer in the user's configuration file or by setting environmental variables as described below.

**Note:** This file is part of the tracked repository and should NOT be changed by the deployer!
### User Config from Prefixed Environmental Variables
Configuration values may also be set by setting environmental variables with names prefixed by a specific prefix string.  By default, all environmental variables prefixed with "SPQ_CONFIG_" will be stripped of the prefix and loaded into the application configuration.

For example, executing `export SPQ_CONFIG_SECRET_KEY="1234"`
would result in a configuration variable of "SECRET_KEY" being made available to the application with a value of "1234".

See the [Flask documentation](https://flask.palletsprojects.com/en/stable/config/#configuring-from-environment-variables) for details on how configuration from prefixed environmental variables is parsed.

**Note:** Configuration from prefixed environmental variables will overwrite default configuration values of the same name.  See "Configuration Precedence" section for a full discussion of this behavior.
### User Config File
Configuration values may also be set from a user provided config file.  The path to this file should be stored in an environmental variable (by default, "FLASK_APP_CONFIG") that is defined when calling the flask application factory function.

The user configuration file should be a simple python file containing no relative imports.  All variables in this file that contain only capital letters and underscores in their names will be loaded into the application configuration.  See the [Flask documentation](https://flask.palletsprojects.com/en/stable/config/#configuring-from-python-files) for a discussion of this behavior.

An environmental variable command and user configuration file are provided below:

```
export FLASK_APP_CONFIG="/home/USER/Documents/config.py" 
```
```python
import os

deployment_dir = os.path.abspath(os.path.dirname(__file__))

db_host = ""
db_port = ""
db_database = ""
db_username = ""
db_password = ""

SECRET_KEY = 'MEOW'
SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_database}"
APP_LOG_DIR = os.path.join(deployment_dir, "logs")
```
**Note:** Configuration from a user config file will overwrite prefixed environmental variables and default configuration values of the same name.  See "Configuration Precedence" section for a full discussion of this behavior.
## Configuration Precedence
When multiple configuration methods define the same application configuration variables, the value of the configuration variable with the highest precedence will be used.

From lowest to highest, the order of configuration precedence is as follows:
* default_config.py
* User Config from Prefixed Environmental Variables
* User Config File
## Configuration Settings
This section details the configuration settings that the application accepts.

### DEBUG
* Type:  bool
* Default Value:  False
* Source:  Flask

Whether debug mode is enabled. See in [Flask documentation](https://flask.palletsprojects.com/en/stable/config/#DEBUG).
### SECRET_KEY
* Type:  str
* Default Value:  Undefined
* Source:  Flask

The application requires a secret key. This will be used to sign the session cookies, JWT tokens, CSRF protection tokens, etc. As such, it is CRITICAL that the token is as cryptographically strong as possible and is stored in such a manor that its access is restricted as much as possible.

The SECRET_KEY must be explicitly defined by the deployer as it should be unique to each instance.

The following line, executed from Bash, should save a strong SECRET_KEY to a file named secret_key.py:
```
python -c "import secrets; print(f'SECRET_KEY = \'{secrets.token_urlsafe(256)}\'')" > secret_key.py
```
### SESSION_COOKIE_NAME
* Type:  str
* Default Value:  "programming_quiz_session_cookie"
* Source:  Flask

The name of the session cookie.  See in [Flask documentation](https://flask.palletsprojects.com/en/stable/config/#SESSION_COOKIE_NAME).
### SESSION_COOKIE_DOMAIN
* Type:  str | None
* Default Value None
* Source:  Flask

The value of the Domain parameter on the session cookie.  See in [Flask documentation](https://flask.palletsprojects.com/en/stable/config/#SESSION_COOKIE_DOMAIN).
### SESSION_COOKIE_PATH
* Type:  str | None
* Default Value:  None
* Source:  Flask

The path that the session cookie will be valid for.  See in [Flask documentation](https://flask.palletsprojects.com/en/stable/config/#SESSION_COOKIE_PATH).
### SESSION_COOKIE_HTTPONLY
* Type:  bool
* Default Value:  True
* Source:  Flask

Browsers will not allow JavaScript access to cookies marked as “HTTP only” for security.  See in [Flask documentation](https://flask.palletsprojects.com/en/stable/config/#SESSION_COOKIE_HTTPONLY).
### SESSION_COOKIE_SECURE
* Type:  bool
* Default Value:  True
* Source:  Flask

Browsers will only send cookies with requests over HTTPS if the cookie is marked “secure”.   See in [Flask documentation](https://flask.palletsprojects.com/en/stable/config/#SESSION_COOKIE_SECURE).
### SESSION_COOKIE_SAMESITE
* Type:  str
* Default Value:  "Strict"
* Source:  Flask

Restrict how cookies are sent with requests from external sites.  See [SameSite attribute and MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#samesitesamesite-value).  See in [Flask Documentation](https://flask.palletsprojects.com/en/stable/config/#SESSION_COOKIE_SAMESITE)
### PERMANENT_SESSION_LIFETIME
* Type:  datetime.timedelta | int
* Default Value:  dt.timedelta(days=2)
* Source:  Flask

If session.permanent is true, the cookie’s expiration will be set this number of seconds in the future.  See in [Flask documentation](https://flask.palletsprojects.com/en/stable/config/#PERMANENT_SESSION_LIFETIME).
### SESSION_REFRESH_EACH_REQUEST
* Type:  bool
* Default Value:  False
* Source:  Flask

Control whether the cookie is sent with every response when session.permanent is true.   See in [Flask documentation](https://flask.palletsprojects.com/en/stable/config/#SESSION_REFRESH_EACH_REQUEST).
### SEND_FILE_MAX_AGE_DEFAULT
* Type:  datetime.timedelta | int | None
* Default Value:  None
* Source:  Flask

When serving files, set the cache control max age to this number of seconds.  If None, send_file tells the browser to use conditional requests instead of timed cache.  See in [Flask documentation](https://flask.palletsprojects.com/en/stable/config/#SEND_FILE_MAX_AGE_DEFAULT).
### SERVER_NAME
* Type:  str | None
* Default Value:  None
* Source:  Flask

Inform the application what host and port it is bound to.  See in [Flask documentation](https://flask.palletsprojects.com/en/stable/config/#SERVER_NAME).
### APPLICATION_ROOT
* Type:  str
* Default Value:  "/"
* Source:  Flask

Inform the application what path it is mounted under by the web server.  See in [Flask documentation](https://flask.palletsprojects.com/en/stable/config/#APPLICATION_ROOT).
### PREFERRED_URL_SCHEME
* Type:  str
* Default Value:  "https"
* Source:  Flask

Use this scheme for generating external URLs when not in a request context.  See in [Flask documentation](https://flask.palletsprojects.com/en/stable/config/#PREFERRED_URL_SCHEME).
### MAX_CONTENT_LENGTH
* Type:  int | None
* Default Value:  None
* Source:  Flask

The maximum number of bytes that will be read during this request. If this limit is exceeded, a 413 RequestEntityTooLarge error is raised. If it is set to None, no limit is enforced at the Flask application level.  See in [Flask documentation](https://flask.palletsprojects.com/en/stable/config/#MAX_CONTENT_LENGTH).
### MAX_COOKIE_SIZE
* Type:  int
* Default Value:  4093
* Source:  Flask

Warn if cookie headers are larger than this many bytes.  Set to 0 to disable warnings.  See in [Flask documentation](https://flask.palletsprojects.com/en/stable/config/#MAX_COOKIE_SIZE).
### SQLALCHEMY_DATABASE_URI
* Type:  str
* Default Value:  Undefined
* Source:  SQLAlchemy

The database connection URI used for the default engine.  See in [Flask-SQLAlchemy documentation](https://flask-sqlalchemy.readthedocs.io/en/stable/config/#flask_sqlalchemy.config.SQLALCHEMY_DATABASE_URI).

**Note:** This variable MUST be explicitly set by the application deployer as database name, server, port, and credentials may very.  That said, this application is designed to be used with MariaDB/ MySQL databases.  As such, the URI should follow the example below:
```python
db_host = ""
db_port = ""
db_database = ""
db_username = ""
db_password = ""

SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_database}"
``` 
### SQLALCHEMY_ENGINE_OPTIONS
* Type:  dict
* Default Value:  {'pool_size': 10, 'pool_recycle': 60, 'pool_pre_ping': True}
* Source:  SQLAlchemy

A dict of arguments to pass to `sqlalchemy.create_engine()` for the default engine.  See in [Flask-SQLAlchemy documentation](https://flask-sqlalchemy.readthedocs.io/en/stable/config/#flask_sqlalchemy.config.SQLALCHEMY_ENGINE_OPTIONS).  See the Engine Creation API Parameters from the [SQLAlchemy documentation](https://docs.sqlalchemy.org/en/20/core/engines.html#engine-creation-api) for acceptable entries in this dict.
### FLASK_TALISMAN_CONFIG
* Type:  dict
* Default Value:  {"force_https": True, "content_security_policy":{"default-src":["'self'", "data:"], "script-src":["'self'", "https://cdn.jsdelivr.net"],"style-src":["'self'", "https://cdn.jsdelivr.net"],},}
* Source:  Flask-Talisman

Settings to be passed to Flask-Talisman to set security headers.  See [Flask-Talisman documentation](https://github.com/GoogleCloudPlatform/flask-talisman?tab=readme-ov-file#options) for details on the acceptable headers.

**Note:** The default value above is optimized for the production environment and is quite restrictive.  For development environments, you will need much less restrictive settings such as those below.  The following example settings should **NEVER** be used in a production environment!
```python
FLASK_TALISMAN_CONFIG = {
    "force_https": False,
    "content_security_policy":{
        "default-src":["'self'", "data:", "http://127.0.0.1:5173", "http://localhost:5173", "ws://localhost:5173"],
        "script-src":["'self'", "'unsafe-inline'", "http://localhost:5173", "https://cdn.jsdelivr.net"],
        "style-src":["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
    },
}
```
### APP_LOG_ENABLED
* Type:  bool
* Default Value:  True
* Source:  Programming Quiz Web App

If True, the Flask application will log to a rotating file.  If True, "APP_LOG_DIR", "APP_LOG_FILE_NAME", "APP_LOG_FILE_MAX_BYTES", and "APP_LOG_FILE_BACKUP_COUNT" must also be set.
### APP_LOG_DIR
* Type:  str
* Default Value:  "/var/logs/programming_quiz_web_app"
* Source:  Programming Quiz Web App

The directory to save the rotating log files in.
### APP_LOG_FILE_NAME
* Type:  str
* Default Value:  "programming_quiz.log"
* Source:  Programming Quiz Web App

The base file name for the rotating log files.
### APP_LOG_FILE_MAX_BYTES
* Type:  int
* Default Value:  51200  # 50KiB
* Source:  Programming Quiz Web App

The maximum length (in bytes) of each log file before a new log file is created.
### APP_LOG_FILE_BACKUP_COUNT
* Type:  int
* Default Value:  10
* Source:  Programming Quiz Web App

The number of old log files to keep before previous ones are deleted.