from flask import Blueprint

bp = Blueprint('data', __name__, cli_group = "data")

from programming_quiz_web_app.data import cli