from flask import Blueprint

bp = Blueprint('auth', __name__)

from programming_quiz_web_app.auth import routes

