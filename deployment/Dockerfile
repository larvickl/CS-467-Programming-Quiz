FROM python:3.10-slim

# Name of the wheel file.
ARG wheel="programming_quiz_web_app-0.1.dev113+g82ac1c8-py3-none-any.whl"

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