# Docker Deployment
The following sections explain how to build a Docker Container and deploy this application.
## Build Python Wheel
### Install Python Dependencies
```bash
pip install build
```
### Build the wheel
```bash
python -m build --wheel --outdir deployment/
```
Note:  The above command should be run from the directory containing the pyproject.toml file.
## Build Docker Container
### Create a dockerfile
Create a dockerfile named "Dockerfile" in the same directory containing the wheel file that was produced in the above section.  Ensure that the contents of the dockerfile are as follows, replacing "WHEEL_FILE.whl" with the name of the wheel file created in the previous section.
```dockerfile
FROM python:3.10-slim

# Name of the wheel file.
ARG wheel="WHEEL_FILE.whl"

# Set the working directory within the container.
WORKDIR /app

# Copy the necessary files and directories into the container.
COPY ${wheel} /app/

# Upgrade pip and install Python dependencies.
RUN pip3 install --upgrade pip
RUN pip install gunicorn

# Install application.
RUN pip install ${wheel}

# Expose port 5000 for the Flask application.
EXPOSE 5000

# Run Flask application using Gunicorn.
CMD ["gunicorn", "programming_quiz_web_app:create_app()", "-b", "0.0.0.0:5000", "-w", "4"]
```
### Build the Docker
```bash
docker build -t software_programming_quiz .
```
Note:  This command must be executed from the directory containing the dockerfile and the wheel file.
### Confirm Image Creation
```bash
docker images
```
A repository with the name given in the previous step (i.e., "software_programming_quiz") should be in the returned list.
## Run Docker Image
### Configure Docker Environment
Create a configuration file named software_programming_quiz.env.  All environmental variables contained in this file prefixed with "SPQ_CONFIG_" will be used in the Flask configuration (with the prefix removed).

At a minimum, SPQ_CONFIG_SECRET_KEY and SPQ_CONFIG_SQLALCHEMY_DATABASE_URI must be defined.  The following in an example of the minimum configuration required:
```
SPQ_CONFIG_SECRET_KEY="<SECRET_KEY>"
SPQ_CONFIG_SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://<DB_USERNAME>:<DB_PASSWORD>@<DB_HOST>:<DB_PORT>/<DB_NAME>"
```
Note:  In the above example "<SECRET_KEY>" should be replaced with the applications secret key, "<DB_USERNAME>" should be replaced withe database user's username, "<DB_PASSWORD>" should be replaced with the database user's password, "<DB_HOST>" should be replaced with the database's host, "<DB_PORT>" should be replaced with the port that the database is available on, and "<DB_NAME>" should be replaced with the name of the database.
### Run the Image
```bash
docker run -p 5000:5000 --env-file=software_programming_quiz.env software_programming_quiz
```
