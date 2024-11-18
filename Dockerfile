FROM python:3

WORKDIR /src
COPY /src /src

ENV PYTHONPATH=/src

RUN pip install --no-cache-dir -r programming_quiz_web_app.egg-info/requires.txt
EXPOSE 8080
ENV FLASK_APP=src/programming_quiz_web_app:create_app()
CMD ["gunicorn", "-b", ":8080", "programming_quiz_web_app:create_app"]
