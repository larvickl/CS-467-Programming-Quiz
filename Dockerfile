FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /src/programming_quiz_web_app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY /src/programming_quiz_web_app .

EXPOSE 8080

CMD ["gunicorn", "-b", ":8080", "app:app"]
