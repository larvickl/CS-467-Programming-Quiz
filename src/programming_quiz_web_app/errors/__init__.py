from flask import Blueprint

bp = Blueprint('errors', __name__)

from programming_quiz_web_app.errors import handlers
