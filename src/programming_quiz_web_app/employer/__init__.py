from flask import Blueprint

bp = Blueprint('employer', __name__)

from programming_quiz_web_app.employer import routes
