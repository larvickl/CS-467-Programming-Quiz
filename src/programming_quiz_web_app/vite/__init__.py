import os
from flask import Blueprint

project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vite-flask-integration")
static_directory = os.path.join(os.path.join(project_path, "assets_compiled"), "bundled")

bp = Blueprint(
    'vite',
    __name__,
    static_folder=static_directory,
    static_url_path="/assets/bundled",
    cli_group = "vite")

from programming_quiz_web_app.vite import assets, cli