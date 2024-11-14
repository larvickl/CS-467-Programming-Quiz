from flask import Blueprint

bp = Blueprint('main', __name__)

from programming_quiz_web_app.applicant import routes
