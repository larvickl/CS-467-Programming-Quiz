from flask import Blueprint

bp = Blueprint('main', __name__)

from programming_quiz_web_app.main import routes
from programming_quiz_web_app.main import auth
from programming_quiz_web_app.main import protected
