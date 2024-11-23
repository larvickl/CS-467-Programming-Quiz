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
### Database
This application is built with a MySQL/ MariaDB database in mind.  In order to use this application, a database and a database user must be setup.  The following commands from the MySQL shell will create a database and a user:
```sql
sudo mysql
create database <DATABASE_NAME> character set utf8mb4 collate utf8mb4_bin;
create user '<DATABASE_USER>'@'localhost' identified by '<DATABASE_USER_PASSWORD>';
grant all privileges on <DATABASE_NAME>.* to '<DATABASE_USER>'@'localhost';
flush privileges;
quit;
```
### Application Configuration
In order to run the web application appropriate static configuration must be provided.  See [doc/configuration.md](doc/configuration.md) for details on setting the static configuration.

### Define FLASK_APP
In order to use the `flask` command the FLASK_APP environmental variable must be set and describe how to run the application.  This may be done by executing the following:

```
export FLASK_APP="programming_quiz_web_app:create_app()"
```

### Add Database Schema
In order to migrate the database schema to the current version, execute the following command:
```python
flask db upgrade
```
This command MUST be executed on the development server each time a new database migration file is created!
## Running the Application
### Development Environment
For development purposes ONLY you may use the Flask development server.  To launch the flask development server, execute the following command:
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
gunicorn -w 4 -b localhost:8080 "programming_quiz_web_app:create_app()" --log-file="./logs/gunicorn.log"
```
Alternatively, if you have set the "FLASK_APP" environmental variable as described above, you may rune the Gunicorn server using the following command:
```bash
gunicorn -w 4 -b localhost:8080 "$FLASK_APP" --log-file="./logs/gunicorn.log"
```

**Note:**  The -w option specifies the number of processes to run.  The Flask documentation recommends using a starting value could be CPU * 2.  The default is only 1 worker.

See the [Flask documentation](https://flask.palletsprojects.com/en/3.0.x/deploying/gunicorn/#running) on Gunicorn for more information.

**Note:** Gunicorn can be run as a daemon.  See the [Gunicorn documentation](https://docs.gunicorn.org/en/latest/deploy.html#systemd) for details on doing so.
### Production Environment - mod_wsgi
If you decided to use mod_wsgi, a WSGI interface file MUST be created.  The following WSGI interface file should be fine in most cases:
```python
from programming_quiz_web_app import create_app

application = create_app()
```
**Note:** The application MUST be named "application" an in the example above for mod_wsgi to find it.

The specific configuration, depending on which http server is being used, will greatly vary.  See the [mod_wsgi documentation](https://modwsgi.readthedocs.io/en/master/) to get started.