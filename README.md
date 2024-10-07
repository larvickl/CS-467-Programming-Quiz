# CS-467-Programming-Quiz
A web application for creating and taking programming quizzes. This application will allow employers to create and manage quizzes, authorize applicants to take timed quizzes through unique key links, and enable employers to view ranked quiz results and the statuses of individual applicants.
## Installation
### Create a Python Environment
The following steps will install the programming-quiz-web-app package and all of its dependencies into the active environment.  It is thus STRONGLY recommend that you create and activate a virtual python environment (See [venv](https://docs.python.org/3/library/venv.html) or [Anaconda](https://anaconda.org/)) before installing the package.

### Install the python Package
Use the following command to install the python package directly into your site-packages from github.  This should be done ONLY in production environments!
```bash
pip install git+https://github.com/larvickl/CS-467-Programming-Quiz.git
```

If you need to edit the code (i.e., in a development environment), clone the repository and install the package via pip as an editable package using the following commands:
```bash
git clone https://github.com/larvickl/CS-467-Programming-Quiz.git
cd Quiz/CS-467-Programming-Quiz$
pip install -e .
```

### Application Configuration
In order to run the web application, a WSGI interface file (wsgi.py) must be created and provided with the appropriate static configuration.  

This section will describe how to create a WSGI interface with a functioning configuration.  Though not the only possible structure, this section will describe how to create the following files:
```
app
├── app_config.py
├── app_secrets
│   └── secret_key.py
└── wsgi.py
```
#### Directories
Outside of the cloned repository tree, though the exact location does not matter, create a directory that will contain the WSGI interface file, the application configuration, and the app_secrets directory.
```bash
mkdir app
cd app
```
Create the app_secrets directory and restrict access to the user of the web application.
```bash
mkdir app_secrets
chown <APP_USER>:<APP_GROUP> app_secrets
chmod 700 app_secrets
```
#### Secret Key
The application requires a secret key.  This will be used to sign the session cookies, CSRF protection tokens, etc.  As such, it is CRITICAL that the token is as cryptographically strong as possible and is stored in such a manor that its access is restricted as much as possible.

Create a secret key within the app_secrets directory. Executing the following command from BASH will generate a cryptographically strong SECRET KEY using secrets from the Python standard library:
```bash
python -c "import secrets; print(f'SECRET_KEY = \'{secrets.token_urlsafe(256)}\'')" > secret_key.py
```
Note that other methods may be used to create a secret key.

Restrict access to the secret key.
```bash
chown <APP_USER>:<APP_GROUP> secret_key.py
chmod 600 app_secrets
```
#### Configuration File
Within the "app" directory that we created, create a configuration file.  This configuration file will contain all of the application's static configuration information and will be passed to the Flask factory function at the time of application creation.

A sample configuration file is included in this repository at examples/app_config.py.  Copy this file to the "app" directory and make any desired changes.  Ensure that this configuration file imports the secret key and that the configuration class contains a SECRET_KEY class variable.

Explanations of the Flask configuration values may be found in the [Flask Documentation](https://flask.palletsprojects.com/en/3.0.x/config/#builtin-configuration-values).

#### WSGI Interface File
Now that the configuration is setup, create a WSGI interface file named "wsgi.py" in the same directory as the configuration file.  

A sample WSGI interface file has been included in this repository at examples/wsgi.py.  This file should work without any changes.  Copy this file to the "app" directory.  

This file will be used as the entry point for the application.

Note:  If Mod-WSGI is being used, the application that is created in the WSGI file MUST be named "application".

#### Environmental Variables
In order to use the "flask" command (e.g., flask run) you must execute the command from the directory containing the wsgi.py file.

Alternatively, the flask command may be fun from any directory if you either set the FLASK_APP environmental variable to be the path to the WSGI file or use the --app argument with the "flask" command to specify the WSGI file.  Details regarding both of these options may be found in the [Flask documentation](https://flask.palletsprojects.com/en/3.0.x/cli/).

## Running the Application
### Development Environment
For development purposes ONLY you may use the Flask development server.  To launch the flask development server, execute the following command from the directory containing the wsgi.py file:
```bash
flask run
```
### Production Environment - Gunicorn
Ensure that Gunicorn is installed in the application's virtual python environment.
```bash
pip install gunicorn
```
Run the Gunicorn server:
```bash
cd <APP_DIRECTORY>
gunicorn -w 4 -b localhost:8080 wsgi:application --log-file="./logs/gunicorn.log"
```
See the [Flask documentation](https://flask.palletsprojects.com/en/3.0.x/deploying/gunicorn/#running) on Gunicorn for mor information.

Note:  
The -w option specifies the number of processes to run.  The Flask documentation recommends using a starting value could be CPU * 2.  The default is only 1 worker.

### Production - mod_wsgi
See the [mod_wsgi documentation](https://modwsgi.readthedocs.io/en/master/).